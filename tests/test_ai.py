import os
from app.utils.resume_parser import extract_text_from_resume

def test_extract_text_from_resume():
    # Path to a sample PDF in your project root or a test resources folder
    sample_pdf_path = os.path.join(os.path.dirname(__file__), "test_documents", "Ahnaf_Khan_Resume.pdf")
    
    # Check if the sample PDF exists
    assert os.path.exists(sample_pdf_path), "Test PDF file does not exist."
    
    # Extract text from the PDF
    with open(sample_pdf_path, "rb") as f:
        extracted_text = extract_text_from_resume(f)
    
    # Check that the output is a non-empty string
    assert isinstance(extracted_text, str)
    assert len(extracted_text.strip()) > 0, "Extracted text should not be empty."
    
    # (Optional) Check for expected content
    # assert "Expected Name" in extracted_text
