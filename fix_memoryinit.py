#!/usr/bin/env python3
"""Fix MemoryInitPeiLib.c: replace CRLF inside C string literals with \\r\\n escape sequences."""

path = "/home/linux/edk2/ArmPlatformPkg/MemoryInitPei/MemoryInitPeiLib.c"

with open(path, "rb") as f:
    content = f.read()

# The file currently has actual CRLF (0x0D 0x0A) inside C string literals.
# We need literal backslash-r backslash-n (0x5C 0x72 0x5C 0x6E) instead.
crlf = bytes([0x0D, 0x0A])  # actual CR LF
escaped = bytes([0x5C, 0x72, 0x5C, 0x6E])  # \r\n as C escape sequence

# Patterns of strings that should end with \r\n escape (not CRLF)
patterns = [
    b'calling ArmConfigureMmu',
    b'ArmConfigureMmu returned',
    b'InitMmu: FAILED',
    b'enable MMU',
    b'InitMmu: MMU OK',
]

for pat in patterns:
    needle = pat + crlf + b'"'
    replace = pat + escaped + b'"'
    if needle in content:
        content = content.replace(needle, replace)
        print(f"Fixed: {pat.decode()}")
    else:
        print(f"NOT FOUND (CRLF pattern): {pat.decode()}")

with open(path, "wb") as f:
    f.write(content)

# Verify
with open(path, "rb") as f:
    v = f.read()

idx = v.find(b'calling ArmConfigureMmu')
print("\nVerify bytes after 'calling ArmConfigureMmu':")
print(repr(v[idx:idx+45]))
print("Hex:", v[idx+len(b'calling ArmConfigureMmu'):idx+len(b'calling ArmConfigureMmu')+6].hex())
