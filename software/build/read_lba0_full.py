DISK = r"\\.\PhysicalDrive3"
with open(DISK, "rb") as f:
    lba0 = f.read(512)

print("Bytes 236-259 (words 59-64):")
for i in range(236, 260, 4):
    w = int.from_bytes(lba0[i:i+4], "little")
    print(f"  word {i//4:3d} (bytes {i:3d}-{i+3:3d}): {lba0[i]:02X} {lba0[i+1]:02X} {lba0[i+2]:02X} {lba0[i+3]:02X}  LE={w:08X}")

print()
print("Bytes 492-511 (words 123-127):")
for i in range(492, 512, 4):
    w = int.from_bytes(lba0[i:i+4], "little")
    print(f"  word {i//4:3d} (bytes {i:3d}-{i+3:3d}): {lba0[i]:02X} {lba0[i+1]:02X} {lba0[i+2]:02X} {lba0[i+3]:02X}  LE={w:08X}")
