"""Interaction model: a meeting, call, email, or note logged for a customer."""

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class InteractionType(str, enum.Enum):
    MEETING = "meeting"
    CALL = "call"
    EMAIL = "email"
    NOTE = "note"


# Stored as VARCHAR + CHECK (works in Postgres and the SQLite test database).
type_column_type = Enum(
    InteractionType,
    native_enum=False,
    values_callable=lambda types: [t.value for t in types],
)


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Deleting a customer also deletes its interactions.
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"), index=True
    )
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    type: Mapped[InteractionType] = mapped_column(type_column_type, default=InteractionType.NOTE)
    title: Mapped[str] = mapped_column(String(255))
    notes: Mapped[str] = mapped_column(Text)  # the meeting notes the AI will summarize
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
