import unittest
import random
import string
from main import generate_unique_id, is_valid_url, app, url_data
from flask import jsonify, redirect


class TestApp(unittest.TestCase):

    def test_is_valid_url(self):
        self.assertTrue(is_valid_url('https://www.google.com'))
        self.assertTrue(is_valid_url('http://localhost:5000/'))
        self.assertTrue(is_valid_url('http://127.0.0.1:8000'))
        self.assertFalse(is_valid_url('google.com'))
        self.assertFalse(is_valid_url('ftp://example.com'))
        self.assertFalse(is_valid_url('http://example.com/path with spaces'))

    def test_generate_unique_id(self):
        # Create a set to store generated IDs and check for duplicates
        generated_ids = set()

        # Generate 100 IDs and check that each one is unique and has the correct length
        for _ in range(100):
            new_id = generate_unique_id()
            self.assertEqual(len(new_id), 6, f"Generated ID '{new_id}' does not have length 6")
            self.assertNotIn(new_id, generated_ids, f"Duplicate ID generated: {new_id}")
            generated_ids.add(new_id)

if __name__ == '__main__':
    unittest.main()