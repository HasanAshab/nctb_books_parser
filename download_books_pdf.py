import json
import os
import re
import requests
import urllib3
from urllib.parse import urlparse, parse_qs

def extract_file_id(url):
    """Extract file ID from URL"""
    if not url:
        return None

    # Pattern for egovcloud: /s/{id}/download or /s/{id}
    match = re.search(r'/s/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    return None

def download_file(url, output_path):
    """Download file from URL"""
    temp_path = output_path + '.tmp'
    
    try:
        response = requests.get(url, stream=True, verify=False)
        response.raise_for_status()

        # Save to temporary file first
        with open(temp_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=32768):
                if chunk:
                    f.write(chunk)
        
        # Rename to final name only if download completed
        os.rename(temp_path, output_path)
    except:
        # Clean up temporary file if download failed or interrupted
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise

def download_books():
    print("Downloading Book PDFs")
    
    # Read book_pdf_url.json
    maps_dir = 'maps'
    book_pdf_file = os.path.join(maps_dir, 'book_pdf_url.json')
    
    with open(book_pdf_file, 'r', encoding='utf-8') as f:
        books = json.load(f)

    # Create books directory
    books_dir = 'books'
    os.makedirs(books_dir, exist_ok=True)

    downloaded = 0
    skipped = 0
    total = len(books)

    for idx, book in enumerate(books, 1):
        url = book.get('url')
        if not url:
            skipped += 1
            continue

        # Extract file ID
        file_id = extract_file_id(url)
        if not file_id:
            skipped += 1
            continue
        
        # Check if already downloaded
        output_path = os.path.join(books_dir, f"{file_id}.pdf")
        if os.path.exists(output_path):
            print(f"[{idx}/{total}] Skipping {file_id}.pdf (already exists)")
            skipped += 1
            continue
        
        # Download
        try:
            print(f"[{idx}/{total}] Downloading {file_id}.pdf...")
            download_file(url, output_path)
            downloaded += 1
        except Exception as e:
            print(f"[{idx}/{total}] Failed to download {file_id}: {e}")
            skipped += 1
    
    print(f"Downloaded {downloaded} PDFs, Skipped {skipped}")

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    download_books()
