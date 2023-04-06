import re
import string
import random
from flask import Flask, request, redirect, jsonify


app = Flask(__name__)
url_data = {}

def is_valid_url(url):

    """
    Validates a URL using a regular expression.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """

    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def generate_unique_id():

    """
    Generates a unique six-character identifier using a combination of ASCII letters and digits.

    Returns:
        str: A six-character unique identifier.

    Raises:
        None
    """

    characters = string.ascii_letters + string.digits
    while True:
        unique_id = ''.join(random.choices(characters, k=6))
        if unique_id not in url_data:
            return unique_id
        

