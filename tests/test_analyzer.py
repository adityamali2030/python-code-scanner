import unittest

from app.analyzer import analyze_code, MAX_CODE_LENGTH


class TestAnalyzer(unittest.TestCase):

    def test_function_and_docstring(self):
        code = '''
def greet(name):
    """Return a greeting."""
    return f"Hello, {name}"
'''
        result = analyze_code(code)

        self.assertTrue(result["valid_syntax"])
        self.assertEqual(result["summary"]["function_count"], 1)
        self.assertEqual(result["functions"][0]["name"], "greet")
        self.assertEqual(
            result["functions"][0]["docstring"],
            "Return a greeting.",
        )

    def test_class_and_method(self):
        code = """
class Greeter:
    def greet(self):
        return "Hello"
"""
        result = analyze_code(code)

        self.assertEqual(result["summary"]["class_count"], 1)
        self.assertEqual(result["summary"]["function_count"], 1)

    def test_async_function(self):
        result = analyze_code("async def fetch():\n    pass\n")

        self.assertTrue(result["functions"][0]["is_async"])

    def test_imports(self):
        code = "import math, os\nfrom pathlib import Path\n"
        result = analyze_code(code)

        self.assertEqual(
            result["summary"]["import_statement_count"], 2
        )
        self.assertEqual(len(result["imports"]), 3)

    def test_syntax_error(self):
        result = analyze_code("def broken(:\n    pass")

        self.assertFalse(result["valid_syntax"])
        self.assertIn("message", result["syntax_error"])

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            analyze_code("   ")

    def test_oversized_input(self):
        with self.assertRaises(ValueError):
            analyze_code("x" * (MAX_CODE_LENGTH + 1))

    def test_code_is_not_executed(self):
        result = analyze_code(
            'raise RuntimeError("This must not execute")'
        )

        self.assertTrue(result["valid_syntax"])


if __name__ == "__main__":
    unittest.main()