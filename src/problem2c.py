from problem1d import *
import bcrypt

# Implement the password file
# store the username, hashed password, salt, role
SEPARATOR = ":"
PASSWORD_FILE = "passwd.txt"

# TODO: make function to add and retrieve user

class User():
    def __init__(self, username: str, hashed_password: str = None, role: DefaultRole = DefaultRole()) -> None:
        self.username: str = username
        self.hashed_password = hashed_password
        self.role: DefaultRole = role
    
    def set_role(self, role: DefaultRole):
        self.role = role

    def __str__(self):
        return f"User [{self.username}, {self.hashed_password}, {self.role}]"

    @classmethod
    def get_user_from_entry(cls, entry: str) -> 'User':
        split_entry: list[str] = entry.split(SEPARATOR)
        username, hashed_password, role_str = split_entry[0], split_entry[1], split_entry[2]
        role = get_role_from_str(role_str)()
        user: User = User(username, hashed_password, role)
        return user


def add_user(username: str, password: str, role: DefaultRole = DefaultRole()) -> bool:
    # check username doesn't exist
    if retrieve_user(username):
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

def retrieve_user_entry(username: str) -> str:
    with open(PASSWORD_FILE, 'r') as f:
        entries = f.read().splitlines()

        for entry in entries:
            if username in entry:
                return entry
    f.close()
    return None

def retrieve_user(username: str) -> User:
    # find user's entry
    user_entry: str = None
    user: User = None
    
    user_entry = retrieve_user_entry(username)
    if not user_entry:
        return None
    
    user = User.get_user_from_entry(user_entry)
    print(user)
    return user


if __name__ == "__main__":
    add_user('zak', '123', Client())
    retrieve_user('zak')