"""Interaction business logic.

Access is governed by the parent customer: if a user can access the customer,
they can manage that customer's interactions. We reuse CustomerService for the
access check so the rules live in one place.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.deps.auth import is_admin_or_manager
from app.models.interaction import Interaction, InteractionType
from app.models.user import User
from app.repositories.interaction import InteractionRepository
from app.schemas.interaction import InteractionCreate, InteractionUpdate
from app.services.customer_service import CustomerService


class InteractionService:
    def __init__(self, db: Session):
        self.repo = InteractionRepository(db)
        self.customers = CustomerService(db)

    def create_interaction(self, current_user: User, data: InteractionCreate) -> Interaction:
        # Raises if the user can't access the parent customer.
        self.customers.get_customer(current_user, data.customer_id)

        values = data.model_dump()
        values["created_by_id"] = current_user.id
        return self.repo.create(values)

    def get_interaction(self, current_user: User, interaction_id: int) -> Interaction:
        interaction = self.repo.get(interaction_id)
        if not interaction:
            raise NotFoundError("Interaction not found")
        # Access follows the parent customer.
        self.customers.get_customer(current_user, interaction.customer_id)
        return interaction

    def list_interactions(
        self,
        current_user: User,
        customer_id: int | None = None,
        type: InteractionType | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Interaction]:
        if customer_id is not None:
            # Check the user can see this customer, then list its interactions.
            self.customers.get_customer(current_user, customer_id)
            return self.repo.list_interactions(
                customer_id=customer_id, type=type, date_from=date_from, date_to=date_to,
                skip=skip, limit=limit,
            )

        # No customer filter: admins/managers see everything; a CSM sees only
        # interactions belonging to their own customers.
        if is_admin_or_manager(current_user):
            return self.repo.list_interactions(
                type=type, date_from=date_from, date_to=date_to, skip=skip, limit=limit
            )
        return self.repo.list_for_owner(
            current_user.id, type=type, date_from=date_from, date_to=date_to, skip=skip, limit=limit
        )

    def update_interaction(
        self, current_user: User, interaction_id: int, data: InteractionUpdate
    ) -> Interaction:
        # get_interaction also enforces access via the parent customer.
        interaction = self.get_interaction(current_user, interaction_id)
        changes = data.model_dump(exclude_unset=True)
        return self.repo.update(interaction, changes)
