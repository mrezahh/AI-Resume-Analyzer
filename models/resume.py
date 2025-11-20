from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

class Resume(Base):
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    skills = Column(String)
    parsed_text = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    