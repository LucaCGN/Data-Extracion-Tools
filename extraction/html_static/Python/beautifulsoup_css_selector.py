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

def extract_content_with_css_selector(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    content_sections = soup.select('p')  # Using CSS selector to extract paragraphs
    return "\n\n".join([section.get_text(separator='\n', strip=True) for section in content_sections])

def sanitize_file_name(file_name):
    # Replace invalid characters for Windows file names
    return re.sub(r'[<>:"/\\|?*]', '_', file_name)

def save_content(content, method, url):
    os.makedirs(output_dir, exist_ok=True)
    file_name = f"{method}_{sanitize_file_name(url.replace('https://', ''))}.txt"
    save_path = os.path.join(output_dir, file_name)
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Content saved to {save_path}")

# Example usage
url = "https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html?=&t=noticias-e-releases"
html_content = fetch_html_content(url)
if html_content:
    content = extract_content_with_css_selector(html_content)
    save_content(content, 'beautifulsoup_css_selector', url)
