import fitz  # PyMuPDF

def analyze_guions(file_path, page_number, target_font_size, max_lines):
    # Abrimos el PDF
    doc = fitz.open(file_path)
    
    # Función para analizar el texto y detectar guiones
    def analyze_text(text, font_size):
        if font_size == target_font_size:
            for char in text:
                if char in ('\u2010', '\u2011', '\u2012', '\u2013', '\u2014', '\u2015', '\u2212', '\u00AD'):
                    print(f"Character: '{char}' (Unicode: {ord(char)}) - Type: Hyphen")
                else:
                    print(f"Character: '{char}' (Unicode: {ord(char)}) - Type: Other")

    # Procesamos la página especificada
    page = doc.load_page(page_number - 1)
    print(f"Processing page {page_number}")  # Imprime la página que se está procesando
    blocks = page.get_text("dict")["blocks"]

    # Contador para las primeras líneas
    line_count = 0

    # Procesamos cada bloque de texto en la página
    for block in blocks:
        if 'lines' not in block:
            continue  # Saltamos este bloque si no tiene líneas de texto

        for line in block["lines"]:
            if line_count >= max_lines:
                print("Reached the limit of 50 lines.")
                return
            for span in line["spans"]:
                text = span["text"]
                font_size = round(span["size"], 1)  # Redondear el tamaño de fuente a 1 decimal
                analyze_text(text, font_size)
                
            line_count += 1

    print("Análisis completado.")

# Ejecuta la función para analizar la página 87 con tamaño de fuente 10.5 y límite de 50 líneas
analyze_guions("data/book/ml_interviews.pdf", 87, 10.5, 50)
