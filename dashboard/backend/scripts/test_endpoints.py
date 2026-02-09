import sys
from pathlib import Path

# Ensure dashboard/backend is on path so we can import app
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app

app = create_app()
client = app.test_client()

endpoints = ["/api/health", "/api/prices/", "/api/events/", "/api/change-points/"]

for ep in endpoints:
    resp = client.get(ep)
    try:
        data = resp.get_json()
    except Exception:
        data = resp.data.decode('utf-8')
    print(f"ENDPOINT: {ep} -> STATUS: {resp.status_code}")
    print(data)
    print("---")
