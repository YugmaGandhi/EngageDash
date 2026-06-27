"""Pydantic schemas for authentication requests and responses."""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Sign-up payload. New users always start with the 'csm' role; only an
    admin can change a user's role later."""

    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Asha Patel",
                "email": "asha@example.com",
                "password": "supersecret123",
            }
        }
    }


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {"email": "asha@example.com", "password": "supersecret123"}
        }
    }


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    """Returned on login and refresh."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
