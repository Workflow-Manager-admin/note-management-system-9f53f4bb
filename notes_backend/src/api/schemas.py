"""
Pydantic schemas for request/response models for Notes API.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# PUBLIC_INTERFACE
class NoteBase(BaseModel):
    """Shared properties of a Note."""
    title: str = Field(..., description="The title of the note", max_length=128)
    content: Optional[str] = Field(None, description="The content of the note")

# PUBLIC_INTERFACE
class NoteCreate(NoteBase):
    """Schema for creating a note."""

# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Schema for updating a note."""
    title: Optional[str] = Field(None, description="The title of the note", max_length=128)
    content: Optional[str] = Field(None, description="The content of the note")

# PUBLIC_INTERFACE
class NoteInDB(NoteBase):
    """Schema representing a Note in DB (with id and timestamps)."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# PUBLIC_INTERFACE
class NoteList(BaseModel):
    """Schema for a list of notes."""
    notes: list[NoteInDB]
