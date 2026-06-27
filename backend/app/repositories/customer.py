"""Database access for customers, including filtered listing."""

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.customer import Customer, CustomerStatus
from app.repositories.base import BaseRepository


class CustomerRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Customer, db)

    def list_customers(
        self,
        assigned_csm_id: int | None = None,
        status: CustomerStatus | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Customer]:
        """List customers, optionally filtered by owner, status, or a search term."""
        query = select(Customer)

        if assigned_csm_id is not None:
            query = query.where(Customer.assigned_csm_id == assigned_csm_id)
        if status is not None:
            query = query.where(Customer.status == status)
        if search:
            term = f"%{search}%"
            query = query.where(
                or_(
                    Customer.name.ilike(term),
                    Customer.company.ilike(term),
                    Customer.email.ilike(term),
                )
            )

        query = query.order_by(Customer.id).offset(skip).limit(limit)
        return list(self.db.scalars(query).all())
