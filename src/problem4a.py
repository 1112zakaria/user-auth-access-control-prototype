import getpass
import requests
import pprint
import signal
import sys
from flask import Flask, request
from threading import Thread

# Problem 4 Login Users

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
        self.host = 'localhost'
        self.port = 4000
        self.auth_endpoint = '/signin'
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
        credentials = self.get_user_credentials()
        payload = {'username': credentials[0], 'password': credentials[1]}
        # Send credentials to the server
        response = requests.post(f'https://{self.host}:{self.port}{self.auth_endpoint}', json=payload, verify=False)
        pprint.pprint(response.text)


        # Based on result, either display user info or re-request credentials


class AuthServer:
    def __init__(self):
        self.server_address = ('localhost', 4000)
        self.app = Flask(__name__)
        
        self.add_endpoints()
        signal.signal(signal.SIGINT, self.cleanup)
    
    def add_endpoints(self):
        self.app.add_url_rule('/signin', 'signin', self.signin, methods=['POST'])

    def listen(self):
        print(f"Serving at {self.server_address}...")
        context = ('snakeoil.pem', 'snakeoil.key')
        self.app.run('localhost', debug=True, port=4000, ssl_context=context)

    def signin(self):
        data = request.json
        return f"Hello user {data['username']}"

    def cleanup(self, sig, frame):
        sys.exit(0)

    def run(self):
        self.listen()


if __name__ == "__main__":
    auth_server = AuthServer()
    UI = UserInterface()

    auth_server.run()
    UI.run()
        
