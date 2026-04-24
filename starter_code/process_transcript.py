import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def _detect_price_vnd(text):
    # Try explicit numeric format first: "500,000 VND"
    match = re.search(r'(\d[\d,\.]+)\s*VND', text)
    if match:
        digits = re.sub(r'[,\.]', '', match.group(1))
        try:
            return int(digits)
        except ValueError:
            pass
    # Fallback: Vietnamese "năm trăm nghìn" = 500,000
    if re.search(r'năm\s+trăm\s+nghìn|năm\s+trăm\s+ngàn', text, re.IGNORECASE):
        return 500000
    return None


def clean_transcript(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Extract price before stripping text
    detected_price = _detect_price_vnd(text)

    # Remove timestamps like [00:00:00]
    cleaned = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)
    # Remove speaker labels like [Speaker 1]:
    cleaned = re.sub(r'\[Speaker \d+\]\s*:', '', cleaned)
    # Remove noise tokens
    noise = r'\[Music\s*(?:starts?|ends?)?\]|\[inaudible\]|\[Laughter\]|\[Applause\]'
    cleaned = re.sub(noise, '', cleaned, flags=re.IGNORECASE)
    # Collapse extra whitespace
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)
    cleaned = re.sub(r'\n\s*\n', '\n', cleaned).strip()

    return {
        "document_id": "transcript-demo-001",
        "content": cleaned,
        "source_type": "Video",
        "author": "Speaker 1",
        "timestamp": None,
        "source_metadata": {
            "original_file": "demo_transcript.txt",
            "detected_price_vnd": detected_price,
        }
    }

