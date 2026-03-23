import ctypes, ctypes.wintypes, sys

GENERIC_READ  = 0x80000000
GENERIC_WRITE = 0x40000000
OPEN_EXISTING = 3
FILE_SHARE_READ  = 1
FILE_SHARE_WRITE = 2
FSCTL_LOCK_VOLUME   = 0x00090018
FSCTL_UNLOCK_VOLUME = 0x0009001C
INVALID_HANDLE_VALUE = ctypes.wintypes.HANDLE(-1).value

kernel32 = ctypes.windll.kernel32

IMG  = r"D:\Projects\PortaRe0\software\build\sd_boot.img"
DISK = r"\\.\PhysicalDrive3"
SKIP = 0x020000
SIZE = 16 * 1024 * 1024

h = kernel32.CreateFileW(
    DISK, GENERIC_READ | GENERIC_WRITE,
    FILE_SHARE_READ | FILE_SHARE_WRITE,
    None, OPEN_EXISTING, 0, None
)
if h == INVALID_HANDLE_VALUE:
    print(f"ERROR: Cannot open {DISK} (err={kernel32.GetLastError()})")
    sys.exit(1)
print(f"Opened {DISK}")

bytes_ret = ctypes.wintypes.DWORD(0)
ok = kernel32.DeviceIoControl(h, FSCTL_LOCK_VOLUME, None, 0, None, 0, ctypes.byref(bytes_ret), None)
print(f"Lock: {'OK' if ok else 'skipped (err=' + str(kernel32.GetLastError()) + ')'}")

with open(IMG, "rb") as f:
    f.seek(SKIP)
    raw = f.read(SIZE - SKIP)

buf = ctypes.create_string_buffer(raw)
kernel32.SetFilePointer(h, SKIP, None, 0)
written = ctypes.wintypes.DWORD(0)
ok = kernel32.WriteFile(h, buf, len(raw), ctypes.byref(written), None)
if not ok:
    print(f"ERROR: WriteFile failed (err={kernel32.GetLastError()})")
    kernel32.CloseHandle(h)
    sys.exit(1)

print(f"Written: {written.value // 1024}KB at offset 0x{SKIP:06X}")
kernel32.DeviceIoControl(h, FSCTL_UNLOCK_VOLUME, None, 0, None, 0, ctypes.byref(bytes_ret), None)
kernel32.CloseHandle(h)
print("Done. GPT preserved.")
