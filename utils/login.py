from functools import wraps
from flask import flash, request, redirect, url_for
import service.session_service as Sessions


def require_login(function_to_protect):
    @wraps(function_to_protect)
    def wrapper(*args, **kwargs):
        key = request.cookies.get('user_session')
        if key:
            session = Sessions.get(key)
            if session:
                return function_to_protect(*args, **kwargs)
            else:
                flash("Session does not exist")
                return redirect(url_for('login'))
        else:
            flash("Please log in")
            return redirect(url_for('login'))
    return wrapper
