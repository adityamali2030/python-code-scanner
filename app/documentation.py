from app.analyzer import analyze_code


def generate_documentation(code: str) -> str:
    """Generate a plain Markdown report from Python code structure."""
    result = analyze_code(code)

    if not result["valid_syntax"]:
        error = result["syntax_error"]
        return (
            "# Code Analysis Report\n\n"
            "Python syntax is invalid.\n\n"
            f"- Line: {error['line']}\n"
            f"- Column: {error['column']}\n"
            f"- Error: {error['message']}\n"
        )

    summary = result["summary"]
    lines = [
        "# Code Analysis Report",
        "",
        "Generated from static analysis; code was not executed.",
        "",
        "## Overview",
        f"- Lines: {result['line_count']}",
        f"- Functions and methods: {summary['function_count']}",
        f"- Classes: {summary['class_count']}",
        f"- Import statements: {summary['import_statement_count']}",
        "",
        "## Module Docstring",
        result["module_docstring"] or "No module docstring provided.",
        "",
        "## Functions and Methods",
    ]

    for function in result["functions"]:
        kind = "Async function" if function["is_async"] else "Function"
        lines.extend([
            "",
            f"### {function['name']}",
            f"- Type: {kind}",
            f"- Line: {function['line']}",
            "- Docstring:",
            function["docstring"] or "No docstring provided.",
        ])

    if not result["functions"]:
        lines.append("No functions found.")

    lines.extend(["", "## Classes"])

    for class_info in result["classes"]:
        lines.extend([
            "",
            f"### {class_info['name']}",
            f"- Line: {class_info['line']}",
            "- Docstring:",
            class_info["docstring"] or "No docstring provided.",
        ])

    if not result["classes"]:
        lines.append("No classes found.")

    return "\n".join(lines) + "\n"