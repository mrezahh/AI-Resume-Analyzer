from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator

class UserCreate(BaseModel):
    full_name: str 
    email: EmailStr
    password: str 
    
    # @validator('password')
    # def validate_password(cls, value):
    #     if not value:
    #         raise ValueError("Password must not be empty")
    #     if len(value.encode("utf-8")) > 72:
    #         raise ValueError("Password must not exceed 72 bytes")
    #     return value

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    created_at: datetime

    # Tells Pydantic that this schema can read data from ORM objects
    class Config:
        orm_mode = True
        
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"