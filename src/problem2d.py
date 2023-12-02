import os
import tempfile
import unittest

import bcrypt
from problem1d import Client, Teller
from problem2c import User, add_user, retrieve_user, retrieve_user_entry, set_password_file, clear_password_file

TEST_PASSWORD_FILE = 'test_passwd.txt'

class TestPasswordFileMechanism(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_file = tempfile.NamedTemporaryFile()
        os.environ['PASSWORD_FILE'] = cls.temp_file.name
        set_password_file(TEST_PASSWORD_FILE)
        clear_password_file()
        

    @classmethod
    def tearDownClass(cls):
        pass

    def test_add_user(self):
        # Test add user successful
        username = 'test_user'
        password = 'test_password'
        role = Client()

        result = add_user(username, password, role)
        self.assertTrue(result)

        # Test add user duplicate
        username = 'test_user'
        password = 'test_password'
        role = Client()

        add_user(username, password, role)
        result = add_user(username, password, role)
        self.assertFalse(result)

    def test_retrieve_user_entry_existing(self):
        username = 'test_user'
        password = 'test_password'
        role = Client()

        add_user(username, password, role)
        entry = retrieve_user_entry(username)
        self.assertIsNotNone(entry)

    def test_retrieve_user_entry_non_existing(self):
        username = 'non_existing_user'

        entry = retrieve_user_entry(username)
        self.assertIsNone(entry)

    def test_retrieve_user_existing(self):
        username = 'test_user'
        password = 'test_password'
        role = Client()

        add_user(username, password, role)
        user = retrieve_user(username)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, username)
        self.assertEqual(user.role.get_role_name(), role.get_role_name())

    def test_retrieve_user_non_existing(self):
        username = 'non_existing_user'

        user = retrieve_user(username)
        self.assertIsNone(user)

    def test_user_class(self):
        username = 'test_user'
        password = 'test_password'
        role = Client()

        user = User(username, password, role)
        self.assertEqual(user.username, username)
        self.assertEqual(user.hashed_password, password)
        self.assertEqual(user.role, role)

        new_role = Teller()
        user.set_role(new_role)
        self.assertEqual(user.role.get_role_name(), new_role.get_role_name())

if __name__ == '__main__':
    unittest.main()
