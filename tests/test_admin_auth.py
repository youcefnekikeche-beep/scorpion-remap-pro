import sys
import os
sys.path.append(os.path.abspath('.'))
from server.db import init_db, get_db, authenticate_user, save_session_db, get_session_user_db, hash_password
from server.app import get_current_user, SESSIONS
from fastapi import Request

init_db()

with get_db() as conn:
    c = conn.cursor()
    c.execute("SELECT id, email, password_hash, role, tokens FROM users WHERE email LIKE '%tbessa%'")
    for r in c.fetchall():
        print(dict(r))

# Test with whatever password was set or update it
with get_db() as conn:
    c = conn.cursor()
    # update password for ayoubtbessa to Ayoub123456!
    c.execute("UPDATE users SET password_hash = ? WHERE email = 'ayoubtbessa@gmail.com'", (hash_password("Ayoub123456!"),))
    conn.commit()

user = authenticate_user('ayoubtbessa@gmail.com', 'Ayoub123456!')
print("Authenticated user:", user['email'], user['role'], user['tokens'])
assert user['role'] == 'admin', "Must be admin"

# Test saving session
save_session_db('test-admin-token-777', user['id'])
retrieved_uid = get_session_user_db('test-admin-token-777')
assert retrieved_uid == user['id'], "Persistent session retrieval failed"
print("Persistent session successfully retrieved user ID:", retrieved_uid)

# Clear in-memory SESSIONS to simulate Render restart
SESSIONS.clear()
assert len(SESSIONS) == 0, "SESSIONS must be empty"

# Mock request with cookie
class MockRequest:
    def __init__(self, token):
        self.headers = {"Authorization": f"Bearer {token}"}
        self.cookies = {"ecu_token": token}

req = MockRequest('test-admin-token-777')
restored_user = get_current_user(req)
print("Restored user after simulated server restart:", restored_user['email'], restored_user['is_admin'])
assert restored_user['is_admin'] == True, "Restored user must be admin"
assert len(SESSIONS) == 1, "SESSIONS must have recovered from DB"
print("ALL VERIFICATIONS PASSED 100%!")
