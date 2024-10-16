import pdfplumber
import json

font_size_texts = {}


with pdfplumber.open("../data/book/ml_interviews.pdf") as pdf:
    for page_number in range(24, 25):  
        page = pdf.pages[page_number]
        print(f"Processing page {page_number}")

        current_font_size = None
        accumulated_text = ""

        for char in page.chars:
            text = char.get('text', '')
            font_size = char.get('size', 0)

            # Print character info for debugging
            print(f"Text: {text}, Font size: {font_size}")

            if font_size != current_font_size:
                if current_font_size and accumulated_text.strip():
                    if current_font_size not in font_size_texts:
                        font_size_texts[current_font_size] = ""
                    font_size_texts[current_font_size] += accumulated_text.strip() + " "
                accumulated_text = ""

                # Update font size
                current_font_size = font_size

            # Accumulate text for the same font size
            accumulated_text += text

        # Finalize the last accumulated text for the page
        if accumulated_text.strip():
            if current_font_size not in font_size_texts:
                font_size_texts[current_font_size] = ""
            font_size_texts[current_font_size] += accumulated_text.strip() + " "

# Save the results to a JSON file
with open("../data/font_size_texts.json", "w") as jsonfile:
    json.dump(font_size_texts, jsonfile, indent=4)

for font_size, text in font_size_texts.items():
    print(f"Font size: {font_size}")
    print(f"Text: {text}")
    print("-" * 80)
