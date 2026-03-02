from sqlalchemy.orm import Session
from app.models.note import Note, Tag

def save_note(db: Session, title: str, content: str, tag_names: list = []):
    db_note = Note(title = title, content = content, archived=False)

    db_note.tags = tag_names

    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_or_create_tag(db: Session, name:str):
    name = name.lower().strip()
    tag = db.query(Tag).filter(Tag.name == name).first()
    if not tag:
        tag = Tag(name = name)
        db.add(tag)
        db.commit()
        db.refresh(tag)
    return tag

def get_notes_by_tag(db: Session, tag_name: str):
    return db.query(Note).join(Note.tags).filter(Tag.name == tag_name).all()

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
        db.delete(db_note)
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