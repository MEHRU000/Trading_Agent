"""
Database connection module.
Initializes SQLAlchemy engine and session factory.
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.utils.config import settings
from app.utils.logger import app_logger

# SQLAlchemy declarative base for ORM models
Base = declarative_base()

# Configure database engine
connect_args = {}
# SQLite requires disabling thread check for multi-threaded FastAPI access
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

try:
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args=connect_args,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    app_logger.info(f"Database engine initialized for {settings.DATABASE_URL.split('///')[-1]}")
except Exception as e:
    app_logger.critical(f"Failed to initialize database engine: {e}")
    raise e


def get_db() -> Generator[Session, None, None]:
    """
    Dependency generator for database sessions.
    Ensures sessions are closed after request lifecycle.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initializes all database tables based on ORM definitions.
    """
    try:
        Base.metadata.create_all(bind=engine)
        app_logger.info("Database tables initialized successfully.")
    except Exception as e:
        app_logger.error(f"Error initializing database tables: {e}")
        raise e
