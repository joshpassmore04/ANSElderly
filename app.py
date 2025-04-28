import json
import secrets

from cachelib import FileSystemCache
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from flask_session import Session
from sqlalchemy import create_engine, Engine

from data.sqlalchemy.sqlalchemy_airport_data import SQLAlchemyAirportData
from data.sqlalchemy.sqlalchemy_user_data import SQLAlchemyUserData
from orm import Base
from routes.flight_routes import create_flight_blueprint
from routes.user_routes import create_user_blueprint
from service.errors.server_error import ServerError
from service.flight_service import FlightService
from service.user_service import UserService


def create_app(engine: Engine, debug: bool = False) -> Flask:

    flask_app = Flask(__name__)
    flask_app.config.from_file("config.json", load=json.load)

    flask_app.config["SECRET_KEY"] = secrets.token_hex(16)
    flask_app.config["SESSION_CACHELIB"] = FileSystemCache(cache_dir="sessions", threshold=500)
    flask_app.config["SESSION_TYPE"] = "cachelib"
    flask_app.config["SESSION_PERMANENT"] = True
    CORS(flask_app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    Session(flask_app)
    Base.metadata.create_all(engine)

    user_data = SQLAlchemyUserData(engine)
    airport_data = SQLAlchemyAirportData(engine)
    user_service = UserService(user_data)
    flight_service = FlightService(airport_data, user_data)

    flask_app.register_blueprint(create_user_blueprint(flask_app.config["ENDPOINT"], user_service, debug))
    flask_app.register_blueprint(create_flight_blueprint(flask_app.config["ENDPOINT"], user_service, flight_service))

    @flask_app.errorhandler(ServerError)
    def handle_db_error():
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
    engine = create_engine(f"sqlite:///test.db", echo=False)
    app = create_app(engine)
    app.run(port=app.config["PORT"], debug=True)