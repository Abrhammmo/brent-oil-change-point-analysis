from __future__ import annotations

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
backend_path = repo_root / "dashboard" / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app import create_app  # noqa: E402


def test_api_health_and_prices() -> None:
    app = create_app()
    client = app.test_client()

    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.get_json()["status"] == "OK"

    prices = client.get("/api/prices/")
    assert prices.status_code == 200
    payload = prices.get_json()
    assert "data" in payload
    assert payload["count"] >= 1


def test_change_points_endpoint() -> None:
    app = create_app()
    client = app.test_client()
    resp = client.get("/api/change-points/")
    assert resp.status_code == 200
    payload = resp.get_json()
    assert "change_points" in payload or "tau_date" in payload
