import urllib.request
import json

# 1. Login
login_req = urllib.request.Request(
    'http://127.0.0.1:8000/api/v1/auth/login',
    data=json.dumps({'username': 'client_demo', 'password': 'Client123456'}).encode(),
    headers={'Content-Type': 'application/json'}
)
with urllib.request.urlopen(login_req) as resp:
    login_data = json.loads(resp.read().decode('utf-8'))
    token = login_data['access_token']
    print('Login success! Token:', token[:10], '...')

# 2. Upload & Analyze a real binary (Crafter 2.0 TDI EDC17C54)
test_file = r'C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer\server\storage\uploads\42dd94a41f3f4d729205906f6d9347d5_Vw_Crafter_2.0_TDI_EDC17C54_536222_EGR DPF off.bin'
with open(test_file, 'rb') as f:
    file_bytes = f.read()

boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
body = bytearray()
body.extend(f'--{boundary}\r\n'.encode())
body.extend(b'Content-Disposition: form-data; name="file"; filename="Crafter_EDC17C54.bin"\r\n')
body.extend(b'Content-Type: application/octet-stream\r\n\r\n')
body.extend(file_bytes)
body.extend(f'\r\n--{boundary}--\r\n'.encode())

analyze_req = urllib.request.Request(
    'http://127.0.0.1:8000/api/v1/tuning/analyze',
    data=body,
    headers={
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'Authorization': f'Bearer {token}'
    }
)
with urllib.request.urlopen(analyze_req) as resp:
    analyze_data = json.loads(resp.read().decode('utf-8'))

print('\n=== ANALYZE RESULT ===')
print('ECU Type:', analyze_data.get('ecu_type'))
print('SW Version:', analyze_data.get('sw_version'))
print('Brand / Model:', analyze_data.get('brand'), '/', analyze_data.get('model'))
print('Supported Solutions:', analyze_data.get('supported_solutions'))
print('Default Solutions:', analyze_data.get('default_solutions'))
print('Initial DTC Count:', analyze_data.get('dtc_count'))

file_token = analyze_data.get('file_token')

# 3. Test Preview DTC with DPF + EGR + Custom DTC P0234
preview_req = urllib.request.Request(
    'http://127.0.0.1:8000/api/v1/tuning/preview-dtc',
    data=json.dumps({
        'file_token': file_token,
        'selected_solutions': ['DPF / FAP', 'EGR'],
        'custom_dtcs': ['P0234']
    }).encode(),
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
)
with urllib.request.urlopen(preview_req) as resp:
    preview_data = json.loads(resp.read().decode('utf-8'))

print('\n=== PREVIEW DTC RESULT ===')
print('Total Codes:', preview_data.get('total_codes'))
for item in preview_data.get('items', [])[:8]:
    print(f"  [{item['code']}] Offset: {item['offset']} | {item['val_ori']} -> {item['val_mod']} | {item['source']} | {item['description'][:30]}")
