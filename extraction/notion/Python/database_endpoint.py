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
