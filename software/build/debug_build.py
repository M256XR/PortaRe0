#!/usr/bin/env python3
import sys, os, traceback
sys.path.insert(0, '/home/linux/edk2/BaseTools/Source/Python')
os.environ['WORKSPACE'] = '/home/linux/edk2'

# Check what TargetTxtClassObject.TargetTxtDictionary actually calls
import inspect
from Common.TargetTxtClassObject import TargetTxtClassObject

# Inspect the class
print("TargetTxtClassObject methods/props:")
for name in dir(TargetTxtClassObject):
    if not name.startswith('__'):
        print(f"  {name}")

# Try accessing .Target property which triggers _GetTarget
t = TargetTxtClassObject()
print("\nAccessing .Target property...")
try:
    target = t.Target
    print(f"Target result: {target!r}")
except Exception as e:
    print(f"Exception: {e}")
    traceback.print_exc()

print(f"\nTargetTxtDictionary: {t.TargetTxtDictionary!r}")
