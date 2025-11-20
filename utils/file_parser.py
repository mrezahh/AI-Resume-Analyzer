import re
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
                text += para.text + '\n'
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

def extract_email(text: str) -> str:
    """Extract email address from text."""
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return match.group(0) if match else None

def extract_phone_number(text: str) -> str:
    """Extract phone number from text."""
    match = re.search(r'\+?\d[\d -]{8,}\d', text)
    return match.group(0) if match else None

def extract_name(text: str) -> str:
    """Extract name from text (assumes name is the first line)."""
    lines = text.strip().split('\n')
    return lines[0] if lines else None

def extract_skills(text: str, skills_list: list | None = None) -> list[str]:
    """Extract skills from text based on a predefined skills list."""
    
    if skills_list is None:
        skills_list = ['Python', 'Java', 'C++', 'JavaScript', 'SQL', 'Machine Learning', 'Data Analysis', 'Project Management']
    
    found_skills = []
    
    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found_skills.append(skill)
    return found_skills

# ================= Analyze Resume =================
def analyze_resume(file_path: str, skills_list: list[str] = None) -> dict:
    """Analyze resume and extract key information."""
    text = parse_resume(file_path)
    if not text:
        return {}
    
    analysis = {
        'name': extract_name(text),
        'email': extract_email(text),
        'phone_number': extract_phone_number(text),
        'skills': extract_skills(text, skills_list),
        'parsed_text': text
    }
    return analysis