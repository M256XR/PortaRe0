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

BOOT0DUMP   = "D:/Projects/PortaRe0/software/boot0dump.bin"
EDK2_FD     = "D:/Projects/PortaRe0/software/build/A733.fd"
OUTPUT_IMG  = "D:/Projects/PortaRe0/software/build/sd_boot.img"

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

    # Verify FD starts with our jump stub
    if edk2_fd[:4] == bytes([0x0E, 0x1D, 0x00, 0x14]):
        print("  FD jump stub OK: b #0x7438")
    else:
        print(f"  WARNING: unexpected FD start: {edk2_fd[:4].hex()}")

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
    PEILESS_ENTRY = 0x4A007550   # PeilessSec _ModuleEntryPoint (FV ZeroVector confirmed: FV_base 0x4A001000 + 0x6550)
    ARM32_B_TARGET = 0x640       # matches original u-boot header
    ARM64_ENTRY_OFFSET = ARM32_B_TARGET  # we put ARM64 code here

    # Offset 0: ARM64 B from 0x4A000000 to PeilessSec entry 0x4A0074D8
    # Using ARM64 B (not ARM32) tells boot0/BL31 that BL33 is AArch64.
    arm64_b_offset = PEILESS_ENTRY - FD_BASE   # = 0x7480
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
