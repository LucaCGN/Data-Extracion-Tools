

# Data Extraction - Tools & Examples (Versão em Portugûes Abaixo)

This repository contains a comprehensive collection of tools and code examples for data extraction from various sources, focusing on automation, processing, and data integration. The code examples cover different programming languages, such as Python, R, and VBA, and address data sources that include APIs, dynamic and static HTML, WebSockets, and static files like PDFs.

## Repository Structure

The repository is divided into several modules, each designed for a specific use case:

### 1. **extraction/bcb** (Central Bank of Brazil)
- **Python**: This module uses the `bcb` library to extract data from the Central Bank of Brazil's Market Expectations. The code makes API calls to different endpoints and saves the data in CSV files.
  - **Python Libraries**: `pandas`, `os`, `bcb`
  
- **R**: Utilizes the `rbcb` package to access time series from the Central Bank, with functions for data manipulation and graphical visualizations.
  - **R Libraries**: `rbcb`, `dplyr`, `ggplot2`, `zoo`

### 2. **extraction/comex** (Brazilian Trade Balance)
- **Python**: A set of scripts that download, filter, and enrich trade balance data. It uses asynchronous HTTP requests to download large volumes of data and process them in chunks, optimizing memory usage.
  - **Python Libraries**: `aiohttp`, `pandas`, `os`, `logging`, `asyncio`, `requests`, `aiofiles`

### 3. **extraction/html_dynamic** (Dynamic HTML Data Extraction)
- **Python**: Examples of automating navigation with `Selenium` for handling dynamic pages, such as executing JavaScript, managing pop-ups, and extracting data using XPath.
  - **Python Libraries**: `selenium`, `webdriver_manager`, `os`, `pandas`, `time`, `datetime`

### 4. **extraction/html_static** (Static HTML Data Extraction)
- **Python**: Scripts that use `BeautifulSoup` for parsing static HTML pages and extracting specific content, such as links to PDF files and data in structured text.
  - **Python Libraries**: `requests`, `beautifulsoup4`, `fake_useragent`, `PyMuPDF`, `re`

### 5. **extraction/html_feed** (WebSocket Data Extraction)
- **Python**: Example of using WebSockets to collect real-time data from Binance, such as cryptocurrency prices. The script listens to real-time feeds and saves the received data.
  - **Python Libraries**: `websockets`, `asyncio`, `pandas`, `json`

### 6. **extraction/indec** (Argentina's Foreign Trade)
- **Python**: Scripts for downloading and processing Argentina's foreign trade data using the INDEC website.
  - **Python Libraries**: `requests`, `pandas`, `os`, `json`, `re`, `zipfile`, `io`
  
- **R**: R script that handles downloading, extracting, and cleaning Argentina's export data.
  - **R Libraries**: `httr`, `readr`, `jsonlite`, `dplyr`, `tidyr`, `readxl`, `lubridate`, `stringr`

### 7. **extraction/notion** (Integration with Notion)
- **Python**: Scripts that interact with the Notion API to query and extract data from Notion databases. Uses the Notion REST API to retrieve structured data and save it in CSV format.
  - **Python Libraries**: `requests`, `json`, `csv`, `os`, `logging`

### 8. **extraction/usda** (United States Department of Agriculture - USDA)
- **Python**: Scripts for interacting with the USDA's PSD and WASDE APIs to obtain forecasts and market data.
  - **Python Libraries**: `requests`, `csv`, `os`, `datetime`
  
- **R**: Scripts that use the USDA's PSD API to extract data on commodities and markets.
  - **R Libraries**: `httr`, `jsonlite`, `dplyr`, `purrr`, `readr`
  
- **VBA**: Macros that interact with the USDA's APIs to automatically update Excel spreadsheets with the latest data.

-------

# Data Extraction - Tools & Examples

Este repositório contém uma coleção abrangente de ferramentas e exemplos de código para extração de dados de diversas fontes, com foco em automação, processamento e integração de dados. Os exemplos de código cobrem diferentes linguagens de programação, como Python, R e VBA, e abordam fontes de dados que incluem APIs, HTML dinâmico e estático, WebSockets e arquivos estáticos, como PDFs.

## Estrutura do Repositório

O repositório é dividido em vários módulos, cada um projetado para um caso de uso específico:

### 1. **extraction/bcb** (Banco Central do Brasil)
   - **Python**: Este módulo utiliza a biblioteca `bcb` para extrair dados das Expectativas de Mercado do Banco Central do Brasil. O código realiza chamadas à API para diferentes endpoints e salva os dados em arquivos CSV.
     - **Bibliotecas Python**: `pandas`, `os`, `bcb`
   
   - **R**: Utiliza o pacote `rbcb` para acessar séries temporais do Banco Central, com funções para manipulação de dados e visualizações gráficas.
     - **Bibliotecas R**: `rbcb`, `dplyr`, `ggplot2`, `zoo`

### 2. **extraction/comex** (Balança Comercial Brasileira)
   - **Python**: Conjunto de scripts que fazem o download, filtragem e enriquecimento de dados da balança comercial. Utiliza requisições HTTP assíncronas para baixar grandes volumes de dados e processá-los em chunks, otimizando o uso de memória.
     - **Bibliotecas Python**: `aiohttp`, `pandas`, `os`, `logging`, `asyncio`, `requests`, `aiofiles`

### 3. **extraction/html_dynamic** (Extração de Dados HTML Dinâmicos)
   - **Python**: Exemplos de automação de navegação com `Selenium` para manipulação de páginas dinâmicas, como execução de JavaScript, manipulação de pop-ups e extração de dados através de XPath.
     - **Bibliotecas Python**: `selenium`, `webdriver_manager`, `os`, `pandas`, `time`, `datetime`
   
### 4. **extraction/html_static** (Extração de Dados HTML Estáticos)
   - **Python**: Scripts que utilizam `BeautifulSoup` para parsing de páginas HTML estáticas e extração de conteúdo específico, como links para arquivos PDF e dados em textos estruturados.
     - **Bibliotecas Python**: `requests`, `beautifulsoup4`, `fake_useragent`, `PyMuPDF`, `re`

### 5. **extraction/html_feed** (WebSocket Data Extraction)
   - **Python**: Exemplo de uso de WebSockets para coletar dados em tempo real do Binance, como preços de criptomoedas. O script escuta os feeds em tempo real e salva os dados recebidos.
     - **Bibliotecas Python**: `websockets`, `asyncio`, `pandas`, `json`

### 6. **extraction/indec** (Comércio Exterior da Argentina)
   - **Python**: Scripts para download e processamento de dados do comércio exterior da Argentina, utilizando o site do INDEC.
     - **Bibliotecas Python**: `requests`, `pandas`, `os`, `json`, `re`, `zipfile`, `io`
   
   - **R**: Script em R que lida com o download, extração e limpeza dos dados de exportação da Argentina.
     - **Bibliotecas R**: `httr`, `readr`, `jsonlite`, `dplyr`, `tidyr`, `readxl`, `lubridate`, `stringr`
   
### 7. **extraction/notion** (Integração com Notion)
   - **Python**: Scripts que interagem com a API do Notion para consulta e extração de dados de bancos de dados do Notion. Utiliza a API REST do Notion para recuperar dados estruturados e salvá-los em CSV.
     - **Bibliotecas Python**: `requests`, `json`, `csv`, `os`, `logging`

### 8. **extraction/usda** (Departamento de Agricultura dos Estados Unidos - USDA)
   - **Python**: Scripts para interação com as APIs PSD e WASDE do USDA, para obtenção de previsões e dados de mercado.
     - **Bibliotecas Python**: `requests`, `csv`, `os`, `datetime`
   
   - **R**: Scripts que utilizam a API PSD do USDA para extração de dados sobre commodities e mercados.
     - **Bibliotecas R**: `httr`, `jsonlite`, `dplyr`, `purrr`, `readr`
   
   - **VBA**: Macros que interagem com as APIs do USDA para atualizar automaticamente planilhas do Excel com os dados mais recentes.
  
