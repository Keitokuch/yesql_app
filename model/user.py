class User():

    """User object representation"""

    def __init__(self):
        self.id = -1
        self.username = 'Invalid'
        self._passwd = ''
        self.is_authenticated = False

    @property
    def passwd(self):
        return self._passwd

    @passwd.setter
    def passwd(self, raw):
        #  self._passwd = sha512_crypt.encrypt(raw)
        self._passwd = raw
