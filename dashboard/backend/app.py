from flask import Flask
from flask_cors import CORS

from routes.prices import prices_bp
from routes.change_points import change_points_bp
from routes.events import events_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(prices_bp, url_prefix="/api/prices")
    app.register_blueprint(change_points_bp, url_prefix="/api/change-points")
    app.register_blueprint(events_bp, url_prefix="/api/events")

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return {"status": "OK"}, 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
