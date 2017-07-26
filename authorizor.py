import auth


class Authorizor:
    def __init__(self, authenticator):
        self.authenticator = authenticator
        self.permissions = {}

    def add_permission(self, perm_name):
        '''crea permisos a los que se pueden agregar usuarios
        user --- > permiso'''

        try:
            perm_set = self.add_permissions[perm_name]
        except KeyError:
            self.add_permissions[perm_name] = set()
        else:
            raise PermissionError("Permission Exists")

    def permit_user(self, perm_name, username):
        ''' Otorga el permiso x recibido como input al usuario y'''

        try:
            perm_set = self.permissions[username]
        except KeyError:
            raise PermissionError("Permission does not exist")
        else:
            if username not in self.authenticator.users:
                raise auth.InvalidUsername(username)
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


class PermissionError(Exception):
    pass


class NotLoggedInError(Exception):
    pass


class NotPermittedError(Exception):
    pass


if __name__ == "__main__":

    authorizor = Authorizor(auth.authenticator)
