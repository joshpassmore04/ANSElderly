import json
import secrets

from cachelib import FileSystemCache
from flask import Flask
from flask_cors import CORS
from flask_session import Session


def create_app():

    flask_app = Flask(__name__)
    flask_app.config.from_file("config.json", load=json.load)

    flask_app.config["SECRET_KEY"] = secrets.token_hex(16)
    flask_app.config["SESSION_CACHELIB"] = FileSystemCache(cache_dir="sessions", threshold=500)
    flask_app.config["SESSION_TYPE"] = "cachelib"
    flask_app.config["SESSION_PERMANENT"] = True
    CORS(flask_app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    Session(flask_app)

    return flask_app


if __name__ == '__main__':
    app = create_app()
    app.run(port=app.config["PORT"])