import json
import secrets

from cachelib import FileSystemCache
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from flask_session import Session
from sqlalchemy import create_engine

from data.sqlalchemy.sqlalchemy_user_data import SQLAlchemyUserData
from orm import Base
from routes.user_routes import create_user_blueprint
from service.errors.invalid_data import InvalidData
from service.errors.server_error import ServerError
from service.user_service import UserService


def create_app():

    flask_app = Flask(__name__)
    flask_app.config.from_file("config.json", load=json.load)

    flask_app.config["SECRET_KEY"] = secrets.token_hex(16)
    flask_app.config["SESSION_CACHELIB"] = FileSystemCache(cache_dir="sessions", threshold=500)
    flask_app.config["SESSION_TYPE"] = "cachelib"
    flask_app.config["SESSION_PERMANENT"] = True
    CORS(flask_app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    Session(flask_app)

    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)
    user_data = SQLAlchemyUserData(engine)
    user_service = UserService(user_data)

    flask_app.register_blueprint(create_user_blueprint(flask_app.config["ENDPOINT"], user_service))

    @flask_app.errorhandler(InvalidData)
    def handle_invalid_data(exception):
        return jsonify({"status": "error", "message": "Invalid data provided"}), 400

    @flask_app.errorhandler(ServerError)
    def handle_db_error(exception):
        message = {
            "status": "error",
            "message": "Internal server error",
        }
        return jsonify(message), 500

    @flask_app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            res = Response()
            res.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
            res.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
            res.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            res.headers["Access-Control-Allow-Credentials"] = "true"
            return res

    return flask_app


if __name__ == '__main__':
    app = create_app()
    app.run(port=app.config["PORT"], debug=True)