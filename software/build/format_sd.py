"""Format PhysicalDrive3 with a GPT and minimal FAT32 ESP using Windows ctypes."""

import binascii
import ctypes
import ctypes.wintypes
import struct
import subprocess
import sys
import uuid


SECTOR_SIZE = 512
DISK = r"\\.\PhysicalDrive3"
DISK_NUMBER = 3
DISK_SIZE_BYTES = 127_861_977_600
DISK_SECTORS = 249_730_815
LAST_LBA = DISK_SECTORS - 1

GPT_HEADER_LBA = 1
GPT_ENTRIES_LBA = 2
GPT_ENTRY_COUNT = 128
GPT_ENTRY_SIZE = 128
GPT_ENTRIES_SECTORS = (GPT_ENTRY_COUNT * GPT_ENTRY_SIZE) // SECTOR_SIZE
PRIMARY_FIRST_USABLE_LBA = 34
PRIMARY_LAST_USABLE_LBA = 249_730_781
BACKUP_ENTRIES_LBA = 249_730_782
BACKUP_HEADER_LBA = 249_730_814

ESP_START_LBA = 2048
ESP_SECTOR_COUNT = 532_480
ESP_END_LBA = ESP_START_LBA + ESP_SECTOR_COUNT - 1

BYTES_PER_SECTOR = 512
SECTORS_PER_CLUSTER = 8
RESERVED_SECTORS = 32
FAT_COUNT = 2
ROOT_CLUSTER = 2
FSINFO_SECTOR = 1
BACKUP_BOOT_SECTOR = 6
MEDIA_DESCRIPTOR = 0xF8

GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
OPEN_EXISTING = 3
FILE_SHARE_READ = 0x1
FILE_SHARE_WRITE = 0x2
FILE_BEGIN = 0
FSCTL_LOCK_VOLUME = 0x00090018
FSCTL_UNLOCK_VOLUME = 0x0009001C
FSCTL_DISMOUNT_VOLUME = 0x00090020
INVALID_HANDLE_VALUE = ctypes.wintypes.HANDLE(-1).value

k32 = ctypes.windll.kernel32


def fail(message):
    raise OSError(f"{message} (WinError={k32.GetLastError()})")


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
        fail(f"CreateFileW failed for {path}")
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
        fail(f"{label} failed")
    print(f"[ok] {label}")


def seek_absolute(handle, offset):
    new_pos = ctypes.c_longlong()
    ok = k32.SetFilePointerEx(
        handle,
        ctypes.c_longlong(offset),
        ctypes.byref(new_pos),
        FILE_BEGIN,
    )
    if not ok or new_pos.value != offset:
        fail(f"SetFilePointerEx failed at offset {offset}")


def write_at(handle, offset, data, label):
    seek_absolute(handle, offset)
    buffer = ctypes.create_string_buffer(data)
    written = ctypes.wintypes.DWORD(0)
    ok = k32.WriteFile(handle, buffer, len(data), ctypes.byref(written), None)
    if not ok:
        fail(f"WriteFile failed for {label}")
    if written.value != len(data):
        raise OSError(f"Short write for {label}: wrote {written.value} of {len(data)} bytes")
    print(f"[ok] {label}: {len(data)} bytes at LBA {offset // SECTOR_SIZE}")


def close_handle(handle):
    if handle:
        k32.CloseHandle(handle)


def crc32(data):
    return binascii.crc32(data) & 0xFFFFFFFF


def calculate_fat_size(total_sectors, reserved, sectors_per_cluster, fat_count):
    fat_size = 1
    while True:
        data_sectors = total_sectors - reserved - (fat_count * fat_size)
        cluster_count = data_sectors // sectors_per_cluster
        needed = ((cluster_count + 2) * 4 + (BYTES_PER_SECTOR - 1)) // BYTES_PER_SECTOR
        if needed == fat_size:
            return fat_size
        fat_size = needed


def build_protective_mbr():
    mbr = bytearray(SECTOR_SIZE)
    mbr[446:462] = struct.pack(
        "<B3sB3sII",
        0x00,
        b"\x00\x02\x00",
        0xEE,
        b"\xFF\xFF\xFF",
        1,
        0xFFFFFFFF,
    )
    mbr[510:512] = b"\x55\xAA"
    return bytes(mbr)


def build_partition_entries():
    entries = bytearray(GPT_ENTRY_COUNT * GPT_ENTRY_SIZE)
    esp_type_guid = uuid.UUID("c12a7328-f81f-11d2-ba4b-00a0c93ec93b").bytes_le
    esp_unique_guid = uuid.uuid4().bytes_le
    esp_name = "ESP".encode("utf-16le").ljust(72, b"\x00")
    entries[0:GPT_ENTRY_SIZE] = struct.pack(
        "<16s16sQQQ72s",
        esp_type_guid,
        esp_unique_guid,
        ESP_START_LBA,
        ESP_END_LBA,
        0,
        esp_name,
    )
    return bytes(entries)


def build_gpt_header(my_lba, alternate_lba, entries_lba, entries_crc, disk_guid):
    header = bytearray(SECTOR_SIZE)
    struct.pack_into(
        "<8sIIIIQQQQ16sQIII",
        header,
        0,
        b"EFI PART",
        0x00010000,
        92,
        0,
        0,
        my_lba,
        alternate_lba,
        PRIMARY_FIRST_USABLE_LBA,
        PRIMARY_LAST_USABLE_LBA,
        disk_guid,
        entries_lba,
        GPT_ENTRY_COUNT,
        GPT_ENTRY_SIZE,
        entries_crc,
    )
    header_crc = crc32(header[:92])
    struct.pack_into("<I", header, 16, header_crc)
    return bytes(header)


def build_fat32_vbr(total_sectors, fat_size_sectors):
    vbr = bytearray(SECTOR_SIZE)
    vbr[0:3] = b"\xEB\x58\x90"
    vbr[3:11] = b"MSDOS5.0"
    struct.pack_into("<H", vbr, 11, BYTES_PER_SECTOR)
    vbr[13] = SECTORS_PER_CLUSTER
    struct.pack_into("<H", vbr, 14, RESERVED_SECTORS)
    vbr[16] = FAT_COUNT
    struct.pack_into("<H", vbr, 17, 0)
    struct.pack_into("<H", vbr, 19, 0)
    vbr[21] = MEDIA_DESCRIPTOR
    struct.pack_into("<H", vbr, 22, 0)
    struct.pack_into("<H", vbr, 24, 63)
    struct.pack_into("<H", vbr, 26, 255)
    struct.pack_into("<I", vbr, 28, ESP_START_LBA)
    struct.pack_into("<I", vbr, 32, total_sectors)
    struct.pack_into("<I", vbr, 36, fat_size_sectors)
    struct.pack_into("<H", vbr, 40, 0)
    struct.pack_into("<H", vbr, 42, 0)
    struct.pack_into("<I", vbr, 44, ROOT_CLUSTER)
    struct.pack_into("<H", vbr, 48, FSINFO_SECTOR)
    struct.pack_into("<H", vbr, 50, BACKUP_BOOT_SECTOR)
    vbr[64] = 0x80
    vbr[66] = 0x29
    vbr[67:71] = struct.pack("<I", uuid.uuid4().int & 0xFFFFFFFF)
    vbr[71:82] = b"ESP        "
    vbr[82:90] = b"FAT32   "
    vbr[510:512] = b"\x55\xAA"
    return bytes(vbr)


def build_fsinfo():
    fsinfo = bytearray(SECTOR_SIZE)
    struct.pack_into("<I", fsinfo, 0, 0x41615252)
    struct.pack_into("<I", fsinfo, 484, 0x61417272)
    struct.pack_into("<I", fsinfo, 488, 0xFFFFFFFF)
    struct.pack_into("<I", fsinfo, 492, 0xFFFFFFFF)
    struct.pack_into("<I", fsinfo, 508, 0xAA550000)
    return bytes(fsinfo)


def build_fat_sector_image(fat_size_sectors):
    fat = bytearray(fat_size_sectors * SECTOR_SIZE)
    struct.pack_into("<I", fat, 0, 0x0FFFFFF8)
    struct.pack_into("<I", fat, 4, 0x0FFFFFFF)
    struct.pack_into("<I", fat, 8, 0x0FFFFFFF)
    return bytes(fat)


def get_volume_ids():
    command = (
        f"Get-Partition -DiskNumber {DISK_NUMBER} | "
        "Get-Volume | ForEach-Object { $_.UniqueId }"
    )
    result = subprocess.run(
        ["powershell", "-Command", command],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or "no stderr"
        raise RuntimeError(f"PowerShell volume query failed: {stderr}")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main():
    print(f"Formatting {DISK}")
    print(f"Disk size: {DISK_SIZE_BYTES} bytes ({DISK_SECTORS} sectors)")

    fat_size_sectors = calculate_fat_size(
        ESP_SECTOR_COUNT,
        RESERVED_SECTORS,
        SECTORS_PER_CLUSTER,
        FAT_COUNT,
    )
    fat_start_lba = ESP_START_LBA + RESERVED_SECTORS
    fat2_start_lba = fat_start_lba + fat_size_sectors
    data_start_lba = fat2_start_lba + fat_size_sectors
    root_dir_lba = data_start_lba
    print(f"ESP FAT size: {fat_size_sectors} sectors per FAT")
    print(f"ESP root directory starts at LBA {root_dir_lba}")

    print("Building GPT structures")
    partition_entries = build_partition_entries()
    entries_crc = crc32(partition_entries)
    disk_guid = uuid.uuid4().bytes_le
    primary_header = build_gpt_header(
        GPT_HEADER_LBA,
        BACKUP_HEADER_LBA,
        GPT_ENTRIES_LBA,
        entries_crc,
        disk_guid,
    )
    backup_header = build_gpt_header(
        BACKUP_HEADER_LBA,
        GPT_HEADER_LBA,
        BACKUP_ENTRIES_LBA,
        entries_crc,
        disk_guid,
    )
    protective_mbr = build_protective_mbr()

    print("Building FAT32 structures")
    vbr = build_fat32_vbr(ESP_SECTOR_COUNT, fat_size_sectors)
    fsinfo = build_fsinfo()
    fat = build_fat_sector_image(fat_size_sectors)
    root_dir = bytes(SECTORS_PER_CLUSTER * SECTOR_SIZE)

    print("Finding volumes on Disk 3")
    volume_ids = get_volume_ids()
    print(f"Volumes: {volume_ids if volume_ids else 'none'}")

    disk_handle = None
    volume_handles = []
    try:
        for volume_id in volume_ids:
            path = volume_id.rstrip("\\")
            print(f"Locking volume {path}")
            volume_handle = open_handle(path, write=True)
            ioctl(volume_handle, FSCTL_LOCK_VOLUME, f"Lock {path}")
            ioctl(volume_handle, FSCTL_DISMOUNT_VOLUME, f"Dismount {path}")
            volume_handles.append(volume_handle)

        print(f"Opening {DISK}")
        disk_handle = open_handle(DISK, write=True)
        ioctl(disk_handle, FSCTL_LOCK_VOLUME, f"Lock {DISK}")

        print("Writing GPT")
        write_at(disk_handle, 0 * SECTOR_SIZE, protective_mbr, "Protective MBR")
        write_at(disk_handle, GPT_HEADER_LBA * SECTOR_SIZE, primary_header, "Primary GPT header")
        write_at(disk_handle, GPT_ENTRIES_LBA * SECTOR_SIZE, partition_entries, "Primary GPT entries")
        write_at(disk_handle, BACKUP_ENTRIES_LBA * SECTOR_SIZE, partition_entries, "Backup GPT entries")
        write_at(disk_handle, BACKUP_HEADER_LBA * SECTOR_SIZE, backup_header, "Backup GPT header")

        print("Writing FAT32 ESP")
        write_at(disk_handle, ESP_START_LBA * SECTOR_SIZE, vbr, "FAT32 VBR")
        write_at(disk_handle, (ESP_START_LBA + FSINFO_SECTOR) * SECTOR_SIZE, fsinfo, "FAT32 FSInfo")
        write_at(
            disk_handle,
            (ESP_START_LBA + BACKUP_BOOT_SECTOR) * SECTOR_SIZE,
            vbr,
            "FAT32 backup boot sector",
        )
        write_at(disk_handle, fat_start_lba * SECTOR_SIZE, fat, "FAT32 FAT1")
        write_at(disk_handle, fat2_start_lba * SECTOR_SIZE, fat, "FAT32 FAT2")
        write_at(disk_handle, root_dir_lba * SECTOR_SIZE, root_dir, "FAT32 root directory cluster")

        if not k32.FlushFileBuffers(disk_handle):
            fail("FlushFileBuffers failed")
        print("[ok] FlushFileBuffers")
    finally:
        if disk_handle:
            try:
                ioctl(disk_handle, FSCTL_UNLOCK_VOLUME, f"Unlock {DISK}")
            except OSError as exc:
                print(f"[warn] {exc}")
            close_handle(disk_handle)

        for volume_handle, volume_id in zip(volume_handles, volume_ids):
            path = volume_id.rstrip("\\")
            try:
                ioctl(volume_handle, FSCTL_UNLOCK_VOLUME, f"Unlock {path}")
            except OSError as exc:
                print(f"[warn] {exc}")
            close_handle(volume_handle)

    print("Format complete")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
