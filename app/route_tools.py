from flask import jsonify
from flask_jwt_extended import get_jwt
from functools import wraps


def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role")
            if user_role != role:
                return jsonify({"message": "Insufficient permissions"}), 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper
