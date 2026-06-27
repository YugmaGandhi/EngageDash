"""Schemas for AI insights."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.insight import InsightStatus, Sentiment


class InsightAI(BaseModel):
    """The shape we expect the AI to return. Used to validate the parsed JSON."""

    summary: str
    sentiment: Sentiment
    action_items: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)


class InsightResponse(BaseModel):
    """An insight as returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    interaction_id: int
    summary: str
    sentiment: Sentiment
    action_items: list[str]
    risks: list[str]
    status: InsightStatus  # "success" or "fallback"
    model: str | None
    created_at: datetime
