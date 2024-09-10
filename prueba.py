import pdfplumber
import json

# Initialize variables
data = []
current_chapter_title = ""
is_chapter_title = False
accumulated_text = ""

# Font size threshold for chapter titles
CHAPTER_TITLE_SIZE_THRESHOLD = 20

def finalize_chapter_title(title):
    """Finalize the chapter title, ensuring there is a space between parts of the title if necessary."""
    # Add a space at the end of the first line if a second line exists
    if title:
        # Add space before the second part if necessary
        return title.strip()
    return title

def process_page(page):
    global accumulated_text, is_chapter_title
    accumulated_text = ""
    
    for char in page.chars:
        text = char.get('text', '')
        font_size = char.get('size', 0)
        
        # If the font size is large, we might be in a chapter title
        if font_size >= CHAPTER_TITLE_SIZE_THRESHOLD:
            if is_chapter_title:
                # If we are accumulating a chapter title, add the current text
                accumulated_text += text
            else:
                # If we find a chapter title, start accumulating text
                accumulated_text = text
                is_chapter_title = True
        else:
            # If the font size is smaller and we are accumulating a chapter title
            if is_chapter_title:
                # Add a space at the end of the first line if a second line exists
                if accumulated_text.strip():
                    if len(text.strip()) == 0:  # If the text is empty, we might be moving to the next line
                        accumulated_text += ' '  # Add space between lines
                    else:
                        # Finalize the title
                        current_chapter_title = finalize_chapter_title(accumulated_text)
                        data.append({"title": current_chapter_title})
                        accumulated_text = ""
                        is_chapter_title = False
                else:
                    accumulated_text = text

# Process the PDF pages
with pdfplumber.open("data/book/ml_interviews.pdf") as pdf:
    for page_number in range(22, 23):  # Specify page range
        page = pdf.pages[page_number]
        print(f"Processing page {page_number}")
        process_page(page)

# Save to JSON file
with open("data/dataset_prueba.json", "w") as jsonfile:
    json.dump(data, jsonfile, indent=4)
