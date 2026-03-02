from sqlalchemy.orm import Session, joinedload
from app.repositories import note_repository
from app.models.note import Note

def get_all_notes(db: Session):
    return db.query(Note).options(joinedload(Note.tags)).all()

def create_new_note(db: Session, title: str, content: str, tag_names: list[str] = []):
    if not title.strip():
        raise ValueError("Tittle can't be empty")

    tag_objects = [note_repository.get_or_create_tag(db, name) for name in tag_names]            
    return note_repository.save_note(db, title, content, tag_names=tag_objects)

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

def filter_notes_by_tag(db: Session, tag_name: str):
    if not tag_name:
        return note_repository.get_all_notes(db)
    return note_repository.get_notes_by_tag(db, tag_name)