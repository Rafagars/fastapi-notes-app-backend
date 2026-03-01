from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable = False)
    content = Column(String)
    archived = Column(Boolean, default = False)