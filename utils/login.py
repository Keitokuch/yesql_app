from functools import wraps
from flask import flash, request, redirect, url_for
import service.user_service as users


def require_login(function_to_protect):
    @wraps(function_to_protect)
    def wrapper(*args, **kwargs):
        user_id = request.cookies.get('session')
        if user_id:
            user_id = int(user_id)
            user = users.get_by_id(user_id)
            if user:
                return function_to_protect(*args, **kwargs)
            else:
                flash("Session exists, but user does not exist (anymore)")
                return redirect(url_for('login'))
        else:
            flash("Please log in")
            return redirect(url_for('login'))
    return wrapper
