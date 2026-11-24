import struct, re, json, os

DTC_JSON = r'C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer\server\storage\dtc_table.json'
with open(DTC_JSON, 'r', encoding='utf-8') as f:
    dtc_db = json.load(f)

# Test file
fpath = r'C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer\server\storage\uploads\23353bfbd0ef4b2db53930980865518f_Vw_Transporter_2.0_TDI_CR_Bosch_EDC17CP20-518078 nodpf.bin'
with open(fpath, 'rb') as f:
    data = f.read()

def scan_dtc_offsets(binary_data, target_dtcs):
    results = []
    for dtc in target_dtcs:
        code_num = None
        try:
            # e.g. P0401 -> 0x0401, P2002 -> 0x2002
            if dtc.startswith('P') and len(dtc) == 5:
                code_num = int(dtc[1:], 16)
        except:
            continue
        
        if code_num is None: continue
        
        # Search 16-bit little endian and big endian
        le_bytes = struct.pack('<H', code_num)
        be_bytes = struct.pack('>H', code_num)
        
        # Find matches
        matches = []
        pos = binary_data.find(le_bytes)
        while pos != -1 and len(matches) < 3:
            matches.append((pos, 'LE'))
            pos = binary_data.find(le_bytes, pos + 2)
            
        pos = binary_data.find(be_bytes)
        while pos != -1 and len(matches) < 5:
            matches.append((pos, 'BE'))
            pos = binary_data.find(be_bytes, pos + 2)
            
        if matches:
            offset = matches[0][0]
            val_ori = f"0x{binary_data[offset]:02X}"
            results.append({
                'code': dtc,
                'offset': f"0x{offset:06X}",
                'val_ori': val_ori,
                'val_mod': "0x00",
                'desc': dtc_db.get(dtc, 'Défaut système gestion moteur')
            })
    return results

sample_dtcs = ['P0401', 'P0402', 'P0403', 'P2002', 'P2463', 'P2452']
res = scan_dtc_offsets(data, sample_dtcs)
print(f'Found {len(res)} DTC offsets in binary:')
for r in res:
    print(f"  {r['code']} @ {r['offset']} | {r['val_ori']} -> {r['val_mod']} | {r['desc'][:45]}")
