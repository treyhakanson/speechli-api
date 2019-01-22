from flask import Flask, g

from routes.base import base_bp


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.register_blueprint(base_bp)

    @app.teardown_appcontext
    def close_connection(e):
        if g.get("db_conn", None):
            g.get("db_conn").close()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
