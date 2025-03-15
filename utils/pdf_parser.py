import PyPDF2
import io

def extract_text_from_pdf(pdf_file):
    """
    Extract text from a PDF file.
    
    Args:
        pdf_file: The uploaded PDF file object
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")
