import pdfplumber
import csv

with pdfplumber.open("data/book/ml_interviews.pdf") as pdf:
    with open("data/dataset.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)

        for page in pdf.pages:
            text = page.extract_text()
            
            if text:
                lines = text.split("\n")
                for line in lines:
                    row = line.split()  
                    writer.writerow(row)
