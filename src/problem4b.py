from problem2c import *
from enum import Enum, auto
import bcrypt

# Problem 4b - Implement the password verification mechanism
class LoginResult(Enum):
    SUCCESS                 = 0
    INVALID_CREDENTIALS     = 1

def verify_password(input_password: str, user: User) -> bool:
    encoded_password: bytes = input_password.encode('utf-8')
    result: bool = bcrypt.checkpw(encoded_password, user.hashed_password)
    return result

def login_user(username: str, password: str) -> 'tuple[User, LoginResult]':
    # fetch user record from password file
    user: User = retrieve_user(username)
    if not user:
        # username does not exist
        return None, LoginResult.INVALID_CREDENTIALS
    
    if not verify_password(password, user):
        return None, LoginResult.INVALID_CREDENTIALS
    return user, LoginResult.SUCCESS

if __name__ == "__main__":
    print(login_user('zak', '123'))
    print(login_user('zak', 'abc'))
    print(login_user('bob', '123'))