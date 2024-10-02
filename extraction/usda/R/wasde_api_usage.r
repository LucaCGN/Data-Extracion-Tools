# Pacotes necessários
library(httr)  # Para fazer as requisições HTTP
library(readr)  # Para manipulação de arquivos CSV
library(stringr)  # Para manipulação de strings
library(lubridate)  # Para manipulação de datas e horas
library(dplyr)  # Para manipulação de data frames

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

# Função para processar e carregar dados do CSV
process_csv_data <- function(csv_url, output_file) {
  tryCatch({
    # Faz a requisição HTTP para o CSV
    response <- GET(csv_url)
    stop_for_status(response)  # Verifica se a requisição foi bem-sucedida
    
    # Lê o CSV inteiro como um data frame
    csv_content <- content(response, as = "text", encoding = "UTF-8")
    data <- read_csv(csv_content, col_names = TRUE, show_col_types = FALSE)
    
    # Exibe as primeiras linhas e os nomes das colunas para entender o conteúdo
    print("Colunas encontradas no CSV:")
    print(names(data))
    print("Primeiras linhas do CSV:")
    print(head(data))
    
    # Filtra as linhas com os relatórios desejados (verifique o nome exato da coluna de título)
    # Ajuste "Report Title" para o nome correto da coluna no CSV.
    filtered_data <- data %>% filter(`ReportTitle` %in% SELECTED_REPORTS)
    
    # Verifica se há dados para salvar
    if (nrow(filtered_data) > 0) {
      # Salva o arquivo CSV no modo de adição (append)
      write_csv(filtered_data, output_file, append = TRUE)
    }
    
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
