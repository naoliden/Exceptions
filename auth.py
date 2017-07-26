import hashlib


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = str(self._encriptar_pw(password))
        # self.password = (password)

        self.is_logged_in = False

    def _encriptar_pw(self, password):
        '''Encripta el password con el username y retorna el sha digest'''
        hash_string = str(self.username) + str(password)
        hash_string = hash_string.encode('utf8')
        return hashlib.sha256(hash_string).hexdigest()

    def check_password(self, password):
        encrypted = self._encriptar_pw(password)
        return encrypted == self.password


class Authenticator:

    def __init__(self):
        self.users = {}

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


class Authorizor:

    def __init__(self, authenticator):
        self.authenticator = authenticator
        self.permissions = {}

    def add_permission(self, perm_name):
        '''crea permisos a los que se pueden agregar usuarios
        user --- > permiso'''

        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            self.permissions[perm_name] = set()
        else:
            raise PermissionError("Permission Exists")

    def permit_user(self, perm_name, username):
        ''' Otorga el permiso x recibido como input al usuario y'''

        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            raise PermissionError("Permission does not exist")
        else:
            if username not in self.authenticator.users:
                raise InvalidUsername(username)
            perm_set.add(username)

    def check_permission(self, perm_name, username):
        if not self.authenticator.is_logged_in(username):
            raise NotLoggedInError(username)
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            raise PermissionError("Permission does not exist")
        else:
            if username not in perm_set:
                raise NotPermittedError(username)
            else:
                return True


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


class PermissionError(Exception):
    pass


class NotLoggedInError(Exception):
    pass


class NotPermittedError(Exception):
    pass


authenticator = Authenticator()
authorizor = Authorizor(authenticator)
