import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from server.app import app as fastapi_app
from server.db import init_db

# Initialize database on startup
init_db()

# Provide WSGI adapter so default 'gunicorn app:app' works seamlessly
try:
    from a2wsgi import ASGIMiddleware
    app = ASGIMiddleware(fastapi_app)
except ImportError:
    app = fastapi_app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port, reload=False)
