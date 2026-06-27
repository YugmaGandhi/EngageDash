"""Password hashing and JWT token helpers.

Passwords are hashed with bcrypt. Logins return two JWTs:
- an *access* token (short-lived) sent with each request, and
- a *refresh* token (long-lived) used to get a new access token.
The "type" claim tells the two apart so a refresh token can't be used as an access token.
"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import get_settings

settings = get_settings()


def hash_password(password: str) -> str:
    """Hash a plain password for storage."""
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()


def verify_password(password: str, hashed_password: str) -> bool:
    """Check a plain password against a stored hash."""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def _create_token(subject: str, token_type: str, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(subject),       # who the token is for (the user id)
        "type": token_type,        # "access" or "refresh"
        "iat": now,                # issued-at time
        "exp": now + expires_delta,  # expiry time
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(subject: str) -> str:
    """Create a short-lived access token for the given user id."""
    expires = timedelta(minutes=settings.access_token_expire_minutes)
    return _create_token(subject, "access", expires)


def create_refresh_token(subject: str) -> str:
    """Create a long-lived refresh token for the given user id."""
    expires = timedelta(days=settings.refresh_token_expire_days)
    return _create_token(subject, "refresh", expires)


def decode_token(token: str) -> dict:
    """Decode and validate a token. Raises jwt.PyJWTError if invalid or expired."""
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
