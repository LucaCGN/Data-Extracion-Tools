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