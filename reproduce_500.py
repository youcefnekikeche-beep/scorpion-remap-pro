import sys
sys.path.append(r'C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer')

import io
from fastapi.testclient import TestClient
from server.app import app

client = TestClient(app, raise_server_exceptions=False)

# Let's find the file
file_path = r'C:\Users\ZY Laptop\.gemini\antigravity\scratch\CloudTuningServer\server\storage\uploads\5b8d3fd7af2a455782023d5647dc259f_Audi A4 2.0TDI EDC17CP04 1037510946 DPF-off.bin'

with open(file_path, 'rb') as f:
    content = f.read()

print("File size:", len(content))

# Login or bypass user
from server.db import save_session_db
import uuid
token = str(uuid.uuid4())
save_session_db(token, 1)

response = client.post(
    "/api/v1/tuning/analyze",
    files={"file": ("Audi A4 2.0TDI EDC17CP04 1037510946 DPF-off.bin", io.BytesIO(content), "application/octet-stream")},
    cookies={"ecu_token": token},
    headers={"Authorization": f"Bearer {token}"}
)

print("Status code:", response.status_code)
print("Response text:", response.text)
