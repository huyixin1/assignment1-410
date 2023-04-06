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
        
@app.route('/<string:id>', methods=['PUT'])
def update_url(id):
     
    """
    Update the URL associated with the given ID.

    Parameters:
    id (str): The ID of the URL to update.

    Returns:
    response (json): A JSON response containing a message or error.
    """

    if id not in url_data:
        return jsonify({'error': 'Not Found'}), 404
    data = request.get_json()
    url = data.get('url')
    if url is not None and is_valid_url(url):
        url_data[id] = url
        return jsonify({'message': 'Updated'}), 200
    else:
        return jsonify({'error': 'Invalid URL'}), 400

@app.route('/<string:id>', methods=['DELETE'])
def delete_url(id):

    """
    Delete the URL associated with the given ID.

    Parameters:
    id (str): The ID of the URL to delete.

    Returns:
    response (json): A JSON response containing a message or error.
    """

    if id not in url_data:
        return jsonify({'error': 'Not Found'}), 404
    del url_data[id]
    return jsonify({'message': 'Deleted'}), 204

@app.route('/', methods=['GET'])
def get_all_keys():

    """
    Retrieve all stored URL identifiers.

    Returns:
    response (json): A JSON response containing a list of URL identifiers.
    """

    return jsonify(list(url_data.keys())), 200

@app.route('/', methods=['POST'])
def create_short_url():

    """
    Create a short URL for the given long URL.

    Returns:
    response (json): A JSON response containing the short URL identifier or an error message.
    """

    data = request.get_json()
    url = data.get('url')
    if url is not None and is_valid_url(url):
        unique_id = generate_unique_id()
        url_data[unique_id] = url
        return jsonify({'id': unique_id}), 201
    else:
        return jsonify({'error': 'Invalid URL'}), 400

@app.route('/', methods=['DELETE'])
def unsupported_delete():

    """
    Handle unsupported DELETE requests without an identifier.

    Returns:
    response (json): A JSON response containing an error message.
    """

    return jsonify({'error': 'Method not supported'}), 404

        

