import auth


class Editor:
    def __init__(self):
        self.username = None
        self.menu_map = {
            "login": self.login,
            "test": self.test,
            "change": self.change,
            "quit": self.quit
        }

    def login(self):
        logged_in = False
        while not logged_in:
            username = input("username: ")
            password = input("password: ")
            try:
                logged_in = auth.authenticator.login(username, password)
            except auth.InvalidUsername:
                print("Sorry, wrong username")
            except auth.InvalidPassword:
                print("Sorry, wrong password")
            else:
                self.username = username

    def is_permitted(self, permission):
        try:
            auth.authorizor.check_permission(permission, self.username)
        except auth.NotLoggedInError as e:
            print("{} is not logged in".format(e.username))
            return False
        else:
            return True

    def test(self):
        if self.is_permitted("test program"):
            print("Testing program now...")

    def change(self):
        if self.is_permitted("change program"):
            print("Changing program now...")

    def quit(self):
        raise SystemExit()

    def menu(self):
        try:
           # answer = ""
            while True:
                print('''
                    Please enter a command:
                    \tlogin\tLogin
                    \ttest\tTest the program
                    \tchange\tChange the program
                    \tquit\tQuit
                    ''')
                answer = input("Enter a command: ").lower()
                try:
                    command = self.menu_map[answer]
                except KeyError:
                    print("{} is not a valid command".format(answer))
                # except ValueError:
                #     print("{} is not a valid command".format(answer))
                else:
                    command()
                # finally:
                #     print("Thank you for testint the auth module")
        finally:
            print("Thank you for testint the auth module")

Editor().menu()


# auth.authenticator.add_users("joe", "joepassword")
# auth.authenticator.login("joe", "joepassword")

# auth.authorizor.add_permission("test program")

# auth.authorizor.add_permission("change program")
# auth.authorizor.permit_user("test program", 'joe')
