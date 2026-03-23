"""Verify LBA 0 contents on PhysicalDrive3 using ctypes (same approach as format_sd.py)."""

import ctypes
import ctypes.wintypes
import struct

SECTOR_SIZE = 512
DISK = r"\\.\PhysicalDrive3"

GENERIC_READ = 0x80000000
OPEN_EXISTING = 3
FILE_SHARE_READ = 0x1
FILE_SHARE_WRITE = 0x2
FILE_BEGIN = 0
INVALID_HANDLE_VALUE = ctypes.wintypes.HANDLE(-1).value

k32 = ctypes.windll.kernel32


def open_handle(path):
    handle = k32.CreateFileW(
        path,
        GENERIC_READ,
        FILE_SHARE_READ | FILE_SHARE_WRITE,
        None,
        OPEN_EXISTING,
        0,
        None,
    )
    if handle == INVALID_HANDLE_VALUE:
        raise OSError(f"CreateFileW failed for {path} (WinError={k32.GetLastError()})")
    return handle


def read_at(handle, lba, count=1):
    offset = lba * SECTOR_SIZE
    new_pos = ctypes.c_longlong()
    ok = k32.SetFilePointerEx(
        handle,
        ctypes.c_longlong(offset),
        ctypes.byref(new_pos),
        FILE_BEGIN,
    )
    if not ok or new_pos.value != offset:
        raise OSError(f"SetFilePointerEx failed at offset {offset} (WinError={k32.GetLastError()})")

    size = count * SECTOR_SIZE
    buf = ctypes.create_string_buffer(size)
    bytes_read = ctypes.wintypes.DWORD(0)
    ok = k32.ReadFile(handle, buf, size, ctypes.byref(bytes_read), None)
    if not ok:
        raise OSError(f"ReadFile failed (WinError={k32.GetLastError()})")
    if bytes_read.value != size:
        raise OSError(f"Short read: got {bytes_read.value} of {size} bytes")
    return bytes(buf.raw)


def hexdump(data, label, max_bytes=64):
    print(f"\n--- {label} ---")
    for i in range(0, min(len(data), max_bytes), 16):
        chunk = data[i:i+16]
        hex_str = " ".join(f"{b:02X}" for b in chunk)
        print(f"  {i:04X}: {hex_str}")


def check_lba(handle, lba, description):
    print(f"\n=== LBA {lba}: {description} ===")
    data = read_at(handle, lba)
    first4 = data[0:4]
    last2 = data[510:512]
    is_zero = all(b == 0 for b in data)
    print(f"  bytes[0:4]    = {first4.hex().upper()} ({first4})")
    print(f"  bytes[510:512]= {last2.hex().upper()}")
    print(f"  all-zero      = {is_zero}")
    hexdump(data, f"LBA {lba} first 64 bytes")
    hexdump(data[496:512], f"LBA {lba} last 16 bytes (496-511)")
    return data


def main():
    print(f"Opening {DISK} for read-only verification")
    handle = open_handle(DISK)
    try:
        # LBA 0: Protective MBR
        # Expected: bytes[446:462] = partition entry with type 0xEE
        #           bytes[510:512] = 0x55 0xAA
        mbr = check_lba(handle, 0, "Protective MBR")
        mbr_sig = mbr[510:512]
        part_type = mbr[446 + 4]  # partition type byte in first entry
        print(f"  MBR signature (55AA?): {mbr_sig.hex().upper()}")
        print(f"  Partition type (EE?):  {part_type:02X}")

        # LBA 1: Primary GPT Header
        # Expected: bytes[0:8] = "EFI PART"
        gpt = check_lba(handle, 1, "Primary GPT Header")
        gpt_sig = gpt[0:8]
        print(f"  GPT signature (EFI PART?): {gpt_sig}")

        # LBA 2: Primary GPT Entries
        # Expected: first 16 bytes = ESP type GUID
        entries = check_lba(handle, 2, "Primary GPT Entries (first sector)")

        # LBA 2048: ESP VBR
        # Expected: bytes[0:3] = EB 58 90, bytes[510:512] = 55 AA
        vbr = check_lba(handle, 2048, "ESP VBR (FAT32)")
        vbr_jump = vbr[0:3]
        vbr_oem = vbr[3:11]
        print(f"  Jump (EB5890?): {vbr_jump.hex().upper()}")
        print(f"  OEM ID: {vbr_oem}")

        # Summary
        print("\n=== SUMMARY ===")
        lba0_ok = mbr_sig == b"\x55\xAA"
        lba1_ok = gpt_sig == b"EFI PART"
        lba0_allzero = all(b == 0 for b in mbr)
        print(f"  LBA 0 (MBR): {'OK - 55AA signature found' if lba0_ok else 'FAIL - no 55AA signature'}")
        print(f"  LBA 0 all-zero: {lba0_allzero}")
        print(f"  LBA 1 (GPT): {'OK - EFI PART signature found' if lba1_ok else 'FAIL - no EFI PART signature'}")
        if lba0_allzero:
            print("\n  => CASE A: LBA 0 reads as all-zero FROM WINDOWS.")
            print("     format_sd.py write did NOT persist to the physical device.")
        elif lba0_ok:
            print("\n  => CASE B: LBA 0 is correct from Windows side.")
            print("     The write reached the USB cache but may not have committed to flash.")
        else:
            print("\n  => UNEXPECTED: LBA 0 has data but 55AA signature is missing.")
    finally:
        k32.CloseHandle(handle)
        print("\nHandle closed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        import sys
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
