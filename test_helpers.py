import unittest
import string
from helpers import is_valid_url, generate_unique_id, hash_password, is_password_strong
import hashlib

# Set the length of the unique ID to use for shortened URLs
URI_LENGTH = 8

# Set the range of max_attempts to create a unique ID
MAX_ATTEMPTS = 100

# Set the max URL length
INTERNET_MAX_PATH_LENGTH = 2048

# Specify hash algorithm
HASH_ALGORITHM = 'sha256'

class TestHelperFunctions(unittest.TestCase):

    def test_is_valid_url(self):

        """
        Testing if the is_valid_url method works correctly for the specified valid and invalid URLs.
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

        # Test valid urls
        for url in valid_urls:
            self.assertTrue(is_valid_url(url))

        # Test invalid urls
        for url in invalid_urls:
            self.assertFalse(is_valid_url(url))

        # Test case for a very long domain name
        long_domain = "https://" + "a" * 63 + "." + "b" * 63 + ".com"
        self.assertTrue(is_valid_url(long_domain))

        # Test case for special characters
        self.assertFalse(is_valid_url('https://www.example.com/<path>alert("test")</error>!'))

    def test_generate_unique_id_length(self):

        """
        Testing if the method generate_unique_id correctly generates a unique ID with the specified length.
        """

        url_data = set()
        unique_id = generate_unique_id(url_data)
        self.assertEqual(len(unique_id), URI_LENGTH, f"Generated ID should have a length of {URI_LENGTH}")

    def test_generate_unique_id_characters(self):

        """
        Testing if the generate_unique_id method generates a unique ID consisting out of only ASCII letters and digits.
        """

        url_data = set()
        unique_id = generate_unique_id(url_data)
        chars = string.ascii_letters + string.digits
        for char in unique_id:
            self.assertIn(char, chars, "Generated ID should only contain ASCII letters and digits.")

    def test_sorted_urls(self):

        """
        Testing if the function within the serve_index method sorts the short URLs correctly.
        """

        short_urls = [
            {"original_url": "https://www.example3.com", "generated_uri": "A4ABAAA3", "created_at": "2023-04-12 12:00:00"},
            {"original_url": "https://www.example2.com", "generated_uri": "AAAA4JA2", "created_at": "2022-04-01 20:12:00"},
            {"original_url": "https://www.example1.com", "generated_uri": "6ZAAJAA1", "created_at": "2023-07-20 09:30:00"}
        ]

        sorted_urls = sorted(short_urls, key=lambda x: (x['created_at'], x['generated_uri']), reverse=True)
        self.assertEqual(sorted_urls[0]['original_url'], "https://www.example1.com")
        self.assertEqual(sorted_urls[1]['original_url'], "https://www.example3.com")
        self.assertEqual(sorted_urls[2]['original_url'], "https://www.example2.com")


    def test_hash_password(self):

        """
        Testing if the hash_password method correctly hashes the given password using the specified hash algorithm.
        """

        password = "Str0ng_P@ssw0rd!"
        hashed_password = hash_password(password)
        expected_hash = hashlib.new(HASH_ALGORITHM, password.encode('utf-8')).hexdigest()

        self.assertEqual(hashed_password, expected_hash, "The hashed password should match the expected hash.")

    def test_is_password_strong(self):

        """
        Testing if the is_password_strong method correctly identifies strong and weak passwords.
        """

        strong_passwords = [
            "P@$$w0rd!",
            "Str0ng_P@ssw0rd!",
            "S3cureP@$$123"
        ]

        weak_passwords = [
            "password",
            "P@ssword",
            "pass123",
            "p@ssword"
        ]

        # Test strong passwords
        for password in strong_passwords:
            self.assertTrue(is_password_strong(password), f"The password '{password}' should be identified as strong.")

        # Test weak passwords
        for password in weak_passwords:
            self.assertFalse(is_password_strong(password), f"The password '{password}' should be identified as weak.")

if __name__ == '__main__':
    unittest.main()