"""Admin-only user management endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.exceptions import NotFoundError
from app.deps.auth import require_admin
from app.repositories.user import UserRepository
from app.schemas.user import AdminUserUpdate, UserResponse

# Every route here requires an admin (applied to the whole router).
router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[UserResponse], summary="List all users (admin only)")
def list_users(db: Session = Depends(get_db)):
    return UserRepository(db).list()


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update a user's role or active status (admin only)",
    responses={404: {"description": "User not found"}},
)
def update_user(user_id: int, data: AdminUserUpdate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get(user_id)
    if not user:
        raise NotFoundError("User not found")
    changes = data.model_dump(exclude_unset=True)
    return repo.update(user, changes)
