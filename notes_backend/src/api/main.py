from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import schemas, crud
from .database import engine, SessionLocal, Base

app = FastAPI(
    title="Notes FastAPI Backend",
    description="API for managing notes: create, read, update, delete.",
    version="1.0.0",
    openapi_tags=[
        {"name": "notes", "description": "Operations for notes management"}
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    """Create database tables at startup if they do not exist."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency that provides a DB session, and closes it after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", summary="Health Check", description="Check backend health", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"message": "Healthy"}

# --- CRUD Endpoints ---

# PUBLIC_INTERFACE
@app.post("/notes/", response_model=schemas.NoteInDB, status_code=status.HTTP_201_CREATED, tags=["notes"], summary="Create Note")
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    """
    Create a new note.
    """
    return crud.create_note(db, note)

# PUBLIC_INTERFACE
@app.get("/notes/", response_model=List[schemas.NoteInDB], tags=["notes"], summary="List Notes")
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all notes, most recent first.
    """
    return crud.get_notes(db, skip=skip, limit=limit)

# PUBLIC_INTERFACE
@app.get("/notes/{note_id}", response_model=schemas.NoteInDB, tags=["notes"], summary="Get Note")
def read_note(note_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single note by its ID.
    """
    db_note = crud.get_note(db, note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

# PUBLIC_INTERFACE
@app.put("/notes/{note_id}", response_model=schemas.NoteInDB, tags=["notes"], summary="Update Note")
def update_note(note_id: int, note_update: schemas.NoteUpdate, db: Session = Depends(get_db)):
    """
    Update an existing note by its ID.
    """
    db_note = crud.update_note(db, note_id, note_update)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

# PUBLIC_INTERFACE
@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["notes"], summary="Delete Note")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """
    Delete a note by its ID.
    """
    db_note = crud.delete_note(db, note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return None
