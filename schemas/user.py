from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    full_name: str 
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    created_at: str

    class Config:
        orm_mode = True
        
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"