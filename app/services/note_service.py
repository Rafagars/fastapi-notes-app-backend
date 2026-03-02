from sqlalchemy.orm import Session
from app.repositories import note_repository
from app.models.note import Note

def get_all_notes(db: Session):
    return db.query(Note).all()

def create_new_note(db: Session, title: str, content: str, tag_names: list[str] = []):
    if not title.strip():
        raise ValueError("Tittle can't be empty")

    new_note = Note(title = title, content = content)

    for name in tag_names:
        name = name.strip().lower()
        if name:
            #We search if it already exists
            tag = db.query(Tag).filter(Tag.name == name).first()
            if not tag:
                tag = Tag(name = name)
                db.add(tag)
            new_note.tags.append(tag)
            
    return note_repository.save_note(db, new_note.title, new_note.content, new_note.tags)

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