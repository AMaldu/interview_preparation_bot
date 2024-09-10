import pdfplumber

# Lista para almacenar los encabezados y su contenido
data = []
current_section = {}

# Abre el PDF desde la ubicación especificada
with pdfplumber.open("data/book/ml_interviews.pdf") as pdf:
    # Itera sobre las páginas desde la 8 hasta la 12 (recuerda que la indexación comienza en 0)
    for page_number in range(7, 12):  # Páginas 8 a 12 en indexación 0-basada
        page = pdf.pages[page_number]
        
        # Extrae el contenido de la página con detalles sobre el formato del texto
        for element in page.extract_words():
            # Inspecciona el tamaño y tipo de fuente de cada elemento
            font_size = element['size']
            font_name = element['fontname']

            # Define el tamaño de fuente para encabezados
            # Ajusta estos umbrales según tu inspección previa
            if font_size > 12:
                # Si encuentras un nuevo encabezado, guarda la sección anterior
                if current_section:
                    data.append(current_section)
                # Inicia una nueva sección para el nuevo encabezado
                current_section = {"header": element['text'], "content": ""}
            else:
                # Si no es un encabezado, añade el texto al contenido de la sección actual
                if current_section:
                    current_section["content"] += element['text'] + " "

        # Añadir la última sección después de salir del bucle de páginas
        if current_section:
            data.append(current_section)

# Imprimir los datos extraídos para revisión
for section in data:
    print("Encabezado:", section["header"])
    print("Contenido:", section["content"])
    print("-" * 80)  # Separador entre secciones

# Opcional: Guardar los datos en un archivo JSON si decides hacerlo
# with open("data/dataset.json", "w") as jsonfile:
#     json.dump(data, jsonfile, indent=4)
