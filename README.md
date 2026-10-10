# Python Code Analysis and Documentation API

A Python application that inspects source-code structure and generates
Markdown documentation using AST and FastAPI.

## Features
- Identify functions, methods, async functions, classes and imports
- Extract existing module, class and function docstrings
- Report Python syntax errors with line and column information
- Generate template-based Markdown documentation
- Provide REST API endpoints
- Validate empty and oversized inputs
- Include automated analyzer, API and documentation tests

## Technologies
Python, AST, FastAPI, Uvicorn and unittest.
HTTPX2 supports the API test client.

## Setup

Run from the project root:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt

## Run the API

    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

Open http://127.0.0.1:8000/docs for interactive API documentation.

## Endpoints

- GET /health: service health check
- POST /analyze: return code structure as JSON
- POST /document: return a Markdown report in a JSON response

Both POST endpoints accept:

    {"code": "def greet():\n    return 'Hello'\n"}

Invalid Python syntax is reported in the analysis or documentation.
Invalid request input returns HTTP 422.

## Run tests

    python -m unittest discover -s tests -v

The current suite contains 20 passing tests covering analysis,
input validation, documentation generation and API behavior.

## Sample
samples/example.py contains example code.
samples/example_report.md demonstrates generated documentation.

## Safety and limitations
- Submitted code is parsed, not executed.
- No AI models, paid APIs or external code-analysis services are used.
- Documentation describes detected structure and existing docstrings;
  it does not infer program behavior.
- Methods and nested functions are included in the function count.
- This is not a vulnerability scanner or a correctness checker.
- Source code and docstrings are untrusted input. Generated Markdown
  is not sanitized for safe HTML rendering.
- The 50,000-character limit is a basic safeguard, not complete
  protection against resource exhaustion.
- Intended for local development. Public deployment would require
  stronger resource limits, authentication and other safeguards.