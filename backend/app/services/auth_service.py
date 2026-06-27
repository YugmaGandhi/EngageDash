"""Authentication logic: register, login, and refresh.

The router calls these methods; this class holds the actual rules so the router
stays thin.
"""

import jwt
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User, UserRole
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse


class AuthService:
    def __init__(self, db: Session):
        self.users = UserRepository(db)

    def register(self, data: RegisterRequest) -> User:
        """Create a new user. Fails if the email is already taken."""
        email = data.email.lower()
        if self.users.get_by_email(email):
            raise ConflictError("Email already registered")

        return self.users.create(
            {
                "name": data.name,
                "email": email,
                "hashed_password": hash_password(data.password),
                "role": UserRole.CSM,  # everyone starts as a CSM
            }
        )

    def authenticate(self, email: str, password: str) -> User:
        """Return the user if the email/password are correct and active."""
        user = self.users.get_by_email(email.lower())
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")
        if not user.is_active:
            raise UnauthorizedError("Account is disabled")
        return user

    def login(self, data: LoginRequest) -> TokenResponse:
        user = self.authenticate(data.email, data.password)
        return self._tokens_for(user)

    def refresh(self, refresh_token: str) -> TokenResponse:
        """Exchange a valid refresh token for a fresh pair of tokens."""
        try:
            payload = decode_token(refresh_token)
        except jwt.PyJWTError:
            raise UnauthorizedError("Invalid or expired refresh token")

        if payload.get("type") != "refresh":
            raise UnauthorizedError("Wrong token type")

        user = self.users.get(int(payload["sub"]))
        if not user or not user.is_active:
            raise UnauthorizedError("User not found or disabled")

        return self._tokens_for(user)

    def _tokens_for(self, user: User) -> TokenResponse:
        """Build a new access + refresh token pair for a user."""
        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )
