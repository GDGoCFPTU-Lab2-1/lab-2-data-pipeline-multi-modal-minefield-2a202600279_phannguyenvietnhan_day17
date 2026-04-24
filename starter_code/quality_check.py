# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

_TOXIC_STRINGS = [
    'Null pointer exception',
    'NullPointerException',
    'undefined is not a function',
    'Traceback (most recent call last)',
]

def run_quality_gate(document_dict):
    doc_id = document_dict.get('document_id', '<unknown>')
    content = document_dict.get('content', '')

    # Reject documents with content shorter than 20 characters
    if len(content) < 20:
        print(f"  [QA FAIL] {doc_id}: content too short ({len(content)} chars).")
        return False

    # Reject documents containing toxic or error strings
    for toxic in _TOXIC_STRINGS:
        if toxic.lower() in content.lower():
            print(f"  [QA FAIL] {doc_id}: toxic string detected: '{toxic}'")
            return False

    # Flag (but do not reject) discrepancies noted in source_metadata
    flags = document_dict.get('source_metadata', {}).get('discrepancy_flags', [])
    if flags:
        print(f"  [QA WARN] {doc_id}: discrepancy flags — {flags}")

    return True
