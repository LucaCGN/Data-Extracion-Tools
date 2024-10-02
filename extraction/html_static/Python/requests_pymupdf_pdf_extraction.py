import os
import requests
import fitz  # PyMuPDF

# Define project root and output directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
output_dir = os.path.join(project_root, 'data', 'html_static')

def download_pdf(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"PDF downloaded successfully: {save_path}")
        return save_path
    except Exception as e:
        print(f"Failed to download PDF: {e}")
        return None

def extract_text_from_pdf(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)
        text = ""
        for page in pdf_document:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Failed to extract text from PDF: {e}")
        return None

def save_extracted_text(text, method, url):
    file_name = f"{method}_{url.replace('https://', '').replace('/', '_')}.txt"
    save_path = os.path.join(output_dir, file_name)
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Extracted text saved to {save_path}")

# Example usage
pdf_url = "https://www.fhfa.gov/sites/default/files/2024-07/FHFA-HPI-Monthly-07302024.pdf"  # Replace with an actual link
pdf_save_path = os.path.join(output_dir, 'fhfa_report.pdf')
pdf_path = download_pdf(pdf_url, pdf_save_path)
if pdf_path:
    text = extract_text_from_pdf(pdf_path)
    if text:
        save_extracted_text(text, 'requests_pymupdf_pdf_extraction', pdf_url)
