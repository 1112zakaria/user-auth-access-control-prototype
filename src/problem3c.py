from enum import Enum, auto
import getpass
import pprint
import json

import requests
from problem2c import add_user
from flask import Flask, request

import problem4a

# Problem 3c - Implement the enrolment mechanism and proactive password checker
STATUS = 'status'
MIN_PASSWORD_SIZE = 8
SPECIAL_CHAR_SET = {'!','@','#','$','%','?','*'}

class PasswordCheckResult(Enum):
    SUCCESS                 = 'SUCCESS'
    TOO_FEW_CHARS           = f'Too few characters. Password must be at least {MIN_PASSWORD_SIZE} characters in length.'
    MISSING_SPECIAL_CHAR    = f'Password must include at least one special character from the set {SPECIAL_CHAR_SET}'
    MISSING_UPPERCASE_CHAR  = 'Password must include at least one upper-case letter'
    MISSING_LOWERCASE_CHAR  = 'Password must include at least one lower-case letter'
    MISSING_NUMERICAL_DIGIT = 'Password must include at least one numerical digit'
    COMMON_WEAK_PASSWORD    = 'Password is found to be a common weak password.'
    MATCHES_COMMON_NUMBER   = 'Password matches the format of calendar dates, license plate numbers, telephone numbers, or other common number.'
    MATCHES_USERID          = 'Password matches the user ID.'



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
        response = requests.post(f'https://{problem4a.HOST}:{problem4a.PORT}{problem4a.ENROLL_ENDPOINT}', json=payload, verify=False)
        response_json = json.loads(response.text)
        if response_json[STATUS] == False:
            print("User already exists. Try again.")
            valid_credentials = False
    print(f"Successfully enrolled user {username}")


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
        return {STATUS: False}
    return {STATUS: True}


def check_character_length(password: str) -> PasswordCheckResult:
    if len(password) > MIN_PASSWORD_SIZE:
        return PasswordCheckResult.SUCCESS
    return PasswordCheckResult.TOO_FEW_CHARS

def check_special_characters(password: str) -> PasswordCheckResult:
    # check the following:
    # - 1 upper case
    # - 1 lower case
    # - 1 digit
    # - 1 special character from special char set
    errors: list[PasswordCheckResult] = []
    if not any(c for c in password if c.islower()):
        errors += PasswordCheckResult.MISSING_LOWERCASE_CHAR
    if not any(c for c in password if c.isupper()):
        errors += PasswordCheckResult.MISSING_UPPERCASE_CHAR
    if not any(c for c in password if c.isnumeric()):
        errors += PasswordCheckResult.MISSING_NUMERICAL_DIGIT
    if not any(c for c in password if c in SPECIAL_CHAR_SET):
        errors += PasswordCheckResult.MISSING_SPECIAL_CHAR
    
    if errors == []:
        return PasswordCheckResult.SUCCESS
    return errors

def check_weak_common_passwords(password: str) -> PasswordCheckResult:
    pass

def check_common_numbers(password: str) -> PasswordCheckResult:
    pass

def check_user_id_match(username: str, password: str) -> PasswordCheckResult:
    pass

def perform_proactive_password_check(password: str):
    pass




if __name__ == "__main__":
    enrol_user_interface()