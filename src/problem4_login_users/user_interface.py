import getpass
import http.client


class UserInterfaceState:
    pass


class UserInterface:
    """
    User interface client class for the user auth and access control
    prototype.

    Provides interface for user to enter their username and password via
    a command line interface.

    When the user enters their credentials, the interface will send the login
    info to the authentication server via HTTPS.

    Upon successful authentication, the interface will display the authenticated
    user's userID, roles/attributes/labels, & list of access rights.

    TODO: add logout function?
    """
    def __init__(self):
        self.server_connection = http.client.HTTPSConnection("localhost", 4000)
        pass
    
    def display_UI(self):
        pass

    def get_user_credentials(self) -> tuple:
        """
        Query user credentials via simple interface

        Returns: tuple containing username and password
        """
        # FIXME: how do I make the password a series of asterisks?
        
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        return username,password

    def run(self):
        """
        Run Client application.

        Prompts the user to input credentials while not signed-in

        When signed-in, displays user's status
        """
        header =    "Finvest Holdings\n" + \
                    "Client Holdings and Information Systems\n" + \
                    "-----------------------------------------"
        print(header)

        # Get user credentials
        self.get_user_credentials()
        # Send credentials to the server
        self.server_connection.request("POST", "/signin")


        # Based on result, either display user info or re-request credentials


if __name__ == "__main__":
    UI = UserInterface()
    UI.run()
        
