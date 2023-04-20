import unittest
from unittest.mock import MagicMock
from flask import json
from auth import AuthService
from app import URLShortenerApp


class TestURLShortenerApp(unittest.TestCase):

    def setUp(self):
        self.auth_service = AuthService(None)
        self.auth_service.validate_jwt = MagicMock(return_value={"role": "admin"})
        self.url_shortener_app = URLShortenerApp(self.auth_service)
        self.app = self.url_shortener_app.app.test_client()

        self.urls = [
            "https://www.example.com",
            "https://www.google.com",
            "https://www.github.com",
        ]

    def test_create_short_url(self):
        headers = {"Authorization": "Bearer test_token"}

        for url in self.urls:
            data = {"url": url}
            response = self.app.post("/", headers=headers, data=json.dumps(data), content_type="application/json")
            self.assertEqual(response.status_code, 201)

    def test_redirect_url(self):
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
        headers = {"Authorization": "Bearer test_token"}

        # First, create short URLs
        for url in self.urls:
            data = {"url": url}
            response = self.app.post("/", headers=headers, data=json.dumps(data), content_type="application/json")
            self.assertEqual(response.status_code, 201)

        # Now, test get_all_keys
        response = self.app.get("/keys", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_search_uri(self):
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
        headers = {"Authorization": "Bearer test_token"}
        data = {"url": "invalid_url"}
        response = self.app.post("/", headers=headers, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_redirect_url_not_found(self):
        headers = {"Authorization": "Bearer test_token"}
        response = self.app.get("/nonexistent", headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_update_url_invalid_url(self):
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
        headers = {"Authorization": "Bearer test_token"}
        response = self.app.delete("/nonexistent", headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_serve_index(self):
        headers = {"Authorization": "Bearer test_token"}
        response = self.app.get("/", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_unsupported_delete(self):
        headers = {"Authorization": "Bearer test_token"}
        response = self.app.delete("/", headers=headers)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()