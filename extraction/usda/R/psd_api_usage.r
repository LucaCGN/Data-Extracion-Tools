# Required Libraries
library(httr)    # For HTTP requests
library(jsonlite) # For JSON data manipulation
library(dplyr)   # For data manipulation
library(purrr)   # For functional programming tools
library(readr)   # For writing CSV files
library(stringr) # For string manipulation

# Constants
API_KEY <- '697486e5-932d-46d3-804a-388452a19d70'
BASE_URL <- 'https://apps.fas.usda.gov/OpenData/api/psd/'
OUTPUT_FILE <- 'data/usda/commodity_forecast_2024.csv'

# CSV Headers
CABECALHOS <- c(
  "commodityCode", "countryCode", "marketYear", "calendarYear", "month",
  "attributeId", "unitId", "commodityName", "attributeName", "unitDescription",
  "countryName", "regionName", "value"
)

# Commodity Codes and Year
COMMODITIES <- c("0440000", "2631000", "0813700", "0813300", "0814200", 
                 "0813800", "0813200", "0813600", "0813100", "0813500", 
                 "4242000", "4233000", "4235000", "4243000", "4244000", 
                 "4234000", "4239100", "4232000", "4236000", "2231000", 
                 "2223000", "2232000", "2221000", "2226000", "2222000", 
                 "2224000", "0410000")
ANO <- 2024

# Function to perform GET requests
get_api_data <- function(endpoint) {
  url <- paste0(BASE_URL, endpoint)
  response <- GET(url, add_headers('Accept' = 'application/json', 'API_KEY' = API_KEY))
  stop_for_status(response)  # Check if the request was successful
  content(response, as = "text") %>% fromJSON(flatten = TRUE)  # Return the JSON content as a list
}

# Function to retrieve auxiliary data
fetch_auxiliary_data <- function() {
  regioes <- get_api_data('regions') %>% 
    with(setNames(regionName, regionCode))
  
  paises <- get_api_data('countries') %>% 
    mutate(regionName = regioes[regionCode]) %>% 
    select(countryCode, countryName, regionName)
  
  commodities <- get_api_data('commodities') %>% 
    with(setNames(commodityName, commodityCode))
  
  atributos <- get_api_data('commodityAttributes') %>% 
    mutate(attributeId = as.character(attributeId),
           attributeName = str_trim(attributeName)) %>%
    with(setNames(attributeName, attributeId))
  
  unidades <- get_api_data('unitsOfMeasure') %>% 
    mutate(unitId = as.character(unitId)) %>%
    with(setNames(str_trim(unitDescription), unitId))
  
  # Debugging: Print out the auxiliary data to check for completeness and correctness
  message("Auxiliary data fetched: ")
  print(atributos)
  
  list(paises = paises, commodities = commodities, atributos = atributos, unidades = unidades)
}

# Function to fetch forecast data
fetch_forecast_data <- function(commodity_code, ano) {
  dados_paises <- get_api_data(paste0('commodity/', commodity_code, '/country/all/year/', ano))
  dados_mundiais <- get_api_data(paste0('commodity/', commodity_code, '/world/year/', ano))
  
  # Combine country-level and world-level data
  bind_rows(dados_paises, dados_mundiais)
}

# Function to process and save the data
process_and_write_data <- function(paises, commodities, atributos, unidades) {
  write_csv(tibble(), OUTPUT_FILE, col_names = FALSE)  # Create an empty file
  write_lines(paste(CABECALHOS, collapse = ","), OUTPUT_FILE)  # Write headers
  
  walk(COMMODITIES, function(commodity_code) {
    forecast_data <- fetch_forecast_data(commodity_code, ANO) %>%
      mutate(attributeId = as.character(attributeId))  # Ensure IDs are treated as characters
    
    # Debugging: Print unmatched IDs before the join
    unmatched_ids <- setdiff(unique(forecast_data$attributeId), names(atributos))
    if (length(unmatched_ids) > 0) {
      message("Unmatched attribute IDs found: ", paste(unmatched_ids, collapse = ", "))
    }
    
    # Join forecast data with auxiliary data
    forecast_data <- forecast_data %>%
      left_join(paises, by = "countryCode") %>%
      mutate(
        commodityName = commodities[commodityCode],
        attributeName = atributos[attributeId],
        unitDescription = unidades[unitId],
        countryName = if_else(countryCode == "00", "World", countryName),
        regionName = if_else(countryCode == "00", "Global", regionName)
      )
    
    # Debugging: Check for NA values in attributeName after the join
    na_attributes <- forecast_data %>% filter(is.na(attributeName))
    if (nrow(na_attributes) > 0) {
      message("NA attributeNames found after join:")
      print(na_attributes)
    }
    
    # Select columns and save to CSV
    forecast_data %>%
      select(all_of(CABECALHOS)) %>%
      write_csv(OUTPUT_FILE, append = TRUE, col_names = FALSE)
  })
}

# Main function
main <- function() {
  dados_auxiliares <- fetch_auxiliary_data()
  process_and_write_data(dados_auxiliares$paises, dados_auxiliares$commodities, 
                         dados_auxiliares$atributos, dados_auxiliares$unidades)
  message(sprintf("Data successfully saved to %s", OUTPUT_FILE))
}

# Entry point
if (interactive()) {
  main()
}
