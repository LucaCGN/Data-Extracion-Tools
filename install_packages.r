# Lista de pacotes necessários
required_packages <- c(
  "httr",        # Para requisições HTTP
  "jsonlite",    # Para manipulação de dados JSON
  "readr",       # Para ler e escrever arquivos CSV
  "dplyr",       # Para manipulação de data frames
  "purrr",       # Para manipulação funcional
  "stringr",     # Para manipulação de strings
  "lubridate",   # Para manipulação de datas e horas
  "readxl",      # Para leitura de arquivos Excel
  "tidyr",       # Para limpeza de dados
  "rstudioapi"   # Para interação com RStudio (e.g., pegar caminho do script)
)

# Função para instalar pacotes que ainda não estão instalados
install_if_missing <- function(package) {
  if (!require(package, character.only = TRUE)) {
    install.packages(package)
    library(package, character.only = TRUE)
  }
}

# Instalação dos pacotes
lapply(required_packages, install_if_missing)

# Mensagem final
message("Todos os pacotes necessários foram instalados e carregados com sucesso.")
