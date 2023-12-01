from enum import Enum, auto
import getpass
import pprint
import json
import re

import requests
from problem2c import add_user
from flask import Flask, request

import problem4a

# Problem 3c - Implement the enrolment mechanism and proactive password checker
STATUS = 'status'
MIN_PASSWORD_SIZE = 8
SPECIAL_CHAR_SET = {'!','@','#','$','%','?','*'}
WEAK_PASSWORDS_FILE = 'weak_passwords.txt'

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
    with open(WEAK_PASSWORDS_FILE, 'r') as f:
        weak_passwords = f.readlines()
        if password in weak_passwords:
            return PasswordCheckResult.COMMON_WEAK_PASSWORD
    f.close()
    return PasswordCheckResult.SUCCESS

def check_common_numbers(password: str) -> PasswordCheckResult:
    contains_calendar_dates = re.search("[0-9][0-9][0-9][0-9](.|-|[ ]?)[0-9][0-9](.|-|[ ]?)[0-9][0-9]", password)
    contains_license_plate_number = re.search("[A-Za-z][A-Za-z][A-Za-z][A-Za-z](-|[ ]?)[0-9][0-9][0-9]", password)
    contains_telephone_number = re.search("[0-9][0-9][0-9](-|[ ]?)[0-9][0-9][0-9](-|[ ]?)[0-9][0-9][0-9][0-9]", password)

    if contains_calendar_dates or contains_license_plate_number or contains_telephone_number:
        return PasswordCheckResult.MATCHES_COMMON_NUMBER
    return PasswordCheckResult.SUCCESS

def check_user_id_match(username: str, password: str) -> PasswordCheckResult:
    if username.lower() == password.lower():
        return PasswordCheckResult.MATCHES_USERID
    return PasswordCheckResult.SUCCESS

def perform_proactive_password_check(username: str, password: str) -> 'list[PasswordCheckResult]':
    errors: list[PasswordCheckResult] = []
    password_check_functions = [
        check_character_length, check_special_characters, check_weak_common_passwords, check_common_numbers
    ]

    for password_check_function in password_check_functions:
        result = password_check_function(password)
        if result != PasswordCheckResult.SUCCESS:
            errors += result

    result = check_user_id_match(username, password)
    if result != PasswordCheckResult.SUCCESS:
        errors += result

    if errors == []:
        return PasswordCheckResult.SUCCESS
    return errors


if __name__ == "__main__":
    enrol_user_interface()