import fitz  # PyMuPDF
import json

def process_pdf(file_path, start_page, end_page):
    # Abrimos el PDF
    doc = fitz.open(file_path)
    
    # Estructura de datos para almacenar el resultado
    data = []
    current_chapter = None
    current_title = None
    current_content = []
    current_text = ""  # Variable para acumular las líneas de texto
    current_section = ""  # Variable para acumular las líneas de secciones
    title_accumulation = ""  # Variable para acumular títulos en varias líneas
    pending_text = ""  # Variable para almacenar texto pendiente de la línea anterior

    # Función para redondear el tamaño de letra
    def round_font_size(size):
        return round(size)

    def process_pending_text(pending_text, current_text):
        if pending_text:
            if current_text and not current_text.endswith(" "):
                current_text += " "  # Aseguramos un espacio antes de la nueva línea
            current_text += pending_text
            pending_text = ""
        return pending_text, current_text

    # Procesamos las páginas en el rango especificado
    for page_num in range(start_page - 1, end_page):
        page = doc.load_page(page_num)
        print(f"Processing page {page_num + 1}")  # Imprime la página que se está procesando
        blocks = page.get_text("dict")["blocks"]

        # Procesamos cada bloque de texto en la página
        for block in blocks:
            if 'lines' not in block:
                continue  # Saltamos este bloque si no tiene líneas de texto

            for line in block["lines"]:
                for span in line["spans"]:
                    font_size = round_font_size(span["size"])
                    text = span["text"].strip()

                    # Manejo del texto pendiente
                    pending_text, current_text = process_pending_text(pending_text, current_text)

                    # Detectamos el capítulo
                    if text.startswith("CHAPTER"):
                        # Si ya teníamos un capítulo previo, lo guardamos
                        if current_chapter and current_title and current_content:
                            # Guardamos el texto acumulado antes de cambiar de capítulo
                            if current_text:
                                current_content.append({"text": current_text.strip()})
                                current_text = ""
                            # Guardamos la sección acumulada si la hay
                            if current_section:
                                current_content.append({"section": current_section.strip()})
                                current_section = ""
                            data.append({
                                "chapter": current_chapter,
                                "title": current_title,
                                "content": current_content
                            })
                        # Empezamos un nuevo capítulo
                        print(f"Detected chapter: {text}")  # Imprime cuando detecta un capítulo
                        current_chapter = text
                        current_title = None
                        current_content = []
                        current_text = ""  # Reiniciamos el texto acumulado
                        current_section = ""  # Reiniciamos la sección acumulada
                        title_accumulation = ""  # Reiniciamos la acumulación de títulos

                    # Detectamos el título
                    elif font_size == 25:  # Suponiendo que el tamaño 25 es el título
                        # Acumulamos las líneas del título si está dividido
                        if current_title is None:
                            current_title = text
                        else:
                            current_title += " " + text
                        print(f"Accumulating title: {current_title}")  # Imprime cuando acumula un título

                    # Detectamos secciones
                    elif font_size == 19:  # Sección
                        if current_text:
                            # Guardamos el texto acumulado antes de agregar la nueva sección
                            current_content.append({"text": current_text.strip()})
                            current_text = ""  # Reiniciamos el texto acumulado
                        # Acumulamos las líneas de la sección en current_section
                        if current_section and not current_section.endswith(" "):
                            current_section += " "  # Aseguramos un espacio entre líneas de la sección
                        current_section += text
                        print(f"Accumulating section: {text}")  # Imprime cuando acumula una sección
                    
                    # Detectamos el texto (contenido)
                    elif font_size == 10:  # Texto
                        # Si había una sección acumulada, la guardamos antes de agregar nuevo texto
                        if current_section:
                            current_content.append({"section": current_section.strip()})
                            current_section = ""  # Reiniciamos la sección acumulada
                        # Manejo del carácter "-" para eliminarlo y combinar con la línea siguiente
                        if text.endswith("-"):
                            # Si el texto termina en "-", lo guardamos en pending_text para combinar con la siguiente línea
                            pending_text = text[:-1]  # Elimina el carácter "-" y guarda el texto pendiente
                        else:
                            # Acumulamos las líneas de texto en current_text, añadiendo un espacio entre ellas
                            if current_text and not current_text.endswith(" "):
                                current_text += " "  # Aseguramos un espacio antes de la nueva línea
                            current_text += text

                # Al final de cada línea, verificamos si hay texto pendiente para combinar
                pending_text, current_text = process_pending_text(pending_text, current_text)

        # No guardamos el texto en este punto si la página cambia, solo lo hacemos al final del párrafo/sección

    # Guardamos el último capítulo si no ha sido añadido aún
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

    # Guardamos los datos en un archivo JSON
    with open("data/parsed_book.json", "w") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)

    print("Procesamiento completado y guardado en 'data/parsed_book.json'.")

# Ejecuta la función para procesar el PDF
process_pdf("data/book/ml_interviews.pdf", 22, 286)
