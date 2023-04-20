import unittest
from unittest.mock import MagicMock
import json
from auth import AuthService, Flask, JWT_SECRET, USER_DATA, HASH_ALGORITHM
import hashlib

class TestAuthService(unittest.TestCase):

    """
    Test class for the AuthService class.

    Each method tests a specific method or functionality of the AuthService class.
    """

    def setUp(self):

        """
        Set up the test environment by creating an instance of the Flask app, and setting it to test mode.
        Also clears the USER_DATA dictionary for the update_password method.
        """

        self.app = AuthService(Flask(__name__)).app
        self.app.testing = True
        self.client = self.app.test_client()
        USER_DATA.clear()

    def test_create_user(self):

        """
        Test the create_user method of the AuthService class.

        Assert that the method returns a 201 status code and that the hashed password is stored in USER_DATA.
        """

        response = self.client.post('/users', json={'username': 'test_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 201)

        hashed_password = hashlib.new(HASH_ALGORITHM, 'test_password'.encode('utf-8')).hexdigest()
        self.assertEqual(USER_DATA['test_user']['password'], hashed_password)

    def test_login(self):

        """
        Test the login method of the AuthService class.

        Assert that the method returns a 200 status code and that an access_token is returned in the response data.
        """

        # Create a user for testing login
        self.client.post('/users', json={'username': 'test_user', 'password': 'test_password'})

        response = self.client.post('/users/login', json={'username': 'test_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', json.loads(response.data))

    def test_update_password(self):

        """
        Test the update_password method of the AuthService class.

        Assert that the method returns a 200 status code and that the password is updated in USER_DATA.
        """

        # Create a user for testing login
        response = self.client.post('/users', json={'username': 'test_user', 'password': 'test_password'})
        response = self.client.post('/users/login', json={'username': 'test_user', 'password': 'test_password'})
        access_token = json.loads(response.data)['access_token']

        # Update the password
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.put('/users', json={'username': 'test_user', 'old_password': 'test_password', 'new_password': 'new_password'}, headers=headers)
        self.assertEqual(response.status_code, 200)

        # Test if the password has been updated
        old_hashed_password = hashlib.new(HASH_ALGORITHM, 'test_password'.encode('utf-8')).hexdigest()
        new_hashed_password = hashlib.new(HASH_ALGORITHM, 'new_password'.encode('utf-8')).hexdigest()
        self.assertNotEqual(USER_DATA['test_user']['password'], old_hashed_password)
        self.assertEqual(USER_DATA['test_user']['password'], new_hashed_password)

    def test_require_auth(self):

        """
        Test the require_auth decorator of the AuthService class.

        Test with a valid token, an invalid token, and a missing token. Assert that the decorator returns the
        expected status code in each case.
        """

        # Create a user and log in
        self.client.post('/users', json={'username': 'test_user', 'password': 'test_password'})
        login_response = self.client.post('/users/login', json={'username': 'test_user', 'password': 'test_password'})
        access_token = json.loads(login_response.data)['access_token']

        # Test with a valid token
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.put('/users', json={'username': 'test_user', 'old_password': 'test_password', 'new_password': 'new_password'}, headers=headers)
        self.assertEqual(response.status_code, 200)

        # Test with an invalid token
        headers = {'Authorization': 'Bearer invalid_token'}
        response = self.client.put('/users', json={'username': 'test_user', 'old_password': 'test_password', 'new_password': 'new_password'}, headers=headers)
        self.assertEqual(response.status_code, 401)

        # Test with a missing token
        response = self.client.put('/users', json={'username': 'test_user', 'old_password': 'test_password', 'new_password': 'new_password'})
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()