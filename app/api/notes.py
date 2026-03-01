from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import note_service

router = APIRouter()

@router.post("/notes")
def create_note(title: str, content: str, db: Session = Depends(get_db)):
    return note_service.create_new_note(db, title, content)

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
    