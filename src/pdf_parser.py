import fitz  # PyMuPDF
import json

def process_pdf(file_path, start_page, end_page):
    doc = fitz.open(file_path)
    data = []
    current_chapter = None
    current_title = None
    current_content = []
    current_section = ""
    current_text = ""
    pending_text = ""
    section_accumulating = False  

    def round_font_size(size):
        return round(size)

    def process_pending_text(pending_text, current_text):
        if pending_text:
            current_text += pending_text  
        return pending_text, current_text

    for page_num in range(start_page - 1, end_page):
        page = doc.load_page(page_num)
        print(f"Processing page {page_num + 1}")
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if 'lines' not in block:
                continue

            for line in block["lines"]:
                line_text = ""  

                for span in line["spans"]:
                    font_size = round_font_size(span["size"])
                    text = span["text"].strip()

                    if text.endswith("-"):
                        pending_text = text[:-1] 
                    else:
                        if pending_text:
                            line_text += pending_text + text
                            pending_text = ""
                        else:
                            line_text += " " + text if line_text else text

                pending_text, line_text = process_pending_text(pending_text, line_text)

                # Start of a new chapter
                if line_text.startswith("CHAPTER"):
                    if current_chapter and current_title and current_content:
                        if current_text:
                            current_content[-1]["text"] += current_text.strip() 
                        data.append({
                            "chapter": current_chapter,
                            "title": current_title,
                            "content": current_content
                        })
                    current_chapter = line_text
                    current_title = None
                    current_content = []
                    current_section = ""
                    current_text = ""
                    section_accumulating = False

                # Large font size indicates a title
                elif font_size == 25:
                    current_title = current_title + " " + line_text if current_title else line_text
                    print(f"Accumulating title: {current_title}")
                    section_accumulating = False

                # Medium font size indicates a section, accumulate until text stops
                elif font_size == 19:
                    if section_accumulating:
                        current_section += " " + line_text  
                    else:
                        if current_section:
                            # Save the current section with its associated text
                            current_content.append({"section": current_section.strip(), "text": current_text.strip()})
                            current_text = ""
                        current_section = line_text  
                        section_accumulating = True  
                    print(f"Accumulating section: {line_text}")

                # Small font size indicates regular text content
                elif font_size == 10:
                    section_accumulating = False  
                    if current_text and not current_text.endswith(" "):
                        current_text += " "  
                    current_text += line_text  

    # Add the last chapter and its content if exists
    if current_chapter and current_title and current_content:
        if current_text:
            current_content[-1]["text"] += current_text.strip() 
        data.append({
            "chapter": current_chapter,
            "title": current_title,
            "content": current_content
        })

    with open("data/parsed_book.json", "w") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)

    print("Processing completed and saved in 'data/parsed_book.json'.")

process_pdf("data/book/ml_interviews.pdf", 22, 286)
