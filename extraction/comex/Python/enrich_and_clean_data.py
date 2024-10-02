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