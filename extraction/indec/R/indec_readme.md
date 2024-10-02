# Processamento de Dados de Exportação do INDEC com R

## Visão Geral

Este projeto em R automatiza o download, processamento e limpeza dos dados de exportação fornecidos pelo INDEC (Instituto Nacional de Estadística y Censos da Argentina). O script baixa os arquivos CSV de exportação anuais, bem como dados auxiliares, processa as informações e salva os dados limpos em arquivos CSV para análise posterior.

### Funcionalidades

1. **Download de Arquivos de Exportação**: O script baixa e extrai os dados de exportação do INDEC para os últimos três anos e o ano corrente.
2. **Download de Dados Auxiliares**: Também baixa dados auxiliares, como códigos NCM (Nomenclatura Comum do Mercosul) em formato Excel e dados de países em formato JSON.
3. **Processamento de Dados**: Os dados baixados são processados, incluindo a conversão de números, remoção de espaços em branco e tratamento de valores confidenciais.
4. **Mapeamento de Nomes de Países e Descrições de NCM**: Os códigos de países e NCM são mapeados para seus nomes e descrições correspondentes.
5. **Salvamento de Dados Limpos**: Os dados processados são salvos em arquivos CSV, incluindo versões com separadores de ponto e vírgula (`;`) e vírgula (`,`).

## Estrutura do Projeto

O script automatiza todo o processo de download, limpeza e processamento de dados, garantindo que os dados estejam prontos para análise.

### Diretórios e Caminhos

- **BASE_DIR**: Diretório base onde o script está localizado.
- **DATA_DIR**: Diretório onde os arquivos baixados e processados são salvos.

### Funcionalidades do Script

1. **`download_and_extract(year, output_dir)`**:
   - Baixa e extrai os arquivos ZIP de exportação do INDEC para um ano específico.
   - Renomeia os arquivos CSV para incluir o ano no nome.

2. **`download_auxiliary_data(url, output_file)`**:
   - Baixa dados auxiliares (por exemplo, NCM ou países) de uma URL especificada e salva o arquivo.

3. **`clean_export_data(df)`**:
   - Limpa os dados de exportação baixados.
   - Substitui vírgulas por pontos para conversão numérica, remove espaços em branco e marca registros confidenciais.

4. **`fetch_and_process_data()`**:
   - Função principal que orquestra o fluxo de trabalho:
     - Baixa e extrai os dados de exportação.
     - Baixa os dados auxiliares (NCM e países).
     - Processa os arquivos CSV.
     - Mapeia códigos de NCM e países para seus respectivos nomes e descrições.
     - Salva os dados limpos em arquivos CSV.

## Requisitos

Para executar este projeto, você precisará dos seguintes pacotes R:

- **httr**: Para fazer requisições HTTP e baixar arquivos.
- **readr**: Para ler e escrever arquivos CSV.
- **readxl**: Para ler arquivos Excel (dados NCM).
- **jsonlite**: Para manipulação de dados JSON (dados de países).
- **stringr**: Para manipulação de strings.
- **dplyr**: Para manipulação de data frames.
- **tidyr**: Para limpeza de dados.
- **lubridate**: Para manipulação de datas e horas.

Você pode instalar esses pacotes usando o seguinte comando no R:

```r
install.packages(c("httr", "readr", "readxl", "jsonlite", "stringr", "dplyr", "tidyr", "lubridate"))
```

## Como Usar

### Passo 1: Configuração do Ambiente

Certifique-se de ter instalado todos os pacotes R mencionados na seção de "Requisitos". Depois, configure seu ambiente de trabalho no R para garantir que o script funcione corretamente.

### Passo 2: Executar o Script

Para executar o script, simplesmente execute a função principal `fetch_and_process_data()` no R:

```r
fetch_and_process_data()
```

O script irá:

1. Baixar os dados de exportação dos últimos 3 anos e do ano corrente.
2. Baixar dados auxiliares (NCM e países).
3. Processar e limpar os dados.
4. Salvar os dados processados em arquivos CSV.

### Passo 3: Verificação dos Dados

Após a execução, os dados limpos estarão salvos nos seguintes arquivos:

- **`final_processed_export_data.csv`**: Dados processados com separador de ponto e vírgula (`;`).
- **`final_processed_export_data_comma.csv`**: Dados processados com separador de vírgula (`,`).

Esses arquivos estarão localizados no diretório `data/indec`.

## Personalização

Você pode ajustar o período de anos para o qual deseja baixar dados modificando a lógica dentro da função `fetch_and_process_data()`.

Se precisar adicionar novos dados auxiliares ou modificar o processamento de dados, você pode ajustar as funções `download_auxiliary_data()` e `clean_export_data()` conforme necessário.

## Considerações Finais

Este script foi desenvolvido para automatizar o processo de download e processamento dos dados de exportação do INDEC, permitindo que você se concentre na análise dos dados. O uso de pacotes R como `httr`, `readr`, `jsonlite` e `dplyr` garante que o fluxo de trabalho seja eficiente e fácil de adaptar a novos requisitos.
