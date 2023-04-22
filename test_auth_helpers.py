import unittest
from auth_helpers import hash_password, is_password_strong, is_username_valid, JWT_SECRET
import hashlib
import secrets
import hmac

class TestAuthHelperFunctions(unittest.TestCase):

    def test_hash_password(self):

        """
        Test if the hash_password method accurately hashes the given password using sha256.
        """

        password = "Str0ng_P@ssw0rd!"
        expected_hash = hmac.new(JWT_SECRET.encode('utf-8'), password.encode('utf-8'), hashlib.sha256).hexdigest()
        hashed_password = hash_password(password)

        self.assertEqual(hashed_password, expected_hash, "The hashed password should match the expected hash.")

    def test_is_password_strong(self):

        """
        Test if the is_password_strong method correctly identifies strong and weak passwords.
        """

        strong_passwords = [
            "P@$$w0rd!",
            "Str0ng_P@ssw0rd!",
            "S3cureP@$$123"
        ]

        weak_passwords = [
            "password",
            "P@ssword",
            "pass123",
            "p@ssword"
        ]

        # Test strong passwords
        for password in strong_passwords:
            self.assertTrue(is_password_strong(password), f"The password '{password}' identified as strong.")

        # Test weak passwords
        for password in weak_passwords:
            self.assertFalse(is_password_strong(password), f"The password '{password}' identified as weak.")

    def test_is_username_valid(self):

        """
        Test if the is_username_valid method correctly identifies valid and invalid usernames.
        """

        valid_usernames = [
            "user_123",
            "abcde",
            "UserName",
            "valid_1"
        ]

        invalid_usernames = [
            "user",
            "user name",
            "user@domain.com",
            "user!",
            "abc",
            "!"
        ]

        # Test valid usernames
        for username in valid_usernames:
            self.assertTrue(is_username_valid(username), f"The username '{username}' is valid.")

        # Test invalid usernames
        for username in invalid_usernames:
            self.assertFalse(is_username_valid(username), f"The username '{username}' is invalid.")

if __name__ == '__main__':
    unittest.main()
