import unittest
from main import is_valid_url

class TestIsValidUrl(unittest.TestCase):
    
    def test_valid_urls(self):
        self.assertTrue(is_valid_url('https://www.google.com'))
        self.assertTrue(is_valid_url('http://localhost:5000/'))
        self.assertTrue(is_valid_url('http://127.0.0.1:8000'))
        
    def test_invalid_urls(self):
        self.assertFalse(is_valid_url('google.com'))
        self.assertFalse(is_valid_url('ftp://example.com'))
        self.assertFalse(is_valid_url('http://example.com/path with spaces'))
        
if __name__ == '__main__':
    unittest.main()