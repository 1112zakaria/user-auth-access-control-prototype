from problem1d import *
import bcrypt

# Implement the password file
# store the username, hashed password, salt, role
SEPARATOR = ":"
PASSWORD_FILE = "passwd.txt"

# TODO: make function to add and retrieve user

class User():
    def __init__(self, username: str) -> None:
        self.username: str = username
        self.role: DefaultRole = DefaultRole()
    
    def set_role(self, role: DefaultRole):
        self.role = role


def check_user_exists(username: str) -> bool:
    return False

def add_user(username: str, password: str, role: DefaultRole = DefaultRole()) -> bool:
    # check username doesn't exist
    if check_user_exists(username):
        return False

    # hash the password with a salt
    encoded_password: bytes = password.encode('utf-8')
    salt: bytes = bcrypt.gensalt(12)
    hashed_password: bytes = bcrypt.hashpw(encoded_password, salt)
    file_entry: str = username + SEPARATOR + hashed_password.decode('utf-8') + SEPARATOR + role.get_role_name() + '\n'
    
    print(file_entry)

    with open(PASSWORD_FILE, 'a') as f:
        f.write(file_entry)
    f.close()

    return True




if __name__ == "__main__":
    add_user('zak', '123', Client())