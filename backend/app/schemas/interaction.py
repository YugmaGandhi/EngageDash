"""Pydantic schemas for interactions."""

from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.interaction import InteractionType


def _reject_far_future(value: datetime) -> datetime:
    """Don't allow an interaction to be dated more than a day in the future."""
    now = datetime.now(timezone.utc)
    # Treat a naive datetime as UTC so the comparison works.
    compare = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if compare > now + timedelta(days=1):
        raise ValueError("occurred_at cannot be in the future")
    return value


class InteractionCreate(BaseModel):
    customer_id: int
    type: InteractionType = InteractionType.NOTE
    title: str = Field(min_length=1, max_length=255)
    notes: str = Field(min_length=1)
    occurred_at: datetime

    _check_occurred_at = field_validator("occurred_at")(_reject_far_future)

    model_config = {
        "json_schema_extra": {
            "example": {
                "customer_id": 1,
                "type": "meeting",
                "title": "Quarterly review",
                "notes": "Customer is happy with onboarding but worried about pricing.",
                "occurred_at": "2026-06-20T15:00:00Z",
            }
        }
    }


class InteractionUpdate(BaseModel):
    """All fields optional — only the ones provided are changed."""

    type: InteractionType | None = None
    title: str | None = Field(default=None, min_length=1, max_length=255)
    notes: str | None = Field(default=None, min_length=1)
    occurred_at: datetime | None = None

    @field_validator("occurred_at")
    @classmethod
    def _check_occurred_at(cls, value):
        return _reject_far_future(value) if value is not None else value


class InteractionResponse(BaseModel):
    """Full interaction detail."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    created_by_id: int
    type: InteractionType
    title: str
    notes: str
    occurred_at: datetime
    created_at: datetime
    updated_at: datetime


class InteractionListItem(BaseModel):
    """Lighter shape used in list views."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    type: InteractionType
    title: str
    occurred_at: datetime
