"""Insight model: the AI-generated analysis of an interaction's notes.

We keep every generated insight (an interaction can have several over time, e.g.
if it is regenerated). The "latest" insight is simply the newest by created_at.
"""

import enum
from datetime import datetime

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Sentiment(str, enum.Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class InsightStatus(str, enum.Enum):
    SUCCESS = "success"    # the AI returned a usable result
    FALLBACK = "fallback"  # the AI failed, so we stored safe default values


sentiment_column_type = Enum(
    Sentiment,
    native_enum=False,
    values_callable=lambda values: [v.value for v in values],
)
status_column_type = Enum(
    InsightStatus,
    native_enum=False,
    values_callable=lambda values: [v.value for v in values],
)


class Insight(Base):
    __tablename__ = "insights"

    id: Mapped[int] = mapped_column(primary_key=True)
    interaction_id: Mapped[int] = mapped_column(
        ForeignKey("interactions.id", ondelete="CASCADE"), index=True
    )

    summary: Mapped[str] = mapped_column(Text)
    sentiment: Mapped[Sentiment] = mapped_column(sentiment_column_type)
    # JSON arrays of short strings.
    action_items: Mapped[list] = mapped_column(JSON, default=list)
    risks: Mapped[list] = mapped_column(JSON, default=list)

    status: Mapped[InsightStatus] = mapped_column(status_column_type, default=InsightStatus.SUCCESS)
    model: Mapped[str | None] = mapped_column(String(255), nullable=True)  # which AI model produced it
    raw_response: Mapped[str | None] = mapped_column(Text, nullable=True)  # raw text, for debugging

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
