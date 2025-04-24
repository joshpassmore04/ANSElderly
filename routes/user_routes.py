from flask import Blueprint, session, jsonify, request, g
from flask_cors import cross_origin
from pydantic import ValidationError

from data.schema.user import UserRegister, UserLogin, UserOut
from routes.util import login_required
from service.errors.server_error import ServerError
from service.user_service import UserService


def invalid_data():
    return jsonify({"status": "error", "message": "Invalid data provided"}), 400

def create_user_blueprint(base_endpoint, user_service: UserService):
    user_blueprint = Blueprint('user', __name__, url_prefix=base_endpoint + '/user')

    @user_blueprint.route("/login", methods=["POST"])
    @cross_origin(supports_credentials=True)
    def login():

        try:
            print("ONE")
            user_data = UserLogin(**request.json)
            if user_data:
                print("TWO")

                session["EMAIL"] = str(user_data.email)
                user = user_service.validate_login(str(user_data.email), user_data.password)
                if user:
                    session["USER_ID"] = user.id
                    session["USERNAME"] = user.first_name + " " + user.last_name
                    return jsonify(
                        {"status": "success", "message": "Login successful", "session": user.model_dump()}), 200
                else:
                    return invalid_data()
            else:
                return invalid_data()

        except ValidationError as e:
            print(e.errors)
            return invalid_data()

    @user_blueprint.route("/register", methods=["POST"])
    @cross_origin(supports_credentials=True)
    def register():
        try:
            user_data = UserRegister(**request.json)
            print("1")
            if user_data:
                print("2")
                session["USERNAME"] = user_data.first_name + " " + user_data.last_name
                session["EMAIL"] = str(user_data.email)
                user = user_service.register_user(first_name=user_data.first_name,
                                                  last_name=user_data.last_name,
                                                  email=str(user_data.email),
                                                  password=user_data.password)
                if user:
                    session["USER_ID"] = user.id
                    print("3")
                    return jsonify(
                        {"status": "success", "message": "Registration successful", "session": user.model_dump()}), 200
                else:
                    return invalid_data()
            else:
                return invalid_data()
        except ValidationError as e:
            print(e.errors)
            return invalid_data()

    @user_blueprint.route("/@me")
    @cross_origin(supports_credentials=True)
    @login_required
    def get_current_user():
        user_id = g.get("USER_ID")
        user = user_service.get_user_by_id(user_id)
        if user:
            try:
                return jsonify({"status": "success", "user": user.model_dump()}), 200
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

    return user_blueprint

