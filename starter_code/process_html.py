from bs4 import BeautifulSoup
import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def _clean_price(raw):
    if not raw or raw.strip() in ('N/A', 'Liên hệ', ''):
        return None
    digits = re.sub(r'[^\d]', '', raw)
    return int(digits) if digits else None


def parse_html_catalog(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    table = soup.find('table', id='main-catalog')
    if not table:
        return []

    headers = [th.get_text(strip=True) for th in table.find('thead').find_all('th')]
    documents = []

    for row in table.find('tbody').find_all('tr'):
        cells = [td.get_text(strip=True) for td in row.find_all('td')]
        if not cells:
            continue
        data = dict(zip(headers, cells))

        # Vietnamese column names: Mã SP, Tên sản phẩm, Danh mục, Giá niêm yết, Tồn kho, Đánh giá
        product_id = data.get('Mã SP', f'html-{len(documents)+1}')
        name = data.get('Tên sản phẩm', 'Unknown')
        category = data.get('Danh mục', 'Unknown')
        price_raw = data.get('Giá niêm yết', '')
        stock_raw = data.get('Tồn kho', '')
        rating_raw = data.get('Đánh giá', '')

        price = _clean_price(price_raw)
        try:
            stock = int(stock_raw) if stock_raw else None
        except ValueError:
            stock = None

        content = (
            f"Product: {name}. Category: {category}. ID: {product_id}. "
            f"Price: {price_raw}. Stock: {stock_raw}. Rating: {rating_raw}."
        )

        documents.append({
            "document_id": f"html-{product_id}",
            "content": content,
            "source_type": "HTML",
            "author": "Unknown",
            "timestamp": None,
            "source_metadata": {
                "product_id": product_id,
                "product_name": name,
                "category": category,
                "price_cleaned": price,
                "price_raw": price_raw,
                "stock": stock,
                "rating": rating_raw,
            }
        })

    return documents

