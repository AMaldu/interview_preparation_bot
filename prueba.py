import fitz  # PyMuPDF

# Initialize variables
data = []
current_title_parts = []
is_chapter_title = False
last_top_position = None
current_line = ""

# Font size threshold for chapter titles
CHAPTER_TITLE_SIZE_THRESHOLD = 20

def finalize_chapter_title(parts):
    """Combine parts of the title into a single title with a space between lines if necessary."""
    if len(parts) == 0:
        return ""
    combined_title = ' '.join(parts).strip()
    return combined_title

def process_page(page):
    global current_title_parts, is_chapter_title, last_top_position, current_line
    current_title_parts = []
    is_chapter_title = False
    last_top_position = None
    current_line = ""

    for char in page.get_text("dict")["blocks"]:
        for line in char.get("lines", []):
            for span in line.get("spans", []):
                text = span.get('text', '')
                font_size = span.get('size', 0)
                top = span.get('bbox', [0, 0, 0, 0])[1]

                print(f"Character: {text}, Font size: {font_size}, Top: {top}")

                if font_size >= CHAPTER_TITLE_SIZE_THRESHOLD:
                    if not is_chapter_title:
                        # Starting a new chapter title
                        current_title_parts = [text]
                        is_chapter_title = True
                        last_top_position = top
                        current_line = text
                        print(f"Starting new title: {current_line}")
                    else:
                        if top != last_top_position:
                            # End of line detected
                            if current_line.strip():  # If the current line has text, finalize it
                                print(f"Appending line: {current_line}")
                                #current_title_parts.append(current_line)
                            current_line = text
                        else:
                            current_line += text

                        last_top_position = top
                else:
                    # If we encounter text smaller than the threshold and we are in a title
                    if is_chapter_title:
                        if current_line.strip():
                            print(f"Appending line: {current_line}")
                            current_title_parts.append(current_line)
                        current_chapter_title = finalize_chapter_title(current_title_parts)
                        print(f"Added data: {current_chapter_title}")
                        data.append({"title": current_chapter_title})
                        current_title_parts = []
                        is_chapter_title = False
                        current_line = ""

    # Finalize the title if the page ends with a chapter title
    if is_chapter_title and current_line.strip():
        print(f"Appending final line: {current_line}")
        current_title_parts.append(current_line)
        current_chapter_title = finalize_chapter_title(current_title_parts)
        print(f"Added data: {current_chapter_title}")
        data.append({"title": current_chapter_title})

# Process the PDF pages
with fitz.open("data/book/ml_interviews.pdf") as pdf:
    for page_number in range(22, 23):  # Specify page range
        page = pdf.load_page(page_number)
        print(f"Processing page {page_number}")
        process_page(page)

# Print the results
import json
print(json.dumps(data, indent=4))
