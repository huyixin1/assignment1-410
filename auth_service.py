from flask import Flask, request, jsonify
import os
import hashlib
import jwt
from datetime import datetime, timedelta
from datetime import timezone
import os
import secrets


# Generate a random secret key to use for JWT tokens
JWT_SECRET = secrets.token_urlsafe(64)

# User Database
USER_DATA = {}

class AuthService:

    """
    A class representing an authentication service that provides user creation, password updates, and login functionality
    through a Flask application.

    Attributes:
        url_shortener_app (Flask): The Flask application instance to which the authentication routes will be added.
    """

    def __init__(self, url_shortener_app):

        """
        Initializes a new instance of the AuthService class.

        Args:
            url_shortener_app (Flask): The Flask application instance to which the authentication routes will be added.
        """

        self.url_shortener_app = url_shortener_app
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):

        """
        Adds the authentication routes to the Flask application instance.
        """

        self.app.add_url_rule('/users', 'create_user', self.create_user, methods=['POST'])
        self.app.add_url_rule('/users', 'update_password', self.update_password, methods=['PUT'])
        self.app.add_url_rule('/users/login', 'login', self.login, methods=['POST'])

    def create_user(self):

        """
        Creates a new user with the provided username and password.

        Returns:
            Tuple: A tuple containing the HTTP response and status code.
        """

        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400
        username = data.get('username')
        password = data.get('password')

        if username is None or password is None:
            return jsonify({'error': 'Username and password are required'}), 400

        if username in USER_DATA:
            return jsonify({'error': 'Username already exists'}), 409

        USER_DATA[username] = {
            'password': hashlib.sha256(password.encode('utf-8')).hexdigest()
        }

        return '', 201

    def login(self):

        """
        Authenticates a user with the provided username and password and returns a JWT token.

        Returns:
            Tuple: A tuple containing the HTTP response and status code.
        """

        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400
        username = data.get('username')
        password = data.get('password')

        if username is None or password is None:
            return jsonify({'error': 'Username and password are required'}), 400

        if username not in USER_DATA or USER_DATA[username]['password'] != hashlib.sha256(password.encode('utf-8')).hexdigest():
            return jsonify({'error': 'Invalid credentials'}), 401

        # Generate JWT token
        payload = {
            'sub': username,
            'exp': datetime.now(timezone.utc) + timedelta(days=1),
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

        return jsonify({'access_token': token}), 200
    
    def update_password(self):

        """
        Updates the password of the user with the provided username.

        Returns:
            Tuple: A tuple containing the HTTP response and status code.
        """

        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400
        username = data.get('username')
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if username is None or old_password is None or new_password is None:
            return jsonify({'error': 'Username, old password, and new password are required'}), 400

        if username not in USER_DATA or USER_DATA[username]['password'] != hashlib.sha256(old_password.encode('utf-8')).hexdigest():
            return jsonify({'error': 'Invalid credentials'}), 403

        USER_DATA[username]['password'] = hashlib.sha256(new_password.encode('utf-8')).hexdigest()

        return '', 200
    
    def validate_jwt(self, token):

        """
        Validates a JWT token and returns the decoded payload if valid.

        Args:
            token (str): The JWT token to validate.

        Returns:
            Dict or None: The decoded JWT payload if the token is valid, None otherwise.
        """

        try:
            return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return None

    def run(self, *args, **kwargs):

        """
        Runs the Flask application.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        self.app.run(*args, **kwargs)
