import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "excuse-ai-quantum-dev-secret-key-3.14159")
    
    # Database
    db_url = os.environ.get("DATABASE_URL")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = db_url or f"sqlite:///{BASE_DIR / 'excuse.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI Engine Settings
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("AI_API_KEY")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    AI_TIMEOUT = int(os.environ.get("AI_TIMEOUT", "15"))
    
    # Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    MAX_CONTENT_LENGTH = 1024 * 1024  # 1MB limit for safety
