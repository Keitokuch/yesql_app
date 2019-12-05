class ErrorWithCode(Exception):
    def __init__(self, message, code):
        super().__init__(f'Error code {code}: {message}')
        self.code = code


class UserExistsError(ErrorWithCode):
    def __init__(self, username):
        self.msg = f"User with name '{username}' already exists"
        super().__init__(self.msg, 300)


class LoginError(ErrorWithCode):
    def __init__(self, msg, code=400):
        self.msg = msg
        super().__init__(self.msg, code)


class UserNotFoundError(LoginError):
    def __init__(self, username):
        msg = f'Username: {username} not found'
        super().__init__(msg, 402)


class PasswdNotMatchError(LoginError):
    def __init__(self, username):
        msg = f'Password authen failed for username: {username}'
        super().__init__(msg, 401)
