import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager

# Define project root and output directory using relative paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
output_dir = os.path.join(project_root, "data", "html_dynamic")

# Setup Chrome options to avoid detection
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Initialize the Chrome driver using webdriver_manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def disable_cep_popup():
    try:
        # Wait for the popup to appear and insert the CEP
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='CEP']"))
        ).send_keys("01001-000")  # Insert your CEP code here
        
        # Find and click the "Submit" button
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='store-button']"))
        )
        submit_button.click()
        
        # Wait for the popup to disappear
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element((By.XPATH, "//div[@role='dialog']"))
        )
        print("CEP popup disabled successfully.")
    except Exception as e:
        print(f"Failed to insert CEP: {e}")

def fetch_data_using_javascript():
    try:
        # Use JavaScript to fetch product names and prices directly from the DOM
        script = """
        let products = document.querySelectorAll("article.relative.flex.flex-col");
        let data = [];
        let currentDate = new Date().toISOString().split('T')[0];
        
        products.forEach((product) => {
            let name = product.querySelector("span.overflow-hidden.text-ellipsis").getAttribute('title');
            let price = product.querySelector("span.text-base.text-blue-royal.font-medium").innerText;
            data.push([currentDate, name, price]);
        });
        return data;
        """
        data = driver.execute_script(script)
        
        # Clean the prices by removing 'R$\xa0' and converting to float
        cleaned_data = []
        for entry in data:
            # Clean the price string and convert to float
            price_cleaned = entry[2].replace('R$\xa0', '').replace('.', '').replace(',', '.').strip()
            entry[2] = float(price_cleaned)  # Convert to float
            cleaned_data.append(entry)
        
        print(f"[JavaScript Method] Found {len(cleaned_data)} products on the page.")
        return cleaned_data
    except Exception as e:
        print(f"[JavaScript Method] Error: {e}")
        return []

def main():
    # List of search terms
    search_terms = ["leite piracanjuba", "Leite Desnatado Piracanjuba 1 Litro", "Leite Integral Piracanjuba 1 Litro"]
    
    # Base URL
    base_url = "https://mercado.carrefour.com.br/s?q={}&sort=score_desc&page=0"
    
    # Create an empty DataFrame to hold the results
    all_data = pd.DataFrame(columns=["date", "product_name", "price"])
    
    # Loop through search terms
    for term in search_terms:
        search_url = base_url.format(term.replace(' ', '+'))
        
        # Load the page
        driver.get(search_url)
        
        # Give the page some time to load
        time.sleep(5)  # This can be adjusted based on page load speed
        
        # Disable the CEP popup
        disable_cep_popup()
        
        # Fetch data (current_date, product_name, price)
        data_js = fetch_data_using_javascript()
        
        # Append the data to the DataFrame
        if data_js:
            df = pd.DataFrame(data_js, columns=["date", "product_name", "price"])
            all_data = pd.concat([all_data, df], ignore_index=True)
    
    # Save the DataFrame to a CSV file
    current_date = datetime.now().strftime("%Y%m%d")
    os.makedirs(output_dir, exist_ok=True)  # Create the data directory if it doesn't exist
    output_file = os.path.join(output_dir, f"prices_carrefour_{current_date}.csv")
    
    all_data.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()
    driver.quit()
