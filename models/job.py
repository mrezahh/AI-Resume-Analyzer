from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from database import Base

class Resume(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(String, nullable=False)  # Comma-separated skills