#!/usr/bin/env python3
"""Rewrite the InitMmu function in MemoryInitPeiLib.c with correct diagnostic prints."""

path = "/home/linux/edk2/ArmPlatformPkg/MemoryInitPei/MemoryInitPeiLib.c"

with open(path, "rb") as f:
    content = f.read()

# Find the bad DbgStr2+InitMmu region and replace with correct version.
# We'll find from "STATIC VOID\nDbgStr2" to the closing "}\n" of InitMmu.

start_marker = b"STATIC VOID\nDbgStr2"
end_marker = b"/*++"  # The comment block that follows InitMmu

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1:
    print("ERROR: start marker not found")
    exit(1)
if end_idx == -1:
    print("ERROR: end marker not found")
    exit(1)

print(f"Found region: bytes [{start_idx}:{end_idx}]")
print("Current content:")
print(repr(content[start_idx:end_idx]))

# Build the correct replacement
# Use bytes to avoid any escaping issues
# \r = 0x5C 0x72, \n = 0x5C 0x6E
rn = bytes([0x5C, 0x72, 0x5C, 0x6E])  # \r\n as C escape sequence

correct = (
    b"STATIC VOID\n"
    b"DbgStr2 (CONST CHAR8 *Str)\n"
    b"{\n"
    b"  UINTN  Len = 0;\n"
    b"  while (Str[Len]) { Len++; }\n"
    b"  SerialPortWrite ((UINT8 *)Str, Len);\n"
    b"}\n"
    b"\n"
    b"STATIC\n"
    b"VOID\n"
    b"InitMmu (\n"
    b"  IN ARM_MEMORY_REGION_DESCRIPTOR  *MemoryTable\n"
    b"  )\n"
    b"{\n"
    b"  VOID           *TranslationTableBase;\n"
    b"  UINTN          TranslationTableSize;\n"
    b"  RETURN_STATUS  Status;\n"
    b"\n"
    b"  // Note: Because we called PeiServicesInstallPeiMemory() before to call InitMmu() the MMU Page Table resides in\n"
    b"  //      DRAM (even at the top of DRAM as it is the first permanent memory allocation)\n"
    b'  DbgStr2 ("[A733] InitMmu: calling ArmConfigureMmu' + rn + b'");\n'
    b"  Status = ArmConfigureMmu (MemoryTable, &TranslationTableBase, &TranslationTableSize);\n"
    b'  DbgStr2 ("[A733] InitMmu: ArmConfigureMmu returned' + rn + b'");\n'
    b"  if (EFI_ERROR (Status)) {\n"
    b'    DbgStr2 ("[A733] InitMmu: FAILED' + rn + b'");\n'
    b'    DEBUG ((DEBUG_ERROR, "Error: Failed to enable MMU\\n"));\n'
    b"  } else {\n"
    b'    DbgStr2 ("[A733] InitMmu: MMU OK' + rn + b'");\n'
    b"  }\n"
    b"}\n"
    b"\n"
)

content = content[:start_idx] + correct + content[end_idx:]

with open(path, "wb") as f:
    f.write(content)

print("\nFile written. Verifying...")
with open(path, "rb") as f:
    v = f.read()

# Check key parts
checks = [
    b"calling ArmConfigureMmu" + rn + b'"',
    b"ArmConfigureMmu returned" + rn + b'"',
    b"InitMmu: FAILED" + rn + b'"',
    b"InitMmu: MMU OK" + rn + b'"',
    b'DEBUG ((DEBUG_ERROR, "Error: Failed to enable MMU\\n"));',
]
all_ok = True
for check in checks:
    if check in v:
        print(f"OK: {repr(check[:40])}")
    else:
        print(f"MISSING: {repr(check[:40])}")
        all_ok = False

if all_ok:
    print("\nAll checks passed!")
    # Show the function
    idx = v.find(b"STATIC VOID\nDbgStr2")
    end = v.find(b"/*++")
    print("\nFinal content:")
    print(v[idx:end].decode())
