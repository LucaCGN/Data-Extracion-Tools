# Extração de Dados da API PSD do USDA com R

## Visão Geral

Este projeto em R realiza a extração de dados de previsões de commodities da API PSD (Production, Supply, and Distribution) do USDA (Departamento de Agricultura dos Estados Unidos). Ele consome dados da API no formato JSON e os processa para gerar um arquivo CSV contendo previsões de commodities. O principal objetivo é demonstrar como interagir com uma API RESTful, consumir dados JSON e processá-los em R.

### API PSD do USDA

A API PSD do USDA oferece informações sobre produção, oferta e distribuição de commodities agrícolas globalmente. Os principais endpoints incluem:

- **Regiões** (`/api/psd/regions`): Retorna dados sobre as regiões globais.
- **Países** (`/api/psd/countries`): Fornece informações sobre os países e as regiões às quais pertencem.
- **Commodities** (`/api/psd/commodities`): Retorna uma lista de commodities com seus códigos correspondentes.
- **Unidades de Medida** (`/api/psd/unitsOfMeasure`): Lista unidades de medida com seus IDs.
- **Atributos de Commodities** (`/api/psd/commodityAttributes`): Retorna os atributos usados nas previsões das commodities, como "Área Plantada" e "Produção".

A API também permite acessar previsões específicas para commodities por país e ano.

### Estrutura dos Dados JSON

Os dados retornados pela API do USDA estão no formato JSON. Em R, utilizamos pacotes como `jsonlite` para manipular essas estruturas e convertê-las em data frames.

#### Exemplo de Estrutura JSON (Regiões):

```json
[
  {
    "regionCode": "R00",
    "regionName": "World"
  },
  {
    "regionCode": "R01",
    "regionName": "North America"
  }
]
```

Esses dados podem ser convertidos em um data frame no R para facilitar a manipulação.

## Requisitos

Para executar este projeto, você precisará dos seguintes pacotes R instalados:

- **httr**: Para fazer requisições HTTP.
- **jsonlite**: Para manipulação de dados JSON.
- **dplyr**: Para manipulação de data frames.
- **purrr**: Para manipulação funcional.
- **readr**: Para salvar dados em arquivos CSV.

Você pode instalar esses pacotes com o seguinte código:

```r
install.packages(c("httr", "jsonlite", "dplyr", "purrr", "readr"))
```

## Uso da API PSD com R

### Autenticação

Para acessar a API, você precisará de uma chave de API (API_KEY). No código, essa chave é armazenada em uma constante:

```r
API_KEY <- 'sua-chave-api-aqui'
```

A chave é usada em todas as requisições HTTP para autenticar o acesso.

### Estrutura do Código

#### 1. **Função `get_api_data(endpoint)`**

Essa função faz uma requisição GET ao endpoint da API e retorna o conteúdo no formato de lista R (convertido a partir do JSON).

Exemplo:

```r
# Faz uma requisição ao endpoint de regiões
regioes <- get_api_data('regions')
```

#### 2. **Função `fetch_auxiliary_data()`**

Esta função recupera os dados auxiliares de regiões, países, commodities, atributos e unidades de medida. Esses dados são essenciais para mapear os códigos (por exemplo, códigos de países e commodities) aos seus respectivos nomes.

Exemplo:

```r
# Recupera todos os dados auxiliares
dados_auxiliares <- fetch_auxiliary_data()
```

#### 3. **Função `fetch_forecast_data(commodity_code, ano)`**

Esta função faz requisições à API para obter previsões de uma commodity específica em um determinado ano, tanto para dados de países quanto para dados globais.

Exemplo:

```r
# Busca previsões para a commodity "0440000" no ano de 2024
previsao <- fetch_forecast_data("0440000", 2024)
```

#### 4. **Função `process_and_write_data()`**

Essa função processa os dados de previsão e os salva no arquivo CSV final. Ela combina os dados de previsão com as informações auxiliares, como nomes de países e regiões.

Exemplo:

```r
# Processa e salva os dados em um arquivo CSV
process_and_write_data(dados_auxiliares$paises, dados_auxiliares$commodities, dados_auxiliares$atributos, dados_auxiliares$unidades)
```

#### 5. **Função Principal `main()`**

A função `main` coordena a execução do script: obtém os dados auxiliares, processa as previsões e salva os resultados em um arquivo CSV.

### Salvando os Dados

Os dados processados são salvos em um arquivo CSV especificado pela constante `OUTPUT_FILE`. Este arquivo contém todas as previsões de commodities para o ano de 2024, incluindo informações como código da commodity, país, região, unidade de medida e valores das previsões.

### Cabeçalhos de Saída Corretamente Formatados

Após uma execução bem-sucedida, o arquivo CSV de saída terá os seguintes cabeçalhos, seguidos pelos dados extraídos da API:

```csv
commodityCode, countryCode, marketYear, calendarYear, month, attributeId, unitId, commodityName, attributeName, unitDescription, countryName, regionName, value
```

## Exemplo de Execução

Para executar o código, basta rodar a função principal:

```r
main()
```

Após a execução, os dados serão salvos no arquivo `data/usda/commodity_forecast_2024.csv`.

## Considerações Finais

Este projeto demonstra como consumir uma API RESTful em R, manipular dados JSON e salvá-los em um formato estruturado. Ao utilizar pacotes como `httr`, `jsonlite`, `dplyr`, `purrr` e `readr`, o processamento de grandes volumes de dados de APIs se torna uma tarefa simples e eficiente em R.

### Boas Práticas

O código segue boas práticas de programação em R, como uso consistente de espaços, indentação e nomes de funções e variáveis descritivos. Essas práticas ajudam a garantir que o código seja legível e fácil de manter no longo prazo.

