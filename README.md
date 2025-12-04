# AI Resume Analyzer (FastAPI + PostgreSQL + Ollama)

An intelligent Resume Analyzer built with **FastAPI**, **PostgreSQL**, and **Ollama local LLMs**.  
The system allows users to:

- Upload resumes (PDF/DOCX/TXT)
- Extract structured information
- Run AI-powered resume analysis
- Identify skill gaps and weak points
- Get job matching suggestions
- View results in a user dashboard

---

## Features

### Authentication + Roles
- JWT-based login system
- Secure password hashing (PassLib + bcrypt)

### Resume Upload
Users can upload:
- PDF  
- DOCX  
- TXT  

Resume content is extracted and stored in PostgreSQL.

### AI Resume Analysis (Ollama LLM)
The AI generates:

- Extracted personal info  
- Skills (list-format)  
- Experience summary  
- Skill gaps  
- Weak points  
- Matching job titles  
- Suggestions for improvement  

LLM model used:
llama3.2:1b

## Stracture
.
├── core/
│ ├── config.py
│ └── security.py
│
├── utils/
│ ├── ai_model.py
│ ├── auth.py
│ ├── security.py
│ └── file_parser.py
│
├── models/
│ ├── user.py
│ ├── resume.py
│ └── job.py
│
├── routers/
│ └── resume.py
│
├── schemas/
│ ├── user.py
│ └── resume.py
│
├── test/
│ ├── conftest.py
│ └── test_auth.py
│ └── test_resume.py
│
├── main.py
├── README.md
└── requirements.txt



---

## Installation Guide

### 1. Clone the Repository
# in terminal
git clone https://github.com/mrezahh/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer

### 2. Create Virtual Environment
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
.\.venv\Scripts\activate        # Windows


### 3. Install Dependencies
pip install -r requirement.txt


### 4. Start PostgreSQL
create a database (resume_ai)

### 5. Install Ollama + Model
https://ollama.com/download

then pull model (terminal): 
ollama pull llama3.2:1b

### 6. Start server
uvicorn main:app --reload
API avalibale at: http: //127.0.0.1:8000

### 7. run Test
In terminal:
pytest






