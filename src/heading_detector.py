import re
import fitz  
import json

data = []
current_title_parts = []
is_chapter_title = False
current_chapter = None
current_text = ""
current_section = ""
title_size_threshold = 25
section_size_threshold = 19
text_size_threshold = 10

# Round font size to nearest integer
def round_font_size(size):
    return round(size)

# Regex to detect 'CHAPTER' followed by a number
CHAPTER_REGEX = r"^CHAPTER\s\d{1,2}$"

def finalize_title(parts):
    """Combine parts of the title into a single title with a space between lines if necessary."""
    if len(parts) == 0:
        return ""
    combined_title = ' '.join(parts).strip()
    return combined_title

def process_page(page):
    global current_title_parts, is_chapter_title, current_chapter, current_text, current_section
    current_title_parts = []
    is_chapter_title = False
    current_chapter = None
    current_text = ""
    current_section = ""

    for char in page.get_text("dict")["blocks"]:
        for line in char.get("lines", []):
            for span in line.get("spans", []):
                text = span.get('text', '')
                font_size = round_font_size(span.get('size', 0))

                # Detect CHAPTER based on regex (uppercase and followed by a number)
                if re.match(CHAPTER_REGEX, text):
                    current_chapter = text
                    print(f"Detected chapter: {current_chapter}")

                if font_size >= title_size_threshold:
                    if not is_chapter_title:
                        # Starting a new chapter title
                        current_title_parts = [text]
                        is_chapter_title = True
                        print(f"Starting new title: {text}")
                    else:
                        current_title_parts.append(text)
                elif font_size >= section_size_threshold:
                    # Section text
                    if current_section:
                        current_section += " " + text
                    else:
                        current_section = text
                elif font_size == text_size_threshold:
                    # Regular text
                    if current_text and not current_text.endswith(" "):
                        current_text += " "  # Add space if needed
                    current_text += text.strip()
                else:
                    # If we encounter text smaller than the threshold and we are in a title
                    if is_chapter_title:
                        current_title_parts.append(text)
                        current_title = finalize_title(current_title_parts)
                        data_entry = {
                            "chapter": current_chapter if current_chapter else "Unknown Chapter",
                            "title": current_title,
                            "text": current_text.strip()
                        }
                        if current_section:
                            data_entry["section"] = current_section.strip()
                        data.append(data_entry)
                        current_title_parts = []
                        is_chapter_title = False
                        current_text = ""
                        current_section = ""

    # Finalize the title and text if the page ends with a chapter title
    if is_chapter_title:
        current_title = finalize_title(current_title_parts)
        data_entry = {
            "chapter": current_chapter if current_chapter else "Unknown Chapter",
            "title": current_title,
            "text": current_text.strip()
        }
        if current_section:
            data_entry["section"] = current_section.strip()
        data.append(data_entry)

# Process the PDF pages. Specify the range of pages here!
with fitz.open("../data/book/ml_interviews.pdf") as pdf:
    for page_number in range(22, 25):  
        page = pdf.load_page(page_number)
        print(f"Processing page {page_number}")
        process_page(page)

# Print and save
print(json.dumps(data, indent=4))

with open("../data/dataset_prueba.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Data saved into 'dataset_prueba.json'")
