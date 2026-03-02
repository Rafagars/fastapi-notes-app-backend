from sqlalchemy.orm import Session
from app.repositories import note_repository
from app.models.note import Note

def get_all_notes(db: Session):
    return db.query(Note).all()

def create_new_note(db: Session, title: str, content: str):
    if not title.strip():
        raise ValueError("Tittle can't be empty")
    return note_repository.save_note(db, title, content)

def archive_unarchive(db: Session, note_id: int):
    note = note_repository.toggle_archive_note(db, note_id)
    if not note:
        return None
    return None

def delete_existing_note(db: Session, note_id: int):
    return note_repository.delete_note(db, note_id)

def update_existing_note(db: Session, note_id: int, title: str, content: str):
    if not title.strip():
        raise ValueError("Title can't be empty")
    return note_repository.update_note(db, note_id, title, content)