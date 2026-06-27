"""ORM models package.

Import every model module here so that `Base.metadata` is fully populated for
Alembic autogenerate and for table creation. Models are added in later phases.
"""

from app.core.db import Base
from app.models.customer import Customer, CustomerStatus
from app.models.interaction import Interaction, InteractionType
from app.models.user import User, UserRole

__all__ = [
    "Base",
    "User",
    "UserRole",
    "Customer",
    "CustomerStatus",
    "Interaction",
    "InteractionType",
]
