"""Database access for users."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> User | None:
        """Find a user by email, or return None."""
        query = select(User).where(User.email == email)
        return self.db.scalars(query).first()
