"""Write EDK2 boot sectors to PhysicalDrive3, locking all volumes first."""
import ctypes, ctypes.wintypes, subprocess, sys, re, hashlib, os
from pathlib import Path

GENERIC_READ  = 0x80000000
GENERIC_WRITE = 0x40000000
OPEN_EXISTING = 3
FILE_SHARE_READ  = 1
FILE_SHARE_WRITE = 2
FILE_FLAG_WRITE_THROUGH = 0x80000000
FSCTL_LOCK_VOLUME    = 0x00090018
FSCTL_UNLOCK_VOLUME  = 0x0009001C
FSCTL_DISMOUNT_VOLUME = 0x00090020
INVALID_HANDLE_VALUE = ctypes.wintypes.HANDLE(-1).value

k32 = ctypes.windll.kernel32

SCRIPT_DIR = Path(__file__).resolve().parent
IMG  = str(SCRIPT_DIR / "sd_boot.img")
FD   = str(SCRIPT_DIR / "A733.fd")
MAKE_SD_IMAGE = str(SCRIPT_DIR / "make_sd_image.py")
DISK = r"\\.\PhysicalDrive3"
SKIP = 0x000000  # Write from LBA 0: GPT + boot0 + EDK2 in one pass (was 0x020000)
SIZE = 16 * 1024 * 1024


def ensure_fresh_sd_image():
    if not os.path.exists(FD):
        print(f"Missing firmware image: {FD}")
        sys.exit(1)

    if (not os.path.exists(IMG)) or (os.path.getmtime(IMG) < os.path.getmtime(FD)):
        print("--- Regenerating sd_boot.img from latest A733.fd ---")
        subprocess.run([sys.executable, MAKE_SD_IMAGE], check=True)


ensure_fresh_sd_image()

def open_handle(path, write=False):
    access = GENERIC_READ | (GENERIC_WRITE if write else 0)
    flags = FILE_FLAG_WRITE_THROUGH if write else 0
    h = k32.CreateFileW(path, access,
                        FILE_SHARE_READ | FILE_SHARE_WRITE,
                        None, OPEN_EXISTING, flags, None)
    if h == INVALID_HANDLE_VALUE:
        print(f"  Cannot open {path} (err={k32.GetLastError()})")
        return None
    return h

def ioctl(h, code, label=""):
    br = ctypes.wintypes.DWORD(0)
    ok = k32.DeviceIoControl(h, code, None, 0, None, 0, ctypes.byref(br), None)
    print(f"  {label}: {'OK' if ok else 'err=' + str(k32.GetLastError())}")
    return ok

def flush_handle(h, label="Flush"):
    ok = k32.FlushFileBuffers(h)
    print(f"  {label}: {'OK' if ok else 'err=' + str(k32.GetLastError())}")
    return ok

# 1. Get all volume GUIDs on Disk 3
print("--- Finding volumes on Disk 3 ---")
ps = subprocess.run(
    ["powershell", "-Command",
     "Get-Partition -DiskNumber 3 | Get-Volume | ForEach-Object { $_.UniqueId }"],
    capture_output=True, text=True
)
vol_ids = [v.strip() for v in ps.stdout.strip().splitlines() if v.strip()]
print(f"  Volumes: {vol_ids}")

# 2. Lock + dismount each volume
vol_handles = []
for vid in vol_ids:
    # UniqueId from PowerShell looks like \\?\Volume{guid}\
    path = vid.rstrip("\\")
    print(f"  Locking {path}")
    h = open_handle(path, write=True)
    if h:
        ioctl(h, FSCTL_LOCK_VOLUME, "Lock")
        ioctl(h, FSCTL_DISMOUNT_VOLUME, "Dismount")
        vol_handles.append(h)

# 3. Write to disk
print(f"\n--- Writing to {DISK} ---")
hd = open_handle(DISK, write=True)
if not hd:
    sys.exit(1)
ioctl(hd, FSCTL_LOCK_VOLUME, "Disk lock")

with open(IMG, "rb") as f:
    f.seek(SKIP)
    raw = f.read(SIZE - SKIP)
expected_sha = hashlib.sha256(raw).hexdigest()

buf = ctypes.create_string_buffer(raw)
k32.SetFilePointer(hd, SKIP, None, 0)
written = ctypes.wintypes.DWORD(0)
ok = k32.WriteFile(hd, buf, len(raw), ctypes.byref(written), None)
if not ok:
    print(f"WriteFile failed err={k32.GetLastError()}")
    k32.CloseHandle(hd)
    sys.exit(1)

print(f"Written: {written.value // 1024}KB at offset 0x{SKIP:06X}")
flush_handle(hd, "Disk flush")

# 3.5 Read back and verify the bytes that were written.
k32.SetFilePointer(hd, SKIP, None, 0)
read_buf = ctypes.create_string_buffer(len(raw))
read_back = ctypes.wintypes.DWORD(0)
ok = k32.ReadFile(hd, read_buf, len(raw), ctypes.byref(read_back), None)
if not ok:
    print(f"ReadFile verify failed err={k32.GetLastError()}")
    k32.CloseHandle(hd)
    sys.exit(1)
actual = read_buf.raw[:read_back.value]
actual_sha = hashlib.sha256(actual).hexdigest()
print(f"Verify SHA256 expected={expected_sha}")
print(f"Verify SHA256 actual  ={actual_sha}")
if actual != raw:
    mismatch = next((i for i, (a, b) in enumerate(zip(raw, actual)) if a != b), None)
    print(f"VERIFY MISMATCH at offset 0x{mismatch:06X}" if mismatch is not None else "VERIFY LENGTH MISMATCH")
    k32.CloseHandle(hd)
    sys.exit(2)
print("Verify: MATCH")

# 4. Cleanup
ioctl(hd, FSCTL_UNLOCK_VOLUME, "Disk unlock")
k32.CloseHandle(hd)
for h in vol_handles:
    ioctl(h, FSCTL_UNLOCK_VOLUME, "Vol unlock")
    k32.CloseHandle(h)

print("\nDone. GPT preserved.")
