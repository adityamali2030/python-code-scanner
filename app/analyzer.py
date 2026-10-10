import ast

MAX_CODE_LENGTH = 50_000


def analyze_code(code: str) -> dict:
    """Inspect Python source code without executing it."""
    if not code.strip():
        raise ValueError("Please provide some Python code.")

    if len(code) > MAX_CODE_LENGTH:
        raise ValueError(
            f"Code must not exceed {MAX_CODE_LENGTH} characters."
        )

    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        return {
            "valid_syntax": False,
            "syntax_error": {
                "message": error.msg,
                "line": error.lineno,
                "column": error.offset,
            },
        }

    functions = []
    classes = []
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append({
                "name": node.name,
                "line": node.lineno,
                "is_async": isinstance(node, ast.AsyncFunctionDef),
                "docstring": ast.get_docstring(node),
            })

        elif isinstance(node, ast.ClassDef):
            classes.append({
                "name": node.name,
                "line": node.lineno,
                "docstring": ast.get_docstring(node),
            })

        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    "module": alias.name,
                    "alias": alias.asname,
                    "line": node.lineno,
                })

        elif isinstance(node, ast.ImportFrom):
            imports.append({
                "module": "." * node.level + (node.module or ""),
                "names": [
                    {"name": alias.name, "alias": alias.asname}
                    for alias in node.names
                ],
                "line": node.lineno,
            })

    return {
        "valid_syntax": True,
        "line_count": len(code.splitlines()),
        "module_docstring": ast.get_docstring(tree),
        "functions": sorted(functions, key=lambda item: item["line"]),
        "classes": sorted(classes, key=lambda item: item["line"]),
        "imports": sorted(imports, key=lambda item: item["line"]),
        "summary": {
            "function_count": len(functions),
            "class_count": len(classes),
            "import_statement_count": sum(
                isinstance(node, (ast.Import, ast.ImportFrom))
                for node in ast.walk(tree)
            ),
        },
    }