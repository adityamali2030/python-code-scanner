import unittest

from fastapi.testclient import TestClient

from app.documentation import generate_documentation
from app.main import app

client = TestClient(app)


class TestDocumentation(unittest.TestCase):

    def test_function_report(self):
        report = generate_documentation(
            'def greet():\n    """Return a greeting."""\n'
            '    return "Hello"\n'
        )

        self.assertIn("### greet", report)
        self.assertIn("Return a greeting.", report)

    def test_missing_docstring(self):
        report = generate_documentation("def greet():\n    pass\n")

        self.assertIn("No docstring provided.", report)

    def test_syntax_error_report(self):
        report = generate_documentation("def broken(:")

        self.assertIn("Python syntax is invalid.", report)

    def test_document_endpoint(self):
        response = client.post(
            "/document",
            json={"code": "class Example:\n    pass\n"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("### Example", response.json()["markdown"])

    def test_document_empty_input(self):
        response = client.post(
            "/document",
            json={"code": "   "},
        )

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()