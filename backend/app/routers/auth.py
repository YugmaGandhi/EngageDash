"""Authentication endpoints: register, login, refresh, and profile."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.deps.auth import get_current_user
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserResponse, UserUpdate
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    responses={409: {"description": "Email already registered"}},
)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return AuthService(db).register(data)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Log in and receive access + refresh tokens",
    responses={401: {"description": "Invalid email or password"}},
)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return AuthService(db).login(data)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Exchange a refresh token for new tokens",
    responses={401: {"description": "Invalid or expired refresh token"}},
)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    return AuthService(db).refresh(data.refresh_token)


@router.get("/me", response_model=UserResponse, summary="Get my profile")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserResponse, summary="Update my profile")
def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    changes = data.model_dump(exclude_unset=True)
    return UserRepository(db).update(current_user, changes)
