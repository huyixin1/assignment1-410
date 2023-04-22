import unittest
from unittest.mock import MagicMock
from flask import json
from auth import AuthService
from app import URLShortenerApp

class TestURLShortenerApp(unittest.TestCase):

    def setUp(self):

        """
        Initializes AuthService and URLShortenerApp objects for test cases.
        Also initializes an Flask test client instance.
        """

        self.auth_service = AuthService(None)
        self.auth_service.validate_jwt = MagicMock(return_value={"role": "admin"})
        self.url_shortener_app = URLShortenerApp(self.auth_service)
        self.app = self.url_shortener_app.app.test_client()

        self.urls = [
            "https://www.facebook.com",
            "https://www.google.com",
            "https://www.github.com",
        ]

    def test_create_short_url(self):

        """
        Checks if method properly generates short URLs for a list of specified URLs.
        Verify if the response status code is 201 for each request.
        """

        headers = {"Authorization": "Bearer test_token"}

        for url in self.urls:

            data = {"url": url}
            response = self.app.post("/", headers=headers, data=json.dumps(data), content_type="application/json")
            self.assertEqual(response.status_code, 201)

    def test_redirect_url(self):

        """
        Checks if method accurately redirects short URLs to original URLs.
        Validate if the response status code is 301 for each request.
        """

        headers = {"Authorization": "Bearer test_token"}

        for url in self.urls:

            data = {"url": url}
            response = self.app.post("/", headers=headers, data=json.dumps(data), content_type="application/json")
            self.assertEqual(response.status_code, 201)

            response_data = json.loads(response.get_data(as_text=True))
            generated_uri = response_data["generated_uri"]
            response = self.app.get(f"/{generated_uri}", headers=headers)
            self.assertEqual(response.status_code, 301)

    def test_update_url(self):

        """
        Checks if method accurately updates the original URL corresponding to a short URL.
        Verify if the response status code is 200 for each request.
        """

        headers = {"Authorization": "Bearer test_token"}

        for url in self.urls:

            data = {"url": url}
            response = self.app.post("/", headers=headers, data=json.dumps(data), content_type="application/json")
            self.assertEqual(response.status_code, 201)

            response_data = json.loads(response.get_data(as_text=True))
            generated_uri = response_data["generated_uri"]
            new_url = f"{url}/update"
            data = {"url": new_url}
            response = self.app.put(f"/{generated_uri}", headers=headers, data=json.dumps(data), content_type="application/json")
            self.assertEqual(response.status_code, 200)

    def test_delete_url(self):

        """
        Tests if the method correctly deletes short URLs and their corresponding original URLs.
        Validate if the response status code is 204 for each request.
        """

        headers = {"Authorization": "Bearer test_token"}

        for url in self.urls:

            data = {"url": url}
            response = self.app.post("/", headers=headers, data=json.dumps(data), content_type="application/json")
            self.assertEqual(response.status_code, 201)

            response_data = json.loads(response.get_data(as_text=True))
            generated_uri = response_data["generated_uri"]
            response = self.app.delete(f"/{generated_uri}", headers=headers)
            self.assertEqual(response.status_code, 204)

    def test_get_all_keys(self):

        """
        Tests if the method correctly retrieves all short URLs in the dictionary.
        Validate if the response status code is 200.
        """

        headers = {"Authorization": "Bearer test_token"}

        # First, we create short URLs
        for url in self.urls:
            data = {"url": url}
            response = self.app.post("/", headers=headers, data=json.dumps(data), content_type="application/json")
            self.assertEqual(response.status_code, 201)

        # Test get_all_keys
        response = self.app.get("/keys", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_search_uri(self):

        """
        Tests if the method correctly searches short URLs in the dictionary.
        Validate if the response status code is 200 for each request.
        """

        headers = {"Authorization": "Bearer test_token"}

        for url in self.urls:

            data = {"url": url}
            response = self.app.post("/", headers=headers, data=json.dumps(data), content_type="application/json")
            self.assertEqual(response.status_code, 201)

            response_data = json.loads(response.get_data(as_text=True))
            generated_uri = response_data["generated_uri"]
            response = self.app.get(f"/search/{generated_uri}", headers=headers)
            self.assertEqual(response.status_code, 200)

    def test_create_short_url_invalid_url(self):

        """
        Testing the functionality when trying to create a short URL with an invalid URL.
        Check if the response status code is 400.
        """

        headers = {"Authorization": "Bearer test_token"}
        data = {"url": "invalid_url"}
        response = self.app.post("/", headers=headers, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_redirect_url_not_found(self):

        """
        Testing the functionality when trying to redirect a nonexistent short URL.
        Check if the response status code is 404.
        """

        headers = {"Authorization": "Bearer test_token"}
        response = self.app.get("/nonexistent", headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_update_url_invalid_url(self):

        """
        Test the functionality when trying to update a short URL with an invalid URL.
        Check if the response status code is 400.
        """

        headers = {"Authorization": "Bearer test_token"}
        data = {"url": "https://www.example.com"}
        response = self.app.post("/", headers=headers, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

        response_data = json.loads(response.get_data(as_text=True))
        generated_uri = response_data["generated_uri"]
        data = {"url": "invalid_url"}
        response = self.app.put(f"/{generated_uri}", headers=headers, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_delete_url_not_found(self):

        """
        Testing the functionality when trying to delete a non-existent short URL.
        Check if the response status code is 404.
        """

        headers = {"Authorization": "Bearer test_token"}
        response = self.app.delete("/nonexistent", headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_serve_index(self):

        """
        Testing the functionality serving of the application's index page.
        Check if the response status code is 200.
        """

        headers = {"Authorization": "Bearer test_token"}
        response = self.app.get("/", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_unsupported_delete(self):

        """
        Testing the functionality when trying an unsupported DELETE request on the root endpoint.
        Check if the response status code is 404.
        """

        headers = {"Authorization": "Bearer test_token"}
        response = self.app.delete("/", headers=headers)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()