import pdfplumber
import json
import re

# Initialize variables
data = []
current_section = {"header": None, "sections": []}
accumulated_text = ""
accumulated_header = ""
current_font_size = 0
last_font_size = None
header_candidates = []
collecting_header = False

# Font size thresholds
CHAPTER_SIZE_THRESHOLD = 20
SECTION_SIZE_THRESHOLD = 18.92
TEXT_SIZE_THRESHOLD = 10.5

# def finalize_current_section():
#     """Finalize the current section, adding it to the data list."""
#     global current_section, accumulated_text
#     if accumulated_text.strip():
#         current_section["sections"].append({"content": accumulated_text.strip()})
#     if current_section["header"]:
#         data.append(current_section)
#     # Reset for the next section
#     current_section = {"header": None, "sections": []}
#     accumulated_text = ""

def finalize_last_section():
    """Finalize the last section for the current chapter."""
    global accumulated_text
    if accumulated_text.strip():
        current_section["sections"].append({"content": accumulated_text.strip()})
    if current_section["header"]:
        data.append(current_section)
    accumulated_text = ""

def is_chapter_header(text):
    """Check if the text is part of a chapter header."""
    return re.match(r'^CHAPTER\s+\d+', text, re.IGNORECASE)

with pdfplumber.open("data/book/ml_interviews.pdf") as pdf:
    for page_number in range(22, 23):
        page = pdf.pages[page_number]
        print(f"Processing page {page_number}")
        
        # Get the char and its size
        previous_char = None
        for char in page.chars:
            text = char.get('text', '')
            font_size = char.get('size', 0)

            # Debugging: print the character and its font size
            #print(f"Character: {text}, Font size: {font_size}")

            # Compares the vertical position of the char with the previous one
            if previous_char and previous_char['top'] != char['top']:
                accumulated_text += " "

            # Check if the text is a potential chapter header (CHAPTER <number>)
            if font_size >= CHAPTER_SIZE_THRESHOLD:
                if is_chapter_header(accumulated_text.strip()):
                    print(f"Detected chapter header: {accumulated_text.strip()}")

                    # Finalize the previous section before starting a new chapter
                    if current_section["header"]:
                        finalize_last_section()
                    
                    # Start accumulating the chapter title
                    header_candidates = [accumulated_text.strip()]
                    collecting_header = True
                    accumulated_text = ""
                elif collecting_header:
                    # Accumulate chapter title words
                    if font_size >= CHAPTER_SIZE_THRESHOLD:
                        print(f"Accumulating chapter title: {text}")
                        header_candidates.append(text)
                    else:
                        # If font size drops below the threshold, finalize the header
                        collecting_header = False
                        header_text = " ".join(header_candidates).strip()
                        print(f"Final chapter header: {header_text}")
                        current_section = {"header": header_text, "sections": []}
                        accumulated_text = ""

            # Normal text processing
            if font_size >= TEXT_SIZE_THRESHOLD and not collecting_header:
                accumulated_text += text

            previous_char = char

        # Finalize the last section and chapter for the page
        finalize_last_section()



# Combine split chapter titles
for section in data:
    header = section["header"]
    print(f' header is: {header}')
    if header:
        # Join parts if split
        header_parts = re.split(r'(\d+)', header, maxsplit=1)
        if len(header_parts) > 2:
            chapter_number = header_parts[1].strip()
            chapter_title = header_parts[2].strip()
            if chapter_number and chapter_title:
                section["header"] = f"CHAPTER {chapter_number} {chapter_title}"
        else:
            # Ensure proper format if no split detected
            section["header"] = header.strip()

# # Remove duplicate content in sections
# for section in data:
#     seen_contents = set()
#     unique_sections = []
#     for sec in section["sections"]:
#         content = sec.get("content", "").strip()
#         if content not in seen_contents:
#             seen_contents.add(content)
#             unique_sections.append(sec)
#     section["sections"] = unique_sections

# Print results before saving
for section in data:
    print("Chapter:", section["header"])
    for sec in section["sections"]:
        print("  Content:", sec.get("content", ""))
    print("-" * 80)

# Save to JSON file
with open("data/dataset.json", "w") as jsonfile:
    json.dump(data, jsonfile, indent=4)
