"""Primary application entrypoint."""
from flask import Flask, g, jsonify
from routes.base import base_bp
from routes.discovery import discovery_bp
from exceptions import ClientException


def create_app():
    """Create the flask application."""
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.register_blueprint(base_bp)
    app.register_blueprint(discovery_bp)

    @app.teardown_appcontext
    def close_connection(e):
        if g.get("db_conn", None):
            g.get("db_conn").close()

    @app.errorhandler(ClientException)
    def handle_invalid_usage(e):
        res = jsonify(e.to_dict())
        res.status_code = e.status_code
        return res

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
