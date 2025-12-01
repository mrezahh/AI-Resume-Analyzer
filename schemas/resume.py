from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


# ======== Base Resume Schemas ========
class ResumeBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    skills: Optional[str] = None
    experience_summary: Optional[str] = None
    parsed_text: Optional[str] = None
    
# ======== Resume Create and Response Schemas ========
class ResumeCreate(BaseModel):
    pass

# ======== Resume Response Schema ========
class ResumeResponse(ResumeBase):
    id: int
    user_id: int
    file_name: str
    file_path: str
    uploaded_at: datetime 

    # Tells Pydantic that this schema can read data from ORM objects
    class Config:
        orm_mode = True

# ======== Resume AI Analyze Response Schema (match ai_model.py output) ========    
class ResumeAIAnalyzeResponse(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    skills: Optional[List[str]]
    experience_summary: Optional[str]
   
    class Config:
        orm_mode = True