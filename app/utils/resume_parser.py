import pdfplumber
import logging

logger = logging.getLogger(__name__)

def extract_text_from_resume(file):
    # pdfplumber expects a file-like object (e.g., Werkzeug FileStorage from Flask)
    try:
        file.seek(0)  # Ensure we read from the start of the file
        with pdfplumber.open(file) as pdf:
            return "\n".join([text for page in pdf.pages if (text := page.extract_text())])
    except Exception as e:
        logger.error(f"Error seeking to start of resume file: {e}")
        raise ValueError("Invalid file object provided for text extraction.")
