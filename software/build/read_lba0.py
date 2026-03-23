import struct

DISK = r"\\.\PhysicalDrive3"
with open(DISK, "rb") as f:
    lba0 = f.read(512)

print(f"LBA0 b[0..3]    = {lba0[0]:02X} {lba0[1]:02X} {lba0[2]:02X} {lba0[3]:02X}")
print(f"LBA0 b[508-511] = {lba0[508]:02X} {lba0[509]:02X} {lba0[510]:02X} {lba0[511]:02X}")
print()
print("First 64 bytes of LBA0:")
for i in range(0, 64, 16):
    print("  " + " ".join(f"{b:02X}" for b in lba0[i:i+16]))
print("...")
print("Last 32 bytes (480-511):")
for i in range(480, 512, 16):
    print("  " + " ".join(f"{b:02X}" for b in lba0[i:i+16]))
