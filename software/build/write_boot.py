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
import os, sys

IMG   = r"D:\Projects\PortaRe0\software\build\sd_boot.img"
DISK  = r"\\.\PhysicalDrive3"
SKIP  = 0x020000          # start writing from boot0 offset (128KB)
SIZE  = 16 * 1024 * 1024  # total image size (16MB)

with open(IMG, "rb") as f:
    f.seek(SKIP)
    data = f.read(SIZE - SKIP)

write_size = len(data)
print(f"Writing {write_size // 1024}KB at offset 0x{SKIP:06X} (preserving GPT in LBA 0-33)")

with open(DISK, "r+b") as d:
    d.seek(SKIP)
    d.write(data)
    d.flush()
    os.fsync(d.fileno())

print(f"OK: wrote {write_size // 1024}KB to {DISK} (offset 0x{SKIP:06X})")
print("GPT partition table preserved.")
