from model import User
from database import mysql as db
import logging
from passlib.hash import bcrypt
from utils.errors import *

Logger = logging.getLogger('app.'+__name__)


def get_by_id(uid: int) -> User:
    user = User()
    entry, err = db.get_user_by_uid(uid)
    if entry:
        user.id = entry['user_id']
        user.username = entry['username']
        return user
    else:
        return None


def login_user(username: str, passwd: str) -> User:
    user = User()
    user.username = username
    user.passwd = passwd
    return authenticate(user)


def authenticate(user: User) -> User:
    entry, err = db.get_uid_and_passwd_by_name(user.username)
    if entry:
        uid = entry['user_id']
        hashed = entry['passwd']
        if bcrypt.verify(user.passwd, hashed):
            user.id = uid
            user.is_authenticated = True
            Logger.info(f'User: {user.username} login successfully.')
            return user
        else:
            Logger.info(f'User: {user.username} passwd verify failed.')
            raise PasswdNotMatchError(user.username)
    else:
        raise UserNotFoundError(user.username)


def signup_user(username: str, passwd: str) -> User:
    user = User()
    user.username = username
    user.passwd = passwd
    return insert_user(user)


def insert_user(user: User):
    ret, _ = db.get_uid_and_passwd_by_name(user.username)
    if ret:
        raise UserExistsError(user.username)

    ret, err = db.insert_user(user.username, bcrypt.encrypt(user.passwd))
    if ret and not err:
        entry, err = db.get_uid_and_passwd_by_name(user.username)
        if entry:
            user.id = entry['user_id']
            Logger.info(f'Successfully created user {user.username} with id {user.id}')
            return user
        else:
            raise Exception('Inner Error User Insert Not Successful!')
    else:
        return None
