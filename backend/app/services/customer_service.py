"""Customer business logic with role-based access rules.

Access rules (see the RBAC matrix in docs/PLAN.md):
- Admin and Manager can see and manage all customers.
- A CSM can only see and manage customers assigned to them.
- Only Admin and Manager can delete customers.
"""

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.deps.auth import is_admin_or_manager
from app.models.customer import Customer, CustomerStatus
from app.models.user import User
from app.repositories.customer import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    def __init__(self, db: Session):
        self.repo = CustomerRepository(db)

    def list_customers(
        self,
        current_user: User,
        status: CustomerStatus | None = None,
        search: str | None = None,
        assigned_csm_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Customer]:
        # A CSM always sees only their own customers, no matter what filter is asked for.
        if not is_admin_or_manager(current_user):
            assigned_csm_id = current_user.id
        return self.repo.list_customers(
            assigned_csm_id=assigned_csm_id,
            status=status,
            search=search,
            skip=skip,
            limit=limit,
        )

    def get_customer(self, current_user: User, customer_id: int) -> Customer:
        customer = self.repo.get(customer_id)
        if not customer:
            raise NotFoundError("Customer not found")
        self._ensure_can_access(current_user, customer)
        return customer

    def create_customer(self, current_user: User, data: CustomerCreate) -> Customer:
        # If no owner is given, the creator becomes the owner.
        assigned_csm_id = data.assigned_csm_id or current_user.id

        # A CSM can only create customers assigned to themselves.
        if not is_admin_or_manager(current_user) and assigned_csm_id != current_user.id:
            raise PermissionDeniedError("CSMs can only create customers assigned to themselves")

        values = data.model_dump(exclude={"assigned_csm_id"})
        values["assigned_csm_id"] = assigned_csm_id
        values["created_by_id"] = current_user.id
        return self.repo.create(values)

    def update_customer(self, current_user: User, customer_id: int, data: CustomerUpdate) -> Customer:
        # get_customer also enforces that a CSM can only touch their own customer.
        customer = self.get_customer(current_user, customer_id)

        changes = data.model_dump(exclude_unset=True)

        # A CSM cannot reassign a customer to someone else.
        if "assigned_csm_id" in changes and not is_admin_or_manager(current_user):
            if changes["assigned_csm_id"] != current_user.id:
                raise PermissionDeniedError("CSMs cannot reassign customers")

        return self.repo.update(customer, changes)

    def delete_customer(self, current_user: User, customer_id: int) -> None:
        if not is_admin_or_manager(current_user):
            raise PermissionDeniedError("You do not have permission to delete customers")

        customer = self.repo.get(customer_id)
        if not customer:
            raise NotFoundError("Customer not found")
        self.repo.delete(customer)

    def _ensure_can_access(self, current_user: User, customer: Customer) -> None:
        """Raise if a CSM tries to access a customer that isn't theirs."""
        if is_admin_or_manager(current_user):
            return
        if customer.assigned_csm_id != current_user.id:
            raise PermissionDeniedError("You can only access your own customers")
