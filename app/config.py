import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "excuse-ai-quantum-dev-secret-key-3.14159")
    
    # Database configuration
    db_url = os.environ.get("DATABASE_URL")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    if db_url:
        SQLALCHEMY_DATABASE_URI = db_url
    elif os.environ.get("VERCEL"):
        # Vercel serverless functions run on a read-only filesystem except /tmp
        tmp_db = Path("/tmp/excuse.db")
        source_db = BASE_DIR / "excuse.db"
        if source_db.exists() and not tmp_db.exists():
            try:
                shutil.copy2(source_db, tmp_db)
            except Exception:
                pass
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{tmp_db}"
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'excuse.db'}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI Engine Settings
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("AI_API_KEY")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    AI_TIMEOUT = int(os.environ.get("AI_TIMEOUT", "15"))
    
    # Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    MAX_CONTENT_LENGTH = 1024 * 1024  # 1MB limit for safety
