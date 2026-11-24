import struct

fpath = r'C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer\server\storage\uploads\23353bfbd0ef4b2db53930980865518f_Vw_Transporter_2.0_TDI_CR_Bosch_EDC17CP20-518078 nodpf.bin'
with open(fpath, 'rb') as f:
    data = f.read()

# Let's search for sequences of known DTCs in 16-bit little-endian or big-endian
# P0401 = 0x0401, P0402 = 0x0402, P0403 = 0x0403, P0404 = 0x0404, P2002 = 0x2002
p0401_le = struct.pack('<H', 0x0401)
p0402_le = struct.pack('<H', 0x0402)
p0403_le = struct.pack('<H', 0x0403)

p0401_be = struct.pack('>H', 0x0401)
p0402_be = struct.pack('>H', 0x0402)

pos_le = data.find(p0401_le + p0402_le)
print('Little endian sequence pos:', hex(pos_le) if pos_le != -1 else 'Not found')

pos_be = data.find(p0401_be + p0402_be)
print('Big endian sequence pos:', hex(pos_be) if pos_be != -1 else 'Not found')

# Also let's search for P2002 (0x2002)
pos_p2002_le = [hex(i) for i in range(len(data)-1) if data[i:i+2] == struct.pack('<H', 0x2002)]
pos_p2002_be = [hex(i) for i in range(len(data)-1) if data[i:i+2] == struct.pack('>H', 0x2002)]
print('P2002 LE occurrences:', len(pos_p2002_le), pos_p2002_le[:5])
print('P2002 BE occurrences:', len(pos_p2002_be), pos_p2002_be[:5])
