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
                raise InvalidUsername(username)
            perm_set.add(username)


class PermissionError(Exception):
    pass
