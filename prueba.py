import re
import fitz  # PyMuPDF
import json

# Redondea el tamaño de letra a unidades
def round_font_size(size):
    return round(size)

# Inicializar variables
data = []
current_chapter = None
current_title = None
current_text = ""
current_section = None
current_page_text = ""

# Regex para detectar 'CHAPTER' seguido de un número de una o dos cifras
CHAPTER_REGEX = r"^CHAPTER\s\d{1,2}$"
TITLE_SIZE_THRESHOLD = 25
TEXT_SIZE = 10
SECTION_SIZE_THRESHOLD = 19

def process_page(page):
    global current_chapter, current_title, current_text, current_section, current_page_text

    # Variables para esta página
    title_detected = False
    last_font_size = None

    for char in page.get_text("dict")["blocks"]:
        for line in char.get("lines", []):
            for span in line.get("spans", []):
                text = span.get('text', '')
                font_size = round_font_size(span.get('size', 0))
                top = span.get('bbox', [0, 0, 0, 0])[1]

                # Detectar capítulo basado en regex
                if re.match(CHAPTER_REGEX, text):
                    # Si hay un capítulo anterior, guarda su información
                    if current_chapter:
                        data_entry = {
                            "chapter": current_chapter,
                            "title": current_title,
                            "section": current_section,
                            "text": current_text.strip()  # Strip para eliminar espacios finales
                        }
                        data.append(data_entry)

                    # Iniciar un nuevo capítulo
                    current_chapter = text
                    current_title = None
                    current_text = ""
                    current_section = None
                    title_detected = False
                    current_page_text = ""
                    last_font_size = None
                    print(f"Detected chapter: {current_chapter}")

                if font_size >= TITLE_SIZE_THRESHOLD:
                    # Detectar y acumular título
                    if not title_detected:
                        current_title = text
                        title_detected = True
                        print(f"Starting new title: {current_title}")
                    else:
                        current_title += " " + text
                    last_font_size = font_size

                elif font_size == TEXT_SIZE:
                    # Guardar texto si se detecta un cambio de tamaño de fuente
                    if last_font_size == SECTION_SIZE_THRESHOLD and current_section:
                        # Guardar sección si hubo un cambio de tamaño
                        if current_text:
                            data_entry = {
                                "chapter": current_chapter,
                                "title": current_title,
                                "section": current_section,
                                "text": current_text.strip()  # Strip para eliminar espacios finales
                            }
                            data.append(data_entry)
                        current_text = current_page_text.strip()
                        current_page_text = ""
                    current_page_text += " " + text
                    last_font_size = font_size

                elif font_size == SECTION_SIZE_THRESHOLD:
                    # Guardar sección y texto
                    if last_font_size == TEXT_SIZE and current_page_text:
                        # Guardar texto si hubo un cambio de tamaño
                        if current_text:
                            data_entry = {
                                "chapter": current_chapter,
                                "title": current_title,
                                "section": current_section,
                                "text": current_text.strip()  # Strip para eliminar espacios finales
                            }
                            data.append(data_entry)
                        current_text = current_page_text.strip()
                        current_page_text = ""
                    current_section = text
                    print(f"Detected section: {current_section}")
                    last_font_size = font_size

    # Si hay datos acumulados de capítulo al final de la página
    if current_chapter:
        if last_font_size == TEXT_SIZE:
            current_text += " " + current_page_text.strip()
        elif last_font_size == SECTION_SIZE_THRESHOLD and current_section:
            current_text += " " + current_page_text.strip()
            current_page_text = ""
        if current_text or current_page_text:
            data_entry = {
                "chapter": current_chapter,
                "title": current_title,
                "section": current_section,
                "text": current_text.strip()  # Strip para eliminar espacios finales
            }
            data.append(data_entry)

# Procesar las páginas del PDF
with fitz.open("data/book/ml_interviews.pdf") as pdf:
    for page_number in range(22, 25):  # Especificar rango de páginas
        page = pdf.load_page(page_number)
        print(f"Processing page {page_number}")
        process_page(page)

# Guardar el último capítulo en la lista de datos
if current_chapter:
    data_entry = {
        "chapter": current_chapter,
        "title": current_title,
        "section": current_section,
        "text": current_text.strip()  # Strip para eliminar espacios finales
    }
    data.append(data_entry)

# Imprimir los resultados
print(json.dumps(data, indent=4))

# Guardar el resultado en un archivo JSON
with open("data/dataset_prueba.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Datos guardados en 'dataset_prueba.json'")
