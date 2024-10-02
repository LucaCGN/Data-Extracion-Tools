import os
import requests
from fake_useragent import UserAgent

# Define project root and output directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
output_dir = os.path.join(project_root, 'data', 'html_static')

def fetch_content_with_fake_user_agent(url):
    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        response = requests.get(url, headers=headers, verify=False) 
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Failed to fetch content from {url}: {e}")
        return None

def save_content(content, method, url):
    os.makedirs(output_dir, exist_ok=True)
    file_name = f"{method}_{url.replace('https://', '').replace('/', '_')}.txt"
    save_path = os.path.join(output_dir, file_name)
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(content.decode('utf-8'))
    print(f"Content saved to {save_path}")

# Example usage
url = "https://balanca.economia.gov.br/balanca/pg_principal_bc/principais_resultados.html"
content = fetch_content_with_fake_user_agent(url)
if content:
    save_content(content, 'requests_fakeuseragent', url)
