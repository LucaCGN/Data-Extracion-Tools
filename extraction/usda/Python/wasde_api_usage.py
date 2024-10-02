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
