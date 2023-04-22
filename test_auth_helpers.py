import unittest
from auth_helpers import hash_password, is_password_strong, is_username_valid, JWT_SECRET, base64url_encode, base64url_decode, jwt_decode, jwt_encode
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
        Test if method correctly encodes data using base64.
        """

        # Create a bytes object to encode and to be tested
        data = b'data to test'  

        # Generate expected result using urlsafe_b64encode() to encode data, remove any trailing equal signs
        expected_encoded_data = base64.urlsafe_b64encode(data).rstrip(b'=')

        # Execute the function to be tested
        encoded_data = base64url_encode(data)  

        self.assertEqual(encoded_data, expected_encoded_data) 

    def test_base64url_decode(self):

        """
        Test if method correctly decodes data using base64.
        """

        # Create a bytes object to encode and to be tested
        data = b'data to test'  

        # Generate the encoded data
        encoded_data = base64.urlsafe_b64encode(data).rstrip(b'=')

        # Generate the expected decoded data
        expected_decoded_data = base64.urlsafe_b64decode(encoded_data + b'=' * (4 - len(encoded_data) % 4))

        # Call the function which we test
        decoded_data = base64url_decode(encoded_data)  

        self.assertEqual(decoded_data, expected_decoded_data)

    def test_jwt_encode_decode_valid(self):

        """
        Test if both methods with a valid secret successfully encodes/decodes a JWT.
        """
        
        header = {"typ": "JWT", "alg": "HS256"} # JWT header
        payload = {"user_id": 1, "role": "admin"} # JWT payload
        secret = "my_secret_key" # Secret for encoding and decoding

        token = jwt_encode(header, payload, secret) # Execute method to generate token
        decoded_payload = jwt_decode(token, secret) # Execute method to decode generated token

        # Assert decoded payload is not None and matches original payload
        self.assertIsNotNone(decoded_payload)
        self.assertEqual(decoded_payload, payload)

    def test_jwt_encode_decode_invalid(self):

        """"
        Test if both methods with a invalid secret unsuccessfully encodes/decodes a JWT.
        """

        header = {"typ": "JWT", "alg": "HS256"} # JWT header
        payload = {"user_id": 1, "role": "admin"} # JWT payload
        secret = "my_secret_key" # Valid secret for encoding and decoding
        invalid_secret = "invalid_secret_key" # Invalid secret for decoding

        token = jwt_encode(header, payload, secret)  # Execute method to generate the token
        decoded_payload = jwt_decode(token, invalid_secret) # Execute method to decode the token with invalid secret

        # Assert decoded payload is None because invalid secret
        self.assertIsNone(decoded_payload)

if __name__ == '__main__':
    unittest.main()
