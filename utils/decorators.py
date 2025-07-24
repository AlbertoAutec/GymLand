from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from models import UserModel
from flask_smorest import abort

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = UserModel.query.get(user_id)
            if not user or user.ruolo not in roles:
                abort(403, message="Access forbidden: insufficient role")
            return fn(*args, **kwargs)
        return decorator
    return wrapper
