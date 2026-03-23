import struct
DISK = r"\\.\PhysicalDrive3"
with open(DISK, "rb") as f:
    f.seek(512)
    lba1 = f.read(512)
    f.seek(512 * 2)
    entries_raw = f.read(512 * 32)  # up to 32 sectors of entries

sig       = lba1[0:8]
rev       = lba1[8:12].hex()
hdr_size  = int.from_bytes(lba1[12:16], "little")
my_lba    = int.from_bytes(lba1[24:32], "little")
alt_lba   = int.from_bytes(lba1[32:40], "little")
first_use = int.from_bytes(lba1[40:48], "little")
last_use  = int.from_bytes(lba1[48:56], "little")
part_lba  = int.from_bytes(lba1[72:80], "little")
num_parts = int.from_bytes(lba1[80:84], "little")
part_size = int.from_bytes(lba1[84:88], "little")

print(f"GPT Signature:   {sig}")
print(f"Revision:        {rev}")
print(f"MyLBA:           {my_lba}")
print(f"AlternateLBA:    {alt_lba}")
print(f"FirstUsableLBA:  {first_use}")
print(f"LastUsableLBA:   {last_use}")
print(f"PartitionEntryLBA: {part_lba}")
print(f"NumPartitions:   {num_parts}")
print(f"PartEntrySize:   {part_size}")
print()

with open(DISK, "rb") as f:
    f.seek(512 * part_lba)
    for i in range(min(num_parts, 8)):
        e = f.read(part_size)
        type_guid = e[0:16]
        if all(b == 0 for b in type_guid):
            continue
        start = int.from_bytes(e[32:40], "little")
        end   = int.from_bytes(e[40:48], "little")
        name  = e[56:128].decode("utf-16-le", errors="replace").rstrip("\x00")
        print(f"Partition {i}: start=0x{start:X} end=0x{end:X} name='{name}'")
        print(f"  type_guid: {type_guid.hex()}")
