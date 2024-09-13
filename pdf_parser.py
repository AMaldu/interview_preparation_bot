import fitz  # PyMuPDF
import json

def process_pdf(file_path, start_page, end_page):
    doc = fitz.open(file_path)
    data = []
    current_chapter = None
    current_title = None
    current_content = []
    current_text = ""
    current_section = ""
    pending_text = ""

    # Función para redondear el tamaño de letra
    def round_font_size(size):
        return round(size)

    # Procesa el texto pendiente
    def process_pending_text(pending_text, current_text):
        if pending_text:
            current_text += pending_text  # Sin agregar espacios extra
            pending_text = ""
        return pending_text, current_text

    for page_num in range(start_page - 1, end_page):
        page = doc.load_page(page_num)
        print(f"Processing page {page_num + 1}")
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if 'lines' not in block:
                continue

            for line in block["lines"]:
                line_text = ""  # Variable para acumular el texto de la línea actual

                for span in line["spans"]:
                    font_size = round_font_size(span["size"])
                    text = span["text"].strip()

                    # Acumulamos el texto de los spans en la misma línea
                    if text.endswith("-"):
                        pending_text = text[:-1]  # Eliminar guion, añadir a texto pendiente
                    else:
                        if pending_text:
                            # Concatenar el texto pendiente sin espacios adicionales
                            line_text += pending_text + text
                            pending_text = ""
                        else:
                            line_text += " " + text if line_text else text

                # Al final de la línea, combinar el texto pendiente con el texto de la línea
                pending_text, line_text = process_pending_text(pending_text, line_text)

                # Manejo de capítulos, títulos, secciones, y texto
                if line_text.startswith("CHAPTER"):
                    if current_chapter and current_title and current_content:
                        if current_text:
                            current_content.append({"text": current_text.strip()})
                            current_text = ""
                        if current_section:
                            current_content.append({"section": current_section.strip()})
                            current_section = ""
                        data.append({
                            "chapter": current_chapter,
                            "title": current_title,
                            "content": current_content
                        })
                    current_chapter = line_text
                    current_title = None
                    current_content = []
                    current_text = ""
                    current_section = ""

                elif font_size == 25:
                    current_title = current_title + " " + line_text if current_title else line_text
                    print(f"Accumulating title: {current_title}")

                elif font_size == 19:
                    if current_text:
                        current_content.append({"text": current_text.strip()})
                        current_text = ""
                    current_section += " " + line_text if current_section else line_text
                    print(f"Accumulating section: {line_text}")

                elif font_size == 10:
                    if current_section:
                        current_content.append({"section": current_section.strip()})
                        current_section = ""
                    if current_text and not current_text.endswith(" "):
                        current_text += " "  # Aseguramos un espacio entre líneas de texto
                    current_text += line_text

    if current_chapter and current_title and current_content:
        if current_text:
            current_content.append({"text": current_text.strip()})
        if current_section:
            current_content.append({"section": current_section.strip()})
        data.append({
            "chapter": current_chapter,
            "title": current_title,
            "content": current_content
        })

    with open("data/parsed_book.json", "w") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)

    print("Procesamiento completado y guardado en 'data/parsed_book.json'.")

# Ejecuta la función para procesar el PDF
process_pdf("data/book/ml_interviews.pdf", 22, 286)
