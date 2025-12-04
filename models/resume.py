from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func



class Resume(Base):
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    
    # AI extracted fields
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    skills = Column(String, nullable=True) # Separated by commas
    experience_summary = Column(String, nullable=True)
    
    parsed_text = Column(Text, nullable=True)    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
