"""A small base class with the CRUD operations every entity needs.

Each feature repository (CustomerRepository, InteractionRepository, ...) will
subclass this and pass its own model. This keeps the basic get / list / create /
update / delete code in one place instead of repeating it for every entity.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, model, db: Session):
        # `model` is the SQLAlchemy model class (e.g. Customer).
        # `db` is the database session for the current request.
        self.model = model
        self.db = db

    def get(self, id):
        """Return one row by its primary key, or None if not found."""
        return self.db.get(self.model, id)

    def list(self, skip: int = 0, limit: int = 100):
        """Return a page of rows (skip = offset, limit = page size)."""
        query = select(self.model).offset(skip).limit(limit)
        return list(self.db.scalars(query).all())

    def create(self, data: dict):
        """Create a new row from a dict of field values and save it."""
        obj = self.model(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj, data: dict):
        """Update the given row with the provided fields and save it."""
        for field, value in data.items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj):
        """Delete the given row."""
        self.db.delete(obj)
        self.db.commit()
