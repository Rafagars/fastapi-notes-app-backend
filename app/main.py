from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.api import notes
from app.database import engine, Base
from app.models.note import Note

# Creates automatically the tables when it iniciates
Base.metadata.create_all(bind = engine)

app = FastAPI(title="Notes API")

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

origins = [
    "http://localhost:5173",  # Default Vite's port (Vue)
    "http://127.0.0.1:5173",
    frontend_url,
    frontend_url.strip("/"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"], # Allows GET, POST, PUT, DELETE, etc.
    allow_header= ["*"]
)

# Includes the router
app.include_router(notes.router)

@app.get("/")
def health_check():
    return {"status": "ok"}