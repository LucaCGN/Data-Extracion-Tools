

## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\consolidate_codebase.py (Python)

```python
import os

# Define the root directory and output file
root_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(root_dir, "complete_codebase.md")

# Supported file types and their language labels
file_types = {
    '.py': 'Python',
    '.r': 'R',
    '.vba': 'VBA'
}

# Directories to exclude
exclude_dirs = {'__pycache__', 'venv'}

# Initialize counters
line_counts = {lang: 0 for lang in file_types.values()}
total_lines = 0

# Function to count lines in a file
def count_lines_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return len(f.readlines())

# Function to consolidate code into markdown format
def consolidate_code(file_path, lang, output_md):
    with open(file_path, 'r', encoding='utf-8') as f:
        output_md.write(f"\n\n## {file_path} ({lang})\n\n")
        output_md.write("```" + lang.lower() + "\n")
        output_md.write(f.read())
        output_md.write("\n```\n")

# Traverse directories, consolidate files, and count lines
with open(output_file, 'w', encoding='utf-8') as output_md:
    for subdir, _, files in os.walk(root_dir):
        # Skip excluded directories
        if any(exclude in subdir for exclude in exclude_dirs):
            continue
        
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in file_types:
                file_path = os.path.join(subdir, file)
                lang = file_types[file_ext]
                
                # Count lines in the file
                lines_in_file = count_lines_in_file(file_path)
                line_counts[lang] += lines_in_file
                total_lines += lines_in_file
                
                # Consolidate the code into the markdown file
                consolidate_code(file_path, lang, output_md)

# Print the total lines of code for each language and overall
print("Lines of Code per Language:")
for lang, count in line_counts.items():
    print(f"{lang}: {count} lines")
print(f"Total Lines of Code: {total_lines} lines")

# Confirm completion
print(f"\nConsolidation complete. Codebase saved to {output_file}.")

```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\bcb\python\bcb_usage.py (Python)

```python
import os
import pandas as pd
from bcb import Expectativas

# Define project root and output directory using relative paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
output_dir = os.path.join(project_root, "data", "bcb")

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

def save_endpoint_data(endpoint_name):
    em = Expectativas()
    try:
        # Retrieve the endpoint data
        print(f"Fetching data for {endpoint_name}...")
        
        # Adjusted to the general query format
        endpoint = em.get_endpoint(endpoint_name)
        data = endpoint.query().collect()

        # Save the dataset to a CSV file
        filename = os.path.join(output_dir, f'{endpoint_name}_data.csv')
        data.to_csv(filename, index=False)
        print(f"Dataset for {endpoint_name} saved to {filename}")
        
    except Exception as e:
        print(f"Failed to retrieve data for {endpoint_name}: {e}")

def main():
    # List of endpoints to explore
    endpoints = [
        'ExpectativasMercadoTop5Anuais',
        # Other endpoints can be added back for further testing
        # 'ExpectativaMercadoMensais',
        # 'ExpectativasMercadoInflacao24Meses',
        # 'ExpectativasMercadoInflacao12Meses',
        # 'ExpectativasMercadoSelic',
        # 'ExpectativasMercadoTop5Selic',
        # 'ExpectativasMercadoTop5Mensais',
        # 'ExpectativasMercadoTrimestrais',
        # 'ExpectativasMercadoAnuais'
    ]

    for endpoint in endpoints:
        save_endpoint_data(endpoint)

if __name__ == "__main__":
    main()

```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\bcb\R\bcbr_usage.r (R)

```r
# Pacotes necessários
library(rbcb)   # Para acessar dados do Banco Central do Brasil
library(dplyr)  # Para manipulação de dados
library(ggplot2) # Para visualização dos dados

# Função para buscar séries temporais do Banco Central
# Este exemplo busca a série do IPCA (Índice de Preços ao Consumidor Amplo)
buscar_serie_temporal <- function(codigo_serie) {
  # A função get_series() obtém a série temporal especificada pelo código da série
  dados <- get_series(codigo_serie)
  
  # Retorna os dados baixados
  return(dados)
}

# Função para processar e plotar a série temporal
processar_e_plotar <- function(dados, titulo) {
  # Exibe os primeiros registros dos dados
  head(dados)
  
  # Processamento: vamos calcular a média móvel de 12 meses
  dados <- dados %>%
    mutate(media_movel = zoo::rollmean(value, k = 12, fill = NA))
  
  # Plotando a série temporal e a média móvel
  ggplot(dados, aes(x = date, y = value)) +
    geom_line(color = "blue", size = 1) +
    geom_line(aes(y = media_movel), color = "red", linetype = "dashed") +
    labs(title = titulo, x = "Data", y = "Valor") +
    theme_minimal()
}

# Função principal para buscar, processar e plotar uma série temporal do BCB
principal <- function() {
  # Código da série temporal do IPCA (Índice de Preços ao Consumidor Amplo)
  codigo_ipca <- 433
  
  # Busca os dados da série temporal
  dados_ipca <- buscar_serie_temporal(codigo_ipca)
  
  # Processa e plota a série temporal
  processar_e_plotar(dados_ipca, "IPCA - Índice de Preços ao Consumidor Amplo")
}

# Executa o script principal
principal()
```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\comex\Python\enrich_and_clean_data.py (Python)

```python
import os
import pandas as pd
import logging
import asyncio
import requests

# Define the correct paths for the comex module
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'comex')
LOGS_DIR = os.path.join(BASE_DIR, 'extraction', 'comex', 'Python', 'logs')

# Set up logging
log_file = os.path.join(LOGS_DIR, 'enrich_and_clean_data.log')
os.makedirs(LOGS_DIR, exist_ok=True)
logging.basicConfig(level=logging.DEBUG, filename=log_file, format='%(asctime)s - %(levelname)s - %(message)s')

# URL to download the auxiliary tables
AUX_TABLES_URL = "https://balanca.economia.gov.br/balanca/bd/tabelas/TABELAS_AUXILIARES.xlsx"  # Replace with the actual URL

# Function to download auxiliary tables
def download_auxiliary_tables(aux_tables_file):
    try:
        if not os.path.exists(aux_tables_file):
            logging.info(f"Downloading auxiliary tables from {AUX_TABLES_URL}.")
            response = requests.get(AUX_TABLES_URL, verify=False)
            response.raise_for_status()

            with open(aux_tables_file, 'wb') as file:
                file.write(response.content)
            logging.info(f"Auxiliary tables downloaded and saved to {aux_tables_file}.")
        else:
            logging.info("Auxiliary tables already exist. Skipping download.")
    except requests.RequestException as e:
        logging.error(f"Error occurred while downloading the auxiliary tables: {str(e)}")
        raise

# Function to convert specified columns to string
def convert_columns_to_str(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df

# Function to handle duplicate columns generated by merging (_x and _y suffixes)
def handle_duplicate_columns(df, column_base_names):
    for col in column_base_names:
        if f"{col}_x" in df.columns and f"{col}_y" in df.columns:
            df[col] = df[f"{col}_x"].combine_first(df[f"{col}_y"])
            df.drop([f"{col}_x", f"{col}_y"], axis=1, inplace=True)
        elif f"{col}_x" in df.columns:
            df.rename(columns={f"{col}_x": col}, inplace=True)
        elif f"{col}_y" in df.columns:
            df.rename(columns={f"{col}_y": col}, inplace=True)
    return df

# Function to enrich data in chunks
async def enrich_data_chunked(filtered_file, aux_tables_file, output_file, chunk_size=50000):
    try:
        logging.info(f"Starting enrichment of {filtered_file} using {aux_tables_file}.")
        
        # Load auxiliary tables and drop duplicates
        aux_tables = pd.read_excel(aux_tables_file, sheet_name=None)
        table_1 = convert_columns_to_str(aux_tables['1'].drop_duplicates(subset=['CO_NCM']), ['CO_NCM'])
        table_10 = convert_columns_to_str(aux_tables['10'].drop_duplicates(subset=['CO_PAIS']), ['CO_PAIS'])
        table_14 = convert_columns_to_str(aux_tables['14'].drop_duplicates(subset=['CO_VIA']), ['CO_VIA'])
        table_6 = convert_columns_to_str(aux_tables['6'].drop_duplicates(subset=['CO_UNID']), ['CO_UNID'])

        chunk_idx = 0
        with pd.read_csv(filtered_file, delimiter=';', chunksize=chunk_size, dtype=str) as reader:
            for chunk in reader:
                logging.info(f"Processing chunk {chunk_idx + 1}.")
                
                # Convert relevant columns to string for consistent merging
                chunk = convert_columns_to_str(chunk, ['CO_NCM', 'CO_PAIS', 'CO_VIA', 'CO_UNID'])

                # Perform the sequential merging with deduplicated tables
                chunk = chunk.merge(table_1[['CO_NCM', 'NO_NCM_POR', 'NO_SH6_POR', 'NO_SH4_POR', 'NO_SH2_POR', 'NO_SEC_POR']], on='CO_NCM', how='left')
                chunk = chunk.merge(table_10[['CO_PAIS', 'NO_PAIS']], on='CO_PAIS', how='left')
                chunk = chunk.merge(table_14[['CO_VIA', 'NO_VIA']], on='CO_VIA', how='left')
                chunk = chunk.merge(table_6[['CO_UNID', 'NO_UNID']], on='CO_UNID', how='left')

                # Handle duplicated columns (_x and _y suffixes)
                chunk = handle_duplicate_columns(chunk, ['NO_NCM_POR', 'NO_SH6_POR', 'NO_SH4_POR', 'NO_SH2_POR', 'NO_SEC_POR', 'NO_UNID', 'NO_PAIS', 'NO_VIA'])

                # Write the enriched chunk to the output file
                mode = 'w' if chunk_idx == 0 else 'a'
                header = True if chunk_idx == 0 else False
                chunk.to_csv(output_file, mode=mode, index=False, sep=';', header=header)

                chunk_idx += 1

        logging.info(f"Enrichment complete. Data saved to {output_file}.")
    except Exception as e:
        logging.error(f"An error occurred during enrichment: {str(e)}")
        raise

# Function to clean temporary files
def clean_temp_files():
    try:
        logging.info("Cleaning up temporary files...")
        keep_files = {"TABELAS_AUXILIARES.xlsx", "COMEX-EXP_FINAL_ENRICHED.csv", "COMEX-IMP_FINAL_ENRICHED.csv"}
        for filename in os.listdir(DATA_DIR):
            file_path = os.path.join(DATA_DIR, filename)
            if filename not in keep_files and filename.endswith(".csv"):
                os.remove(file_path)
                logging.info(f"Deleted temporary file: {file_path}")
        logging.info("Temporary files cleaned up successfully.")
    except Exception as e:
        logging.error(f"An error occurred during cleanup: {str(e)}")
        raise

# Main execution
if __name__ == "__main__":
    aux_tables_file = os.path.join(DATA_DIR, "TABELAS_AUXILIARES.xlsx")

    # Step 1: Download the auxiliary tables if they do not exist
    download_auxiliary_tables(aux_tables_file)

    # Step 2: Enrich data using the filtered CSV
    filtered_file = os.path.join(DATA_DIR, "COMEX-EXP_FILTERED.csv")
    output_file = os.path.join(DATA_DIR, "COMEX-EXP_FINAL_ENRICHED.csv")
    asyncio.run(enrich_data_chunked(filtered_file, aux_tables_file, output_file))

    # Step 3: Clean temporary files
    clean_temp_files()

```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\comex\Python\fetch_and_process_data.py (Python)

```python
import os
import aiohttp
import asyncio
import aiofiles
import pandas as pd
import logging
from datetime import datetime
import random

# Define the correct paths for the comex module
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'comex')
LOGS_DIR = os.path.join(BASE_DIR, 'extraction', 'comex', 'Python', 'logs')

# Set up logging
log_file = os.path.join(LOGS_DIR, 'fetch_and_process_data.log')
os.makedirs(LOGS_DIR, exist_ok=True)
logging.basicConfig(level=logging.DEBUG, filename=log_file, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for fetching data
BASE_URL = "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/{}_{}.csv"
START_YEAR = 2023
CURRENT_YEAR = datetime.now().year
MAX_CONCURRENT_REQUESTS = 8
RETRY_LIMIT = 5
BATCH_SIZE = 4

# Fetch CSV files
async def fetch_and_save_csv(session, year, dataset_type, retries=0):
    url = BASE_URL.format(dataset_type.split("-")[1], year)
    csv_filepath = os.path.join(DATA_DIR, f"{dataset_type}_{year}.csv")

    if os.path.exists(csv_filepath):
        logging.info(f"File already exists, skipping download for {year}.")
        return

    try:
        logging.info(f"Fetching CSV for {year} from {url}...")
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=60)) as response:
            if response.status == 200:
                content = await response.read()
                async with aiofiles.open(csv_filepath, 'wb') as f:
                    await f.write(content)
                logging.info(f"Saved CSV for {year} to {csv_filepath}.")
            else:
                logging.error(f"Failed to fetch CSV for {year}. Status code: {response.status}")
                if retries < RETRY_LIMIT:
                    backoff_time = (2 ** retries) + random.uniform(0, 1)
                    await asyncio.sleep(backoff_time)
                    await fetch_and_save_csv(session, year, dataset_type, retries=retries + 1)
    except Exception as e:
        logging.error(f"An error occurred while fetching {year}: {str(e)}")
        if retries < RETRY_LIMIT:
            backoff_time = (2 ** retries) + random.uniform(0, 1)
            await asyncio.sleep(backoff_time)
            await fetch_and_save_csv(session, year, dataset_type, retries=retries + 1)

# Process CSV in batches
async def fetch_csv_batch(session, years, dataset_type, semaphore):
    tasks = []
    async with semaphore:
        for year in years:
            task = asyncio.create_task(fetch_and_save_csv(session, year, dataset_type))
            tasks.append(task)
        await asyncio.gather(*tasks)

# Fetch all CSVs
async def fetch_all_csvs(dataset_type):
    connector = aiohttp.TCPConnector(limit_per_host=MAX_CONCURRENT_REQUESTS, ssl=False)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession(connector=connector) as session:
        years = list(range(START_YEAR, CURRENT_YEAR + 1))
        for i in range(0, len(years), BATCH_SIZE):
            batch_years = years[i:i+BATCH_SIZE]
            await fetch_csv_batch(session, batch_years, dataset_type, semaphore)

# Filter large CSV files by NCM codes
async def filter_large_csv_by_ncm_in_chunks(input_file, output_file, ncm_list, chunk_size=100000):
    try:
        logging.info(f"Starting filtering of {input_file} by NCM list.")
        is_imp = "COMEX-IMP" in input_file

        if is_imp:
            expected_columns = [
                "CO_ANO", "CO_MES", "CO_NCM", "CO_UNID", "CO_PAIS", "SG_UF_NCM",
                "CO_VIA", "CO_URF", "QT_ESTAT", "KG_LIQUIDO", "VL_FOB", "VL_FRETE", "VL_SEGURO"
            ]
        else:
            expected_columns = [
                "CO_ANO", "CO_MES", "CO_NCM", "CO_UNID", "CO_PAIS", "SG_UF_NCM",
                "CO_VIA", "CO_URF", "QT_ESTAT", "KG_LIQUIDO", "VL_FOB"
            ]

        with pd.read_csv(input_file, delimiter=';', chunksize=chunk_size, dtype={'CO_NCM': str}) as reader:
            for i, chunk in enumerate(reader):
                chunk = chunk[[col for col in expected_columns if col in chunk.columns]]
                chunk['CO_NCM'] = chunk['CO_NCM'].astype(str).str.strip()
                for col in ["CO_ANO", "CO_MES", "QT_ESTAT", "KG_LIQUIDO", "VL_FOB", "VL_FRETE", "VL_SEGURO"]:
                    if col in chunk.columns:
                        chunk[col] = pd.to_numeric(chunk[col], errors='coerce')

                filtered_chunk = chunk[chunk['CO_NCM'].isin(ncm_list)]
                if not filtered_chunk.empty:
                    write_header = i == 0 and not os.path.exists(output_file)
                    filtered_chunk.to_csv(output_file, mode='a', index=False, sep=';', header=write_header)

        logging.info(f"Finished filtering {input_file}. Filtered data saved to {output_file}.")
    except Exception as e:
        logging.error(f"An error occurred during filtering of {input_file}: {str(e)}")
        raise

# Filter all CSVs in directory
async def filter_all_csvs_in_directory(directory, output_file_imp, output_file_exp, ncm_list, chunk_size=100000):
    try:
        if output_file_imp and os.path.exists(output_file_imp):
            os.remove(output_file_imp)
        if output_file_exp and os.path.exists(output_file_exp):
            os.remove(output_file_exp)

        tasks = []
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                input_file = os.path.join(directory, filename)
                if "COMEX-IMP" in filename and output_file_imp:
                    task = filter_large_csv_by_ncm_in_chunks(input_file, output_file_imp, ncm_list, chunk_size)
                    tasks.append(task)
                elif "COMEX-EXP" in filename and output_file_exp:
                    task = filter_large_csv_by_ncm_in_chunks(input_file, output_file_exp, ncm_list, chunk_size)
                    tasks.append(task)

        if tasks:
            await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f"An error occurred during directory processing: {str(e)}")
        raise

# Main execution
if __name__ == "__main__":
    dataset_type = "COMEX-EXP"
    asyncio.run(fetch_all_csvs(dataset_type))

    directory = DATA_DIR
    output_file_imp = os.path.join(DATA_DIR, "COMEX-IMP_FILTERED.csv")
    output_file_exp = os.path.join(DATA_DIR, "COMEX-EXP_FILTERED.csv")
    ncm_list = ['10051000', '10059010', '10059090', '12010010', '12010090', '12011000', '12019000', '15071000', '15079011']

    asyncio.run(filter_all_csvs_in_directory(directory, output_file_imp, output_file_exp, ncm_list))

```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\html_dynamic\Python\selenium_javascript_execution.py (Python)

```python
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
```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\html_dynamic\Python\selenium_popup_handling.py (Python)

```python
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

```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\html_dynamic\Python\selenium_xpath.py (Python)

```python
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

```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\html_feed\Python\websocket_binance.py (Python)

```python
import os
import asyncio
import websockets
import json
import pandas as pd
from datetime import datetime

# Define project root and output directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
output_dir = os.path.join(project_root, 'data', 'html_feed')

# Binance WebSocket URL for the BTCUSDT ticker
ws_url = "wss://stream.binance.com:9443/ws/btcusdt@trade"

async def listen_to_binance():
    os.makedirs(output_dir, exist_ok=True)
    file_name = "binance_btcusdt_feed.csv"
    save_path = os.path.join(output_dir, file_name)
    
    data_list = []

    async with websockets.connect(ws_url) as websocket:
        print(f"Connected to {ws_url}")
        
        # Run for 5 seconds
        end_time = datetime.now().timestamp() + 5
        
        # Listen for incoming messages
        try:
            while datetime.now().timestamp() < end_time:
                message = await websocket.recv()
                data = json.loads(message)
                
                # Extract relevant information (price and timestamp)
                price = float(data.get('p'))
                timestamp = pd.to_datetime(data.get('T'), unit='ms')
                
                if price and timestamp:
                    data_list.append({'Price': price, 'Timestamp': timestamp})
                    
        except websockets.ConnectionClosed as e:
            print("Connection closed:", e)
        except Exception as e:
            print("Error occurred:", e)

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data_list)
    
    # Save DataFrame to CSV
    df.to_csv(save_path, index=False)
    print(f"Data saved to {save_path}")

# Entry point
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(listen_to_binance())

```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\html_static\Python\beautifulsoup_css_selector.py (Python)

```python
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

```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\html_static\Python\beautifulsoup_link_scraping.py (Python)

```python
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

```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\html_static\Python\requests_fakeuseragent.py (Python)

```python
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

```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\html_static\Python\requests_pymupdf_pdf_extraction.py (Python)

```python
import os
import requests
import fitz  # PyMuPDF

# Define project root and output directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
output_dir = os.path.join(project_root, 'data', 'html_static')

def download_pdf(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"PDF downloaded successfully: {save_path}")
        return save_path
    except Exception as e:
        print(f"Failed to download PDF: {e}")
        return None

def extract_text_from_pdf(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)
        text = ""
        for page in pdf_document:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Failed to extract text from PDF: {e}")
        return None

def save_extracted_text(text, method, url):
    file_name = f"{method}_{url.replace('https://', '').replace('/', '_')}.txt"
    save_path = os.path.join(output_dir, file_name)
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Extracted text saved to {save_path}")

# Example usage
pdf_url = "https://www.fhfa.gov/sites/default/files/2024-07/FHFA-HPI-Monthly-07302024.pdf"  # Replace with an actual link
pdf_save_path = os.path.join(output_dir, 'fhfa_report.pdf')
pdf_path = download_pdf(pdf_url, pdf_save_path)
if pdf_path:
    text = extract_text_from_pdf(pdf_path)
    if text:
        save_extracted_text(text, 'requests_pymupdf_pdf_extraction', pdf_url)

```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\indec\Python\fetch_and_process_indec_data.py (Python)

```python
import os
from datetime import datetime
import requests
from io import BytesIO
from zipfile import ZipFile

# Define the correct paths for the INDEC module
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'indec')

# Ensure the directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Function to download and extract export data for a specific year
def download_and_extract(year, output_dir):
    url = f"https://comex.indec.gob.ar/files/zips/exports_{year}_M.zip"
    response = requests.get(url)
    response.raise_for_status()

    with ZipFile(BytesIO(response.content)) as zip_file:
        for file in zip_file.namelist():
            file_year_suffix = str(year)[-2:]
            if (year < 2018 and file.endswith(f'expom{file_year_suffix}.csv')) or \
               (year >= 2018 and (file.endswith(f'exponm{file_year_suffix}.csv') or file.endswith(f'expopm{file_year_suffix}.csv'))):
                zip_file.extract(file, output_dir)
                new_file_path = os.path.join(output_dir, f"{year}_{file}")
                os.rename(os.path.join(output_dir, file), new_file_path)
                print(f"File '{file}' extracted and saved to: {new_file_path}")
                return new_file_path
    return None

# Function to download auxiliary data (e.g., NCM or countries data)
def download_auxiliary_data(url, output_file):
    response = requests.get(url)
    response.raise_for_status()
    with open(output_file, 'wb') as file:
        file.write(response.content)
    print(f"Auxiliary data downloaded and saved to: {output_file}")

# Main execution
if __name__ == "__main__":
    output_dir = DATA_DIR

    # Remove existing files in the output directory
    for f in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, f))

    # Download and extract export data for the last 3 years and the current year
    for year in range(datetime.now().year - 3, datetime.now().year + 1):
        download_and_extract(year, output_dir)

    # Download auxiliary data (NCM Excel and countries JSON)
    ncm_excel_url = "https://comex.indec.gob.ar/files/amendments/enmienda_VII(desde%202024).xlsx"
    countries_json_url = "https://comexbe.indec.gob.ar/public-api/report/countries?current=en"

    ncm_excel_path = os.path.join(DATA_DIR, 'ncm_data.xlsx')
    countries_json_path = os.path.join(DATA_DIR, 'countries.json')

    download_auxiliary_data(ncm_excel_url, ncm_excel_path)

    # For countries.json, since it's returned as JSON data, save it as JSON directly
    response = requests.get(countries_json_url)
    response.raise_for_status()
    with open(countries_json_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"Countries data downloaded and saved to: {countries_json_path}")
```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\indec\Python\process_indec_export_data.py (Python)

```python
import pandas as pd
import os
import json
import re

# Define the base path for the data directory relative to the script location
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
data_dir = os.path.join(base_dir, 'data', 'indec')

# File paths
processed_file_path = os.path.join(data_dir, 'processed_export_data.csv')
countries_json_path = os.path.join(data_dir, 'countries.json')
ncm_data_path = os.path.join(data_dir, 'ncm_data.xlsx')

# Function to clean and process the export data
def clean_export_data(df):
    # Replace commas with dots for numeric conversion
    df['Pnet(kg)'] = df['Pnet(kg)'].str.replace(',', '.')
    df['FOB(u$s)'] = df['FOB(u$s)'].str.replace(',', '.')

    # Remove trailing blank spaces in all string columns
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Keep 's' values in their respective columns
    df['Confidential'] = df.apply(lambda row: 'Yes' if 's' in str(row['Pnet(kg)']) or 's' in str(row['FOB(u$s)']) else 'No', axis=1)

    # Convert to numeric and keep 's' where appropriate
    df['Pnet(kg)_numeric'] = pd.to_numeric(df['Pnet(kg)'].str.replace('s', ''), errors='coerce')
    df['FOB(u$s)_numeric'] = pd.to_numeric(df['FOB(u$s)'].str.replace('s', ''), errors='coerce')

    return df

# Load the export data CSV files
df_2021 = pd.read_csv(os.path.join(data_dir, '2021_exponm21.csv'), delimiter=';', encoding='latin1')
df_2022 = pd.read_csv(os.path.join(data_dir, '2022_exponm22.csv'), delimiter=';', encoding='latin1')
df_2023 = pd.read_csv(os.path.join(data_dir, '2023_exponm23.csv'), delimiter=';', encoding='latin1')
df_2024 = pd.read_csv(os.path.join(data_dir, '2024_exponm24.csv'), delimiter=';', encoding='latin1')

# Apply the cleaning function
df_2021_clean = clean_export_data(df_2021)
df_2022_clean = clean_export_data(df_2022)
df_2023_clean = clean_export_data(df_2023)
df_2024_clean = clean_export_data(df_2024)

# Combine the cleaned dataframes
combined_df = pd.concat([df_2021_clean, df_2022_clean, df_2023_clean, df_2024_clean], ignore_index=True)

# Ensure the NCM column is treated as strings and only keep rows with numeric NCM values
combined_df['NCM'] = combined_df['NCM'].astype(str)
combined_df = combined_df[combined_df['NCM'].apply(lambda x: re.match(r'^\d+$', x) is not None)]
combined_df['NCM'] = combined_df['NCM'].str.replace('.', '').astype(int)

# Load and map country names using countries.json
with open(countries_json_path, 'r') as f:
    countries_data = json.load(f)['data']

country_mapping = {str(item['_id']): item['nombre'] for item in countries_data}
combined_df['Pdes'] = combined_df['Pdes'].astype(str)
combined_df['Country_Name'] = combined_df['Pdes'].map(country_mapping)

# Load the NCM data from Excel and map NCM descriptions
ncm_data = pd.read_excel(ncm_data_path, sheet_name='NCM enm7', skiprows=3)
ncm_data_clean = ncm_data[['I', 'SECCIÓN I - ANIMALES VIVOS Y PRODUCTOS DEL REINO ANIMAL']].rename(columns={'I': 'NCM', 'SECCIÓN I - ANIMALES VIVOS Y PRODUCTOS DEL REINO ANIMAL': 'NCM_Description'})
ncm_data_clean['NCM'] = ncm_data_clean['NCM'].astype(str).str.replace('.', '')
ncm_data_clean = ncm_data_clean[ncm_data_clean['NCM'].apply(lambda x: re.match(r'^\d+$', x) is not None)]
ncm_data_clean['NCM'] = ncm_data_clean['NCM'].astype(int)
ncm_mapping = ncm_data_clean.set_index('NCM')['NCM_Description'].to_dict()

# Map NCM descriptions in the combined dataframe
combined_df['NCM_Description'] = combined_df['NCM'].map(ncm_mapping)

# Save the final processed data with country names, NCM descriptions, and confidentiality flag
final_processed_file_path = os.path.join(data_dir, 'final_processed_export_data.csv')
combined_df.to_csv(final_processed_file_path, index=False, sep=';')

# Change the CSV separator from ; to ,
final_csv_path = os.path.join(data_dir, 'final_processed_export_data_comma.csv')
combined_df.to_csv(final_csv_path, index=False, sep=',')

# Display the first few rows of the processed data
print(combined_df.head())
```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\indec\R\indec_data_extraction.r (R)

```r
# Pacotes necessários
library(httr)     # Para requisições HTTP
library(readr)    # Para ler e escrever arquivos CSV
library(readxl)   # Para ler arquivos Excel
library(jsonlite) # Para manipular dados JSON
library(stringr)  # Para manipulação de strings
library(dplyr)    # Para manipulação de data frames
library(tidyr)    # Para limpeza de dados
library(lubridate) # Para manipulação de datas e horas

# Diretórios e Caminhos
BASE_DIR <- normalizePath(file.path(dirname(rstudioapi::getActiveDocumentContext()$path), '..', '..', '..'))
DATA_DIR <- file.path(BASE_DIR, 'data', 'indec')

# Garante que o diretório exista
if (!dir.exists(DATA_DIR)) {
  dir.create(DATA_DIR, recursive = TRUE)
}

# Função para baixar e extrair os dados de exportação para um ano específico
download_and_extract <- function(year, output_dir) {
  url <- sprintf("https://comex.indec.gob.ar/files/zips/exports_%d_M.zip", year)
  response <- GET(url)
  
  if (status_code(response) != 200) {
    stop("Falha no download do arquivo ZIP.")
  }
  
  temp <- tempfile()
  writeBin(content(response, "raw"), temp)
  unzip(temp, exdir = output_dir)
  unlink(temp)
  
  files <- list.files(output_dir, pattern = sprintf("expom%s.csv|exponm%s.csv|expopm%s.csv", substr(year, 3, 4), substr(year, 3, 4), substr(year, 3, 4)), full.names = TRUE)
  
  if (length(files) > 0) {
    new_file_path <- file.path(output_dir, sprintf("%d_%s", year, basename(files[1])))
    file.rename(files[1], new_file_path)
    message(sprintf("Arquivo '%s' extraído e salvo em: %s", basename(files[1]), new_file_path))
    return(new_file_path)
  }
  return(NULL)
}

# Função para baixar dados auxiliares (ex.: NCM ou países)
download_auxiliary_data <- function(url, output_file) {
  response <- GET(url)
  
  if (status_code(response) != 200) {
    stop("Falha no download dos dados auxiliares.")
  }
  
  writeBin(content(response, "raw"), output_file)
  message(sprintf("Dados auxiliares baixados e salvos em: %s", output_file))
}

# Limpa o diretório de saída (remover arquivos existentes)
clean_output_directory <- function(output_dir) {
  files <- list.files(output_dir, full.names = TRUE)
  if (length(files) > 0) {
    file.remove(files)
  }
}

# Função para limpar e processar os dados de exportação
clean_export_data <- function(df) {
  # Substitui vírgulas por pontos para conversão numérica
  df <- df %>%
    mutate(across(c('Pnet(kg)', 'FOB(u$s)'), ~ str_replace_all(., ",", "."))) %>%
    mutate(across(everything(), ~ str_trim(.)))  # Remove espaços em branco
  
  # Marca registros confidenciais
  df <- df %>%
    mutate(Confidential = ifelse(str_detect(`Pnet(kg)`, "s") | str_detect(`FOB(u$s)`, "s"), "Yes", "No")) %>%
    mutate(across(c('Pnet(kg)', 'FOB(u$s)'), ~ as.numeric(str_replace_all(., "s", ""))))
  
  return(df)
}

# Função principal para baixar, processar e salvar os dados do WASDE
fetch_and_process_data <- function() {
  clean_output_directory(DATA_DIR)
  
  # Baixa e extrai dados de exportação para os últimos 3 anos e o ano atual
  for (year in seq(from = year(Sys.Date()) - 3, to = year(Sys.Date()), by = 1)) {
    download_and_extract(year, DATA_DIR)
  }
  
  # Baixa dados auxiliares (NCM Excel e países JSON)
  ncm_excel_url <- "https://comex.indec.gob.ar/files/amendments/enmienda_VII(desde%202024).xlsx"
  countries_json_url <- "https://comexbe.indec.gob.ar/public-api/report/countries?current=en"
  
  ncm_excel_path <- file.path(DATA_DIR, 'ncm_data.xlsx')
  countries_json_path <- file.path(DATA_DIR, 'countries.json')
  
  download_auxiliary_data(ncm_excel_url, ncm_excel_path)
  
  response <- GET(countries_json_url)
  write(content(response, "text", encoding = "UTF-8"), file = countries_json_path)
  message(sprintf("Dados de países baixados e salvos em: %s", countries_json_path))
  
  # Carrega os dados de exportação e limpa os dados
  csv_files <- list.files(DATA_DIR, pattern = "\\.csv$", full.names = TRUE)
  export_data <- lapply(csv_files, function(file) {
    read_csv(file, delim = ";", locale = locale(encoding = "ISO-8859-1"))
  }) %>%
    bind_rows() %>%
    clean_export_data()
  
  # Carrega e mapeia nomes de países usando o arquivo JSON
  countries_data <- fromJSON(countries_json_path)$data
  country_mapping <- setNames(countries_data$nombre, countries_data$`_id`)
  export_data <- export_data %>%
    mutate(Pdes = as.character(Pdes), Country_Name = country_mapping[Pdes])
  
  # Carrega dados do NCM do Excel e mapeia as descrições
  ncm_data <- read_excel(ncm_excel_path, sheet = "NCM enm7", skip = 3) %>%
    select(NCM = I, NCM_Description = `SECCIÓN I - ANIMALES VIVOS Y PRODUCTOS DEL REINO ANIMAL`) %>%
    mutate(NCM = as.integer(str_remove_all(NCM, "\\.")))
  
  export_data <- export_data %>%
    left_join(ncm_data, by = "NCM")
  
  # Salva os dados processados em CSV
  final_processed_file_path <- file.path(DATA_DIR, 'final_processed_export_data.csv')
  write_csv(export_data, final_processed_file_path)
  message(sprintf("Dados processados salvos em: %s", final_processed_file_path))
  
  # Salva em um novo arquivo com separador de vírgula
  final_csv_path <- file.path(DATA_DIR, 'final_processed_export_data_comma.csv')
  write_csv(export_data, final_csv_path, delim = ",")
  message(sprintf("Dados processados com separador de vírgula salvos em: %s", final_csv_path))
  
  # Exibe as primeiras linhas do dataframe processado
  print(head(export_data))
}

# Execução principal
fetch_and_process_data()

```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\notion\Python\database_endpoint.py (Python)

```python
import requests
import csv
import json
import os
import logging
# Substitua pelo seu token real do Notion
NOTION_TOKEN = "insert your token here"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# Função para consultar o banco de dados do Notion
# Entrada: database_id - ID do banco de dados do Notion
# Saída: resposta JSON da consulta ao banco de dados ou None em caso de erro
def query_database(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    all_results = []
    payload = {}

    while True:
        response = requests.post(url, headers=headers, json=payload)
        logging.info(f"Querying database {database_id}, status code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            all_results.extend(data.get("results", []))

            if data.get("has_more") and data.get("next_cursor"):
                payload["start_cursor"] = data["next_cursor"]
            else:
                break
        else:
            logging.error(f"Error querying database {database_id}: {response.status_code}")
            return None

    return {"results": all_results}


# Função para recuperar o esquema de um banco de dados do Notion
# Entrada: database_id - ID do banco de dados do Notion
# Saída: resposta JSON do esquema do banco de dados ou None em caso de erro
def retrieve_database_schema(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Função para extrair dados de uma resposta do banco de dados do Notion usando o esquema fornecido
# Entrada: database_response - resposta da consulta ao banco de dados
#         schema - esquema do banco de dados
# Saída: lista de dados extraídos
def extract_data(database_response, schema):
    results = database_response.get("results", [])
    data = []
    for page in results:
        row = {}
        properties = page.get("properties", {})
        for key, value in properties.items():
            property_type = schema[key]["type"]
            if property_type == "title":
                row[key] = value["title"][0]["text"]["content"] if value["title"] else ""
            elif property_type == "rich_text":
                row[key] = value["rich_text"][0]["text"]["content"] if value["rich_text"] else ""
            elif property_type == "number":
                row[key] = value.get("number")
            elif property_type == "select":
                row[key] = value["select"].get("name") if value["select"] else ""
            elif property_type == "multi_select":
                row[key] = ", ".join([option["name"] for option in value["multi_select"]])
            elif property_type == "date":
                row[key] = value["date"].get("start") if value["date"] else ""
            elif property_type == "checkbox":
                row[key] = value["checkbox"]
            elif property_type == "relation":
                row[key] = ", ".join([relation["id"] for relation in value["relation"]])
            elif property_type == "phone_number":
                row[key] = value.get("phone_number", "")
            elif property_type == "email":
                row[key] = value.get("email", "")
            elif property_type == "url":
                row[key] = value.get("url", "")
            elif property_type == "status":
                row[key] = value["status"].get("name") if value["status"] else ""
            else:
                row[key] = None
        data.append(row)
    return data

# Função para salvar dados em um arquivo CSV
# Entrada: data - lista de dados a serem salvos
#         filename - nome do arquivo CSV
def save_to_csv(data, filename):
    if not data:
        logging.info("No data to save.")
        return

    keys = data[0].keys()
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    logging.info(f"Data saved to {filename}")

    # Generate preview text file
    with open(f"{filename}.txt", 'w', encoding='utf-8') as txt_file:
        for row in data[:10]:
            txt_file.write(str(row) + '\n')
    logging.info(f"Preview saved to {filename}.txt")

    # Print header types
    print("Header Types:")
    for key in keys:
        print(key)


# Função para salvar o esquema do banco de dados em um arquivo JSON
# Entrada: schema_response - resposta JSON do esquema do banco de dados
#         filename - nome do arquivo JSON
def save_schema_to_json(schema_response, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(schema_response, file, ensure_ascii=False, indent=4)
    print(f"Schema saved to {filename}")

# Função principal para processar um banco de dados do Notion
# Entrada: database_id - ID do banco de dados do Notion
def process_database(database_id):
    database_response = query_database(database_id)
    schema_response = retrieve_database_schema(database_id)

    if schema_response:
        schema = schema_response.get("properties", {})
        database_name = schema_response.get("title", [{"text": {"content": "Unknown"}}])[0]["text"]["content"]
        # Replace any invalid characters in the database name for safe filenames
        database_name_safe = "".join(x if x.isalnum() else "_" for x in database_name)

        save_schema_to_json(schema_response, filename=f"{database_name_safe}_schema.json")

    if database_response and schema:
        data = extract_data(database_response, schema)
        save_to_csv(data, filename=f"{database_name_safe}_data.csv")


if __name__ == "__main__":
    # Lista de IDs de bancos de dados a serem processados
    database_ids = ["d33518c356284b24a136da8e256d5c53", "b8a8cdea7b574dfcbc63535becdd9d5d","3dbe9a740286479f90513cb93cdeb614"]

    for db_id in database_ids:
        process_database(db_id)

```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\usda\Python\psd_api_usage.py (Python)

```python
import requests
import csv

# Constants
API_KEY = '697486e5-932d-46d3-804a-388452a19d70'
BASE_URL = 'https://apps.fas.usda.gov/OpenData/api/psd/'
OUTPUT_FILE = 'data/usda/commodity_forecast_2024.csv'

# Headers for the CSV output
HEADERS = [
    "commodityCode", "countryCode", "marketYear", "calendarYear", "month",
    "attributeId", "unitId", "commodityName", "attributeName", "unitDescription",
    "countryName", "regionName", "value"
]

# List of commodity codes and the year to query
COMMODITIES = ["0440000", "2631000"]
YEAR = 2024

# Helper function to make GET requests to the API
def get_api_data(endpoint):
    url = BASE_URL + endpoint
    headers = {
        'Accept': 'application/json',
        'API_KEY': API_KEY
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Fetch auxiliary data for regions, countries, commodities, attributes, and units
def fetch_auxiliary_data():
    regions = {item['regionCode']: item['regionName'] for item in get_api_data('regions')}
    countries = {item['countryCode']: (item['countryName'], regions.get(item['regionCode'], '')) for item in get_api_data('countries')}
    commodities = {item['commodityCode']: item['commodityName'] for item in get_api_data('commodities')}
    attributes = {item['attributeId']: item['attributeName'] for item in get_api_data('commodityAttributes')}
    units = {item['unitId']: item['unitDescription'].strip() for item in get_api_data('unitsOfMeasure')}
    
    return countries, commodities, attributes, units

# Fetch forecast data for a given commodity and year (both country and world level)
def fetch_forecast_data(commodity_code, year):
    country_data = get_api_data(f'commodity/{commodity_code}/country/all/year/{year}')
    world_data = get_api_data(f'commodity/{commodity_code}/world/year/{year}')
    
    # Merge country and world data
    all_data = country_data + world_data
    
    return all_data

# Process and write data to CSV
def process_and_write_data(countries, commodities, attributes, units):
    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(HEADERS)  # Write header row
        
        for commodity_code in COMMODITIES:
            forecast_data = fetch_forecast_data(commodity_code, YEAR)
            
            for record in forecast_data:
                commodity_name = commodities.get(record['commodityCode'], '')
                attribute_name = attributes.get(record['attributeId'], '')
                unit_description = units.get(record['unitId'], '')
                
                if record['countryCode'] == '00':  # World data
                    country_name = 'World'
                    region_name = 'Global'
                else:  # Country data
                    country_name, region_name = countries.get(record['countryCode'], ('', ''))
                
                row = [
                    record['commodityCode'], record['countryCode'], record['marketYear'], record['calendarYear'],
                    record['month'], record['attributeId'], record['unitId'], commodity_name, attribute_name,
                    unit_description, country_name, region_name, record['value']
                ]
                
                writer.writerow(row)

# Main function to run the script
def main():
    # Fetch auxiliary data
    countries, commodities, attributes, units = fetch_auxiliary_data()
    
    # Process and write data to CSV
    process_and_write_data(countries, commodities, attributes, units)
    
    print(f"Data successfully written to {OUTPUT_FILE}")

# Entry point of the script
if __name__ == "__main__":
    main()

```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\usda\Python\wasde_api_usage.py (Python)

```python
import requests
import csv
import os
from datetime import datetime, timedelta

# Constants
BASE_URL = "https://www.usda.gov/sites/default/files/documents/oce-wasde-report-data-"
OUTPUT_FILE = 'data/usda/wasde_data_2024.csv'
SELECTED_REPORTS = [
    "U.S. Wheat Supply and Use", "World Soybean Oil Supply and Use", "World Wheat Supply and Use",
    "Mexico Sugar Supply and Use and High Fructose Corn Syrup Consumption", "U.S. Cotton Supply and Use",
    "U.S. Wheat by Class: Supply and Use", "U.S. Soybeans and Products Supply and Use (Domestic Measure)",
    "World Cotton Supply and Use", "World Corn Supply and Use", "U.S. Feed Grain and Corn Supply and Use",
    "World and U.S. Supply and Use for Oilseeds", "World Soybean Supply and Use",
    "World and U.S. Supply and Use for Cotton", "World Soybean Meal Supply and Use"
]

# Generate URLs for all months in the current year up to the current month
def generate_csv_urls_for_current_year():
    current_date = datetime.now()
    csv_urls = []
    for month in range(1, current_date.month + 1):
        year_str = current_date.strftime("%Y")
        month_str = f"{month:02d}"
        csv_urls.append(BASE_URL + year_str + "-" + month_str + ".csv")
    return csv_urls

# Helper function to check if a report is in the selected reports list
def is_selected_report(report_title):
    return report_title in SELECTED_REPORTS

# Process and load CSV data
def process_csv_data(csv_url, output_file):
    try:
        response = requests.get(csv_url)
        response.raise_for_status()
        
        csv_content = response.text
        csv_lines = csv_content.splitlines()

        # Open output file in append mode
        with open(output_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Process each line of the CSV, skipping the header
            for line in csv_lines[1:]:
                data_fields = list(csv.reader([line]))[0]  # Parse CSV line
                if len(data_fields) == 16 and is_selected_report(data_fields[2]):
                    writer.writerow(data_fields)
        
        return True

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return False
    except Exception as err:
        print(f"An error occurred: {err}")
        return False

# Main function to fetch and load WASDE data for this year
def fetch_and_load_wasde_data_for_this_year():
    # Generate URLs for the current year up to this month
    csv_urls = generate_csv_urls_for_current_year()

    print("Fetching reports for the following URLs:")
    for url in csv_urls:
        print(url)

    # Process each CSV URL and load the data
    for url in csv_urls:
        if not process_csv_data(url, OUTPUT_FILE):
            print(f"Report not released for URL: {url}")
    
    print("Data loaded successfully.")

if __name__ == "__main__":
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # Run the data fetching process
    fetch_and_load_wasde_data_for_this_year()

```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\usda\R\psd_api_usage.r (R)

```r
# Pacotes necessários
library(httr)  # Para fazer as requisições HTTP
library(jsonlite)  # Para manipular os dados JSON
library(dplyr)  # Para manipulação de dados
library(purrr)  # Para manipulação funcional
library(readr)  # Para salvar os dados em CSV

# Constantes
API_KEY <- '697486e5-932d-46d3-804a-388452a19d70'
BASE_URL <- 'https://apps.fas.usda.gov/OpenData/api/psd/'
OUTPUT_FILE <- 'data/usda/commodity_forecast_2024.csv'

# Cabeçalhos para o arquivo CSV de saída
CABECALHOS <- c(
  "commodityCode", "countryCode", "marketYear", "calendarYear", "month",
  "attributeId", "unitId", "commodityName", "attributeName", "unitDescription",
  "countryName", "regionName", "value"
)

# Lista de códigos de commodities e o ano para consulta
COMMODITIES <- c("0440000", "2631000")
ANO <- 2024

# Função auxiliar para fazer as requisições GET à API
get_api_data <- function(endpoint) {
  url <- paste0(BASE_URL, endpoint)
  response <- GET(url, add_headers('Accept' = 'application/json', 'API_KEY' = API_KEY))
  stop_for_status(response)  # Verifica se a requisição foi bem-sucedida
  content(response, as = "text") %>% fromJSON(flatten = TRUE)  # Retorna o conteúdo JSON como lista
}

# Função para buscar dados auxiliares de regiões, países, commodities, atributos e unidades
fetch_auxiliary_data <- function() {
  # Cria dicionários (listas nomeadas) para mapear códigos aos nomes correspondentes
  regioes <- get_api_data('regions') %>% 
    setNames(.$regionName, .$regionCode)
  
  paises <- get_api_data('countries') %>% 
    transmute(countryCode, countryName = .$countryName, regionName = regioes[.$regionCode])
  
  commodities <- get_api_data('commodities') %>% 
    setNames(.$commodityName, .$commodityCode)
  
  atributos <- get_api_data('commodityAttributes') %>% 
    setNames(.$attributeName, .$attributeId)
  
  unidades <- get_api_data('unitsOfMeasure') %>% 
    setNames(trimws(.$unitDescription), .$unitId)
  
  list(paises = paises, commodities = commodities, atributos = atributos, unidades = unidades)
}

# Função para buscar dados de previsão para uma commodity e ano específico (tanto nível de país quanto global)
fetch_forecast_data <- function(commodity_code, ano) {
  dados_paises <- get_api_data(paste0('commodity/', commodity_code, '/country/all/year/', ano))
  dados_mundiais <- get_api_data(paste0('commodity/', commodity_code, '/world/year/', ano))
  
  # Mescla os dados de países e mundial
  bind_rows(dados_paises, dados_mundiais)
}

# Função para processar e salvar os dados no CSV
process_and_write_data <- function(paises, commodities, atributos, unidades) {
  # Abre o arquivo CSV para escrita
  write_csv(tibble(CABECALHOS), OUTPUT_FILE)  # Escreve o cabeçalho no arquivo
  
  # Itera sobre cada código de commodity
  walk(COMMODITIES, function(commodity_code) {
    forecast_data <- fetch_forecast_data(commodity_code, ANO)
    
    # Processa cada registro da previsão
    forecast_data %>% 
      mutate(
        commodityName = commodities[commodityCode],
        attributeName = atributos[attributeId],
        unitDescription = unidades[unitId],
        countryName = if_else(countryCode == "00", "World", paises$countryName[paises$countryCode == countryCode]),
        regionName = if_else(countryCode == "00", "Global", paises$regionName[paises$countryCode == countryCode])
      ) %>% 
      select(all_of(CABECALHOS)) %>% 
      write_csv(OUTPUT_FILE, append = TRUE)
  })
}

# Função principal para executar o script
main <- function() {
  # Busca os dados auxiliares
  dados_auxiliares <- fetch_auxiliary_data()
  
  # Processa e salva os dados no CSV
  process_and_write_data(dados_auxiliares$paises, dados_auxiliares$commodities, dados_auxiliares$atributos, dados_auxiliares$unidades)
  
  message(sprintf("Dados salvos com sucesso em %s", OUTPUT_FILE))
}

# Ponto de entrada do script
if (interactive()) {
  main()
}

```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\usda\R\wasde_api_usage.r (R)

```r
# Pacotes necessários
library(httr)  # Para fazer as requisições HTTP
library(readr)  # Para manipulação de arquivos CSV
library(stringr)  # Para manipulação de strings
library(lubridate)  # Para manipulação de datas e horas

# Constantes
BASE_URL <- "https://www.usda.gov/sites/default/files/documents/oce-wasde-report-data-"
OUTPUT_FILE <- 'data/usda/wasde_data_2024.csv'
SELECTED_REPORTS <- c(
  "U.S. Wheat Supply and Use", "World Soybean Oil Supply and Use", "World Wheat Supply and Use",
  "Mexico Sugar Supply and Use and High Fructose Corn Syrup Consumption", "U.S. Cotton Supply and Use",
  "U.S. Wheat by Class: Supply and Use", "U.S. Soybeans and Products Supply and Use (Domestic Measure)",
  "World Cotton Supply and Use", "World Corn Supply and Use", "U.S. Feed Grain and Corn Supply and Use",
  "World and U.S. Supply and Use for Oilseeds", "World Soybean Supply and Use",
  "World and U.S. Supply and Use for Cotton", "World Soybean Meal Supply and Use"
)

# Função para gerar URLs dos CSVs para todos os meses do ano corrente até o mês atual
generate_csv_urls_for_current_year <- function() {
  current_date <- Sys.Date()
  current_year <- year(current_date)
  current_month <- month(current_date)
  
  csv_urls <- vector("character", current_month)  # Vetor para armazenar URLs dos CSVs
  
  for (month in 1:current_month) {
    month_str <- sprintf("%02d", month)  # Formata o mês com dois dígitos
    csv_urls[month] <- paste0(BASE_URL, current_year, "-", month_str, ".csv")
  }
  
  return(csv_urls)
}

# Função auxiliar para verificar se um relatório está na lista de relatórios selecionados
is_selected_report <- function(report_title) {
  return(report_title %in% SELECTED_REPORTS)
}

# Função para processar e carregar dados do CSV
process_csv_data <- function(csv_url, output_file) {
  tryCatch({
    # Faz a requisição HTTP para o CSV
    response <- GET(csv_url)
    stop_for_status(response)  # Verifica se a requisição foi bem-sucedida
    
    # Lê o conteúdo do CSV
    csv_content <- content(response, as = "text")
    csv_lines <- str_split(csv_content, "\n")[[1]]  # Divide o conteúdo em linhas
    
    # Abre o arquivo de saída em modo de adição (append)
    file_conn <- file(output_file, open = "a", encoding = "UTF-8")
    
    # Processa cada linha do CSV, ignorando o cabeçalho
    for (line in csv_lines[-1]) {
      data_fields <- read_csv(line, col_names = FALSE, show_col_types = FALSE)
      
      # Verifica se a linha tem 16 campos e se o relatório está na lista selecionada
      if (ncol(data_fields) == 16 && is_selected_report(data_fields[[3]])) {
        write_csv(data_fields, file_conn, append = TRUE)  # Escreve a linha no arquivo de saída
      }
    }
    
    close(file_conn)  # Fecha a conexão com o arquivo
    return(TRUE)
    
  }, error = function(e) {
    # Captura erros de requisição HTTP e outros erros
    message("Ocorreu um erro: ", e$message)
    return(FALSE)
  })
}

# Função principal para buscar e carregar os dados do WASDE para o ano corrente
fetch_and_load_wasde_data_for_this_year <- function() {
  # Gera URLs dos CSVs até o mês atual
  csv_urls <- generate_csv_urls_for_current_year()
  
  message("Buscando relatórios para as seguintes URLs:")
  print(csv_urls)
  
  # Processa cada URL de CSV e carrega os dados
  for (url in csv_urls) {
    if (!process_csv_data(url, OUTPUT_FILE)) {
      message("Relatório não lançado para a URL: ", url)
    }
  }
  
  message("Dados carregados com sucesso.")
}

# Executa o script principal
if (interactive()) {
  # Garante que o diretório de saída exista
  dir.create(dirname(OUTPUT_FILE), recursive = TRUE, showWarnings = FALSE)
  
  # Inicia o processo de busca e carregamento dos dados
  fetch_and_load_wasde_data_for_this_year()
}

```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\usda\VBA\DB_GRÃOS-USDA_PSD.vba (VBA)

```vba
' API Key and Base URL
Const API_KEY As String = "697486e5-932d-46d3-804a-388452a19d70"
Const BASE_URL As String = "https://apps.fas.usda.gov/OpenData/api/psd/"

' Main Sub to Update All Data
Sub UpdateAllData()
    ' Step 1: Check if the table is up-to-date
    If Not ConfirmUpdate() Then Exit Sub
    
    ' Step 2: Update auxiliary tables
    UpdateRegions
    UpdateCountries
    UpdateCommodities
    UpdateUnitsOfMeasure
    UpdateCommodityAttributes
    
    ' Step 3: Fetch forecast data and update the final table
    UpdateFinalTable
    
    ' Step 4: Update the last update date in Home sheet
    UpdateLastUpdateDate
End Sub

' Function to confirm if update is necessary
Function ConfirmUpdate() As Boolean
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("Hist - USDA - PSD - Vertical")

    ' Find the most recent calendar year and month in the table
    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, "D").End(xlUp).row ' Assuming calendarYear is in column D

    Dim mostRecentYear As Long
    Dim mostRecentMonth As Long
    mostRecentYear = ws.Cells(lastRow, 4).value ' Column D for calendarYear
    mostRecentMonth = ws.Cells(lastRow, 5).value ' Column E for month

    ' Get the current year and month
    Dim currentYear As Long
    Dim currentMonth As Long
    currentYear = Year(Date)
    currentMonth = Month(Date)

    ' Check if the most recent entry matches the current year and month
    If mostRecentYear = currentYear And mostRecentMonth = currentMonth Then
        Dim userResponse As VbMsgBoxResult
        userResponse = MsgBox("The data appears to be up-to-date for the current month and year. Do you still want to proceed with the update?", vbYesNo + vbQuestion, "Confirm Update")
        
        If userResponse = vbNo Then
            ConfirmUpdate = False
            Exit Function
        End If
    End If

    ConfirmUpdate = True
End Function

' Function to Make HTTP GET Requests
Function GetAPIData(endpoint As String) As Object
    Dim http As Object
    Set http = CreateObject("MSXML2.XMLHTTP")

    Dim url As String
    url = BASE_URL & endpoint

    Debug.Print "Constructed URL: " & url ' Print the URL to the Immediate Window

    http.Open "GET", url, False
    http.setRequestHeader "Accept", "application/json"
    http.setRequestHeader "API_KEY", API_KEY
    http.send

    If http.Status = 200 Then
        Set GetAPIData = JsonConverter.ParseJson(http.responseText)
    Else
        MsgBox "Failed to fetch data from " & endpoint & ": " & http.Status & " " & http.StatusText
        Set GetAPIData = Nothing
    End If
End Function

' Update Regions
Sub UpdateRegions()
    Dim data As Object
    Set data = GetAPIData("regions")

    If Not data Is Nothing Then
        Dim ws As Worksheet
        Set ws = ThisWorkbook.Sheets("Tabelas AUX - USDA - PSD")

        ' Load data into an array
        Dim arr() As Variant
        ReDim arr(1 To data.Count, 1 To 2)

        Dim i As Long
        For i = 1 To data.Count
            arr(i, 1) = data(i)("regionCode")
            arr(i, 2) = data(i)("regionName")
        Next i

        ' Sort the array by the second column (Region Name)
        Call SortArray(arr, 2)

        ' Write the sorted data back to the worksheet
        Call WriteArrayToSheet(ws, arr, "O", "P")
    End If
End Sub

' Update Countries
Sub UpdateCountries()
    Dim data As Object
    Set data = GetAPIData("countries")

    If Not data Is Nothing Then
        Dim ws As Worksheet
        Set ws = ThisWorkbook.Sheets("Tabelas AUX - USDA - PSD")

        ' Load data into an array
        Dim arr() As Variant
        ReDim arr(1 To data.Count, 1 To 4)

        Dim i As Long
        For i = 1 To data.Count
            arr(i, 1) = data(i)("countryCode")
            arr(i, 2) = data(i)("countryName")
            arr(i, 3) = data(i)("regionCode")
            arr(i, 4) = data(i)("gencCode")
        Next i

        ' Sort the array by the second column (Country Name)
        Call SortArray(arr, 2)

        ' Write the sorted data back to the worksheet
        Call WriteArrayToSheet(ws, arr, "J", "M")
    End If
End Sub

' Update Commodities
Sub UpdateCommodities()
    Dim data As Object
    Set data = GetAPIData("commodities")

    If Not data Is Nothing Then
        Dim ws As Worksheet
        Set ws = ThisWorkbook.Sheets("Tabelas AUX - USDA - PSD")

        ' Load data into an array
        Dim arr() As Variant
        ReDim arr(1 To data.Count, 1 To 2)

        Dim i As Long
        For i = 1 To data.Count
            ' Append a single quote to force Excel to treat the value as text
            arr(i, 1) = "'" & CStr(data(i)("commodityCode"))
            arr(i, 2) = data(i)("commodityName")
        Next i

        ' Sort the array by the second column (Commodity Name)
        Call SortArray(arr, 2)

        ' Write the sorted data back to the worksheet
        Call WriteArrayToSheet(ws, arr, "A", "B")
    End If
End Sub

' Update Units of Measure
Sub UpdateUnitsOfMeasure()
    Dim data As Object
    Set data = GetAPIData("unitsOfMeasure")

    If Not data Is Nothing Then
        Dim ws As Worksheet
        Set ws = ThisWorkbook.Sheets("Tabelas AUX - USDA - PSD")

        ' Load data into an array
        Dim arr() As Variant
        ReDim arr(1 To data.Count, 1 To 2)

        Dim i As Long
        For i = 1 To data.Count
            arr(i, 1) = data(i)("unitId")
            arr(i, 2) = data(i)("unitDescription")
        Next i

        ' Sort the array by the second column (Unit Description)
        Call SortArray(arr, 2)

        ' Write the sorted data back to the worksheet
        Call WriteArrayToSheet(ws, arr, "G", "H")
    End If
End Sub

' Update Commodity Attributes
Sub UpdateCommodityAttributes()
    Dim data As Object
    Set data = GetAPIData("commodityAttributes")

    If Not data Is Nothing Then
        Dim ws As Worksheet
        Set ws = ThisWorkbook.Sheets("Tabelas AUX - USDA - PSD")

        ' Load data into an array
        Dim arr() As Variant
        ReDim arr(1 To data.Count, 1 To 2)

        Dim i As Long
        For i = 1 To data.Count
            arr(i, 1) = data(i)("attributeId")
            arr(i, 2) = data(i)("attributeName")
        Next i

        ' Sort the array by the second column (Attribute Name)
        Call SortArray(arr, 2)

        ' Write the sorted data back to the worksheet
        Call WriteArrayToSheet(ws, arr, "D", "E")
    End If
End Sub

' Main Sub to Update the Final Table
Sub UpdateFinalTable()
    Dim highlightedCommodities As Collection
    Dim highlightedAttributes As Scripting.Dictionary ' Use Scripting.Dictionary here
    
    ' Step 1: Get highlighted commodities and attributes
    Set highlightedCommodities = GetHighlightedCommodities()
    Set highlightedAttributes = GetHighlightedAttributes() ' This returns a Scripting.Dictionary
    
    ' Step 2: Prompt user for the first year and validate the input
    Dim startYear As Long
    Dim currentYear As Long
    Dim yearDifference As Long
    
    currentYear = Year(Date)
    
    ' Prompt user for the starting year
    startYear = Application.InputBox("Please enter the first year for the update (e.g., 2010):", "Start Year", 2010, Type:=1)
    
    ' Validate the input
    If startYear < 1960 Or startYear > currentYear Then
        MsgBox "Please enter a valid year between 1960 and " & currentYear, vbExclamation
        Exit Sub
    End If
    
    ' Check if the year range is more than 3 years
    yearDifference = currentYear - startYear
    If yearDifference > 3 Then
        Dim proceed As VbMsgBoxResult
        proceed = MsgBox("You have selected more than 3 years. This may result in slow performance and overhead in Excel. Do you want to proceed?", vbExclamation + vbYesNo, "Warning")
        If proceed = vbNo Then Exit Sub
    End If
    
    ' Step 3: Initialize a single-dimension array for storing the final data
    Dim finalData() As Variant
    Dim rowCount As Long
    rowCount = 0 ' Initial row count
    
    ' Loop through highlighted commodities and the selected range of years
    Dim commodityCode As String
    Dim item As Variant
    Dim marketYear As Long
    
    For Each item In highlightedCommodities
        commodityCode = item
        
        ' Loop through the years from the user-selected start year to the current year
        For marketYear = startYear To currentYear
            ' Fetch country-level and world-level data for this commodity and year
            Call FetchAndAppendData(commodityCode, marketYear, highlightedAttributes, finalData, rowCount)
        Next marketYear
    Next item
    
    ' Step 4: Write the final data array to the target sheet
    WriteDataToFinalTable finalData, rowCount
    
    ' Step 5: Update the date in the "Home" sheet after completion
    ThisWorkbook.Sheets("Home").Range("H3").value = Date
End Sub


' Fetch and append data for a specific commodity and year
Sub FetchAndAppendData(commodityCode As String, marketYear As Long, highlightedAttributes As Scripting.Dictionary, ByRef finalData() As Variant, ByRef rowCount As Long)
    Dim countryData As Object
    Dim worldData As Object
    
    ' Remove the leading quote from the commodity code for the API call
    commodityCode = Replace(commodityCode, "'", "")
    
    ' Fetch data for the commodity (country level and world level)
    Set countryData = GetAPIData("commodity/" & commodityCode & "/country/all/year/" & CStr(marketYear))
    Set worldData = GetAPIData("commodity/" & commodityCode & "/world/year/" & CStr(marketYear))
    
    ' Append country-level data to the finalData array
    If Not countryData Is Nothing Then
        Call AppendDataToFinalArray(countryData, highlightedAttributes, finalData, rowCount, False)
    End If
    
    ' Append world-level data to the finalData array
    If Not worldData Is Nothing Then
        Call AppendDataToFinalArray(worldData, highlightedAttributes, finalData, rowCount, True)
    End If
End Sub

' Function to append data to the final single-dimension array, joining with auxiliary data
Sub AppendDataToFinalArray(data As Object, highlightedAttributes As Scripting.Dictionary, ByRef finalData() As Variant, ByRef rowCount As Long, isWorldData As Boolean)
    Dim wsAux As Worksheet
    Set wsAux = ThisWorkbook.Sheets("Tabelas AUX - USDA - PSD")
    
    Dim i As Long
    Const numColumns As Long = 13 ' Number of columns
    
    For i = 1 To data.Count
        ' Only process if the attribute is highlighted
        If highlightedAttributes.Exists(data(i)("attributeId")) Then
            ' Increment the row count
            rowCount = rowCount + 1
            
            ' Resize the finalData array to hold the new row of data
            ReDim Preserve finalData(1 To rowCount * numColumns)
            
            ' Populate the finalData array (flattened structure)
            finalData((rowCount - 1) * numColumns + 1) = data(i)("commodityCode")
            
            ' Handle World Data
            If isWorldData Then
                finalData((rowCount - 1) * numColumns + 2) = "WO" ' Set country code as World (WO)
                finalData((rowCount - 1) * numColumns + 11) = "World" ' Set country name as World
                finalData((rowCount - 1) * numColumns + 12) = "Global" ' Set region name as Global
            Else
                ' Handle Regular Data
                finalData((rowCount - 1) * numColumns + 2) = data(i)("countryCode")
                finalData((rowCount - 1) * numColumns + 11) = GetAuxValue(data(i)("countryCode"), wsAux, "J", "K") ' Fetch country name
                finalData((rowCount - 1) * numColumns + 12) = GetRegionName(CStr(data(i)("countryCode")), wsAux) ' Fetch region name
            End If
            
            ' Common fields
            finalData((rowCount - 1) * numColumns + 3) = data(i)("marketYear")
            finalData((rowCount - 1) * numColumns + 4) = data(i)("calendarYear")
            finalData((rowCount - 1) * numColumns + 5) = data(i)("month")
            finalData((rowCount - 1) * numColumns + 6) = data(i)("attributeId")
            finalData((rowCount - 1) * numColumns + 7) = data(i)("unitId")
            finalData((rowCount - 1) * numColumns + 8) = GetAuxValue(data(i)("commodityCode"), wsAux, "A", "B") ' Commodity name
            finalData((rowCount - 1) * numColumns + 9) = GetAuxValue(data(i)("attributeId"), wsAux, "D", "E") ' Attribute name
            finalData((rowCount - 1) * numColumns + 10) = GetAuxValue(data(i)("unitId"), wsAux, "G", "H") ' Unit description
            finalData((rowCount - 1) * numColumns + 13) = data(i)("value")
        End If
    Next i
End Sub



' Write the final single-dimension array to the final table
Sub WriteDataToFinalTable(finalData() As Variant, rowCount As Long)
    Dim wsFinal As Worksheet
    Set wsFinal = ThisWorkbook.Sheets("Hist - USDA - PSD - Vertical")
    
    ' Only proceed if there is data to write
    If rowCount > 0 Then
        Dim i As Long, j As Long
        Dim numColumns As Long
        numColumns = 13 ' The fixed number of columns
        
        ' Write the data row by row
        For i = 1 To rowCount
            For j = 1 To numColumns
                wsFinal.Cells(i + 2, j).value = finalData((i - 1) * numColumns + j)
            Next j
        Next i
    End If
End Sub

' Function to get highlighted commodities from Tabelas AUX - USDA - PSD
Function GetHighlightedCommodities() As Collection
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("Tabelas AUX - USDA - PSD")
    
    Dim highlighted As New Collection
    Dim i As Long
    
    ' Loop through column A for highlighted commodities
    For i = 3 To ws.Cells(ws.Rows.Count, "A").End(xlUp).row
        If ws.Cells(i, 1).Interior.Color = RGB(255, 165, 0) Then ' Orange highlight
            highlighted.Add ws.Cells(i, 1).value
        End If
    Next i
    
    Set GetHighlightedCommodities = highlighted
End Function

' Function to get highlighted attributes from Tabelas AUX - USDA - PSD
Function GetHighlightedAttributes() As Scripting.Dictionary
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("Tabelas AUX - USDA - PSD")
    
    Dim highlighted As New Scripting.Dictionary
    Dim i As Long
    
    ' Loop through column D for highlighted attributes
    For i = 3 To ws.Cells(ws.Rows.Count, "D").End(xlUp).row
        If ws.Cells(i, 4).Interior.Color = RGB(255, 165, 0) Then ' Orange highlight
            highlighted.Add ws.Cells(i, 4).value, True
        End If
    Next i
    
    Set GetHighlightedAttributes = highlighted
End Function

' Function to get value from auxiliary table
Function GetAuxValue(key As Variant, ws As Worksheet, lookupCol As String, returnCol As String) As String
    Dim rng As Range
    Set rng = ws.Range(lookupCol & "3:" & lookupCol & ws.Cells(ws.Rows.Count, lookupCol).End(xlUp).row)
    
    Dim cell As Range
    Set cell = rng.Find(What:=CStr(key), LookIn:=xlValues, LookAt:=xlWhole) ' Convert key to string
    
    If Not cell Is Nothing Then
        GetAuxValue = cell.Offset(0, ws.Range(returnCol & "1").Column - ws.Range(lookupCol & "1").Column).value
    Else
        GetAuxValue = "" ' Handle the case where no match is found
    End If
End Function



' Function to retrieve region name using country code
Function GetRegionName(countryCode As String, ws As Worksheet) As String
    Dim countryRng As Range, regionRng As Range
    Dim countryCell As Range, regionCell As Range
    Dim regionCode As String
    
    ' Step 1: Find the country code in the countries table (columns J to L)
    Set countryRng = ws.Range("J3:J" & ws.Cells(ws.Rows.Count, "J").End(xlUp).row)
    Set countryCell = countryRng.Find(countryCode, LookIn:=xlValues, LookAt:=xlWhole)
    
    If Not countryCell Is Nothing Then
        ' Step 2: Retrieve the corresponding region code (column L)
        regionCode = countryCell.Offset(0, 2).value
        
        ' Step 3: Find the region code in the regions table (columns O to P)
        Set regionRng = ws.Range("O3:O" & ws.Cells(ws.Rows.Count, "O").End(xlUp).row)
        Set regionCell = regionRng.Find(regionCode, LookIn:=xlValues, LookAt:=xlWhole)
        
        If Not regionCell Is Nothing Then
            ' Step 4: Retrieve the corresponding region name (column P)
            GetRegionName = regionCell.Offset(0, 1).value
        Else
            GetRegionName = "" ' Region code not found
        End If
    Else
        GetRegionName = "" ' Country code not found
    End If
End Function

' Function to update the last update date in Home sheet
Sub UpdateLastUpdateDate()
    Dim wsHome As Worksheet
    Set wsHome = ThisWorkbook.Sheets("Home")
    
    ' Update cell H3 with the current date
    wsHome.Range("H3").value = Date
End Sub

' Function to sort a 2D array by a specified column
Sub SortArray(ByRef arr As Variant, ByVal sortColumn As Long)
    Dim i As Long, j As Long
    Dim temp As Variant

    For i = LBound(arr, 1) To UBound(arr, 1) - 1
        For j = i + 1 To UBound(arr, 1)
            If arr(i, sortColumn) > arr(j, sortColumn) Then
                ' Swap entire rows
                temp = arr(i, 1)
                arr(i, 1) = arr(j, 1)
                arr(j, 1) = temp
                
                temp = arr(i, 2)
                arr(i, 2) = arr(j, 2)
                arr(j, 2) = temp

                ' Continue swapping for additional columns if present
                If UBound(arr, 2) > 2 Then
                    Dim k As Long
                    For k = 3 To UBound(arr, 2)
                        temp = arr(i, k)
                        arr(i, k) = arr(j, k)
                        arr(j, k) = temp
                    Next k
                End If
            End If
        Next j
    Next i
End Sub

' Function to write array data to a worksheet while preserving formulas
Sub WriteArrayToSheet(ws As Worksheet, arr As Variant, startCol As String, endCol As String)
    Dim i As Long, j As Long
    Dim startRow As Long
    startRow = 3 ' Start writing data from row 3

    ' Loop through the array and write data to the worksheet, skipping cells with formulas
    For i = LBound(arr, 1) To UBound(arr, 1)
        For j = 1 To UBound(arr, 2)
            If Not ws.Cells(i + startRow - 1, j + ws.Range(startCol & "1").Column - 1).HasFormula Then
                ws.Cells(i + startRow - 1, j + ws.Range(startCol & "1").Column - 1).value = arr(i, j)
            End If
        Next j
    Next i
End Sub


```


## c:\Users\lnonino\OneDrive - DATAGRO\Documentos\GitHub\Data Extracion Tools\extraction\usda\VBA\DB_GRÃOS-USDA_WASDE.vba (VBA)

```vba
Sub FetchAndLoadWASDEDataForMissingDates()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("Hist - USDA - WASDE - Vertical")

    ' Turn off screen updating and automatic calculation to improve performance
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    On Error GoTo CleanUp

    ' Find the most recent date in the ReportDate column (Column B)
    Dim lastRow As Long
    Dim lastReportDate As Date
    lastRow = ws.Cells(ws.Rows.Count, "B").End(xlUp).row
    lastReportDate = ws.Cells(lastRow, "B").value ' Assuming the date is in Column B

    ' Get the current date
    Dim currentDate As Date
    currentDate = Date

    ' If the most recent date matches the current month and year, show a message and exit
    If Format(lastReportDate, "mm/yyyy") = Format(currentDate, "mm/yyyy") Then
        MsgBox "Current data is up to date.", vbInformation
        GoTo CleanUp
    End If

    ' Generate URLs for the CSV files between the most recent report date and the current date
    Dim csvUrls As Collection
    Set csvUrls = GenerateCSVUrls(lastReportDate, currentDate)

    ' Prompt the user with the list of URLs that will be fetched
    Dim url As Variant
    Dim urlList As String
    For Each url In csvUrls
        urlList = urlList & url & vbCrLf
    Next url

    Dim userResponse As VbMsgBoxResult
    userResponse = MsgBox("The following reports will be fetched:" & vbCrLf & urlList & vbCrLf & "Do you want to proceed?", vbYesNo + vbQuestion, "Confirm Report Fetch")

    If userResponse = vbNo Then GoTo CleanUp

    ' List of selected reports
    Dim selectedReports As Variant
    selectedReports = Array("U.S. Wheat Supply and Use", "World Soybean Oil Supply and Use", "World Wheat Supply and Use", _
                            "Mexico Sugar Supply and Use and High Fructose Corn Syrup Consumption", "U.S. Cotton Supply and Use", _
                            "U.S. Wheat by Class: Supply and Use", "U.S. Soybeans and Products Supply and Use (Domestic Measure)", _
                            "World Cotton Supply and Use", "World Corn Supply and Use", "U.S. Feed Grain and Corn Supply and Use", _
                            "World and U.S. Supply and Use for Oilseeds", "World Soybean Supply and Use", "World and U.S. Supply and Use for Cotton", _
                            "World Soybean Meal Supply and Use")

    ' Loop through each CSV URL and process data
    For Each url In csvUrls
        If Not ProcessCSVData(url, ws, selectedReports) Then
            MsgBox "Report not released for URL: " & url, vbExclamation
        End If
    Next url

    MsgBox "Data loaded successfully.", vbInformation

CleanUp:
    ' Restore screen updating and calculation
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic

    ' Error handling
    If Err.Number <> 0 Then
        MsgBox "An error occurred: " & Err.Description, vbExclamation
    End If
End Sub

Function GenerateCSVUrls(startDate As Date, endDate As Date) As Collection
    Dim csvUrls As New Collection
    Dim currentDate As Date
    Dim yearStr As String, monthStr As String
    Dim baseUrl As String

    baseUrl = "https://www.usda.gov/sites/default/files/documents/oce-wasde-report-data-"

    ' Start generating URLs from the month after the most recent date in the table
    currentDate = DateAdd("m", 1, startDate)
    
    ' Loop through each month and year in the specified date range
    Do While currentDate <= endDate
        yearStr = Format(currentDate, "yyyy")
        monthStr = Format(currentDate, "mm")
        
        ' Generate the URL for the current month and year
        csvUrls.Add baseUrl & yearStr & "-" & monthStr & ".csv"
        
        ' Move to the next month
        currentDate = DateAdd("m", 1, currentDate)
    Loop

    Set GenerateCSVUrls = csvUrls
End Function



Function ProcessCSVData(ByVal csvURL As String, ws As Worksheet, selectedReports As Variant) As Boolean
    On Error GoTo CleanUp

    ' Download CSV data
    Dim http As Object
    Set http = CreateObject("MSXML2.XMLHTTP")
    http.Open "GET", csvURL, False
    http.send

    If http.Status <> 200 Then
        ' Skip if the CSV is not found or cannot be downloaded
        ProcessCSVData = False
        Exit Function
    End If

    ' Split CSV content into lines
    Dim csvContent As String
    csvContent = http.responseText
    Dim csvLines() As String
    csvLines = Split(csvContent, vbCrLf)

    ' Variables to process CSV data
    Dim i As Long
    Dim dataFields() As String
    Dim rowCount As Long
    Dim dataArray As Variant
    Dim dataIndex As Long

    ' Prepare array to store data (optimize for bulk writing)
    ReDim dataArray(1 To UBound(csvLines), 1 To 16)
    dataIndex = 1
    rowCount = ws.Cells(ws.Rows.Count, "A").End(xlUp).row + 1 ' Start from the next available row

    ' Process each line of the CSV (skipping the header)
    For i = 1 To UBound(csvLines) ' Skip the first line which is the header
        If Len(Trim(csvLines(i))) > 0 Then
            dataFields = ParseCSVLine(csvLines(i))
            
            ' Ensure that the line has the expected number of fields (16 in this case)
            If UBound(dataFields) = 15 Then
                ' Check if the report title is in the selected reports list
                If IsInArray(Trim(dataFields(2)), selectedReports) Then
                    ' Store the data in the array
                    dataArray(dataIndex, 1) = dataFields(0)
                    dataArray(dataIndex, 2) = dataFields(1)
                    dataArray(dataIndex, 3) = dataFields(2)
                    dataArray(dataIndex, 4) = dataFields(3)
                    dataArray(dataIndex, 5) = dataFields(4)
                    dataArray(dataIndex, 6) = dataFields(5)
                    dataArray(dataIndex, 7) = dataFields(6)
                    dataArray(dataIndex, 8) = dataFields(7)
                    dataArray(dataIndex, 9) = dataFields(8)
                    dataArray(dataIndex, 10) = dataFields(9)
                    dataArray(dataIndex, 11) = dataFields(10)
                    dataArray(dataIndex, 12) = dataFields(11)
                    dataArray(dataIndex, 13) = dataFields(12)
                    dataArray(dataIndex, 14) = dataFields(13)
                    dataArray(dataIndex, 15) = dataFields(14)
                    dataArray(dataIndex, 16) = dataFields(15)
                    dataIndex = dataIndex + 1
                End If
            End If
        End If
    Next i

    ' Write the entire array to the worksheet in one go
    If dataIndex > 1 Then
        ws.Range("A" & rowCount).Resize(dataIndex - 1, 16).value = dataArray
    End If

    ProcessCSVData = True

CleanUp:
    ' Clean up
    Set http = Nothing

    If Err.Number <> 0 Then
        MsgBox "An error occurred: " & Err.Description, vbExclamation
    End If
End Function

Function ParseCSVLine(ByVal csvLine As String) As Variant
    Dim fields As Collection
    Set fields = New Collection
    Dim currentField As String
    Dim inQuotes As Boolean
    Dim i As Long

    inQuotes = False
    currentField = ""

    For i = 1 To Len(csvLine)
        Dim currentChar As String
        currentChar = Mid(csvLine, i, 1)

        If currentChar = """" Then
            ' Toggle the inQuotes flag when encountering a quote
            inQuotes = Not inQuotes
        ElseIf currentChar = "," And Not inQuotes Then
            ' If not inside quotes, treat the comma as a field delimiter
            fields.Add currentField
            currentField = ""
        Else
            ' Append character to the current field
            currentField = currentField & currentChar
        End If
    Next i

    ' Add the last field
    fields.Add currentField

    ' Convert collection to array
    Dim arr() As String
    ReDim arr(0 To fields.Count - 1)
    For i = 1 To fields.Count
        arr(i - 1) = fields(i)
    Next i

    ParseCSVLine = arr
End Function

Function IsInArray(value As String, arr As Variant) As Boolean
    Dim i As Long
    For i = LBound(arr) To UBound(arr)
        If arr(i) = value Then
            IsInArray = True
            Exit Function
        End If
    Next i
    IsInArray = False
End Function



```
