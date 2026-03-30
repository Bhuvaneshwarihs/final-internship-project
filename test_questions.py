from modules.pdf_extractor import process_pdf
from modules.question_generator import generate_questions

pdf_path = "sample.pdf"

text = process_pdf(pdf_path)

questions = generate_questions(text)

print(questions)
