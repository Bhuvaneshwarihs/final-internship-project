import fitz

def extract_text_from_pdf(file_path):
    text = ""

    try:
        with fitz.open(file_path) as pdf:
            for page in pdf:
                page_text = page.get_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        print(f"Error reading PDF: {e}")

    return text


def clean_text(text):
    # Basic cleaning
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")
    text = text.strip()

    return text


def process_pdf(file_path):
    raw_text = extract_text_from_pdf(file_path)
    cleaned_text = clean_text(raw_text)

    return cleaned_text
    # smqsj