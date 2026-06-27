"""Pydantic schemas for customers."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.customer import CustomerStatus


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    company: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=50)
    status: CustomerStatus = CustomerStatus.PROSPECT
    health_score: int = Field(default=50, ge=0, le=100)
    # Optional: which CSM owns this customer. If left out, the creator is used.
    assigned_csm_id: int | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Jordan Lee",
                "company": "Acme Corp",
                "email": "jordan@acme.com",
                "phone": "+1-555-0100",
                "status": "active",
                "health_score": 80,
            }
        }
    }


class CustomerUpdate(BaseModel):
    """All fields optional — only the ones provided are changed."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    company: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=50)
    status: CustomerStatus | None = None
    health_score: int | None = Field(default=None, ge=0, le=100)
    assigned_csm_id: int | None = None


class CustomerResponse(BaseModel):
    """Full customer detail."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    company: str | None
    email: EmailStr | None
    phone: str | None
    status: CustomerStatus
    health_score: int
    assigned_csm_id: int
    created_by_id: int
    created_at: datetime
    updated_at: datetime


class CustomerListItem(BaseModel):
    """Lighter shape used in list views."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    company: str | None
    status: CustomerStatus
    health_score: int
    assigned_csm_id: int
