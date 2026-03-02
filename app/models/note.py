from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

note_tags = Table(
    "note_tags",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable = False)
    content = Column(String)
    archived = Column(Boolean, default = False)

    tags = relationship("Tag", secondary=note_tags, back_populates="notes")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    notes = relationship("Note", secondary=note_tags, back_populates="tags")