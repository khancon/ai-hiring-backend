import os
import pytest
from unittest.mock import MagicMock, patch
from app.utils.resume_parser import extract_text_from_resume

# Test cases for the resume text extraction utility function
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

# Test cases for invalid file input
def test_extract_text_from_resume_invalid_file():
    # Create a "file" object that will cause pdfplumber.open to raise an Exception
    bad_file = MagicMock()
    # Simulate an error on seek (could also patch pdfplumber.open to raise)
    bad_file.seek.side_effect = Exception("seek error")
    
    # Optionally patch logger to verify it was called
    with patch("app.utils.resume_parser.logger") as mock_logger:
        with pytest.raises(ValueError) as exc_info:
            extract_text_from_resume(bad_file)
        # Check the error message
        assert "Invalid file object provided for text extraction." in str(exc_info.value)
        # Ensure logger.error was called with the underlying error
        error_calls = [call for call in mock_logger.error.call_args_list if "Error seeking to start of resume file" in str(call)]
        assert len(error_calls) > 0

# Test case for pdfplumber raising an exception
def test_extract_text_from_resume_pdfplumber_raises():
    file = MagicMock()
    file.seek.return_value = None  # No error on seek

    with patch("pdfplumber.open", side_effect=Exception("pdfplumber error")), \
         patch("app.utils.resume_parser.logger") as mock_logger:
        with pytest.raises(ValueError) as exc_info:
            extract_text_from_resume(file)
        assert "Invalid file object provided for text extraction." in str(exc_info.value)
        error_calls = [call for call in mock_logger.error.call_args_list if "Error seeking to start of resume file" in str(call)]
        assert len(error_calls) > 0
    