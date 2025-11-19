import os
from sqlalchemy.orm import Session
from fastapi import APIRouter, UploadFile, File,Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from database import get_db
from models.resume import Resume
from schemas.resume import ResumeResponse
from utils.file_parser import parse_resume
from routers.auth import get_current_user

UPLOAD_FOLDER = "uploaded_resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF and DOCX are allowed."
        )
        
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)
    # parse file to extract resume data
    parsed_text = parse_resume(file_location)
    
    # Save resume record in database using class Resume(Base) in models/resume.py
    new_resume = Resume(
        user_id=current_user.id,
        file_name=file.filename,
        file_path=file_location,
        parsed_text=parsed_text
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    
    return new_resume
