from flask import Blueprint, jsonify, request, g, abort, session
from flask_cors import cross_origin
from pydantic import ValidationError

from data.permission import PermissionType, PermissionAction, PermissionResult
from data.schema.user import UserRegister, UserCreate, UserOut, UserUpdatePermission
from routes.util import login_required, authentication_required, invalid_data
from service.errors.server_error import ServerError
from service.user_service import UserService



def create_user_blueprint(base_endpoint, user_service: UserService, is_debug: bool):
    user_blueprint = Blueprint('user', __name__, url_prefix=base_endpoint + '/user')

    @user_blueprint.route("/login", methods=["POST"])
    @cross_origin(supports_credentials=True)
    def login():

        try:
            print("ONE")
            user_data = UserCreate(**request.json)
            if user_data:
                print("TWO")

                user = user_service.validate_login(str(user_data.email), user_data.password)
                if user:
                    user = UserOut.model_validate(user.model_dump(exclude={"password"}))
                    session["EMAIL"] = str(user_data.email)
                    session["USER_ID"] = user.id
                    session["FIRST_NAME"] = user.first_name
                    session["LAST_NAME"] = user.last_name
                    return jsonify(
                        {"status": "success", "message": "Login successful", "session": user.model_dump()}), 200
                else:
                    return invalid_data()
            else:
                return invalid_data()

        except ValidationError:
            return invalid_data()

    @user_blueprint.route("/register", methods=["POST"])
    @cross_origin(supports_credentials=True)
    def register():
        try:
            user_data = UserRegister(**request.json)
            print("1")
            if user_data:
                print("2")
                user = user_service.register_user(first_name=user_data.first_name,
                                                  last_name=user_data.last_name,
                                                  email=str(user_data.email),
                                                  password=user_data.password)
                if user:
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

    @user_blueprint.route("/@me", methods=["POST", "GET"])
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

    def handle_permission_result(result):
        match result:
            case True:
                return jsonify({"status": "success", "message": "Permission exists"}), 200
            case PermissionResult.SUCCESS:
                return jsonify({"status": "success", "message": "Permission change succeeded"}), 200
            case PermissionResult.FAILED:
                return authentication_required()
            case PermissionResult.EXISTS:
                return jsonify({"status": "failed", "message": "Permission already exists"}), 400
            case _:
                return invalid_data()

    def give_permission(to_user_id: int, from_user_id: int, debug_bypass: bool, permission_type: PermissionType):

        to_user = user_service.get_user_by_id(to_user_id)
        if to_user:
            if debug_bypass:
                worked = user_service.give_permission(to_user.id, permission_type.value)
                return handle_permission_result(worked)
            else:
                worked = user_service.give_permission_from(from_user_id, to_user.id,
                                                           permission_type.value)
                return handle_permission_result(worked)
        else:
            return invalid_data()

    def remove_permission(to_user_id: int, from_user_id: int, debug_bypass: bool, permission_type: PermissionType):

        to_user = user_service.get_user_by_id(to_user_id)
        if to_user:
            if debug_bypass:
                worked = user_service.remove_permission(to_user.id, permission_type.value)
                return handle_permission_result(worked)
            else:
                worked = user_service.remove_permission_from(from_user_id, to_user.id,
                                                           permission_type.value)
                return handle_permission_result(worked)
        else:
            return invalid_data()

    @user_blueprint.route("/permission", methods=["POST"])
    @cross_origin(supports_credentials=True)
    @login_required
    def permission():
        from_user_id = g.get("USER_ID")
        try:
            permission_update = UserUpdatePermission(**request.json)
            if permission_update:
                debug_bypass = permission_update.debug_bypass and is_debug
                match permission_update.action:
                    case PermissionAction.GIVE:
                        return give_permission(
                            from_user_id,
                            permission_update.to_id,
                            debug_bypass=debug_bypass,
                            permission_type=permission_update.permission_name
                        )
                    case PermissionAction.REMOVE:
                        return remove_permission(
                            from_user_id,
                            permission_update.to_id,
                            debug_bypass=debug_bypass,
                            permission_type=permission_update.permission_name
                        )
                    case PermissionAction.CHECK_CURRENT_USER:
                        has_permission = user_service.has_permission(from_user_id, permission_update.permission_name) or debug_bypass
                        return handle_permission_result(has_permission)
                    case _:
                        return invalid_data()
            else:
                return invalid_data()

        except ValidationError:
            return invalid_data()

    @user_blueprint.route("/delete", methods=["POST"])
    @cross_origin(supports_credentials=True)
    @login_required
    def delete():
        user_id = g.get("USER_ID")
        if user_service.delete_user_by_id(user_id):
            return jsonify({"status": "success", "message": "Delete successful"}), 200
        raise ServerError

    return user_blueprint

