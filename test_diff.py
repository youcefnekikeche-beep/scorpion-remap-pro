ori_path = r'C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer\server\storage\uploads\a48f8e2775cf4c9599321fc89e0815a6_ORI.bin'
mod_path = r'C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer\server\storage\uploads\42dd94a41f3f4d729205906f6d9347d5_Vw_Crafter_2.0_TDI_EDC17C54_536222_EGR DPF off.bin'

with open(ori_path, 'rb') as f: ori = f.read()
with open(mod_path, 'rb') as f: mod = f.read()

diffs = []
for i in range(min(len(ori), len(mod))):
    if ori[i] != mod[i]:
        diffs.append((i, ori[i], mod[i]))

print(f'Total bytes modified: {len(diffs)}')

# Group contiguous blocks
blocks = []
if diffs:
    curr_start = diffs[0][0]
    curr_len = 1
    for k in range(1, len(diffs)):
        if diffs[k][0] == diffs[k-1][0] + 1:
            curr_len += 1
        else:
            blocks.append((curr_start, curr_len))
            curr_start = diffs[k][0]
            curr_len = 1
    blocks.append((curr_start, curr_len))

print(f'Total changed regions: {len(blocks)}')
for start, length in blocks[:20]:
    b_ori = ori[start:start+length].hex()
    b_mod = mod[start:start+length].hex()
    print(f'  Offset: {hex(start)} (Length: {length}) | ORI: {b_ori} -> MOD: {b_mod}')
