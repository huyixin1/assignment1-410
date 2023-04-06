from flask import Flask, request, jsonify
import re
import string
import random

class URLShortenerApp:

    """
    A URL shortening service implemented as a Flask application.

    Attributes:
        url_data (dict): A dictionary storing unique IDs and their corresponding URLs.
        app (Flask): A Flask application instance.
    """

    def __init__(self):

        """
        Initialize the URLShortenerApp instance and set up the routes.
        """

        self.url_data = {}
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):

        """
        Set up the route handlers for the Flask application.
        """

        self.app.add_url_rule('/<string:id>', 'update_url', self.update_url, methods=['PUT'])
        self.app.add_url_rule('/<string:id>', 'delete_url', self.delete_url, methods=['DELETE'])
        self.app.add_url_rule('/', 'get_all_keys', self.get_all_keys, methods=['GET'])
        self.app.add_url_rule('/', 'create_short_url', self.create_short_url, methods=['POST'])
        self.app.add_url_rule('/', 'unsupported_delete', self.unsupported_delete, methods=['DELETE'])

    def is_valid_url(self, url):

        """
        Validate the given URL using a regular expression.

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
        return bool(re.match(regex, url))

    def generate_unique_id(self):

        """
        Generate a unique six-character identifier using a combination of ASCII letters and digits.

        Returns:
            str: A six-character unique identifier.
        """

        characters = string.ascii_letters + string.digits
        while True:
            unique_id = ''.join(random.choices(characters, k=6))
            if unique_id not in self.url_data:
                return unique_id

    def update_url(self, id):

        """
        Update the URL associated with the given ID.

        Args:
            id (str): The ID of the URL to update.

        Returns:
            response (json): A JSON response containing a message or error.
        """

        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400
        url = data.get('url')
        if url is not None and self.is_valid_url(url):
            if id in self.url_data:
                self.url_data[id] = url
                return jsonify({'message': 'Updated'}), 200
            else:
                return jsonify({'error': 'Not Found'}), 404
        else:
            return jsonify({'error': 'Invalid URL'}), 400

    def delete_url(self, id):

        """
        Delete the URL associated with the given ID.

        Args:
            id (str): The ID of the URL to delete.

        Returns:
            response (json): A JSON response containing a message or error.
        """
        
        if id in self.url_data:
            del self.url_data[id]
            return jsonify({'message': 'Deleted'}), 204
        else:
            return jsonify({'error': 'Not Found'}), 404

    def get_all_keys(self):

        """
        Retrieve all stored URL identifiers.

        Returns:
            response (json): A JSON response containing a list of URL identifiers.
        """

        return jsonify(list(self.url_data.keys())), 200

    def create_short_url(self):

        """
        Create a short URL for the given long URL.

        Returns:
            response (json): A JSON response containing the short URL identifier or an error message.
        """

        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400
        url = data.get('url')
        if url is not None and self.is_valid_url(url):
            unique_id = self.generate_unique_id()
            self.url_data[unique_id] = url
            return jsonify({'id': unique_id}), 201
        else:
            return jsonify({'error': 'Invalid URL'}), 400

    def unsupported_delete(self):

        """
        Handle unsupported DELETE requests without an identifier.

        Returns:
            response (json): A JSON response containing an error message.
        """

        return jsonify({'error': 'Method not supported'}), 404

    def run(self, *args, **kwargs):

        """
        Run the Flask application with the given arguments and keyword arguments.

        Args:
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        self.app.run(*args, **kwargs)

if __name__ == '__main__':
    url_shortener_app = URLShortenerApp()