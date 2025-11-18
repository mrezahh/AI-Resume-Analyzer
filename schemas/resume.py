from datetime import datetime
from pydantic import BaseModel

class ResumeCreate(BaseModel):
    pass

class ResumeResponse(BaseModel):
    id: int
    user_id: int
    file_name: str
    file_path: str
    parsed_text: str | None
    created_at: datetime

    class Config:
        orm_mode = True
   