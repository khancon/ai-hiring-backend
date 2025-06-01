import pdfplumber

def extract_text_from_resume(file):
    # pdfplumber expects a file-like object (e.g., Werkzeug FileStorage from Flask)
    with pdfplumber.open(file) as pdf:
        return "\n".join([text for page in pdf.pages if (text := page.extract_text())])
