import urllib.request
import urllib.parse
import json

BASE_URL = 'http://127.0.0.1:8000'

# 1. Login
req = urllib.request.Request(
    f'{BASE_URL}/api/v1/auth/login',
    data=json.dumps({'username': 'youcef202621', 'password': 'Testeur123456'}).encode(),
    headers={'Content-Type': 'application/json'}
)
with urllib.request.urlopen(req) as resp:
    login_data = json.loads(resp.read().decode('utf-8'))
    token = login_data['access_token']
    initial_credits = login_data['user']['credits']
    print(f'Logged in! Token: {token[:10]}... Credits: {initial_credits}')

# Helper for multipart form upload
def upload_expert_preview(tool, filename, file_bytes, param=""):
    boundary = '----WebKitFormBoundaryExpertTest123'
    body = bytearray()
    
    # tool field
    body.extend(f'--{boundary}\r\n'.encode())
    body.extend(f'Content-Disposition: form-data; name="tool"\r\n\r\n{tool}\r\n'.encode())

    # param field
    if param:
        body.extend(f'--{boundary}\r\n'.encode())
        body.extend(f'Content-Disposition: form-data; name="param"\r\n\r\n{param}\r\n'.encode())

    # file field
    body.extend(f'--{boundary}\r\n'.encode())
    body.extend(f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode())
    body.extend(b'Content-Type: application/octet-stream\r\n\r\n')
    body.extend(file_bytes)
    body.extend(f'\r\n--{boundary}--\r\n'.encode())

    req = urllib.request.Request(
        f'{BASE_URL}/api/v1/expert/preview',
        data=body,
        headers={
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Authorization': f'Bearer {token}'
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))

# 2. Test Security Rejection: Upload Bosch file to DCM 3.4
fake_bosch = b'Bosch EDC17 TriCore' + b'\x00' * 1048550
status, err = upload_expert_preview('renault_dcm34_stage1', 'Crafter_Bosch.bin', fake_bosch)
print(f'Test 1 (Security Rejection): Status={status}, Detail={err.get("detail")}')
assert status == 400
assert "Erreur de sécurité" in err.get("detail", "")

# 3. Test Valid DCM 3.4 Stage 1 Preview
valid_dcm = bytearray(b'\x00' * 1048576)
valid_dcm[100:106] = b'DCM3.4'
valid_dcm[200:210] = b'SW 28267ST'
valid_dcm[1000:1004] = b'\x00\xdc\x05\x00'

status, preview_res = upload_expert_preview('renault_dcm34_stage1', 'Clio4_DCM34_Ori.bin', bytes(valid_dcm))
print(f'Test 2 (DCM 3.4 Stage 1 Preview): Status={status}')
print(f'   ECU: {preview_res.get("ecu_type")} | Bytes Mod: {preview_res.get("bytes_modified")} | Token: {preview_res.get("preview_token")[:10]}...')
assert status == 200
assert preview_res.get("success") is True
preview_token = preview_res.get("preview_token")

# 4. Test Apply & Download with Credit Deduction
apply_data = urllib.parse.urlencode({'preview_token': preview_token}).encode()
apply_req = urllib.request.Request(
    f'{BASE_URL}/api/v1/expert/apply',
    data=apply_data,
    headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {token}'
    }
)
with urllib.request.urlopen(apply_req) as resp:
    apply_res = json.loads(resp.read().decode('utf-8'))
    print(f'Test 3 (DCM 3.4 Stage 1 Apply): Success={apply_res.get("success")}')
    print(f'   Download URL: {apply_res.get("download_url")} | Credits Remaining: {apply_res.get("credits_remaining")}')
    assert apply_res.get("success") is True
    assert apply_res.get("credits_remaining") == initial_credits - 1

# 5. Test Renault Lambda Off
v42_data = bytearray(b'\x00' * 1048576)
v42_data[100:109] = b'VALEO V42'
v42_data[164892:164892+8] = b'$\x0b$"$J$L'
v42_data[164902:164902+2] = b'\x016'
v42_data[166614:166614+5] = b'\x016\x0c\x13\x03'
status, lambda_res = upload_expert_preview('renault_lambda_off', 'Symbol_1.6_V42.bin', bytes(v42_data))
print(f'Test 4 (Lambda Off Preview): Status={status} | Desc={lambda_res.get("description")}')
assert status == 200

# 6. Test Renault Fan Temp Mod (92°C)
v42_fan = bytearray(b'\x00' * 1048576)
v42_fan[100:109] = b'VALEO V42'
v42_fan[1000:1002] = b'\x69\x6E'
status, fan_res = upload_expert_preview('renault_fan_temp', 'Symbol_1.6_V42.bin', bytes(v42_fan), param="92")
print(f'Test 5 (Fan Temp 92°C Preview): Status={status} | Desc={fan_res.get("description")}')
assert status == 200

print('\n>>> ALL 5 END-TO-END EXPERT TESTS PASSED PERFECTLY! <<<')
