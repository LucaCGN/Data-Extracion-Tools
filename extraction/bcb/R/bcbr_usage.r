# Pacotes necessários
library(rbcb)   # Para acessar dados do Banco Central do Brasil
library(dplyr)  # Para manipulação de dados
library(ggplot2) # Para visualização dos dados

# Função para buscar séries temporais do Banco Central
# Este exemplo busca a série do IPCA (Índice de Preços ao Consumidor Amplo)
buscar_serie_temporal <- function(codigo_serie) {
  # A função get_series() obtém a série temporal especificada pelo código da série
  dados <- get_series(codigo_serie)
  
  # Retorna os dados baixados
  return(dados)
}

# Função para processar e plotar a série temporal
processar_e_plotar <- function(dados, titulo) {
  # Exibe os primeiros registros dos dados
  head(dados)
  
  # Processamento: vamos calcular a média móvel de 12 meses
  dados <- dados %>%
    mutate(media_movel = zoo::rollmean(value, k = 12, fill = NA))
  
  # Plotando a série temporal e a média móvel
  ggplot(dados, aes(x = date, y = value)) +
    geom_line(color = "blue", size = 1) +
    geom_line(aes(y = media_movel), color = "red", linetype = "dashed") +
    labs(title = titulo, x = "Data", y = "Valor") +
    theme_minimal()
}

# Função principal para buscar, processar e plotar uma série temporal do BCB
principal <- function() {
  # Código da série temporal do IPCA (Índice de Preços ao Consumidor Amplo)
  codigo_ipca <- 433
  
  # Busca os dados da série temporal
  dados_ipca <- buscar_serie_temporal(codigo_ipca)
  
  # Processa e plota a série temporal
  processar_e_plotar(dados_ipca, "IPCA - Índice de Preços ao Consumidor Amplo")
}

# Executa o script principal
principal()