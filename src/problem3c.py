import getpass
import pprint

import requests
from problem2c import add_user
from flask import Flask, request

from problem4a import *

# Problem 3c - Implement the enrolment mechanism and proactive password checker

## CLIENT
def enrol_user_interface():
    valid_credentials = False

    while not valid_credentials:
        username, password, valid_credentials = get_user_credentials()
        if not valid_credentials:
            print("Passwords do not match. Try again.")
            continue
    
    # send credentials to server
    payload = {'username': username, 'password': password}
    response = requests.post(f'https://{HOST}:{PORT}{ENROLL_ENDPOINT}', json=payload, verify=False)
    pprint.pprint(response.text)


def get_user_credentials() -> 'tuple[str, int, bool]':
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    duplicate_password = getpass.getpass("Enter password again: ")

    if password != duplicate_password:
        return None, None, False
    return username,password, True


## SERVER
def enrol_user_server():
    data = request.json
    user_created = add_user(data['username'], data['password'])
    if not user_created:
        print("User exists")
        return {'status': False}
    return {'status': True}


if __name__ == "__main__":
    enrol_user_interface()