import os
import requests
from bs4 import BeautifulSoup
import re

# Define project root and output directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
output_dir = os.path.join(project_root, 'data', 'html_static')

def fetch_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Failed to fetch content from {url}: {e}")
        return None

def extract_pdf_link_and_date(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Search for the PDF link with a specific regex pattern
    link_element = soup.find('a', href=re.compile(r'/sites/default/files/\d{4}-\d{2}/FHFA-HPI-Monthly-\d{8}.pdf'))
    
    if link_element:
        pdf_link = "https://www.fhfa.gov" + link_element['href']
        print(f"PDF Link found: {pdf_link}")
        
        # Extract the date from the file name (e.g., FHFA-HPI-Monthly-07302024.pdf)
        date_match = re.search(r'FHFA-HPI-Monthly-(\d{8})\.pdf', pdf_link)
        if date_match:
            release_date = date_match.group(1)
            print(f"Release Date extracted from link: {release_date}")
            return pdf_link, release_date
        else:
            print("Failed to extract release date from link.")
            return pdf_link, None
    else:
        print("PDF link not found.")
        return None, None

def save_content(pdf_link, release_date, url):
    os.makedirs(output_dir, exist_ok=True)
    sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', url.replace('https://', ''))
    file_name = f"beautifulsoup_link_scraping_{sanitized_url}.txt"
    save_path = os.path.join(output_dir, file_name)
    
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(f"PDF Link: {pdf_link}\nRelease Date: {release_date}\n")
    
    print(f"PDF link and release date saved to {save_path}")

# Example usage
url = "https://www.fhfa.gov/data/hpi"  # Replace with an actual URL that contains a PDF link
html_content = fetch_html_content(url)
if html_content:
    pdf_link, release_date = extract_pdf_link_and_date(html_content.decode('utf-8'))  # Convert bytes to string
    
    if pdf_link and release_date:
        save_content(pdf_link, release_date, url)
    else:
        print("Failed to extract PDF link or release date.")
