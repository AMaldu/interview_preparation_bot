import fitz  # PyMuPDF

def analyze_guions(file_path, page_number, target_font_size, max_lines):
    doc = fitz.open(file_path)
    
    def analyze_text(text, font_size):
        if font_size == target_font_size:
            for char in text:
                if char in ('\u2010', '\u2011', '\u2012', '\u2013', '\u2014', '\u2015', '\u2212', '\u00AD'):
                    print(f"Character: '{char}' (Unicode: {ord(char)}) - Type: Hyphen")
                else:
                    print(f"Character: '{char}' (Unicode: {ord(char)}) - Type: Other")

    page = doc.load_page(page_number - 1)
    print(f"Processing page {page_number}")  
    blocks = page.get_text("dict")["blocks"]
    line_count = 0
    
    for block in blocks:
        if 'lines' not in block:
            continue  

        for line in block["lines"]:
            if line_count >= max_lines:
                print("Reached the limit of 50 lines.")
                return
            for span in line["spans"]:
                text = span["text"]
                font_size = round(span["size"], 1) 
                analyze_text(text, font_size)
                
            line_count += 1



analyze_guions("../data/book/ml_interviews.pdf", 87, 10.5, 50)
