from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Load DB path from .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///water_tracker.db")

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency to get DB session (useful for FastAPI later)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
