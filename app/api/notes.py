from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import note_service
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class NoteCreate(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []

class TagBase(BaseModel):
    name: str

class TagRead(TagBase):
    id: int
    class Config:
        orm_mode = True
        from_attributes = True

class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    archived: bool
    tags: List[TagRead] = []

    class Config:
        orm_mode = True
        from_attributes = True

@router.get("/notes")
def get_notes(tag: str = None, db: Session = Depends(get_db)):
    if tag:
        return note_service.filter_notes_by_tag(db, tag)
    return note_service.get_all_notes(db)

@router.post("/notes")
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    return note_service.create_new_note(db, note.title, note.content, note.tags)

@router.patch("/notes/{note_id}/archive")
def archive_note(note_id: int, db: Session = Depends(get_db)):
    updated_note = note_service.archive_unarchive(db, note_id)
    if not updated_note:
        return {"error": "Note not found"}
    return updated_note

@router.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    success = note_service.delete_existing_note(db, note_id)
    if not success:
        return {"error": "Couldn't delete the note or it doesn't exist"}
    return {"message": "Note deleted"}

@router.put("/notes/{note_id}")
def update_note(note_id: int, title: str, content: str, db: Session = Depends(get_db)):
    updated = note_service.update_existing_note(db, note_id, title, content)
    if not updated:
        return {"error": "Not not found"}
    return updated
    