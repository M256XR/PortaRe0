#!/usr/bin/env python3
import argparse
import ctypes
import ctypes.wintypes
import re
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
IMAGE_PATH = SCRIPT_DIR / "sd_boot.img"
MAKE_IMAGE_SCRIPT = SCRIPT_DIR / "make_sd_image.py"
BUILD_COMMAND = [
    "wsl.exe",
    "bash",
    "-c",
    "bash /mnt/d/Projects/PortaRe0/software/build/build_edk2.sh 2>&1",
]

WRITE_OFFSET = 0x020000
BUFFER_SIZE = 1024 * 1024
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


def print_section(title: str) -> None:
    print()
    print(f"=== {title} ===")


def fail(message: str, exit_code: int = 1) -> "NoReturn":
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(exit_code)


def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def run_and_stream(command: list[str], description: str, cwd: Path | None = None) -> None:
    print(f"Running: {description}")
    process = subprocess.Popen(
        command,
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="")

    return_code = process.wait()
    if return_code != 0:
        fail(f"{description} failed with exit code {return_code}")


def run_build() -> None:
    print_section("Step 1 - Build")
    run_and_stream(BUILD_COMMAND, "WSL EDK2 build", cwd=REPO_ROOT)


def run_make_image() -> None:
    print_section("Step 2 - Create SD Image")
    run_and_stream(
        [sys.executable, str(MAKE_IMAGE_SCRIPT)],
        "SD image creation",
        cwd=REPO_ROOT,
    )


def parse_wmic_disk_list(output: str) -> list[dict[str, str]]:
    lines = [line.rstrip() for line in output.splitlines() if line.strip()]
    if not lines:
        return []

    header = lines[0]
    device_match = re.search(r"DeviceID", header)
    model_match = re.search(r"Model", header)
    partitions_match = re.search(r"Partitions", header)
    size_match = re.search(r"Size", header)

    if not all([device_match, model_match, partitions_match, size_match]):
        fail("Unable to parse 'wmic diskdrive list brief' output.")

    starts = {
        "device_id": device_match.start(),
        "model": model_match.start(),
        "partitions": partitions_match.start(),
        "size": size_match.start(),
    }

    drives: list[dict[str, str]] = []
    for line in lines[1:]:
        if len(line) < starts["partitions"]:
            continue

        device_id = line[starts["device_id"]:starts["model"]].strip()
        model = line[starts["model"]:starts["partitions"]].strip()
        partitions = line[starts["partitions"]:starts["size"]].strip()
        size = line[starts["size"]:].strip()

        if not device_id:
            continue

        drives.append(
            {
                "device_id": device_id,
                "model": model,
                "partitions": partitions,
                "size": size,
            }
        )

    return drives


def list_physical_drives() -> list[dict[str, str]]:
    result = subprocess.run(
        ["wmic", "diskdrive", "list", "brief"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        fail(f"'wmic diskdrive list brief' failed with exit code {result.returncode}")

    drives = parse_wmic_disk_list(result.stdout)
    if not drives:
        fail("No physical drives found.")
    return drives


def format_size(size_text: str) -> str:
    try:
        size = int(size_text)
    except ValueError:
        return size_text or "unknown"

    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size)
    for unit in units:
        if value < 1024.0 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024.0
    return size_text


def select_drive(drives: list[dict[str, str]]) -> dict[str, str]:
    print("Available physical drives:")
    for index, drive in enumerate(drives):
        print(
            f"  [{index}] {drive['device_id']} | {drive['model']} | "
            f"Partitions: {drive['partitions']} | Size: {format_size(drive['size'])}"
        )

    while True:
        choice = input("Select drive index to write: ").strip()
        try:
            drive_index = int(choice)
        except ValueError:
            print("Enter a valid numeric index.")
            continue

        if 0 <= drive_index < len(drives):
            return drives[drive_index]

        print("Index out of range.")


def confirm_drive(drive: dict[str, str]) -> None:
    print()
    print("Selected drive:")
    print(f"  Device:     {drive['device_id']}")
    print(f"  Model:      {drive['model']}")
    print(f"  Partitions: {drive['partitions']}")
    print(f"  Size:       {format_size(drive['size'])}")
    print(f"  Image:      {IMAGE_PATH}")
    print(f"  Write mode: preserve bytes 0x000000-0x01FFFF, write from 0x{WRITE_OFFSET:06X}")

    response = input("Type 'write' to confirm: ").strip().lower()
    if response != "write":
        fail("Write cancelled.")


def open_device_handle(path: str, write: bool = False):
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


def device_io_control(handle, code: int, label: str) -> None:
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


def unlock_handle(handle) -> None:
    bytes_returned = ctypes.wintypes.DWORD(0)
    k32.DeviceIoControl(
        handle,
        FSCTL_UNLOCK_VOLUME,
        None,
        0,
        None,
        0,
        ctypes.byref(bytes_returned),
        None,
    )


def get_disk_number_from_device_id(device_id: str) -> int:
    match = re.search(r"PhysicalDrive(\d+)$", device_id, re.IGNORECASE)
    if not match:
        fail(f"Unable to derive disk number from device id: {device_id}")
    return int(match.group(1))


def get_volume_ids_for_disk(disk_number: int) -> list[str]:
    result = subprocess.run(
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
    if result.returncode != 0:
        fail(f"Failed to query volumes for disk {disk_number}: {result.stderr.strip()}")

    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def write_image_to_drive(drive_path: str) -> None:
    if not IMAGE_PATH.exists():
        fail(f"Image not found: {IMAGE_PATH}")

    image_size = IMAGE_PATH.stat().st_size
    if image_size <= WRITE_OFFSET:
        fail(
            f"Image is too small ({image_size} bytes); expected data beyond 0x{WRITE_OFFSET:06X}"
        )

    bytes_to_write = image_size - WRITE_OFFSET
    print(
        f"Writing {bytes_to_write} bytes from {IMAGE_PATH.name} to {drive_path} "
        f"at offset 0x{WRITE_OFFSET:06X}"
    )

    disk_number = get_disk_number_from_device_id(drive_path)
    volume_ids = get_volume_ids_for_disk(disk_number)

    volume_handles = []
    disk_handle = None
    written = 0
    try:
        for volume_id in volume_ids:
            volume_path = volume_id.rstrip("\\")
            handle = open_device_handle(volume_path, write=True)
            device_io_control(handle, FSCTL_LOCK_VOLUME, f"Lock {volume_path}")
            device_io_control(handle, FSCTL_DISMOUNT_VOLUME, f"Dismount {volume_path}")
            volume_handles.append(handle)

        disk_handle = open_device_handle(drive_path, write=True)
        device_io_control(disk_handle, FSCTL_LOCK_VOLUME, f"Lock {drive_path}")

        position = ctypes.c_long(WRITE_OFFSET)
        if k32.SetFilePointer(disk_handle, position.value, None, FILE_BEGIN) == 0xFFFFFFFF:
            error = k32.GetLastError()
            if error != 0:
                fail(f"SetFilePointer failed (err={error})")

        with open(IMAGE_PATH, "rb") as image_file:
            image_file.seek(WRITE_OFFSET)

            while True:
                chunk = image_file.read(BUFFER_SIZE)
                if not chunk:
                    break

                buffer = ctypes.create_string_buffer(chunk)
                chunk_written = ctypes.wintypes.DWORD(0)
                ok = k32.WriteFile(
                    disk_handle,
                    buffer,
                    len(chunk),
                    ctypes.byref(chunk_written),
                    None,
                )
                if not ok:
                    fail(f"WriteFile failed (err={k32.GetLastError()})")
                if chunk_written.value != len(chunk):
                    fail(
                        f"Short write: expected {len(chunk)} bytes, wrote {chunk_written.value}"
                    )

                written += chunk_written.value
                print(f"\rProgress: {written}/{bytes_to_write} bytes", end="", flush=True)

        if not k32.FlushFileBuffers(disk_handle):
            fail(f"FlushFileBuffers failed (err={k32.GetLastError()})")
    finally:
        if disk_handle is not None:
            unlock_handle(disk_handle)
            k32.CloseHandle(disk_handle)

        for handle in volume_handles:
            unlock_handle(handle)
            k32.CloseHandle(handle)

    print()
    print(f"OK: wrote {written} bytes to {drive_path} at offset 0x{WRITE_OFFSET:06X}")
    print("GPT partition table preserved.")


def run_write() -> None:
    print_section("Step 3 - Write To SD Card")

    if not is_admin():
        fail("This script must be run as Administrator for disk write access.")

    drives = list_physical_drives()
    selected = select_drive(drives)
    confirm_drive(selected)
    write_image_to_drive(selected["device_id"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build EDK2, create sd_boot.img, and write it to an SD card."
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip step 1 and only create the image and write it.",
    )
    parser.add_argument(
        "--skip-image",
        action="store_true",
        help="Skip steps 1 and 2 and only write the existing image.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.skip_image:
        args.skip_build = True

    if not args.skip_build:
        run_build()

    if not args.skip_image:
        run_make_image()

    run_write()


if __name__ == "__main__":
    main()
