import re


def normalize_whitespace(text: str) -> str:
    """
    Normaliza espacios y saltos de línea.
    """
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fix_hyphen_line_breaks(text: str) -> str:
    """
    Une palabras cortadas por salto de línea con guion:
    Ej: 'monetary-\npolicy' → 'monetary policy'
    """
    return re.sub(r"-\s*\n\s*", "", text)


def fix_line_break_words(text: str) -> str:
    """
    Reemplaza saltos de línea por espacios.
    """
    return re.sub(r"\n+", " ", text)


def fix_spaced_letters(text: str) -> str:
    """
    Reconstruye palabras con letras separadas por espacios.
    Ej: 'E L E C T R O N' → 'ELECTRON'
    """
    pattern = r"(?:\b(?:[A-Za-z]\s){2,}[A-Za-z]\b)"

    def replace_match(match):
        return match.group(0).replace(" ", "")

    return re.sub(pattern, replace_match, text)


def fix_camel_case_and_joined_words(text: str) -> str:
    """
    Separa palabras pegadas por cambios de minúscula a mayúscula.
    Ej: 'LaintegraciónEuropea' → 'Laintegración Europea'
    """
    return re.sub(
        r"(?<=[a-záéíóúñ])(?=[A-ZÁÉÍÓÚÑ])",
        " ",
        text
    )


def remove_pdf_noise(text: str) -> str:
    """
    Limpia ruido típico de PDFs sin ser demasiado agresivo.
    """

    # Eliminar patrones tipo /G69/G67
    text = re.sub(r"/[A-Za-z0-9]+", " ", text)

    # Eliminar caracteres no deseados manteniendo puntuación básica
    text = re.sub(r"[^\w\s\.\,\;\:\-\(\)]", " ", text)

    # Eliminar espacios duplicados generados por limpieza anterior
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_text(text: str) -> str:
    """
    Pipeline de limpieza optimizado para PDFs en RAG.

    Orden lógico:
    1. Limpieza de ruido PDF
    2. Corrección de guiones de fin de línea
    3. Unificación de saltos de línea
    4. Reconstrucción de palabras con letras separadas
    5. Separación de palabras pegadas por mayúsculas
    6. Normalización final de espacios
    """

    if not text:
        return ""

    # 1. Limpieza base
    text = remove_pdf_noise(text)

    # 2. Correcciones estructurales
    text = fix_hyphen_line_breaks(text)
    text = fix_line_break_words(text)

    # 3. Reconstrucciones ligeras
    text = fix_spaced_letters(text)
    text = fix_camel_case_and_joined_words(text)

    # 4. Normalización final
    text = normalize_whitespace(text)

    return text


def clean_documents(documents: list) -> list:
    """
    Aplica limpieza a documentos de ingesta.
    Añade campo 'clean_text'.
    """
    cleaned_docs = []

    for doc in documents:
        cleaned_docs.append({
            **doc,
            "clean_text": clean_text(doc["text"])
        })

    return cleaned_docs


if __name__ == "__main__":
    from src.ingestion.load_documents import load_pdfs

    docs = load_pdfs()

    for doc in docs[:2]:
        print("\nSOURCE:", doc["source"])

        print("\n--- RAW ---")
        print(doc["text"][:300])

        print("\n--- CLEAN ---")
        print(clean_text(doc["text"])[:300])

        print("\n" + "-" * 80)