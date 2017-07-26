import hashlib


class User:
    def __init__(self, username, password):
        self.password = self.encriptar_pw(password)
        self.is_logged_in = False

    def _encriptar_pw(self, password):
        '''Encripta el password con el username y retorna el sha digest'''
        hash_string = self.username + self.password
        hash_string = hash_string.encode('utf8')
        return hashlib.sha256(hash_string).hexdigest()

    def check_password(self, password):
        encrypted = self._encriptar_pw(password)
        return encrypted == self.password


class AuthException(Exception):
    def __init__(self, username, user=None):
        ''' El primer parametro es un nuombre de usuario y el segundo es el objeto
         User asociado a este nombre.'''
        super().__init__(username, user)
        self.username = username
        self.user = user


class UsernameAlreadyExists(AuthException):
    pass


class PasswordTooShort(AuthException):
    pass


class InvalidUsername(AuthException):
    pass


class InvalidPassword(AuthException):
    pass


class Authenticator:
    def __init__(self):
        self.users = []

    def add_users(self, username, password):
        if username in self.users:
            raise UsernameAlreadyExists(username)
        if len(password) < 6:
            raise PasswordTooShort(username)
        self.users[username] = User(username, password)

    def login(self, username, password):
        try:
            user = self.users[username]
        except KeyError:
            raise InvalidUsername(username)
        ''' Levanto una excepcion pq agarro un Error, algo que hace que se me caiga el flujo'''
        if not user.check_password(password):
            raise InvalidPassword(username, user)
        ''' Hago un chequeo y si me tira false o true da lo mismo, pq no es que alg ohaya fallado,
        esto es parte normal del flujo. Levanto una excepcion para manejar el problema solamente,
        pero todo es normal, no hay un error.'''
        user.is_logged_in = True
        return True

    def is_logged_in(self, username):
        if username in self.users:
            return self.users[username].is_logged_in
        else:
            return False


# if __name__ == '__main__':
authenticator = Authenticator()
