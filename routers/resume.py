import os
from sqlalchemy.orm import Session
from fastapi import APIRouter, UploadFile, File,Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from database import get_db
from models.resume import Resume
from schemas.resume import ResumeAIAnalyzeResponse, ResumeResponse

from utils.auth import get_current_user
from utils.file_parser import analyze_resume
from utils.ai_model import analyze_resume_with_ai

UPLOAD_FOLDER = "uploaded_resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def convert_resume_model(resume):
    """Convert Database resume info to API dictionary."""
    return {
        "id": resume.id,
        "user_id": resume.user_id,
        "file_name": resume.file_name,
        "file_path": resume.file_path,
        "parsed_text": resume.parsed_text,
        "created_at": resume.created_at,
        "name": resume.name,
        "email": resume.email,
        "phone_number": resume.phone_number,
        "skills": resume.skills.split(',') if resume.skills else [],
        "experience_summary": resume.experience_summary if hasattr(resume, 'experience_summary') else None,
    }


router = APIRouter(prefix="/resumes", tags=["Resumes"])

# ================= Upload Resume =================
@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):
    """Upload and parse a resume file (PDF or DOCX)."""
    
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF and DOCX are allowed."
        )
        
    # Save uploaded file
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)
        
    # Extract raw text and info with parser
    parsed_info = analyze_resume(file_location)
    
    # AI Analysis (summary + suggestions)
    ai_result = analyze_resume_with_ai(parsed_info.get('parsed_text', ''))
    experience_summary = ai_result.get('experience_summary', '')
    
    # Use classical parser values (not AI) for Database safe structured 
    extracted_name = parsed_info.get('name')
    extracted_email = parsed_info.get('email')
    extracted_phone = parsed_info.get('phone')
    extracted_skills = parsed_info.get('skills', [])
    
    
    # Save to Database
    new_resume = Resume(
        user_id=current_user.id,
        file_name=file.filename,
        file_path=file_location,
        
        # Raw parsed text - stored for reference
        parsed_text=parsed_info.get('parsed_text'),
        
        # Stracture fields -> paser output 
        name=extracted_name,
        email=extracted_email,
        phone_number=extracted_phone,
        skills=",".join(extracted_skills),  # Store as comma-separated string
        experience_summary=experience_summary
    )
     
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    
    return convert_resume_model(new_resume)

# ================= Get Resumes =================
@router.get("/", response_model=list[ResumeResponse])
def list_resumes(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):    
    """List all resumes for the current user."""
    
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    return [convert_resume_model(r) for r in resumes] # Database stores "Python,Java,FastAPI" → string


# ================= Get Specific Resume with ID =================
@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):
    """Get a specific resume by ID for the current user."""
    
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found."
        )
    
    return resume

# ================= Delete Resume =================
@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):
    """Delete a specific resume by ID for the current user."""
    
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found."
        )
    
    # Delete the file from storage
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)
    
    # Delete the record from the database
    db.delete(resume)
    db.commit()
    
    return {"detail": "Resume deleted successfully."}

@router.get("/{resume_id}/ai-analyze", response_model=ResumeAIAnalyzeResponse)
def ai_analysis(resume_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):
    """Get AI analysis for a specific resume by ID for the current user."""
    
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found."
        )
    try: 
        ai_result = analyze_resume_with_ai(resume.parsed_text or "")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ai_result = {"skill_gaps": [], "weak_points": [], "matching_job_titles": [], "suggestions": []}
        )
    
    return ai_result
