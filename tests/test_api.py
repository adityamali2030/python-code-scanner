import unittest

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestAPI(unittest.TestCase):

    def test_health(self):
        response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_valid_code(self):
        response = client.post(
            "/analyze",
            json={"code": "def greet():\n    return 'Hello'\n"},
        )

        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result["valid_syntax"])
        self.assertEqual(result["summary"]["function_count"], 1)

    def test_invalid_syntax(self):
        response = client.post(
            "/analyze",
            json={"code": "def broken(:"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["valid_syntax"])

    def test_empty_code(self):
        response = client.post("/analyze", json={"code": ""})

        self.assertEqual(response.status_code, 422)

    def test_whitespace_code(self):
        response = client.post("/analyze", json={"code": "   "})

        self.assertEqual(response.status_code, 422)

    def test_missing_code(self):
        response = client.post("/analyze", json={})

        self.assertEqual(response.status_code, 422)

    def test_oversized_code(self):
        response = client.post(
            "/analyze",
            json={"code": "x" * 50_001},
        )

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()