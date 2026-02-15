from __future__ import annotations

from pathlib import Path
import sys

from flask import Flask
from flask_cors import CORS

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cache import InMemoryCache
from routes.change_points import change_points_bp
from routes.events import events_bp
from routes.prices import prices_bp


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.config["CACHE"] = InMemoryCache(ttl_seconds=120)

    app.register_blueprint(prices_bp, url_prefix="/api/prices")
    app.register_blueprint(change_points_bp, url_prefix="/api/change-points")
    app.register_blueprint(events_bp, url_prefix="/api/events")

    @app.route("/api/health", methods=["GET"])
    def health_check() -> tuple[dict[str, str], int]:
        return {"status": "OK"}, 200

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
