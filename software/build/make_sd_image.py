#!/usr/bin/env python3
"""
Allwinner A733 EDK2 SD card image builder
Creates a 16MB raw image to be written to an SD card at offset 0.

Layout (copied from eMMC analysis):
  0x020000: boot0 (eGON.BT0, 240KB)
  0xC00000: sunxi-package with EDK2 replacing u-boot component

Usage:
  python3 make_sd_image.py
  Then write sd_boot.img to SD card:
    Linux:   sudo dd if=sd_boot.img of=/dev/sdX bs=1M
    Windows: use Win32DiskImager or 'dd' for Windows
"""

import struct
import sys
import os

import platform
_BASE = "/mnt/d/Projects/PortaRe0/software" if platform.system() == "Linux" else "D:/Projects/PortaRe0/software"
BOOT0DUMP   = f"{_BASE}/boot0dump.bin"
EDK2_FD     = f"{_BASE}/build/A733.fd"
OUTPUT_IMG  = f"{_BASE}/build/sd_boot.img"

# Offsets confirmed from eMMC analysis
BOOT0_OFFSET   = 0x020000  # boot0 start (sector 256) - A733 SUNXI_GEN_NCAT2, same for SD and eMMC
BOOT0_SIZE     = 0x03C000  # boot0 size (240KB)
PKG_OFFSET     = 0xC00000  # sunxi-package start
PKG_UBOOT_OFF  = 0x000800  # u-boot component offset within package
PKG_MONITOR_OFF= 0x12C400  # monitor (TF-A BL31) offset
PKG_SCP_OFF    = 0x13F800  # scp offset
PKG_SCP_SIZE   = 0x01CAE8  # scp size (to know total package extent)

IMG_SIZE = 0x1000000  # 16MB image

def recalc_checksum(data, checksum_offset, checksum_size=4):
    """Recalculate Allwinner simple checksum (sum of all u32 words except checksum field)."""
    total = 0
    view = memoryview(data)
    for i in range(0, len(data), 4):
        if i == checksum_offset:
            continue
        word = struct.unpack_from('<I', view, i)[0]
        total = (total + word) & 0xFFFFFFFF
    return total

def main():
    print("=== A733 SD Boot Image Builder ===")

    # Load inputs
    print(f"Loading boot0dump: {BOOT0DUMP}")
    with open(BOOT0DUMP, 'rb') as f:
        dump = bytearray(f.read())
    print(f"  dump size: {len(dump):#x} bytes")

    print(f"Loading EDK2 FD: {EDK2_FD}")
    with open(EDK2_FD, 'rb') as f:
        edk2_fd = bytearray(f.read())
    print(f"  FD size: {len(edk2_fd):#x} bytes ({len(edk2_fd)//1024}KB)")

    # Show FD[0] for reference (will be overwritten by our ARM64 B patch below)
    fd0 = struct.unpack_from('<I', edk2_fd, 0)[0]
    print(f"  FD[0] = 0x{fd0:08X} (will be patched)")

    # Patch Allwinner u-boot binary header into EDK2 FD
    #
    # boot0 checks the BL33 binary magic by verifying:
    #   - Offset 0x00: ARM32 unconditional branch (top byte == 0xEA)
    #   - Offset 0x04: "uboot\0\0\0" string magic
    #
    # The original u-boot has: 0xEA00018E at offset 0 = ARM32 B #0x640
    # boot0 derives entry point from the ARM32 B target: offset 0x640 from binary start.
    # It then jumps to (load_addr + 0x640) = 0x4A000640 in AArch64 mode.
    #
    # We replicate this header exactly, and place an ARM64 B at offset 0x640
    # that jumps to our actual PeilessSec entry point at FD offset 0x7438.
    #
    # ARM32 B to offset 0x640: imm24 = (0x640-8)/4 = 0x18E → 0xEA00018E
    # ARM64 B from 0x4A000640 to 0x4A007438: offset=0x6DF8, imm26=0x1B7E → 0x14001B7E

    FD_BASE = 0x4A000000
    FV_OFFSET = 0x1000   # FV starts at FD+0x1000
    FV_BASE   = FD_BASE + FV_OFFSET  # 0x4A001000

    # Auto-detect PEILESS_ENTRY from FV ZeroVector ARM64 B instruction
    # The EDK2 build places a B _ModuleEntryPoint at the very start of the FV.
    zv_instr = struct.unpack_from('<I', edk2_fd, FV_OFFSET)[0]
    if (zv_instr >> 26) != 0x05:
        print(f"ERROR: FV ZeroVector[0] = 0x{zv_instr:08X} is not an ARM64 B instruction!")
        sys.exit(1)
    zv_imm26 = zv_instr & 0x3FFFFFF
    if zv_imm26 & (1 << 25):
        zv_imm26 -= (1 << 26)
    PEILESS_ENTRY = FV_BASE + zv_imm26 * 4
    print(f"  Auto-detected PEILESS_ENTRY = {PEILESS_ENTRY:#010x} (FV ZeroVector B: 0x{zv_instr:08X})")

    # Offset 0: ARM64 B from FD[0] to PeilessSec entry
    # Using ARM64 B (not ARM32) tells boot0/BL31 that BL33 is AArch64.
    arm64_b_offset = PEILESS_ENTRY - FD_BASE
    arm64_b_imm26  = (arm64_b_offset >> 2) & 0x3FFFFFF
    arm64_b_instr  = 0x14000000 | arm64_b_imm26
    edk2_fd[0x00:0x04] = struct.pack('<I', arm64_b_instr)

    # Offset 4: "uboot\0\0\0" magic
    edk2_fd[0x04:0x0C] = b'uboot\x00\x00\x00'

    # Offset 0x0C: checksum seed (match original)
    edk2_fd[0x0C:0x10] = struct.pack('<I', 0x5F0A6C39)

    # Offset 0x10: header size (match original = 0x4000)
    edk2_fd[0x10:0x14] = struct.pack('<I', 0x4000)

    # Offset 0x2C: run address
    edk2_fd[0x2C:0x30] = struct.pack('<I', FD_BASE)

    print(f"  Patched ARM64 B at offset 0: instr={arm64_b_instr:#010x} → {PEILESS_ENTRY:#010x} (_ModuleEntryPoint, AArch64 BL33)")

    # Read sunxi-package from dump
    pkg_data = bytearray(dump[PKG_OFFSET:PKG_OFFSET + 0x160000])

    # Verify package magic
    magic = pkg_data[:13]
    if magic == b'sunxi-package':
        print(f"sunxi-package magic OK")
    else:
        print(f"ERROR: bad package magic: {magic}")
        sys.exit(1)

    # Check u-boot slot size
    uboot_entry_off = 0x3C
    uboot_off  = struct.unpack_from('<I', pkg_data, uboot_entry_off + 68)[0]
    uboot_size = struct.unpack_from('<I', pkg_data, uboot_entry_off + 72)[0]
    print(f"u-boot slot: pkg+0x{uboot_off:06X}, size=0x{uboot_size:06X} ({uboot_size//1024}KB)")
    print(f"EDK2 FD:     size=0x{len(edk2_fd):06X} ({len(edk2_fd)//1024}KB)")

    if len(edk2_fd) > uboot_size:
        print(f"ERROR: FD ({len(edk2_fd)//1024}KB) larger than u-boot slot ({uboot_size//1024}KB)")
        sys.exit(1)
    print(f"  OK: FD fits in slot ({uboot_size - len(edk2_fd)} bytes to spare)")

    # Replace u-boot with EDK2 FD in package
    print("Patching sunxi-package: replacing u-boot with EDK2 FD...")
    pkg_data[uboot_off:uboot_off + len(edk2_fd)] = edk2_fd
    # Zero out remainder of u-boot slot
    remainder_start = uboot_off + len(edk2_fd)
    remainder_end   = uboot_off + uboot_size
    pkg_data[remainder_start:remainder_end] = bytes(remainder_end - remainder_start)

    # Update u-boot entry size in package header
    struct.pack_into('<I', pkg_data, uboot_entry_off + 72, len(edk2_fd))

    # -------------------------------------------------------------------------
    # Patch BL31 (TF-A monitor) to enable SMHC2 (eMMC) clocks before BL33
    #
    # Problem: TF-A (BL31) locks CCU from EL1 (NS world). SMHC2 clocks are
    # never enabled by boot0 (it only sets up SMHC0 for SD boot). We inject a
    # small stub into a zero-filled gap in BL31 that enables SMHC2 clocks while
    # still in EL3, then redirect a BL call right before the BL33 ERET.
    #
    # Injection plan:
    #   - BL31+0x032D8: BL to original function at BL31+0x3940 (pre-BL33 setup)
    #   - We redirect this BL to our stub at BL31+0x0E2D8 (1320-byte zero gap)
    #   - Stub: enable SMHC2 in CCU BGR + SMHC2_CLK_REG, then BL original, RET
    #
    # CCU registers (EL3-accessible, CCU_BASE=0x03001000):
    #   Confirmed H618 layout by BL31 disassembly:
    #     GIC @ 0x03400000, SPC @ 0x03000000, SID @ 0x03006200, R_PRCM @ 0x07010000
    #   All match H618 memory map → CCU at 0x03001000.
    #   CCU_SMHC_BGR_REG  = CCU_BASE + 0x84C  = 0x0300184C
    #   CCU_SMHC2_CLK_REG = CCU_BASE + 0x838  = 0x03001838
    # -------------------------------------------------------------------------
    BL31_OFF        = PKG_MONITOR_OFF   # 0x12C400 within pkg_data
    BL31_VA         = 0x48000000        # BL31 load VA

    STUB_OFF_IN_BL31  = 0x0E2D8         # text-section alignment padding: 1320 bytes, executable
    ORIG_BL_OFF       = 0x032D8         # BL instruction to redirect
    ORIG_CALLEE_OFF   = 0x3940          # original callee function offset in BL31

    STUB_VA     = BL31_VA + STUB_OFF_IN_BL31   # 0x48012914
    ORIG_BL_VA  = BL31_VA + ORIG_BL_OFF        # 0x480032D8
    ORIG_CALLEE_VA = BL31_VA + ORIG_CALLEE_OFF  # 0x48003940

    # Verify: current BL at BL31+0x032D8 must call ORIG_CALLEE (imm26 = 0x668/4 = 0x19A)
    expected_orig_bl = 0x9400019A
    actual_orig_bl   = struct.unpack_from('<I', pkg_data, BL31_OFF + ORIG_BL_OFF)[0]
    if actual_orig_bl != expected_orig_bl:
        print(f"WARNING: BL31+0x{ORIG_BL_OFF:X} expected 0x{expected_orig_bl:08X}, got 0x{actual_orig_bl:08X}")
        print(f"  BL31 layout may differ — skipping BL31 patch (eMMC clock may not work)")
    else:
        print(f"BL31 patching: BL at +0x{ORIG_BL_OFF:X} = 0x{actual_orig_bl:08X} OK")

        # Verify injection area is zero
        stub_area = pkg_data[BL31_OFF + STUB_OFF_IN_BL31 : BL31_OFF + STUB_OFF_IN_BL31 + 144]
        if any(stub_area):
            print(f"WARNING: BL31+0x{STUB_OFF_IN_BL31:X} is not zero — skipping BL31 patch")
        else:
            # Build stub instructions (ARM64 little-endian 32-bit words)
            # Diagnostic scratch area in DRAM: 0x41000000 (below BL33 load @ 0x4A000000)
            # UEFI driver reads:
            #   [+0x00] SID base @ 0x03006200 (BL31 reads this; non-zero = EL3 MMIO works)
            #   [+0x04] SPC+8   @ 0x03000008 (BL31 accesses; non-zero = EL3 MMIO works)
            #   [+0x08] SMHC0_CTRL @ 0x04020000 (NS-accessible; non-zero = EL3 reads work)
            #   [+0x0C] 0xC0DEBABE sentinel (always written: proves stub ran)
            #   [+0x10] SMHC0_CLK @ CCU_A=0x02001000+0x830
            #   [+0x14] SMHC0_CLK @ CCU_B=0x03001000+0x830
            #   [+0x18] SMHC0_CLK_old @ CCU_A+0x088 (sun8i-style offset)
            #   [+0x1C] SMHC0_CLK @ CCU_C=0x02000000+0x830
            #
            # BL within stub at instruction index 34
            bl_in_stub_va = STUB_VA + 34 * 4
            bl_offset     = ORIG_CALLEE_VA - bl_in_stub_va
            bl_imm26      = (bl_offset >> 2) & 0x3FFFFFF
            bl_instr      = 0x94000000 | bl_imm26

            # Compute sentinel instruction words at runtime
            # MOVZ W5, #0xBABE (hw=0, Rd=5): 0x52800000|(0xBABE<<5)|5
            movz_babe = 0x52800000 | (0xBABE << 5) | 5
            # MOVK W5, #0xC0DE, LSL#16 (hw=1, Rd=5): 0x72A00000|(0xC0DE<<5)|5
            movk_c0de = 0x72A00000 | (0xC0DE << 5) | 5
            print(f"  Sentinel instrs: MOVZ=0x{movz_babe:08X}, MOVK=0x{movk_c0de:08X} → 0xC0DEBABE")

            # Instruction encodings (all verified):
            # LDR W1, [Xn, #off]: 0xB9400000|(off//4<<10)|(n<<5)|1
            # STR W1, [X4, #off]: 0xB9000000|(off//4<<10)|(4<<5)|1
            # MOVZ X1, #hi, LSL#16: 0xD2A00000|(hi<<5)|1
            # MOVK X1, #lo       : 0xF2800000|(lo<<5)|1
            stub_instrs = [
                0xA9BF7BFD,  # [0]  STP X29, X30, [SP, #-16]!
                0x910003FD,  # [1]  MOV X29, SP
                0xD2A82004,  # [2]  MOVZ X4, #0x4100, LSL#16   ; X4 = 0x41000000
                # Sentinel: [X4+0xC] = 0xC0DEBABE (always prove stub ran)
                movz_babe,   # [3]  MOVZ W5, #0xBABE
                movk_c0de,   # [4]  MOVK W5, #0xC0DE, LSL#16   ; W5 = 0xC0DEBABE
                0xB9000C85,  # [5]  STR W5, [X4, #0xC]         ; [0x4100000C] = sentinel
                # Probe 0x03006200 (SID) → [X4+0x00]  BL31 reads this; EL3 MMIO sanity
                0xD2A06001,  # [6]  MOVZ X1, #0x300, LSL#16    ; X1 = 0x03000000
                0xF28C4001,  # [7]  MOVK X1, #0x6200           ; X1 = 0x03006200
                0xB9400021,  # [8]  LDR W1, [X1]               ; W1 = SID
                0xB9000081,  # [9]  STR W1, [X4, #0]           ; [0x41000000] = SID
                # Probe 0x03000008 (SPC+8) → [X4+0x04]  BL31 accesses this
                0xD2A06001,  # [10] MOVZ X1, #0x300, LSL#16    ; X1 = 0x03000000
                0xB9400421,  # [11] LDR W1, [X1, #8]           ; W1 = SPC+8  (imm12=2)
                0xB9000481,  # [12] STR W1, [X4, #4]           ; [0x41000004] = SPC+8
                # Probe 0x04020000 (SMHC0 CTRL) → [X4+0x08]  NS-accessible, EL3 must work
                0xD2A08041,  # [13] MOVZ X1, #0x402, LSL#16    ; X1 = 0x04020000
                0xB9400021,  # [14] LDR W1, [X1]               ; W1 = SMHC0_CTRL
                0xB9000881,  # [15] STR W1, [X4, #8]           ; [0x41000008] = SMHC0_CTRL
                # Probe CCU_A=0x02001000+0x830 → [X4+0x10]
                0xD2A04001,  # [16] MOVZ X1, #0x200, LSL#16    ; X1 = 0x02000000
                0xF2820001,  # [17] MOVK X1, #0x1000           ; X1 = 0x02001000
                0xB9483021,  # [18] LDR W1, [X1, #0x830]       ; W1 = CLK@0x02001830
                0xB9001081,  # [19] STR W1, [X4, #0x10]        ; [0x41000010] = CLK@02001
                # Probe CCU_B=0x03001000+0x830 → [X4+0x14]
                0xD2A06001,  # [20] MOVZ X1, #0x300, LSL#16
                0xF2820001,  # [21] MOVK X1, #0x1000           ; X1 = 0x03001000
                0xB9483021,  # [22] LDR W1, [X1, #0x830]       ; W1 = CLK@0x03001830
                0xB9001481,  # [23] STR W1, [X4, #0x14]        ; [0x41000014] = CLK@03001
                # Probe CCU_A+0x088 (sun8i-style SMHC0_CLK) → [X4+0x18]
                0xD2A04001,  # [24] MOVZ X1, #0x200, LSL#16
                0xF2820001,  # [25] MOVK X1, #0x1000           ; X1 = 0x02001000
                0xB9408821,  # [26] LDR W1, [X1, #0x88]        ; W1 = CLK@0x02001088
                0xB9001881,  # [27] STR W1, [X4, #0x18]        ; [0x41000018] = CLK_old@02001
                # Probe CCU_C=0x02000000+0x830 → [X4+0x1C]
                0xD2A04001,  # [28] MOVZ X1, #0x200, LSL#16    ; X1 = 0x02000000
                0xB9483021,  # [29] LDR W1, [X1, #0x830]       ; W1 = CLK@0x02000830
                0xB9001C81,  # [30] STR W1, [X4, #0x1C]        ; [0x4100001C] = CLK@02000
                0xD5033F9F,  # [31] DSB SY
                0xD5033F9F,  # [32] ISB (ensure visibility)
                0xD503201F,  # [33] NOP
                bl_instr,    # [34] BL ORIG_CALLEE
                0xA8C17BFD,  # [35] LDP X29, X30, [SP], #16
                0xD65F03C0,  # [36] RET
            ]

            # Write stub into BL31 zero gap
            stub_bytes = b''.join(struct.pack('<I', i) for i in stub_instrs)
            stub_start = BL31_OFF + STUB_OFF_IN_BL31
            pkg_data[stub_start : stub_start + len(stub_bytes)] = stub_bytes
            print(f"  Stub written at BL31+0x{STUB_OFF_IN_BL31:X} ({len(stub_bytes)} bytes)")
            print(f"  BL in stub → 0x{ORIG_CALLEE_VA:08X} (imm26=0x{bl_imm26:X}, instr=0x{bl_instr:08X})")

            # Patch the BL at BL31+0x032D8 to call our stub instead
            new_bl_offset = STUB_VA - ORIG_BL_VA   # 0xF63C
            new_bl_imm26  = (new_bl_offset >> 2) & 0x3FFFFFF
            new_bl_instr  = 0x94000000 | new_bl_imm26
            struct.pack_into('<I', pkg_data, BL31_OFF + ORIG_BL_OFF, new_bl_instr)
            print(f"  Redirected BL at BL31+0x{ORIG_BL_OFF:X}: 0x{actual_orig_bl:08X} → 0x{new_bl_instr:08X}")
            print(f"  (now calls stub at 0x{STUB_VA:08X})")

    # Recalculate package checksum
    # Allwinner sunxi-package: checksum at 0x14, seed=0x5F0A6C39, sum over all u32 in package
    PKG_CHECKSUM_OFF = 0x14
    PKG_CHECKSUM_SEED = 0x5F0A6C39
    struct.pack_into('<I', pkg_data, PKG_CHECKSUM_OFF, 0)  # zero checksum field before computing
    pkg_total_for_chk = PKG_SCP_OFF + PKG_SCP_SIZE
    total = PKG_CHECKSUM_SEED
    view = memoryview(pkg_data)
    for i in range(0, pkg_total_for_chk, 4):
        if i == PKG_CHECKSUM_OFF:
            continue
        total = (total + struct.unpack_from('<I', view, i)[0]) & 0xFFFFFFFF
    struct.pack_into('<I', pkg_data, PKG_CHECKSUM_OFF, total)
    print(f"  Package checksum updated: {total:#010x}")

    # Build 16MB image
    print(f"Building {IMG_SIZE//1024//1024}MB SD image...")
    img = bytearray(IMG_SIZE)  # all zeros

    # Write boot0
    boot0 = dump[BOOT0_OFFSET:BOOT0_OFFSET + BOOT0_SIZE]
    img[BOOT0_OFFSET:BOOT0_OFFSET + len(boot0)] = boot0
    print(f"  boot0 written at 0x{BOOT0_OFFSET:06X} ({len(boot0)//1024}KB)")

    # Write sunxi-package
    pkg_total = PKG_SCP_OFF + PKG_SCP_SIZE
    img[PKG_OFFSET:PKG_OFFSET + pkg_total] = pkg_data[:pkg_total]
    print(f"  sunxi-package written at 0x{PKG_OFFSET:06X} ({pkg_total//1024}KB)")

    # Write output
    print(f"Writing: {OUTPUT_IMG}")
    with open(OUTPUT_IMG, 'wb') as f:
        f.write(img)
    print(f"Done! Image size: {len(img)//1024//1024}MB")
    print()
    print("=== Next steps ===")
    print("Write to SD card:")
    print("  Linux (from Cubie or PC):")
    print("    sudo dd if=sd_boot.img of=/dev/sdX bs=1M status=progress")
    print("  Windows (Win32DiskImager or balena Etcher):")
    print("    Select sd_boot.img → select SD card drive → Write")
    print()
    print("Insert SD card into Cubie A7Z and power on.")
    print("Connect UART (115200 8N1) to see UEFI debug output.")

if __name__ == '__main__':
    main()
