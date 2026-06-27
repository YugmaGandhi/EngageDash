"""User model and the three roles used for access control."""

import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class UserRole(str, enum.Enum):
    """The roles a user can have. Values are what we store in the database."""

    ADMIN = "admin"
    MANAGER = "manager"
    CSM = "csm"


# Store the role as a VARCHAR with a CHECK constraint (native_enum=False) instead
# of a Postgres ENUM type. This keeps migrations simple and also works in the
# SQLite database used by the tests. `values_callable` makes us store "admin"
# rather than the member name "ADMIN".
role_column_type = Enum(
    UserRole,
    native_enum=False,
    values_callable=lambda roles: [role.value for role in roles],
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(role_column_type, default=UserRole.CSM)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
