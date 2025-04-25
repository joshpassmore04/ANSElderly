from functools import wraps

from flask import session, jsonify, g

def invalid_data():
    return jsonify({"status": "error", "message": "Invalid data provided"}), 400

def authentication_required():
    return jsonify({"status": "error", "message": "Authentication required"}), 401

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if 'USER_ID' is in the session
        user_id = session.get("USER_ID")
        if not user_id:
            return authentication_required()

        # Store the user_id in the 'g' object
        g.USER_ID = user_id

        return func(*args, **kwargs)

    return wrapper