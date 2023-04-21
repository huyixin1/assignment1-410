import unittest
from unittest.mock import MagicMock
import json
from auth import AuthService, Flask, USER_DATA
import hashlib
from helpers import hash_password, is_password_strong

# Specify hash algorithm
HASH_ALGORITHM = 'sha256'

class TestAuthService(unittest.TestCase):

    def setUp(self):

        """
        Set up the test environment by creating an instance of the Flask app.
        The instance is set to test mode so the app can run in a controlled environment dedicated to testing.
        Also clearing the USER_DATA dictionary for the update_password method.
        """

        self.app = AuthService(Flask(__name__)).app
        self.app.testing = True
        self.client = self.app.test_client()
        USER_DATA.clear()

    def test_create_user(self):

        """
        Test if the method returns a 201 status code and that the hashed password is stored in USER_DATA.
        """

        response = self.client.post('/users', json={'username': 'test_user', 'password': 'Str6ng_P@ssword!'})
        self.assertEqual(response.status_code, 201)

        hashed_password = hashlib.new(HASH_ALGORITHM, 'Str6ng_P@ssword!'.encode('utf-8')).hexdigest()
        self.assertEqual(USER_DATA['test_user']['password'], hashed_password)

    def test_login(self):

        """
        Test if the method returns a 200 status code and that an access_token is returned in the response data.
        """

        # First, create a user for testing login
        self.client.post('/users', json={'username': 'test_user', 'password': 'Str6ng_P@ssword!'})
        response = self.client.post('/users/login', json={'username': 'test_user', 'password': 'Str6ng_P@ssword!'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', json.loads(response.data))

    def test_weak_password(self):

        """
        Test if the method returns a 400 status code when attempting to create a user with a weak password.
        """

        response = self.client.post('/users', json={'username': 'test_user', 'password': 'weak_password'})
        self.assertEqual(response.status_code, 400)

    def test_update_password(self):

        """
        Test if the method returns a 200 status code and that the password is updated in USER_DATA.
        """

        # First, create a user for testing login
        response = self.client.post('/users', json={'username': 'test_user', 'password': 'Str6ng_P@ssword!'})
        response = self.client.post('/users/login', json={'username': 'test_user', 'password': 'Str6ng_P@ssword!'})
        access_token = json.loads(response.data)['access_token']

        # Update the password
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.put('/users', json={'username': 'test_user', 'old_password': 'Str6ng_P@ssword!', 'new_password': 'new_Str6ng_P@ssword!'}, headers=headers)
        self.assertEqual(response.status_code, 200)

        # Test if the password has been updated
        old_hashed_password = hashlib.new(HASH_ALGORITHM, 'Str6ng_P@ssword!'.encode('utf-8')).hexdigest()
        new_hashed_password = hashlib.new(HASH_ALGORITHM, 'new_Str6ng_P@ssword!'.encode('utf-8')).hexdigest()
        self.assertNotEqual(USER_DATA['test_user']['password'], old_hashed_password)
        self.assertEqual(USER_DATA['test_user']['password'], new_hashed_password)

    def test_update_weak_password(self):
        
        """
        Test if the method returns a 400 status code when trying to update the user's password with a weak password.
        """

        # First, create a user for testing login
        response = self.client.post('/users', json={'username': 'test_user', 'password': 'Str6ng_P@ssword!'})
        response = self.client.post('/users/login', json={'username': 'test_user', 'password': 'Str6ng_P@ssword!'})
        access_token = json.loads(response.data)['access_token']

        # Attempt to update the password with a weak password
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.put('/users', json={'username': 'test_user', 'old_password': 'Str6ng_P@ssword!', 'new_password': 'weakpw'}, headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_require_auth(self):

        """
        Test if the decorator returns the expected status code for each case.
        Attempt with a valid token, an invalid token, and a missing token. 
        """

        # Create a user and log in
        self.client.post('/users', json={'username': 'test_user', 'password': 'Str6ng_P@ssword!'})
        login_response = self.client.post('/users/login', json={'username': 'test_user', 'password': 'Str6ng_P@ssword!'})
        access_token = json.loads(login_response.data)['access_token']

        # Test with a valid token
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.put('/users', json={'username': 'test_user', 'old_password': 'Str6ng_P@ssword!', 'new_password': 'new_Str6ng_Password'}, headers=headers)
        self.assertEqual(response.status_code, 200)

        # Test with an invalid token
        headers = {'Authorization': 'Bearer invalid_token'}
        response = self.client.put('/users', json={'username': 'test_user', 'old_password': 'Str6ng_P@ssword!', 'new_password': 'new_Str6ng_Password'}, headers=headers)
        self.assertEqual(response.status_code, 401)

        # Test with a missing token
        response = self.client.put('/users', json={'username': 'test_user', 'old_password': 'Str6ng_P@ssword!', 'new_password': 'new_Str6ng_Password'})
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()