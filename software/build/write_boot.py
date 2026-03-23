"""
Write Allwinner boot sectors to PhysicalDrive (SD card) while preserving GPT.

Allwinner T527/A733 boot layout:
  LBA   0- 33  (     0 - 16383): GPT protective MBR + GPT header/entries  <- SKIP
  LBA  34- 255 ( 17408 - 130559): unused (zeros in image)                  <- skip (safe)
  LBA 256-...  (131072 - ...   ): boot0                                    <- WRITE
  LBA 24576-.. (12582912 -     ): sunxi-package (EDK2 FD)                  <- WRITE

Strategy: write image bytes starting from offset 0x020000 (boot0 start),
preserving everything before that (GPT lives in LBA 0-33).
"""
import ctypes
import ctypes.wintypes
import re
import subprocess
import sys

IMG   = r"D:\Projects\PortaRe0\software\build\sd_boot.img"
DISK  = r"\\.\PhysicalDrive3"
SKIP  = 0x020000          # start writing from boot0 offset (128KB)
SIZE  = 16 * 1024 * 1024  # total image size (16MB)

GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
OPEN_EXISTING = 3
FILE_SHARE_READ = 1
FILE_SHARE_WRITE = 2
FILE_BEGIN = 0
FSCTL_LOCK_VOLUME = 0x00090018
FSCTL_UNLOCK_VOLUME = 0x0009001C
FSCTL_DISMOUNT_VOLUME = 0x00090020
INVALID_HANDLE_VALUE = ctypes.wintypes.HANDLE(-1).value

k32 = ctypes.windll.kernel32


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def open_handle(path, write=False):
    access = GENERIC_READ | (GENERIC_WRITE if write else 0)
    handle = k32.CreateFileW(
        path,
        access,
        FILE_SHARE_READ | FILE_SHARE_WRITE,
        None,
        OPEN_EXISTING,
        0,
        None,
    )
    if handle == INVALID_HANDLE_VALUE:
        fail(f"Cannot open {path} (err={k32.GetLastError()})")
    return handle


def ioctl(handle, code, label):
    bytes_returned = ctypes.wintypes.DWORD(0)
    ok = k32.DeviceIoControl(
        handle,
        code,
        None,
        0,
        None,
        0,
        ctypes.byref(bytes_returned),
        None,
    )
    if not ok:
        fail(f"{label} failed (err={k32.GetLastError()})")


def get_disk_number(disk_path):
    match = re.search(r"PhysicalDrive(\d+)$", disk_path, re.IGNORECASE)
    if not match:
        fail(f"Unable to derive disk number from path: {disk_path}")
    return int(match.group(1))


def get_volume_ids_for_disk(disk_number):
    ps = subprocess.run(
        [
            "powershell",
            "-Command",
            (
                f"Get-Partition -DiskNumber {disk_number} | "
                "Get-Volume | Select-Object -ExpandProperty UniqueId -Unique"
            ),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if ps.returncode != 0:
        fail(f"Failed to query volumes for disk {disk_number}: {ps.stderr.strip()}")

    return [line.strip() for line in ps.stdout.splitlines() if line.strip()]


def write_file(handle, data):
    buffer = ctypes.create_string_buffer(data)
    bytes_written = ctypes.wintypes.DWORD(0)
    ok = k32.WriteFile(handle, buffer, len(data), ctypes.byref(bytes_written), None)
    if not ok:
        fail(f"WriteFile failed (err={k32.GetLastError()})")
    if bytes_written.value != len(data):
        fail(f"Short write: expected {len(data)} bytes, wrote {bytes_written.value}")


def write_image_to_drive():
    disk_number = get_disk_number(DISK)
    volume_ids = get_volume_ids_for_disk(disk_number)

    volume_handles = []
    disk_handle = None
    try:
        for volume_id in volume_ids:
            volume_path = volume_id.rstrip("\\")
            handle = open_handle(volume_path, write=True)
            ioctl(handle, FSCTL_LOCK_VOLUME, f"Lock {volume_path}")
            ioctl(handle, FSCTL_DISMOUNT_VOLUME, f"Dismount {volume_path}")
            volume_handles.append(handle)

        disk_handle = open_handle(DISK, write=True)
        ioctl(disk_handle, FSCTL_LOCK_VOLUME, f"Lock {DISK}")

        with open(IMG, "rb") as image_file:
            image_file.seek(SKIP)
            data = image_file.read(SIZE - SKIP)

        write_size = len(data)
        print(f"Writing {write_size // 1024}KB at offset 0x{SKIP:06X} (preserving GPT in LBA 0-33)")

        position = ctypes.c_long(SKIP)
        if k32.SetFilePointer(disk_handle, position.value, None, FILE_BEGIN) == 0xFFFFFFFF:
            error = k32.GetLastError()
            if error != 0:
                fail(f"SetFilePointer failed (err={error})")

        write_file(disk_handle, data)
        if not k32.FlushFileBuffers(disk_handle):
            fail(f"FlushFileBuffers failed (err={k32.GetLastError()})")
        return write_size
    finally:
        if disk_handle is not None:
            k32.DeviceIoControl(
                disk_handle,
                FSCTL_UNLOCK_VOLUME,
                None,
                0,
                None,
                0,
                ctypes.byref(ctypes.wintypes.DWORD(0)),
                None,
            )
            k32.CloseHandle(disk_handle)

        for handle in volume_handles:
            k32.DeviceIoControl(
                handle,
                FSCTL_UNLOCK_VOLUME,
                None,
                0,
                None,
                0,
                ctypes.byref(ctypes.wintypes.DWORD(0)),
                None,
            )
            k32.CloseHandle(handle)

write_size = write_image_to_drive()

print(f"OK: wrote {write_size // 1024}KB to {DISK} (offset 0x{SKIP:06X})")
print("GPT partition table preserved.")
