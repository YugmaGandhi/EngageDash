"""FastAPI dependencies for authentication and role-based access control.

- `get_current_user` reads the bearer token and loads the logged-in user.
- `require_roles(...)` is used on endpoints to restrict them to certain roles.
- `is_admin_or_manager` is a small helper used when scoping data access.
"""

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.exceptions import PermissionDeniedError, UnauthorizedError
from app.core.security import decode_token
from app.models.user import User, UserRole
from app.repositories.user import UserRepository

# Reads the "Authorization: Bearer <token>" header. auto_error=False so we can
# raise our own consistent error instead of FastAPI's default.
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Return the user identified by the access token, or raise 401."""
    if credentials is None:
        raise UnauthorizedError("Not authenticated")

    try:
        payload = decode_token(credentials.credentials)
    except jwt.PyJWTError:
        raise UnauthorizedError("Invalid or expired token")

    if payload.get("type") != "access":
        raise UnauthorizedError("Wrong token type")

    user = UserRepository(db).get(int(payload["sub"]))
    if not user or not user.is_active:
        raise UnauthorizedError("User not found or disabled")

    return user


def require_roles(*allowed_roles: UserRole):
    """Build a dependency that only allows users with one of the given roles."""

    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise PermissionDeniedError("You do not have permission to perform this action")
        return user

    return checker


# Convenience dependency for admin-only endpoints.
require_admin = require_roles(UserRole.ADMIN)


def is_admin_or_manager(user: User) -> bool:
    """True if the user can see all data; CSMs only see their own."""
    return user.role in (UserRole.ADMIN, UserRole.MANAGER)
