"""Database access for interactions, including filtered listing."""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.interaction import Interaction, InteractionType
from app.repositories.base import BaseRepository


class InteractionRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Interaction, db)

    def _apply_filters(self, query, type, date_from, date_to):
        """Add the optional type/date filters to a query."""
        if type is not None:
            query = query.where(Interaction.type == type)
        if date_from is not None:
            query = query.where(Interaction.occurred_at >= date_from)
        if date_to is not None:
            query = query.where(Interaction.occurred_at <= date_to)
        return query.order_by(Interaction.occurred_at.desc())

    def list_interactions(
        self,
        customer_id: int | None = None,
        type: InteractionType | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Interaction]:
        """List interactions, optionally for one customer."""
        query = select(Interaction)
        if customer_id is not None:
            query = query.where(Interaction.customer_id == customer_id)
        query = self._apply_filters(query, type, date_from, date_to)
        return list(self.db.scalars(query.offset(skip).limit(limit)).all())

    def list_for_owner(
        self,
        owner_id: int,
        type: InteractionType | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Interaction]:
        """List interactions across all customers owned by a given CSM."""
        # Join to customers so we can filter by who the customer is assigned to.
        query = select(Interaction).join(Customer, Interaction.customer_id == Customer.id).where(
            Customer.assigned_csm_id == owner_id
        )
        query = self._apply_filters(query, type, date_from, date_to)
        return list(self.db.scalars(query.offset(skip).limit(limit)).all())
