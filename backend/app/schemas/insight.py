"""Schemas for AI insights."""

from pydantic import BaseModel, Field

from app.models.insight import Sentiment


class InsightAI(BaseModel):
    """The shape we expect the AI to return. Used to validate the parsed JSON."""

    summary: str
    sentiment: Sentiment
    action_items: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
