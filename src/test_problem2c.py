import os
import tempfile
import unittest

import bcrypt
from problem2c import User, add_user, retrieve_user, retrieve_user_entry


class TestPasswordFileMechanism(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_file = tempfile.NamedTemporaryFile()
        os.environ['PASSWORD_FILE'] = cls.temp_file.name

    @classmethod
    def tearDownClass(cls):
        cls.temp_file.close()

    def test_add_user_successful(self):
        username = 'test_user'
        password = 'test_password'
        role = 'test_role'

        result = add_user(username, password, role)
        self.assertTrue(result)

    def test_add_user_duplicate(self):
        username = 'test_user'
        password = 'test_password'
        role = 'test_role'

        add_user(username, password, role)
        result = add_user(username, password, role)
        self.assertFalse(result)

    def test_retrieve_user_entry_existing(self):
        username = 'test_user'
        password = 'test_password'
        role = 'test_role'

        add_user(username, password, role)
        entry = retrieve_user_entry(username)
        expected_entry = f"{username}:{password}:{role}\n"
        self.assertEqual(entry, expected_entry)

    def test_retrieve_user_entry_non_existing(self):
        username = 'non_existing_user'

        entry = retrieve_user_entry(username)
        self.assertIsNone(entry)

    def test_retrieve_user_existing(self):
        username = 'test_user'
        password = 'test_password'
        role = 'test_role'

        add_user(username, password, role)
        user = retrieve_user(username)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, username)
        self.assertEqual(user.hashed_password, password)
        self.assertEqual(user.role, role)

    def test_retrieve_user_non_existing(self):
        username = 'non_existing_user'

        user = retrieve_user(username)
        self.assertIsNone(user)

    def test_user_class(self):
        username = 'test_user'
        password = 'test_password'
        role = 'test_role'

        user = User(username, password, role)
        self.assertEqual(user.username, username)
        self.assertEqual(user.hashed_password, password)
        self.assertEqual(user.role, role)

        new_role = 'new_test_role'
        user.set_role(new_role)
        self.assertEqual(user.role, new_role)

if __name__ == '__main__':
    unittest.main()
