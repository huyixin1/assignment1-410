import unittest
import string
from helpers import is_valid_url, generate_unique_id

# Set the length of the unique ID to use for shortened URLs
URI_LENGTH = 8

# Set the range of max_attempts to create a unique ID
MAX_ATTEMPTS = 100

# Set the max URL length
INTERNET_MAX_PATH_LENGTH = 2048

class TestHelperFunctions(unittest.TestCase):

    """
    A test class for the helper functions in the URL shortener app.

    Each method tests a specific method or functionality of the Helper Functions.
    """

    def test_is_valid_url(self):

        """
        Test if is_valid_url function works correctly for valid and invalid URLs.
        """

        valid_urls = [
            "https://www.example.com",
            "http://example.org",
            "https://localhost:8080",
            "http://192.168.0.1"
        ]

        invalid_urls = [
            "htp://www.example.com",
            "https://",
            "http://",
            "example.com",
            "https://<script>alert('XSS')</script>.example.com"
        ]

        for url in valid_urls:
            self.assertTrue(is_valid_url(url))

        for url in invalid_urls:
            self.assertFalse(is_valid_url(url))

        # Test case for a very long domain name
        long_domain = "https://" + "a" * 63 + "." + "b" * 63 + ".com"
        self.assertTrue(is_valid_url(long_domain))

    def test_generate_unique_id_length(self):

        """
        Test if generate_unique_id function generates a unique ID with the correct length.
        """

        url_data = set()
        unique_id = generate_unique_id(url_data)
        self.assertEqual(len(unique_id), URI_LENGTH, f"Generated ID should have a length of {URI_LENGTH}")

    def test_generate_unique_id_content(self):

        """
        Test if generate_unique_id function generates a unique ID with only ASCII letters and digits.
        """

        url_data = set()
        unique_id = generate_unique_id(url_data)
        chars = string.ascii_letters + string.digits
        for char in unique_id:
            self.assertIn(char, chars, "Generated ID should only contain ASCII letters and digits.")

    def test_sorted_urls(self):

        """
        Test if sorted function sorts short URLs correctly.
        """

        short_urls = [
            {"original_url": "https://www.example3.com", "generated_uri": "AAAAAAA3", "created_at": "2023-04-12 12:00:00"},
            {"original_url": "https://www.example2.com", "generated_uri": "AAAAAAA2", "created_at": "2023-04-12 11:00:00"},
            {"original_url": "https://www.example1.com", "generated_uri": "AAAAAAA1", "created_at": "2023-04-12 10:00:00"},
        ]

        sorted_urls = sorted(short_urls, key=lambda x: x['created_at'], reverse=True)
        self.assertEqual(sorted_urls[0]['original_url'], "https://www.example3.com")
        self.assertEqual(sorted_urls[1]['original_url'], "https://www.example2.com")
        self.assertEqual(sorted_urls[2]['original_url'], "https://www.example1.com")

    def test_is_valid_url_special_characters(self):

        """
        Test if is_valid_url function works correctly for URLs with special characters.
        """

        self.assertFalse(is_valid_url('https://www.example.com/<script>alert("test")</script>'))


if __name__ == '__main__':
    unittest.main()