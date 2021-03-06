from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


# Decorator functions are used where views need certain permissions
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Special decorator to add @admin_required in views
def admin_required(f):
    return permission_required(Permission.ADMIN)(f)
