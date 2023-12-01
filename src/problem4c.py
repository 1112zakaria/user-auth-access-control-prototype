from problem4b import *
from problem1d import *
import json

# Problem 4c - Enforce the access control mechanism
USER_ID = 'userId'
ROLE = 'role'
PERMISSIONS = 'perms'
STATUS = 'status'

class AccessControl():
    def __init__(self, user: User, result: LoginResult):
        self.payload: dict = {}

        self.payload[STATUS] = result.value
        if user and result == LoginResult.SUCCESS:
            self.payload[USER_ID] = user.username
            self.payload[ROLE] = user.role.get_role_name()
            self.payload[PERMISSIONS] = user.role.get_json_permissions()
    
    def encode(self):
        return json.dumps(self.payload)
    
    @classmethod
    def decode(cls, encoded_data: str):
        pass

        

def enforce_access_control(username: str, password: str):
    user, result = login_user(username, password)
    access_control = AccessControl(user, result)
    print(access_control.encode())
    return access_control

if __name__ == "__main__":
    enforce_access_control('zak', '123')
    enforce_access_control('zak', 'abc')
