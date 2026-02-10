import requests
from bs4 import BeautifulSoup
import json
import os
import time

def scrape_book_pdfs():
    print("Scrapping Book PDF URL's")
    
    # Read booklist_url.json
    maps_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'maps')
    booklist_file = os.path.join(maps_dir, 'booklist_url.json')
    
    with open(booklist_file, 'r', encoding='utf-8') as f:
        booklist = json.load(f)
    
    result = []
    
    for item in booklist:
        url = item['url']
        
        # Fetch the page
        response = requests.get(url, verify=False)
        response.raise_for_status()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table
        table = soup.find('table')
        if not table:
            continue
        
        tbody = table.find('tbody')
        if not tbody:
            continue
        
        rows = tbody.find_all('tr')
        if not rows:
            continue
        
        # First row is header, skip it
        header_row = rows[0]
        header_cells = header_row.find_all('td')
        
        # Determine table structure by counting columns
        num_columns = len(header_cells)
        
        # Process data rows
        for row in rows[1:]:
            cells = row.find_all('td')
            
            if num_columns == 5:
                # Structure 1: Has both Bangla and English versions
                # Columns: ক্রমিক | বাংলা নাম | বাংলা ডাউনলোড | ইংরেজি নাম | ইংরেজি ডাউনলোড
                if len(cells) >= 5:
                    # Bangla version
                    bangla_name = cells[1].get_text(strip=True)
                    bangla_links = cells[2].find_all('a')
                    bangla_url = f"{bangla_links[1].get('href')}/download" if bangla_links else None
                    
                    if bangla_name:
                        result.append({
                            'book_name': bangla_name,
                            'class': item['class'],
                            'version': 'বাংলা',
                            'url': bangla_url
                        })
                    
                    # English version
                    english_name = cells[3].get_text(strip=True)
                    english_links = cells[4].find_all('a')
                    english_url = english_links[0].get('href') if english_links else None
                    
                    if english_name:
                        result.append({
                            'book_name': english_name,
                            'class': item['class'],
                            'version': 'ইংরেজি',
                            'url': english_url
                        })
            
            elif num_columns == 3:
                # Structure 2: Single version
                # Columns: ক্রমিক | পাঠ্যপুস্তকের নাম | ডাউনলোড
                if len(cells) >= 3:
                    book_name = cells[1].get_text(strip=True)
                    links = cells[2].find_all('a')
                    book_url = links[0].get('href') if links else None
                    
                    if book_name:
                        result.append({
                            'booklist_url': url,
                            'book_name': book_name,
                            'version': None,
                            'url': book_url
                        })

        # Small delay to be respectful
        time.sleep(0.5)

    # Save to JSON file
    output_file = os.path.join(maps_dir, 'book_pdf_url.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Found {len(result)} Items")

scrape_book_pdfs()
