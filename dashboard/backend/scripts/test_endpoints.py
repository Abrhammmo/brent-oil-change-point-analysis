from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app  # noqa: E402


def main() -> None:
    app = create_app()
    client = app.test_client()
    endpoints = ["/api/health", "/api/prices/", "/api/events/", "/api/change-points/"]

    for endpoint in endpoints:
        response = client.get(endpoint)
        try:
            data: Any = response.get_json()
        except Exception:
            data = response.data.decode("utf-8")
        print(f"ENDPOINT: {endpoint} -> STATUS: {response.status_code}")
        print(data)
        print("---")


if __name__ == "__main__":
    main()
