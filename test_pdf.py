from modules.pdf_extractor import process_pdf

pdf_path = "sample.pdf"  # put your PDF here

text = process_pdf(pdf_path)

print(text[:1000])  # print first 1000 characters
