"""
Database models for Notes.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .database import Base

class Note(Base):
    """
    SQLAlchemy Note model.
    """
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
