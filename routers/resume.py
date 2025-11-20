import os
from sqlalchemy.orm import Session
from fastapi import APIRouter, UploadFile, File,Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from database import get_db
from models.resume import Resume
from schemas.resume import ResumeResponse
from utils.file_parser import analyze_resume
from routers.auth import get_current_user

UPLOAD_FOLDER = "uploaded_resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

router = APIRouter(prefix="/resumes", tags=["Resumes"])

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
        
    # parse and analyze resume
    parsed_info = analyze_resume(file_location)
    
    # Save resume record in database using class Resume(Base) in models/resume.py
    new_resume = Resume(
        user_id=current_user.id,
        file_name=file.filename,
        file_path=file_location,
        parsed_text=parsed_info.get('parsed_text'),
        name=parsed_info.get('name'),
        email=parsed_info.get('email'),
        phone_number=parsed_info.get('phone_number'),
        skills=parsed_info.get('skills')      
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    
    return new_resume

# ================= Get Resumes =================
@router.get("/", response_model=list[ResumeResponse])
def list_resumes(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):    
    """List all resumes for the current user."""
    
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    return resumes

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