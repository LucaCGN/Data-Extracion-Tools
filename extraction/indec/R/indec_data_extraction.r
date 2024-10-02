# Função principal para baixar, processar e salvar os dados do INDEC
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
  
  export_data_list <- lapply(csv_files, function(file) {
    df <- read_delim(file, delim = ";", locale = locale(encoding = "ISO-8859-1"))
    
    # Remove linhas que contêm totais ou sumários
    df <- df %>%
      filter(!grepl("Total", df$`Pnet(kg)`, ignore.case = TRUE))
    
    # Retorna o data frame processado
    df
  })
  
  # Combina os data frames, assegurando que tenham as mesmas colunas
  export_data <- bind_rows(export_data_list) %>%
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
