from flask import Flask, request, jsonify
import secrets
import os
import json
from functools import wraps
from helper_modules.auth_helpers import hash_password, is_password_strong, is_username_valid, jwt_decode, generate_jwt_token

# Get the jwt secret from environment variable, or generate for jwt token
JWT_SECRET = os.environ.get("JWT_SECRET", secrets.token_urlsafe(64))

class AuthService:

    """
    A class that consists out of an authentication service that provides user creation, password updates, and login functionality
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
        self.data_file = 'user_data/user_data.json'
        self.user_data = self._load_data()
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):

        """
        Adds the authentication routes to the Flask application instance.
        """

        self.app.add_url_rule('/users', 'create_user', self.create_user, methods=['POST'])
        self.app.add_url_rule('/users', 'update_password', self.update_password, methods=['PUT'])
        self.app.add_url_rule('/users/login', 'login', self.login, methods=['POST'])

    def _load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                return json.load(file)
        else:
            return {}
        
    def _save_data(self):
        with open(self.data_file, "w") as file:
            json.dump(self.user_data, file)

    def require_auth(f):

        """
        A decorator function that provides authentication to the wrapped function.
        It checks the presence of the 'Authorization' header in the incoming request, 
        and if present, it attempts to decode and validate the JWT token in the header.
        
        Args:
            f (function): The function to be wrapped with authentication.

        Returns:
            function: The decorated function that enforces authentication.
        """

        @wraps(f)
        def decorated_function(self, *args, decoded_payload=None, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header is None:
                return jsonify({'error': 'Missing Authorization header'}), 401

            token = auth_header.split(' ')[-1]
            decoded_payload = self.validate_jwt(token)
            if decoded_payload is None:
                return jsonify({'error': 'Invalid JWT token'}), 401

            return f(self, *args, decoded_payload=decoded_payload, **kwargs)

        return decorated_function
    
    def validate_jwt(self, token):
        
        """
        Validates a JWT token and returns the decoded payload if valid.

        Args:
            token (str): The JWT token to validate.

        Returns:
            Dict or None: The decoded JWT payload if the token is valid, None otherwise.
        """

        payload = jwt_decode(token, JWT_SECRET)
        if payload is None:
            return None
        else:
            return payload

    def create_user(self):

        """
        Creates a new user with the provided username and password. 
        When a user creates an account, the password they provide is hashed and stored in a dictionary to be later used for authentication. 

        Returns:
            Tuple: A tuple containing the HTTP response and status code.
        """

        data = request.get_json()

        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400

        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'regular') # the role is 'regular' by default

        if username is None:
            return jsonify({'error': 'Username is required'}), 400
        
        if not is_username_valid(username):
            return jsonify({'error': 'Invalid username. Must be at least 5 characters long and contain only alphanumeric characters and underscores'}), 400

        if password is None:
            return jsonify({'error': 'Password is required'}), 400
        
        if not is_password_strong(password):
            return jsonify({'error': 'Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, and a digit'}), 400
        
        if role is None or role.strip() == '':
            return jsonify({'error': 'Role is required'}), 400

        if role not in ['admin', 'regular']:
            return jsonify({'error': 'Invalid role'}), 400

        if username in self.user_data:
            return jsonify({'error': 'Username already exists'}), 409

        self.user_data[username] = {
            'password': hash_password(password),
            'role': role
        }
        self._save_data()

        return '', 201

    def login(self):

        """
        Authenticates a user with the provided username and password and return the generated a JWT token.
        When a user logs in, their provided password is hashed, and the resulting hash value is compared with the stored hash value for the corresponding username. 
        If the hash values match, the user is authenticated.

        Returns:
            Tuple: A tuple containing the JSON response with the 'access_token' key, the corresponding JWT token as value, and the HTTP status code.
        """

        data = request.get_json()

        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400

        username = data.get('username')
        password = data.get('password')

        if username is None:
            return jsonify({'error': 'Username is required'}), 400
        if password is None:
            return jsonify({'error': 'Password is required'}), 400

        if username not in self.user_data:
            return jsonify({'error': 'User not found'}), 403

        stored_password = self.user_data[username]['password']
        provided_hash_password = hash_password(password)

        if stored_password != provided_hash_password:
            return jsonify({'error': 'Invalid credentials'}), 403

        # Generate JWT token
        token = generate_jwt_token(username, self.user_data[username]['role'], JWT_SECRET)

        return jsonify({'access_token': token}), 200
        
    @require_auth
    def update_password(self, decoded_payload):

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

        if username is None:
            return jsonify({'error': 'Username is required'}), 400
        
        if old_password is None:
            return jsonify({'error': 'Old password is required'}), 400
        
        if new_password is None:
            return jsonify({'error': 'New password is required'}), 400
        
        if not is_password_strong(new_password):
            return jsonify({'error': 'Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, and a digit'}), 400

        if username not in self.user_data or self.user_data[username]['password'] != hash_password(old_password):
            return jsonify({'error': 'Invalid credentials'}), 403

        self.user_data[username]['password'] = hash_password(new_password)
        self._save_data()

        return '', 200
        
    def run(self, *args, **kwargs):

        """
        Runs the Flask application.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        self.app.run(host='0.0.0.0', *args, **kwargs)
