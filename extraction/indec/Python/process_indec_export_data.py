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