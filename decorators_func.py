from functools import wraps

from flask import abort
from flask_login import current_user

def therapist_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)  # Unauthorized
        if current_user.is_therapist:
            return func(*args, **kwargs)
        else:
            abort(403)  # Forbidden
    return decorated_function

def user_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)  # Unauthorized
        if not current_user.is_therapist:
            return func(*args, **kwargs)
        else:
            abort(403)  # Forbidden
    return decorated_function