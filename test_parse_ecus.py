import os, glob, re

uploads = glob.glob(r'C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer\server\storage\uploads\*.bin')
print(f'Found {len(uploads)} upload binaries.')

for fpath in uploads:
    fname = os.path.basename(fpath)
    with open(fpath, 'rb') as f:
        data = f.read()
    
    # 1. Search for Bosch 1037xxxxxx
    sw_matches = re.findall(b'1037[0-9]{6}', data)
    # 2. Search for Bosch 0281xxxxxx
    hw_matches = re.findall(b'0281[0-9]{6}', data)
    # 3. Search for ECU strings
    ecu_matches = re.findall(rb'(?:EDC1[67][A-Z0-9_]{1,10}|MED17[A-Z0-9_\.]{1,10}|MD1[A-Z0-9_]{1,10}|DCM[0-9\._]{1,8}|PCR\s?2\.1|SID[0-9]{3}|ME7[A-Z0-9\._]{1,8})', data, re.IGNORECASE)
    # 4. Search for VAG part numbers (e.g. 03L906xxx, 04L906xxx)
    vag_matches = re.findall(rb'0[34]L\s?906\s?[0-9]{3}\s?[A-Z]{1,3}', data)
    
    print(f'=== {fname} ({len(data)} bytes) ===')
    if sw_matches:
        print('  SW numbers:', list(set(s.decode('ascii') for s in sw_matches)))
    if hw_matches:
        print('  HW numbers:', list(set(s.decode('ascii') for s in hw_matches)))
    if ecu_matches:
        print('  ECU detected:', list(set(s.decode('ascii') for s in ecu_matches)))
    if vag_matches:
        print('  VAG Part:', list(set(s.decode('ascii') for s in vag_matches)))
