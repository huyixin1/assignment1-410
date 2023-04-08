from flask import Flask, request, jsonify, render_template, redirect
import re
import string
import random
from datetime import datetime
import os
from urllib.parse import urlparse

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")

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
        self.app.add_url_rule('/<string:id>', 'redirect_url', self.redirect_url, methods=['GET'])
        self.app.add_url_rule('/', 'serve_index', self.serve_index, methods=['GET'])
        self.app.add_url_rule('/<string:id>', 'update_url', self.update_url, methods=['PUT'])
        self.app.add_url_rule('/<string:id>', 'delete_url', self.delete_url, methods=['DELETE'])
        self.app.add_url_rule('/keys', 'get_all_keys', self.get_all_keys, methods=['GET'])
        self.app.add_url_rule('/', 'create_short_url', self.create_short_url, methods=['POST'])
        self.app.add_url_rule('/', 'unsupported_delete', self.unsupported_delete, methods=['DELETE'])

    def redirect_url(self, id):
        """
        Redirect the user to the original URL associated with the given ID.
        Args:
            id (str): The unique identifier of the shortened URL.
        Returns:
            response (redirect): A redirect response to the original URL if found,
                                a JSON response with an error message otherwise.
        """
        if id in self.url_data:
            return redirect(self.url_data[id]['url'])
        else:
            return jsonify({"error": "URL not found"}), 404

    def serve_index(self):
        """
        Retrieve all stored URLs.
        Returns:
            response (json): A JSON response containing a dictionary of all URLs.
        """
        short_urls = [
            {"id": key, "url": f"{BASE_URL}/{key}", "created_at": self.url_data[key]["created_at"], "original_url": self.url_data[key]["url"]}
            for key in self.url_data
        ]
        short_urls = sorted(short_urls, key=lambda x: x['created_at'], reverse=True)
        return render_template('index.html', short_urls=short_urls)

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
            return jsonify({'message': 'Deleted'}), 200
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
        if url is None or not self.is_valid_url(url):
            return jsonify({'error': 'Invalid URL'}), 400
        if existing_id := next(
            (key for key, value in self.url_data.items() if value['url'] == url),
            None,
        ):
            # Return the existing short URL if found
            short_url = f"{BASE_URL}/{existing_id}"
        else:
            # Create a new short URL if the URL does not exist
            unique_id = self.generate_unique_id()
            self.url_data[unique_id] = {"url": url, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            short_url = f"{BASE_URL}/{unique_id}"

        return jsonify({'short_url': short_url}), 201

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
        self.app.run(debug=True, *args, **kwargs)

if __name__ == '__main__':
    url_shortener_app = URLShortenerApp()
    url_shortener_app.run()
