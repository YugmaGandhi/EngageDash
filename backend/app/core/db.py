"""Database engine, session factory, and the declarative base.

Uses SQLAlchemy 2.0 (sync) with psycopg 3. Request handlers depend on `get_db`
to receive a session that is always closed after the request.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()


class Base(DeclarativeBase):
    """Base class that all ORM models inherit from."""

    pass


# `pool_pre_ping` checks a connection is alive before using it (avoids errors
# from connections the database closed while idle).
engine = create_engine(settings.database_url, pool_pre_ping=True)

# `expire_on_commit=False` lets us keep reading an object's fields after commit
# without SQLAlchemy firing another query.
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a DB session and guarantees cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
