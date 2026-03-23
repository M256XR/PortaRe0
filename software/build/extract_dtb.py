#!/usr/bin/env python3
"""Dump card_boot_para and power_sply nodes from A733 DTB."""
import struct

DTB = "D:/Projects/PortaRe0/software/build/a733.dtb"

with open(DTB, 'rb') as f:
    data = f.read()

_, _, off_struct, off_strings, _, _, _, _, sz_strings, sz_struct = \
    struct.unpack_from('>IIIIIIIIII', data, 0)

struct_data  = data[off_struct:off_struct+sz_struct]
strings_data = data[off_strings:off_strings+sz_strings]

def align4(n): return (n + 3) & ~3
def get_str(off):
    end = strings_data.index(b'\x00', off)
    return strings_data[off:end].decode('utf-8', errors='replace')

FDT_BEGIN_NODE=1; FDT_END_NODE=2; FDT_PROP=3; FDT_NOP=4; FDT_END=9

pos = 0
path = []
in_dump = False
dump_depth = 0

DUMP_KEYWORDS = ['card0_boot_para', 'card2_boot_para', 'card_boot']

while pos < len(struct_data):
    token = struct.unpack_from('>I', struct_data, pos)[0]
    pos += 4
    if token == FDT_BEGIN_NODE:
        end = struct_data.index(b'\x00', pos)
        name = struct_data[pos:end].decode('utf-8', errors='replace')
        pos = align4(end + 1)
        path.append(name)
        if any(k in name for k in DUMP_KEYWORDS):
            in_dump = True
            dump_depth = len(path)
            print(f"\n[{name}]")
    elif token == FDT_END_NODE:
        if in_dump and len(path) == dump_depth:
            in_dump = False
        if path: path.pop()
    elif token == FDT_PROP:
        plen, noff = struct.unpack_from('>II', struct_data, pos)
        pos += 8
        pval = struct_data[pos:pos+plen]
        pos = align4(pos + plen)
        pname = get_str(noff)
        if in_dump:
            if plen == 0:
                print(f"  {pname}")
            elif plen == 4:
                ival = struct.unpack_from('>I', pval)[0]
                print(f"  {pname} = 0x{ival:08X} ({ival})")
            elif plen <= 64:
                try:
                    txt = pval.rstrip(b'\x00').replace(b'\x00', b' ').decode(errors='replace')
                    print(f"  {pname} = {txt!r}")
                except:
                    print(f"  {pname} = {pval.hex()}")
            else:
                print(f"  {pname} = [{plen}B] {pval[:16].hex()}...")
    elif token == FDT_NOP: pass
    elif token == FDT_END: break
