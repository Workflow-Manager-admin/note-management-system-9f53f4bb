"""
Database connection and session management for notes_backend.

Uses SQLAlchemy and reads database URL from environment variable.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

Base = declarative_base()

# PUBLIC_INTERFACE
def get_database_url():
    """
    Get the database URL from environment variables or default to sqlite.
    """
    return os.getenv("DATABASE_URL", "sqlite:///./notes.db")

DATABASE_URL = get_database_url()

# Create SQLAlchemy engine and session
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
