import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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

def fetch_data_using_javascript(url):
    try:
        driver.get(url)
        script = """
        let paragraphs = document.querySelectorAll("p");
        let data = [];
        paragraphs.forEach((p) => {
            data.push(p.innerText);
        });
        return data;
        """
        data = driver.execute_script(script)
        return "\n\n".join([line for line in data if line.strip() != ""])
    except Exception as e:
        print(f"[JavaScript Method] Error: {e}")
        return None

def save_content(content, method, url):
    os.makedirs(output_dir, exist_ok=True)
    file_name = f"{method}_{url.replace('https://', '').replace('/', '_')}.txt"
    save_path = os.path.join(output_dir, file_name)
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Content saved to {save_path}")

# Example usage
url = "https://www.nar.realtor/research-and-statistics/housing-statistics/existing-home-sales"
content = fetch_data_using_javascript(url)
if content:
    save_content(content, 'selenium_javascript_execution', url)
driver.quit()