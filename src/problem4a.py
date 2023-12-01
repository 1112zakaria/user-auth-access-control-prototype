import getpass
import requests
import pprint
from flask import Flask, request
from threading import Thread
import time
from multiprocessing import Process
from problem3c import enrol_user_server
from problem4c import *
import json
import logging
import urllib3

# Problem 4 Login Users

logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HOST = 'localhost'
PORT = 4000
AUTH_ENDPOINT = '/signin'
ENROLL_ENDPOINT = '/enroll'

# def signal_handler(sig, frame):
#     server_process.terminate()
#     sys.exit(0)

#signal.signal(signal.SIGINT, signal_handler)

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
        self.host = HOST
        self.port = PORT
        self.auth_endpoint = AUTH_ENDPOINT
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

        valid_credentials = False

        while not valid_credentials:
            # Get user credentials
            credentials = self.get_user_credentials()
            payload = {'username': credentials[0], 'password': credentials[1]}
            # Send credentials to the server
            response = requests.post(f'https://{self.host}:{self.port}{self.auth_endpoint}', json=payload, verify=False)
            #pprint.pprint(response.text)
            response_json = json.loads(response.text)

            if response_json[STATUS] == 'SUCCESS':
                valid_credentials = True
            else:
                print('Invalid credentials. Try again.')

        pprint.pprint(response_json)
        # Based on result, either display user info or re-request credentials


class AuthServer:
    def __init__(self):
        self.server_address = ('localhost', 4000)
        self.app = Flask(__name__)
        
        self.add_endpoints()
    
    def add_endpoints(self):
        self.app.add_url_rule('/signin', 'signin', self.signin, methods=['POST'])
        self.app.add_url_rule('/enroll', 'enroll', enrol_user_server, methods=['POST'])

    def listen(self):
        print(f"Serving at {self.server_address}...")
        context = ('snakeoil.pem', 'snakeoil.key')
        self.app.run('localhost', debug=True, port=4000, ssl_context=context)

    def signin(self):
        data = request.json
        response = enforce_access_control(data['username'], data['password'])
        print(response)
        return response.encode()

    def run(self):
        self.listen()


if __name__ == "__main__":
    auth_server = AuthServer()
    UI = UserInterface()

    # server_thread = Thread(target=auth_server.run)
    # server_thread.start()
    server_process = Process(target=auth_server.run)
    server_process.start()

    time.sleep(1)
    UI.run()

    server_process.join()
    # server_thread.join()
        
