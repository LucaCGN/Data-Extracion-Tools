import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Define project root and output directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
output_dir = os.path.join(project_root, 'data', 'html_dynamic')

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def fetch_data_using_xpath(url):
    try:
        driver.get(url)
        # Locate the elements using XPath
        paragraphs = driver.find_elements(By.XPATH, "//p")
        data = [p.text for p in paragraphs]
        return "\n\n".join(data)
    except Exception as e:
        print(f"[XPath Method] Error: {e}")
        return None

def save_content(content, method, url):
    os.makedirs(output_dir, exist_ok=True)
    file_name = f"{method}_{url.replace('https://', '').replace('/', '_')}.txt"
    save_path = os.path.join(output_dir, file_name)
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Content saved to {save_path}")

# Example usage
url = "https://www.conference-board.org/topics/consumer-confidence"
content = fetch_data_using_xpath(url)
if content:
    save_content(content, 'selenium_xpath', url)
driver.quit()
