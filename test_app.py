import unittest
import json
from flask import json as flask_json
from app import URLShortenerApp  # Assuming your original code is in a file named app.py

class TestURLShortenerApp(unittest.TestCase):

    def setUp(self):
        self.url_shortener_app = URLShortenerApp()
        self.app = self.url_shortener_app.app.test_client()

    def test_is_valid_url(self):
        """
        Test the is_valid_url method with valid and invalid URLs.
        """
        self.assertTrue(self.url_shortener_app.is_valid_url('https://www.google.com'))
        self.assertTrue(self.url_shortener_app.is_valid_url('https://www.facebook.nl'))
        self.assertTrue(self.url_shortener_app.is_valid_url('http://localhost:5000/'))
        self.assertTrue(self.url_shortener_app.is_valid_url('http://127.0.0.1:8000'))
        self.assertFalse(self.url_shortener_app.is_valid_url('google.com'))
        self.assertFalse(self.url_shortener_app.is_valid_url('ftp://example.com'))
        self.assertFalse(self.url_shortener_app.is_valid_url('http://example.com/path with spaces'))
        self.assertFalse(self.url_shortener_app.is_valid_url('http://examplecom/'))

    def test_generate_unique_id(self):
        """
        Test the generate_unique_id method to ensure it generates unique IDs with the correct length.
        """
        # Create a set to store generated IDs and check for duplicates
        generated_ids = set()

        # Generate 100 IDs and check that each one is unique and has the correct length
        for _ in range(100):
            new_id = self.url_shortener_app.generate_unique_id()
            self.assertEqual(len(new_id), 6, f"Generated ID '{new_id}' does not have length 6")
            self.assertNotIn(new_id, generated_ids, f"Duplicate ID generated: {new_id}")
            generated_ids.add(new_id)

    def test_create_short_url(self):
        """
        Test the creation of a short URL for a valid URL.
        """
        response = self.app.post('/', data=flask_json.dumps({'url': 'https://www.example.com'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('id', response_data)

    def test_invalid_url(self):
        """
        Test the creation of a short URL for an invalid URL.
        """
        response = self.app.post('/', data=flask_json.dumps({'url': 'invalid_url'}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_url(self):  # sourcery skip: avoid-builtin-shadow
        """
        Test updating an existing URL.
        """
        response = self.app.post('/', data=flask_json.dumps({'url': 'https://www.example.com'}), content_type='application/json')
        id = json.loads(response.data)['id']
        response = self.app.put(f'/{id}', data=flask_json.dumps({'url': 'https://www.updated-example.com'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_url(self):  # sourcery skip: avoid-builtin-shadow
        """
        Test deleting a URL by its ID.
        """
        response = self.app.post('/', data=flask_json.dumps({'url': 'https://www.example.com'}), content_type='application/json')
        id = json.loads(response.data)['id']
        response = self.app.delete(f'/{id}')
        self.assertEqual(response.status_code, 204)

    def test_get_all_keys(self):
        """
        Test getting all stored URL identifiers.
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_unsupported_delete(self):
        """
        Test an unsupported DELETE request without an identifier.
        """
        response = self.app.delete('/')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()