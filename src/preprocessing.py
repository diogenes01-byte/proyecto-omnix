# src/preprocessing.py
import os
import pdfplumber

RAW_DIR = "C:\\Users\\lugod\\Downloads\\ecorag\\data\\raw"
PROCESSED_DIR = "C:\\Users\\lugod\\Downloads\\ecorag\\data\\processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)

for filename in os.listdir(RAW_DIR):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(RAW_DIR, filename)
        text_path = os.path.join(PROCESSED_DIR, filename.replace(".pdf", ".txt"))

        with pdfplumber.open(pdf_path) as pdf:
            full_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(full_text)

print("Extracción de PDFs completada.")