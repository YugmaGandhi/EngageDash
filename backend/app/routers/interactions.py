"""Interaction endpoints. All require a logged-in user; the service applies the
access rules based on the parent customer."""

from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.deps.auth import get_current_user
from app.models.interaction import InteractionType
from app.models.user import User
from app.schemas.interaction import (
    InteractionCreate,
    InteractionListItem,
    InteractionResponse,
    InteractionUpdate,
)
from app.services.interaction_service import InteractionService

router = APIRouter(prefix="/interactions", tags=["interactions"])


@router.post(
    "",
    response_model=InteractionResponse,
    status_code=201,
    summary="Log an interaction",
    responses={403: {"description": "Not your customer"}, 404: {"description": "Customer not found"}},
)
def create_interaction(
    data: InteractionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return InteractionService(db).create_interaction(current_user, data)


@router.get(
    "",
    response_model=list[InteractionListItem],
    summary="List interactions (with filters)",
)
def list_interactions(
    customer_id: int | None = Query(None, description="Filter by customer"),
    type: InteractionType | None = Query(None, description="Filter by type"),
    date_from: datetime | None = Query(None, description="Only on/after this time"),
    date_to: datetime | None = Query(None, description="Only on/before this time"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return InteractionService(db).list_interactions(
        current_user,
        customer_id=customer_id,
        type=type,
        date_from=date_from,
        date_to=date_to,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{interaction_id}",
    response_model=InteractionResponse,
    summary="Get an interaction",
    responses={403: {"description": "Not allowed"}, 404: {"description": "Not found"}},
)
def get_interaction(
    interaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return InteractionService(db).get_interaction(current_user, interaction_id)


@router.patch(
    "/{interaction_id}",
    response_model=InteractionResponse,
    summary="Update an interaction",
    responses={403: {"description": "Not allowed"}, 404: {"description": "Not found"}},
)
def update_interaction(
    interaction_id: int,
    data: InteractionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return InteractionService(db).update_interaction(current_user, interaction_id, data)
