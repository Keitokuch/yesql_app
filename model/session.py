from model import User

class Session():
    def __init__(self, session_key: str, user: User):
        self.key = session_key
        self.user = User

    def to_dict(self):
        return self.__dict__
