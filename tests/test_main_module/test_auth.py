import unittest
from flask import json
from main_modules.auth import AuthService
from flask import Flask

class TestAuthService(unittest.TestCase):

    def setUp(self):
        self.app = AuthService(Flask(__name__))
        self.client = self.app.app.test_client()

    def test_create_user(self):

        """"
        Test the creation of a username, strong password, and regular role. 
        """

        response = self.client.post('/users', json={'username': 'test_user', 'password': 'Str3ngP4ss1!', 'role': 'regular'})
        self.assertEqual(response.status_code, 201)

    def test_create_user_existing_user(self):

        """
        Test the creation of an existing username.
        """

        self.client.post('/users', json={'username': 'test_user', 'password': 'Str3ngP4ss1!', 'role': 'regular'})
        response = self.client.post('/users', json={'username': 'test_user', 'password': 'AnotherPass1', 'role': 'regular'})
        self.assertEqual(response.status_code, 409)

    def test_login(self):

        """
        Test the login functionality.
        """        

        self.client.post('/users', json={'username': 'test_user', 'password': 'Str3ngP4ss1!', 'role': 'regular'})
        response = self.client.post('/users/login', json={'username': 'test_user', 'password': 'Str3ngP4ss1!'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)

    def test_update_password(self):

        """
        Test the updating of a user password.
        """

        self.client.post('/users', json={'username': 'test_user', 'password': 'Str3ngP4ss1!', 'role': 'regular'})
        login_response = self.client.post('/users/login', json={'username': 'test_user', 'password': 'Str3ngP4ss1!'})
        access_token = json.loads(login_response.data)['access_token']

        response = self.client.put('/users', json={'username': 'test_user', 'old_password': 'Str3ngP4ss1!', 'new_password': 'Str3ngP4ss1!'},
                                   headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)

    def test_update_password_wrong_old_password(self):

        """
        Test the updating of a new user password with a invalid old password.
        """

        self.client.post('/users', json={'username': 'test_user', 'password': 'Str3ngP4ss1!', 'role': 'regular'})
        login_response = self.client.post('/users/login', json={'username': 'test_user', 'password': 'Str3ngP4ss1!'})
        access_token = json.loads(login_response.data)['access_token']

        response = self.client.put('/users', json={'username': 'test_user', 'old_password': 'WrongPass1', 'new_password': 'Str3ngP4ss1!'},
                                   headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 403)

    def test_update_password_missing_authorization(self):

        "Test updating the password of a user without authorization."

        self.client.post('/users', json={'username': 'test_user', 'password': 'Str3ngP4ss1!', 'role': 'regular'})
        response = self.client.put('/users', json={'username': 'test_user', 'old_password': 'Str3ngP4ss1!', 'new_password': 'Str3ngP4ss1!'})
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()