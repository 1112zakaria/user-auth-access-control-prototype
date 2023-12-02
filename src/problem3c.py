from enum import Enum, auto
import getpass
import pprint
import json
import re

import requests
from problem2c import add_user, retrieve_user
from flask import Flask, request
import pdb

import problem4a

# Problem 3c - Implement the enrolment mechanism and proactive password checker
STATUS = 'status'
MIN_PASSWORD_SIZE = 8
SPECIAL_CHAR_SET = {'!','@','#','$','%','?','*'}
WEAK_PASSWORDS_FILE = 'weak_passwords.txt'

class UserEnrollResult(Enum):
    SUCCESS                 = 'SUCCESS'
    TOO_FEW_CHARS           = f'Too few characters. Password must be at least {MIN_PASSWORD_SIZE} characters in length.'
    MISSING_SPECIAL_CHAR    = f'Password must include at least one special character from the set {SPECIAL_CHAR_SET}'
    MISSING_UPPERCASE_CHAR  = 'Password must include at least one upper-case letter'
    MISSING_LOWERCASE_CHAR  = 'Password must include at least one lower-case letter'
    MISSING_NUMERICAL_DIGIT = 'Password must include at least one numerical digit'
    COMMON_WEAK_PASSWORD    = 'Password is found to be a common weak password.'
    MATCHES_COMMON_NUMBER   = 'Password matches the format of calendar dates, license plate numbers, telephone numbers, or other common number.'
    MATCHES_USERID          = 'Password matches the user ID.'
    USER_EXISTS             = 'User already exists.'



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
        if response_json[STATUS] == UserEnrollResult.SUCCESS.value:
            print(f"Successfully enrolled user {username}.")
            valid_credentials = True
            break

        errors: list[str] = response_json[STATUS]
        print("The following errors occurred: ")
        for error in errors:
            print(f"\t- {error}")
        print("Try again.")
        valid_credentials = False

    


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
    username, password = data['username'], data['password']
    errors: list[UserEnrollResult] = []
    
    errors = perform_proactive_password_check(username, password)

    if retrieve_user(username):
       errors += [UserEnrollResult.USER_EXISTS]
     
    if UserEnrollResult.SUCCESS not in errors:
        return {STATUS: [error.value for error in errors]}

    # if user does not exist and no errors, attempt to add the user
    add_user(username, password)
    return {STATUS: UserEnrollResult.SUCCESS.value}


def check_character_length(password: str) -> UserEnrollResult:
    if len(password) > MIN_PASSWORD_SIZE:
        return UserEnrollResult.SUCCESS
    return UserEnrollResult.TOO_FEW_CHARS

def check_special_characters(password: str) -> UserEnrollResult:
    # check the following:
    # - 1 upper case
    # - 1 lower case
    # - 1 digit
    # - 1 special character from special char set
    errors: list[UserEnrollResult] = []
    if not any(c for c in password if c.islower()):
        errors += [UserEnrollResult.MISSING_LOWERCASE_CHAR]
    if not any(c for c in password if c.isupper()):
        errors += [UserEnrollResult.MISSING_UPPERCASE_CHAR]
    if not any(c for c in password if c.isnumeric()):
        errors += [UserEnrollResult.MISSING_NUMERICAL_DIGIT]
    if not any(c for c in password if c in SPECIAL_CHAR_SET):
        errors += [UserEnrollResult.MISSING_SPECIAL_CHAR]
    
    if errors == []:
        return UserEnrollResult.SUCCESS
    return errors

def check_weak_common_passwords(password: str) -> UserEnrollResult:
    with open(WEAK_PASSWORDS_FILE, 'r') as f:
        weak_passwords = f.readlines()
        if password in weak_passwords:
            return UserEnrollResult.COMMON_WEAK_PASSWORD
    f.close()
    return UserEnrollResult.SUCCESS

def check_common_numbers(password: str) -> UserEnrollResult:
    contains_calendar_dates = re.search("[0-9][0-9][0-9][0-9](.|-|[ ]?)[0-9][0-9](.|-|[ ]?)[0-9][0-9]", password)
    contains_license_plate_number = re.search("[A-Za-z][A-Za-z][A-Za-z][A-Za-z](-|[ ]?)[0-9][0-9][0-9]", password)
    contains_telephone_number = re.search("[0-9][0-9][0-9](-|[ ]?)[0-9][0-9][0-9](-|[ ]?)[0-9][0-9][0-9][0-9]", password)

    if contains_calendar_dates or contains_license_plate_number or contains_telephone_number:
        return UserEnrollResult.MATCHES_COMMON_NUMBER
    return UserEnrollResult.SUCCESS

def check_user_id_match(username: str, password: str) -> UserEnrollResult:
    if username.lower() == password.lower():
        return UserEnrollResult.MATCHES_USERID
    return UserEnrollResult.SUCCESS

def perform_proactive_password_check(username: str, password: str) -> 'list[UserEnrollResult]':
    errors: list[UserEnrollResult] = []
    password_check_functions = [
        check_character_length, check_special_characters, check_weak_common_passwords, check_common_numbers
    ]

    for password_check_function in password_check_functions:
        result = password_check_function(password)
        if result != UserEnrollResult.SUCCESS:
            if type(result) is list: 
                errors += result
            elif isinstance(result, UserEnrollResult): 
                errors.append(result)

    result = check_user_id_match(username, password)
    if result != UserEnrollResult.SUCCESS:
        errors += [result]

    if errors == []:
        return [UserEnrollResult.SUCCESS]
    return errors


if __name__ == "__main__":
    enrol_user_interface()