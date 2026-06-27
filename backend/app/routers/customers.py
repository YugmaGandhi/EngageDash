"""Customer endpoints. All require a logged-in user; the service applies the
role-based access rules."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.deps.auth import get_current_user
from app.models.customer import CustomerStatus
from app.models.user import User
from app.schemas.customer import (
    CustomerCreate,
    CustomerListItem,
    CustomerResponse,
    CustomerUpdate,
)
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("", response_model=CustomerResponse, status_code=201, summary="Create a customer")
def create_customer(
    data: CustomerCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return CustomerService(db).create_customer(current_user, data)


@router.get("", response_model=list[CustomerListItem], summary="List customers (with filters)")
def list_customers(
    status: CustomerStatus | None = Query(None, description="Filter by status"),
    search: str | None = Query(None, description="Search name, company, or email"),
    assigned_csm_id: int | None = Query(None, description="Filter by owner (admin/manager only)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return CustomerService(db).list_customers(
        current_user,
        status=status,
        search=search,
        assigned_csm_id=assigned_csm_id,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
    summary="Get a customer",
    responses={403: {"description": "Not your customer"}, 404: {"description": "Not found"}},
)
def get_customer(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return CustomerService(db).get_customer(current_user, customer_id)


@router.patch(
    "/{customer_id}",
    response_model=CustomerResponse,
    summary="Update a customer",
    responses={403: {"description": "Not allowed"}, 404: {"description": "Not found"}},
)
def update_customer(
    customer_id: int,
    data: CustomerUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return CustomerService(db).update_customer(current_user, customer_id, data)


@router.delete(
    "/{customer_id}",
    status_code=204,
    summary="Delete a customer (admin/manager only)",
    responses={403: {"description": "Not allowed"}, 404: {"description": "Not found"}},
)
def delete_customer(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    CustomerService(db).delete_customer(current_user, customer_id)
