# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import get_settings

settings = get_settings()

# SQLAlchemy Engine
# echo=False - we control logging through our logging configuration instead
# This prevents SQLAlchemy from creating its own handler and ensures
# all logs go through our custom formatter
# For SQLite: connect_args with check_same_thread=False is needed for FastAPI
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.LOG_SQL_QUERIES,
    future=True,
    connect_args=connect_args,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)


def get_db():
    """
    FastAPI dependency: provides a DB session per request
    and makes sure it's closed afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()