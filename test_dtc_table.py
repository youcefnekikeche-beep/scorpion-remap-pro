import struct

fpath = r'C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer\server\storage\uploads\23353bfbd0ef4b2db53930980865518f_Vw_Transporter_2.0_TDI_CR_Bosch_EDC17CP20-518078 nodpf.bin'
with open(fpath, 'rb') as f:
    data = f.read()

offset = 0x3194e - 20
codes = []
for i in range(offset, offset + 100, 2):
    val = struct.unpack('<H', data[i:i+2])[0]
    codes.append((hex(i), f"P{val:04X}"))

print('Found DTC sequence:')
for addr, code in codes:
    print(f'  {addr}: {code}')
