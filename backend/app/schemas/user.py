"""Pydantic schemas for users (what the API accepts and returns)."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.user import UserRole


class UserResponse(BaseModel):
    """A user as returned by the API (never includes the password)."""

    # from_attributes lets us build this straight from a SQLAlchemy User object.
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime


class UserUpdate(BaseModel):
    """Fields a user can change on their own profile."""

    name: str | None = None


class AdminUserUpdate(BaseModel):
    """Fields an admin can change on another user."""

    role: UserRole | None = None
    is_active: bool | None = None
