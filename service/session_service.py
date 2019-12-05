from flask import request
from model import Session
from secrets import token_urlsafe

sessions = {}


def new(user):
    new_key = token_urlsafe(32)
    session = Session(new_key, user)
    # rare
    while new_key in sessions:
        new_key = token_urlsafe(32)
    sessions[new_key] = session
    return session


def get(session_key=None):
    if not session_key:
        session_key = request.cookies.get('user_session')
    if session_key in sessions:
        return sessions[session_key]
    else:
        return None
