import unittest
from auth_helpers import hash_password, is_password_strong, is_username_valid, JWT_SECRET, base64url_encode, base64url_decode
import hashlib
import base64
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
    
    def test_base64url_encode(self):

        """
        Test if method correctly encodes data.
        """

        # Create a bytes object to encode.
        data = b'data to test'  

        # Generate expected result using urlsafe_b64encode() to encode data
        # Remove any trailing equal signs
        expected_result = base64.urlsafe_b64encode(data).rstrip(b'=') 

        self.assertEqual(base64url_encode(data), expected_result) 

    def test_base64url_decode(self):

        """
        Test if method correctly decodes data.
        """

        # Create bytes object for encoding and removing any trailing equal signs
        data = base64.urlsafe_b64encode(b'test data').rstrip(b'=')

        # Generate expected result by decoding encoded data and adding padding
        expected_result = base64.urlsafe_b64decode(data + b'==')  
        self.assertEqual(base64url_decode(data), expected_result)

if __name__ == '__main__':
    unittest.main()
