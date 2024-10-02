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
