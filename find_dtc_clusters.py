import struct

fpath = r'C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer\server\storage\uploads\a48f8e2775cf4c9599321fc89e0815a6_ORI.bin'
with open(fpath, 'rb') as f: data = f.read()

# Let's search for DTC codes near 0x280000 or elsewhere in the file
# In Bosch EDC17, the DTC table is typically before or after the switch table, or indexed
# Let's search for P0401 (0x0401), P2002 (0x2002), P2463 (0x2463)
p_egr = struct.pack('<H', 0x0401)
p_dpf = struct.pack('<H', 0x2002)

pos_egr = [hex(i) for i in range(len(data)-1) if data[i:i+2] == p_egr]
pos_dpf = [hex(i) for i in range(len(data)-1) if data[i:i+2] == p_dpf]

print('Crafter P0401 occurrences:', len(pos_egr))
print('Crafter P2002 occurrences:', len(pos_dpf))

# Let's find clusters where multiple P04xx and P20xx appear together
clusters = []
for i in range(0, len(data) - 200, 2):
    sub = data[i:i+200]
    # count how many standard DTCs (0x0100 to 0x3000) are in sub
    c = 0
    for j in range(0, 200, 2):
        val = struct.unpack('<H', sub[j:j+2])[0]
        if 0x0100 <= val <= 0x3500:
            c += 1
    if c >= 60: # dense cluster of 16-bit DTC codes
        clusters.append(i)

# condense clusters
dense_tables = []
if clusters:
    curr = clusters[0]
    for x in clusters[1:]:
        if x - curr > 500:
            dense_tables.append(hex(curr))
        curr = x
    dense_tables.append(hex(curr))

print('Dense DTC code tables found at:', dense_tables)
