from sqlalchemy.orm import Session
from app.models.note import Note

def save_note(db: Session, title: str, content: str):
    db_note = Note(title = title, content = content, archived=False)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def toggle_archive_note(db: Session, note_id: int):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note:
        db_note.archived = not db_note.archived #Change from True to False and viceversa
        db.commit()
        db.refresh(db_note)
    return db_note

def delete_note(db: Session, note_id: int):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note:
        db.delete_note(db_note)
        db.commit()
        return True
    return False

def update_note(db: Session, note_id: int, title: str, content: str):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note:
        db_note.title = title
        db_note.content = content
        db.commit()
        db.refresh(db_note)
    return db_note