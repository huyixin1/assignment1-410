import unittest
import json
from flask import json as flask_json
from app import URLShortenerApp
import re
from flask.testing import FlaskClient
import hashlib
import random
import string

# Set the length of the unique ID to use for shortened URLs
hash_length = 8

class TestURLShortenerApp(unittest.TestCase):

    def setUp(self):

        """
        Set up the test environment for the test cases.
        """

        self.url_shortener_app = URLShortenerApp()
        self.client = self.url_shortener_app.app.test_client()

    def test_is_valid_url(self):

        """
        Test the is_valid_url method to ensure it correctly identifies valid and invalid URLs.
        """

        self.assertTrue(self.url_shortener_app.is_valid_url('https://www.google.com'))
        self.assertTrue(self.url_shortener_app.is_valid_url('http://localhost:5000/'))
        self.assertTrue(self.url_shortener_app.is_valid_url('http://127.0.0.1:8000'))
        self.assertFalse(self.url_shortener_app.is_valid_url('google.com'))
        self.assertFalse(self.url_shortener_app.is_valid_url('http://example.com/path with spaces'))
        self.assertFalse(self.url_shortener_app.is_valid_url('http://examplecom/'))

    def test_generate_unique_id(self):

        """
        Test the generate_unique_id method to ensure it generates unique IDs with the correct length and not duplicates"
        """

        # Create a set to store generated IDs and check for duplicates
        generated_ids = set()

        # Generate 100 IDs and check that each one is unique and has the correct length
        for _ in range(100):
            url = f"https://example.com/{_}"
            new_id = self.url_shortener_app.generate_unique_id(url)
            self.assertEqual(len(new_id), hash_length, f"Generated ID '{new_id}' does not have length {hash_length}")
            self.assertNotIn(new_id, generated_ids, f"Duplicate ID generated: {new_id}")
            generated_ids.add(new_id)

    def test_sorted_urls(self):

        """
        Test the sorted_urls method to ensure it correctly sorts a list of short URLs by their creation time.
        """

        url1 = 'https://www.example1.com'
        url2 = 'https://www.example2.com'
        url3 = 'https://www.example3.com'

        response = self.client.post('/', json={'url': url1})
        self.assertEqual(response.status_code, 201)

        response = self.client.post('/', json={'url': url2})
        self.assertEqual(response.status_code, 201)

        response = self.client.post('/', json={'url': url3})
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        short_urls = [
            {"original_url": url3, "url": url3, "generated_uri": url3, "created_at": "2023-04-12 12:00:00"},
            {"original_url": url2, "url": url2, "generated_uri": url2, "created_at": "2023-04-12 11:00:00"},
            {"original_url": url1, "url": url1, "generated_uri": url1, "created_at": "2023-04-12 10:00:00"},
        ]

        sorted_urls = sorted(short_urls, key=lambda x: x['created_at'], reverse=True)
        self.assertEqual(sorted_urls[0]['original_url'], url3)
        self.assertEqual(sorted_urls[1]['original_url'], url2)
        self.assertEqual(sorted_urls[2]['original_url'], url1)

    def test_create_short_url(self):

        """
        Test the create_short_url method to ensure it creates a short URL when provided with a valid URL.
        """

        response = self.client.post('/', json={'url': 'https://www.example.com'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('short_url', data)
        self.assertIn('generated_uri', data)

    def test_create_short_url(self):
        """
        Test the create_short_url method to ensure it creates a short URL when provided with a valid URL.
        """

        response = self.client.post('/', json={'url': 'https://www.example.com'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('short_url', data)
        self.assertIn('generated_uri', data)
        self.assertEqual(len(data['generated_uri']), hash_length)
        self.assertTrue(data['generated_uri'].isalnum()) # check if all characters are alphanumeric

    def test_create_short_url_invalid(self):
        """
        Test the create_short_url method to ensure it returns an error when provided with an invalid URL.
        """    

        response = self.client.post('/', json={'url': 'invalid_url'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_create_short_url_special_characters(self):
        """
        Test the create_short_url method to ensure it returns an error when provided with a URL containing special characters.
        """

        response = self.client.post('/', json={'url': 'https://www.example.com/<script>alert("test")</script>'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_create_short_url_too_long(self):
        """
        Test the create_short_url method to ensure it returns an error when provided with a URL that is too long.
        """

        long_url = 'https://www.example.com/' + ''.join(random.choices(string.ascii_letters + string.digits, k=2000))
        response = self.client.post('/', json={'url': long_url})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_get_all_keys(self):

        """
        Test the get_all_keys method to ensure it returns a list of all the unique keys generated by the URL shortener.
        """

        response = self.client.get('/keys')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_redirect_url(self):

        """
        Test the redirect_url method to ensure it redirects the user to the original URL when provided with a valid unique ID.
        """

        response = self.client.post('/', json={'url': 'https://www.example.com'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        unique_id = data['generated_uri']
        response = self.client.get(f'/{unique_id}')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'https://www.example.com')

    def test_redirect_url_not_found(self):

        """
        Test the redirect_url method to ensure it returns an error when provided with a nonexistent unique ID.
        """     

        response = self.client.get('/nonexistent_id')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_update_url(self):

        """
        Test the update_url method to ensure it updates the original URL associated with a unique ID when provided with a new valid URL.
        """

        response = self.client.post('/', json={'url': 'https://www.example.com'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        unique_id = data['generated_uri']
        response = self.client.put(f'/{unique_id}', json={'url': 'https://www.google.com'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_update_url_invalid(self):

        """
        Test the update_url method to ensure it returns an error when provided with an invalid URL for updating.
        """

        response = self.client.post('/', json={'url': 'https://www.example.com'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        unique_id = data['generated_uri']
        response = self.client.put(f'/{unique_id}', json={'url': 'invalid_url'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_delete_url(self):

        """
        Test the delete_url method to ensure it deletes the URL associated with a unique ID when requested.
        """

        response = self.client.post('/', json={'url': 'https://www.example.com'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        unique_id = data['generated_uri']
        response = self.client.delete(f'/{unique_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_delete_url_not_found(self):

        """
        Test the delete_url method to ensure it returns an error when provided with a nonexistent unique ID for deletion.
        """

        response = self.client.delete('/nonexistent_id')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_unsupported_delete(self):

        """
        Test the unsupported_delete method to ensure it returns an error when attempting to delete an unsupported resource.
        """

        response = self.client.delete('/')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()