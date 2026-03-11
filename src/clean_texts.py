import os
import re

PROCESSED_DIR = r"C:\\Users\\lugod\\Downloads\\ecorag\\data\\processed"
CLEAN_DIR = r"C:\\Users\\lugod\\Downloads\\ecorag\\data\\processed\\cleaned"

os.makedirs(CLEAN_DIR, exist_ok=True)

for txt_file in os.listdir(PROCESSED_DIR):
    if txt_file.endswith(".txt"):
        with open(os.path.join(PROCESSED_DIR, txt_file), "r", encoding="utf-8") as f:
            text = f.read()

        # Limpieza básica
        text = re.sub(r'\n+', '\n', text)          # quita saltos de línea múltiples
        text = re.sub(r'\s+', ' ', text)           # quita espacios múltiples
        text = text.strip()                         # quita espacios al inicio y fin
        text = re.sub(r'[^ -~áéíóúÁÉÍÓÚñÑüÜ]+', '', text)  # caracteres extraños, deja letras y símbolos básicos

        with open(os.path.join(CLEAN_DIR, txt_file), "w", encoding="utf-8") as f:
            f.write(text)

print("Limpieza de textos completada.")