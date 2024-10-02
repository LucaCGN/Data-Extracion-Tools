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
