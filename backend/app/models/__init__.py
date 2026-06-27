"""ORM models package.

Import every model module here so that `Base.metadata` is fully populated for
Alembic autogenerate and for table creation. Models are added in later phases.
"""

from app.core.db import Base

__all__ = ["Base"]
