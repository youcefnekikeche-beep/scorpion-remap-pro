import json

path = r'C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer\server\storage\supported_ecus.json'
with open(path, 'r', encoding='utf-8') as f:
    ecus = json.load(f)

# List of valid genuine solutions in SCORPION REMAP PRO:
VALID_SOLUTIONS = {
    'DPF / FAP OFF',
    'EGR OFF',
    'ADBLUE / SCR OFF',
    'HOT START FIX',
    'SWIRL FLAPS OFF',
    'TVA OFF',
    'MAF OFF',
    'TORQUE MONITORING OFF',
    'SPEED LIMIT (VMAX) OFF',
    'IMMO OFF',
    'DECAT / LAMBDA OFF',
    'EVAP OFF',
    'START-STOP OFF',
    'STAGE 1 (+20%)',
    'COLD START FIX',
    'FAN MOD (95°C / 92°C / 90°C)'
}

# Clean each ECU entry
cleaned_ecus = []
for item in ecus:
    ecu_name = item.get('ecu', '')
    brand = item.get('brand', '')
    
    # Exclude Continental PCR 2.1 OBD unlocker if present and no genuine unlock
    # But PCR 2.1 flash has DPF/EGR
    new_solutions = []
    for s in item.get('solutions', []):
        s_clean = s.strip()
        if 'POP' in s_clean.upper() or 'FLEX' in s_clean.upper() or 'OBD UNLOCK' in s_clean.upper():
            continue
        # Standardize solution names
        if 'DPF' in s_clean.upper() or 'FAP' in s_clean.upper():
            new_solutions.append('DPF / FAP OFF')
        elif 'EGR' in s_clean.upper():
            new_solutions.append('EGR OFF')
        elif 'ADBLUE' in s_clean.upper() or 'SCR' in s_clean.upper() or 'UREA' in s_clean.upper() or 'NOX' in s_clean.upper():
            new_solutions.append('ADBLUE / SCR OFF')
        elif 'HOT START' in s_clean.upper():
            new_solutions.append('HOT START FIX')
        elif 'SWIRL' in s_clean.upper():
            new_solutions.append('SWIRL FLAPS OFF')
        elif 'TVA' in s_clean.upper():
            new_solutions.append('TVA OFF')
        elif 'MAF' in s_clean.upper():
            new_solutions.append('MAF OFF')
        elif 'TORQUE' in s_clean.upper():
            new_solutions.append('TORQUE MONITORING OFF')
        elif 'SPEED' in s_clean.upper() or 'VMAX' in s_clean.upper():
            new_solutions.append('SPEED LIMIT (VMAX) OFF')
        elif 'IMMO' in s_clean.upper():
            new_solutions.append('IMMO OFF')
        elif 'DECAT' in s_clean.upper() or 'LAMBDA' in s_clean.upper():
            new_solutions.append('DECAT / LAMBDA OFF')
        elif 'EVAP' in s_clean.upper():
            new_solutions.append('EVAP OFF')
        elif 'START' in s_clean.upper() and 'STOP' in s_clean.upper():
            new_solutions.append('START-STOP OFF')
        elif 'COLD START' in s_clean.upper():
            new_solutions.append('COLD START FIX')
        elif 'FAN' in s_clean.upper():
            new_solutions.append('FAN MOD (95°C / 92°C / 90°C)')
        elif 'STAGE 1' in s_clean.upper():
            new_solutions.append('STAGE 1 (+20%)')
        elif 'DTC' in s_clean.upper():
            new_solutions.append('DTC TABLE REMOVAL')

    # Remove duplicates preserving order
    seen = set()
    deduped = []
    for sol in new_solutions:
        if sol not in seen:
            seen.add(sol)
            deduped.append(sol)
            
    if deduped:
        item['solutions'] = deduped
        cleaned_ecus.append(item)

print(f"Total ECUs after cleaning: {len(cleaned_ecus)}")
with open(path, 'w', encoding='utf-8') as f:
    json.dump(cleaned_ecus, f, indent=2, ensure_ascii=False)
print("Updated supported_ecus.json successfully!")
