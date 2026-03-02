import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,    
)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_note_with_tags():
    response = client.post(
        "/notes",
        json={"title": "Test Note", "content": "Content with tags", "tags": ["work", "pytest"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert len(data["tags"]) == 2
    assert data["tags"][0]["name"] == "work"

def test_filter_notes_by_tag():
    
    client.post("/notes", json={"title": "Urgent Note", "content": "...", "tags": ["urgent"]})
   
    client.post("/notes", json={"title": "Normal Note", "content": "...", "tags": ["normal"]})
    
    
    response = client.get("/notes?tag=urgent")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Urgent Note"