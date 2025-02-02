from flask import jsonify
from flask_jwt_extended import get_jwt
from functools import wraps


def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()  # Pobiera cały payload tokena
            user_role = claims.get("role")
            # current_user = get_jwt_identity()
            if user_role != role:
                return jsonify({"message": "Insufficient permissions"}), 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper
