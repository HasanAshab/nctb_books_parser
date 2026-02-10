
import requests
from bs4 import BeautifulSoup
import json
import os


target_page = "https://nctb.gov.bd/pages/static-pages/695b98afc4774958d7b7044c"

def scrape_booklist():
    print("Scrapping Booklist URL's")
    
    # Fetch the page
    response = requests.get(target_page, verify=False)
    response.raise_for_status()
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table
    table = soup.find('table')
    
    if not table:
        return
    
    # Target column headings
    target_headings = ['মাধ্যমিক স্তর', 'উচ্চ মাধ্যমিক স্তর']
    
    # Get all rows from tbody
    tbody = table.find('tbody')
    if not tbody:
        return
    
    rows = tbody.find_all('tr')
    if not rows:
        return
    
    # First row contains headers
    header_row = rows[0]
    headers = []
    header_indices = {}
    
    for idx, cell in enumerate(header_row.find_all('td')):
        header_text = cell.get_text(strip=True)
        headers.append(header_text)
        if header_text in target_headings:
            header_indices[idx] = header_text
    
    # Extract data from remaining rows
    result = []
    for row in rows[1:]:  # Skip header row
        cells = row.find_all('td')
        for idx, cell in enumerate(cells):
            if idx in header_indices:
                # Find all anchor tags in this cell
                anchors = cell.find_all('a')
                for anchor in anchors:
                    href = anchor.get('href', '')
                    strong = anchor.find('strong')
                    class_text = strong.get_text(strip=True) if strong else anchor.get_text(strip=True)
                    
                    # Create full URL if relative
                    if href.startswith('/'):
                        full_url = f"https://nctb.gov.bd{href}"
                    else:
                        full_url = href
                    
                    result.append({
                        'category': header_indices[idx],
                        'class': class_text,
                        'url': full_url
                    })
    
    # Save to JSON file
    maps_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'maps')
    os.makedirs(maps_dir, exist_ok=True)
    
    output_file = os.path.join(maps_dir, 'booklist_url.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"Found {len(result)} Items")

scrape_booklist()

