import re
import hashlib
import re
import json
import hmac
import os
import base64
import secrets
from datetime import datetime, timedelta, timezone

# Get the password secret from environment variable, or generate to hash password
PASSWORD_SECRET = os.environ.get("PASSWORD_SECRET", secrets.token_urlsafe(64))

# Set expiration date JWT_token
DAYS_EXPIRE = 1

def generate_jwt_token(username, role, secret_key):

    """
    
    Generates a JWT token for a user with the given username and role, using the provided secret key.

    The `payload` dictionary includes a `datetime` object with an expiration time for the token that is one day in the future. 
    The `timezone` module is used to create a `timezone.utc` object that represents the (UTC) timezone, and the `timedelta` function is used to add one day to the current time to generate the expiration time for the token. 
    This ensures that the token expires after a certain amount of time, providing an additional layer of security to the authentication process.

    Args:
        username (str): The username of the user.
        role (str): The role of the user.
        secret_key (str): The secret key used for JWT token encoding.

    Returns:
        str: A JWT token.

    """
    payload = {
        'sub': username,
        'role': role,
        'exp': int((datetime.now(timezone.utc) + timedelta(days=DAYS_EXPIRE)).timestamp()) # JWT_token expires X day from creation
    }
    return jwt_encode({"alg": "HS256", "typ": "JWT"}, payload, secret_key) # return JWT_token

def hash_password(password):

    """
    Hashes the given password using the specified sha256 algorithm.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password in hexadecimal format.
    """

    return hmac.new(PASSWORD_SECRET.encode('utf-8'), password.encode('utf-8'), hashlib.sha256).hexdigest()

def is_password_strong(password):

    """
    Validates the strength of the provided password.

    Args:
        password (str): The password to be validated.

    Returns:
        bool: True if the password is strong, False otherwise.
    """

    if len(password) < 8:
        return False

    if not re.search('[a-z]', password):
        return False

    if not re.search('[A-Z]', password):
        return False

    if not re.search('[0-9]', password):
        return False

    return True


def is_username_valid(username):

    """
    Check if a username satisfies to specified rules.
    
    Args:
        username (str): The username to validate.
        
    Returns:
        bool: True if the username is valid, False otherwise.
    """
    # At least 5 characters long
    if len(username) < 5:
        return False
    
    # Only alphanumeric characters and underscores
    if not re.match(r'^[\w_]+$', username):
        return False

    return True

def base64url_encode(self):

    """
    Encodes the given data using the URL-safe Base64 encoding.

    Args:
        self (bytes): The data to be encoded.

    Returns:
        bytes: The URL-safe Base64-encoded data with trailing padding removed.
    """

    return base64.urlsafe_b64encode(self).rstrip(b'=')

def jwt_encode(self, payload, secret, algorithm='HS256'):

    """
    Encodes the given payload as a JSON Web Token (JWT) using the specified secret and algorithm.

    Args:
        self (dict): The JWT header.
        payload (dict): The JWT payload.
        secret (str): The secret used to sign the JWT.
        algorithm (str, optional): The signing algorithm. Defaults to 'HS256'.

    Returns:
        str: The encoded and signed JWT.
    """

    # Encode the JWT header using URL-safe Base64 encoding
    encoded_header = base64url_encode(json.dumps(self).encode('utf-8'))

    # Encode the JWT payload using URL-safe Base64 encoding
    encoded_payload = base64url_encode(json.dumps(payload).encode('utf-8'))

    # Concatenate the encoded header and payload with a period separator
    message = f'{encoded_header.decode("utf-8")}.{encoded_payload.decode("utf-8")}'

    # Create the signature using the secret and the HMAC-SHA256 algorithm
    signature = hmac.new(secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()

    # Encode the signature using URL-safe Base64 encoding
    encoded_signature = base64url_encode(signature)

    # Return the encoded and signed JWT
    return f'{message}.{encoded_signature.decode("utf-8")}'
    
def base64url_decode(self):

    """
    Decodes the given data using the URL-safe Base64 encoding.

    Args:
        self (bytes): The data to be decoded.

    Returns:
        bytes: The decoded data with necessary padding added.
    """

    # Add necessary padding to the input data
    padding = b'=' * (4 - len(self) % 4)

    return base64.urlsafe_b64decode(self + padding)

def jwt_decode(token, secret):

    """
    Decodes the given JSON Web Token (JWT) using the specified secret.

    Args:
        token (str): The JWT to be decoded.
        secret (str): The secret used to verify the JWT.

    Returns:
        dict or None: The decoded payload if the JWT is valid, otherwise None.
    """


    # Split the input token into its components (header, payload, signature)
    header_str, payload_str, signature_str = token.split('.')

    # Decode the header and payload using URL-safe Base64 encoding
    header = json.loads(base64url_decode(header_str.encode('utf-8')).decode('utf-8'))
    payload = json.loads(base64url_decode(payload_str.encode('utf-8')).decode('utf-8'))

    # Decode the signature using URL-safe Base64 encoding
    signature = base64url_decode(signature_str.encode('utf-8'))

    # Concatenate the header and payload strings with a period separator
    message = f'{header_str}.{payload_str}'

    # Compute the expected signature using the secret and HMAC-SHA256 algorithm
    expected_signature = hmac.new(secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()

    # Compare the input signature with the expected signature
    if not hmac.compare_digest(signature, expected_signature):
        return None
    else:
        return payload
