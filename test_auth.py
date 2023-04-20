import unittest
from unittest.mock import MagicMock
import json
from auth import AuthService, Flask, JWT_SECRET, USER_DATA, HASH_ALGORITHM
import hashlib

class TestAuthService(unittest.TestCase):

    def setUp(self):
        self.app = AuthService(Flask(__name__)).app
        self.app.testing = True
        self.client = self.app.test_client()
        USER_DATA.clear()

    def test_create_user(self):
        response = self.client.post('/users', json={'username': 'test_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 201)

        hashed_password = hashlib.new(HASH_ALGORITHM, 'test_password'.encode('utf-8')).hexdigest()
        self.assertEqual(USER_DATA['test_user']['password'], hashed_password)

    def test_login(self):
        # Create a user for testing login
        self.client.post('/users', json={'username': 'test_user', 'password': 'test_password'})

        response = self.client.post('/users/login', json={'username': 'test_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', json.loads(response.data))

    def test_update_password(self):
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
        # Create a user and log in
        self.client.post('/users', json={'username': 'test_user', 'password': 'test_password'})
        login_response = self.client.post('/users/login', json={'username': 'test_user', 'password': 'test_password'})
        access_token = json.loads(login_response.data)['access_token']

        # Test with a valid token
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.put('/users', json={'username': 'test_user', 'old_password': 'test_password', 'new_password': 'new_password'}, headers=headers)
        self.assertEqual(response.status_code, 200)

        # Test with an invalid token
        headers = {'Authorization': f'Bearer invalid_token'}
        response = self.client.put('/users', json={'username': 'test_user', 'old_password': 'test_password', 'new_password': 'new_password'}, headers=headers)
        self.assertEqual(response.status_code, 401)

        # Test with a missing token
        response = self.client.put('/users', json={'username': 'test_user', 'old_password': 'test_password', 'new_password': 'new_password'})
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()