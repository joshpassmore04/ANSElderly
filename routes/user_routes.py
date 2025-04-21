from flask import Blueprint, session, jsonify, request, g
from flask_cors import cross_origin
from pydantic import ValidationError

from data.schema.user import UserCreate, UserOut
from routes.util import login_required
from service.errors.invalid_data import InvalidData
from service.errors.server_error import ServerError
from service.user_service import UserService


def create_user_blueprint(base_endpoint, user_service: UserService):
    user_blueprint = Blueprint('user', __name__, url_prefix=base_endpoint + '/user')

    @user_blueprint.route("/login", methods=["POST"])
    @cross_origin(supports_credentials=True)
    def login():

        try:
            user_data = UserCreate(**request.json)
            if user_data.is_valid():
                session["USER_ID"] = user_data.id
                session["USERNAME"] = user_data.username
                session["EMAIL"] = str(user_data.email)
                user = user_service.validate_login(str(user_data.email), user_data.plaintext_password)
                if user:
                    user_out = UserOut.model_validate(user)
                    return jsonify(
                        {"status": "success", "message": "Login successful", "session": user_out.model_dump()}), 200
                else:
                    raise InvalidData("Incorrect login")
            else:
                raise InvalidData("Incorrect login")

        except ValidationError:
            raise InvalidData("Incorrect login")

    @user_blueprint.route("/register", methods=["POST"])
    @cross_origin(supports_credentials=True)
    def register():

        try:
            user_data = UserCreate(**request.json)
            if user_data.is_valid():
                session["USER_ID"] = user_data.id
                session["USERNAME"] = user_data.username
                session["EMAIL"] = str(user_data.email)
                user = user_service.register_user(first_name=user_data.first_name,
                                                  last_name=user_data.last_name,
                                                  email=str(user_data.email),
                                                  password=user_data.plaintext_password)
                if user:
                    user_out = UserOut.model_validate(user)
                    return jsonify(
                        {"status": "success", "message": "Registration successful", "session": user_out.model_dump()}), 200
                else:
                    raise InvalidData("Incorrect login")


            else:
                raise InvalidData("Incorrect login")

        except ValidationError:
            raise InvalidData("Incorrect login")

    @user_blueprint.route("/@me")
    @cross_origin(supports_credentials=True)
    @login_required
    def get_current_user():
        user_id = g.get("USER_ID")
        user = user_service.get_user_by_id(user_id)
        if user:
            try:
                user_out = UserOut.model_validate(user)
                return jsonify({"status": "success", "user": user_out.model_dump()}), 200
            except ValidationError:
                raise ServerError
        else:
            raise ServerError

    @user_blueprint.route("/logout", methods=["POST", "GET"])
    @cross_origin(supports_credentials=True)
    @login_required
    def logout():
        session.clear()
        return jsonify({"status": "success", "message": "Logged out successfully"}), 200

    @user_blueprint.route("/delete", methods=["POST"])
    @cross_origin(supports_credentials=True)
    @login_required
    def delete():
        user_id = g.get("USER_ID")
        if user_service.delete_user_by_id(user_id):
            return jsonify({"status": "success", "message": "Delete successful"}), 200
        raise ServerError



