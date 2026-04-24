import ast
import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()

    tree = ast.parse(source_code)

    # Extract module-level docstring
    module_doc = ast.get_docstring(tree) or ""

    # Extract per-function docstrings
    func_docs = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            doc = ast.get_docstring(node)
            if doc:
                func_docs[node.name] = doc

    # Extract inline business rule comments (e.g., "# Business Logic Rule 001")
    rule_comments = re.findall(r'#\s*(Business Logic Rule[^\n]+)', source_code)

    # Detect discrepancy flags in comments (WARNING / IMPORTANT / Intentional)
    discrepancy_flags = re.findall(
        r'#\s*((?:WARNING|IMPORTANT|Intentional)[^\n]+)', source_code, re.IGNORECASE
    )

    content_parts = []
    if module_doc:
        content_parts.append(f"Module: {module_doc.strip()}")
    for fname, doc in func_docs.items():
        content_parts.append(f"[{fname}] {doc.strip()}")
    if rule_comments:
        content_parts.append("Rules: " + " | ".join(rule_comments))

    content = " || ".join(content_parts)

    return {
        "document_id": "code-legacy-pipeline-001",
        "content": content,
        "source_type": "Code",
        "author": "Senior Dev (retired)",
        "timestamp": None,
        "source_metadata": {
            "filename": "legacy_pipeline.py",
            "functions_with_docstrings": list(func_docs.keys()),
            "business_rules": rule_comments,
            "discrepancy_flags": discrepancy_flags,
        }
    }

