from flask import g
from flask import request

from functools import wraps


def token_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not g.user.token:
            return "Token required", 300

        try:
            token.user = g.user.token
            profile = g.user.profile

        except Exception:
            return "Token invalid", 400

        return f(*args, **kwargs)

    return decorated_function
