import pdfplumber
from docx import Document

def parse_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    try:
        with pdfplumber.open(file_path) as pdf:
            text= ''
            for page in pdf.pages:
                text += page.extract_text() + '\n'
        return text
    except Exception as e:
        print(f"Error parsing PDF file: {e}")
        return ""
    
def parse_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    try:
        with Document(file_path) as doc:
            text = ''
            for para in doc.paragraphs:
                text += para.text() + '\n'
        return text    
    except Exception as e:
        print(f"Error parsing DOCX file: {e}")
        return ""
    
def parse_resume(file_path: str) -> str:
    """Determine file type and extract text accordingly."""
    if file_path.lower().endswith('.pdf'):
        return parse_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        return parse_docx(file_path)
    else:
        print("Unsupported file format.")
        return ""