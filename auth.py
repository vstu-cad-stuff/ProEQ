from flask import request, Response
from functools import wraps
from model import User


# auth failure response
def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


# decorator for the authentication function
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        # check authorization
        if auth:
            user = User.query.filter_by(name=auth.username).first()
            # check user and check password
            if user is not None and user.password == auth.password:
                # success
                return f(*args, **kwargs)
        # failure
        return authenticate()
    # return decorator function
    return decorated
