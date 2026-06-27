"""Customer model and the statuses a customer can be in."""

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.user import User


class CustomerStatus(str, enum.Enum):
    PROSPECT = "prospect"
    ACTIVE = "active"
    AT_RISK = "at_risk"
    CHURNED = "churned"


# Same approach as UserRole: store the value as VARCHAR + CHECK so it works in
# both Postgres and the SQLite test database.
status_column_type = Enum(
    CustomerStatus,
    native_enum=False,
    values_callable=lambda statuses: [status.value for status in statuses],
)


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[CustomerStatus] = mapped_column(
        status_column_type, default=CustomerStatus.PROSPECT, index=True
    )
    health_score: Mapped[int] = mapped_column(Integer, default=50)

    # The CSM who owns this customer, and the user who created the record.
    assigned_csm_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Eager-loaded so responses can show the owner's/creator's name (no extra query
    # per customer). Two FKs point at users, so we say which one each uses.
    assigned_csm: Mapped[User] = relationship(foreign_keys=[assigned_csm_id], lazy="joined")
    created_by: Mapped[User] = relationship(foreign_keys=[created_by_id], lazy="joined")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    @property
    def assigned_csm_name(self) -> str | None:
        return self.assigned_csm.name if self.assigned_csm else None

    @property
    def created_by_name(self) -> str | None:
        return self.created_by.name if self.created_by else None
