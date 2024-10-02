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
