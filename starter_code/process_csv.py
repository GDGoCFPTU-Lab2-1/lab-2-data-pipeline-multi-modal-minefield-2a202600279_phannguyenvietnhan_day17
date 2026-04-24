import pandas as pd
import re
from datetime import datetime

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

_TEXT_PRICES = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
}

def _clean_price(val):
    if pd.isna(val):
        return None
    s = str(val).strip()
    if s in ('N/A', 'NULL', 'Liên hệ', '', 'nan'):
        return None
    s = s.replace('$', '').replace(',', '').strip()
    try:
        return float(s)
    except ValueError:
        word = s.lower().split()[0] if s else ''
        return float(_TEXT_PRICES[word]) if word in _TEXT_PRICES else None


def _normalize_date(val):
    if pd.isna(val):
        return None
    s = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', str(val).strip())
    for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d', '%d-%m-%Y',
                '%B %d %Y', '%d %b %Y', '%B %d, %Y'):
        try:
            return datetime.strptime(s, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return str(val)


def process_sales_csv(file_path):
    df = pd.read_csv(file_path)
    # Remove duplicate rows based on 'id', keep first occurrence
    df = df.drop_duplicates(subset=['id'], keep='first')

    documents = []
    for _, row in df.iterrows():
        price = _clean_price(row.get('price'))
        date = _normalize_date(row.get('date_of_sale'))
        product = str(row.get('product_name', 'Unknown'))
        category = str(row.get('category', 'Unknown'))
        currency = str(row.get('currency', ''))
        seller = str(row.get('seller_id', 'Unknown'))
        row_id = int(float(row['id']))

        content = (
            f"Product: {product}. Category: {category}. "
            f"Price: {price} {currency}. Date of Sale: {date}. Seller: {seller}."
        )

        documents.append({
            "document_id": f"csv-{row_id}",
            "content": content,
            "source_type": "CSV",
            "author": "Unknown",
            "timestamp": None,
            "source_metadata": {
                "price_cleaned": price,
                "date_normalized": date,
                "seller_id": seller,
                "currency": currency,
            }
        })

    return documents

