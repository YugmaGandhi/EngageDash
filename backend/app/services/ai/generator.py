"""Generate an insight from notes, with retries and a safe fallback.

This function never raises: if the AI call fails (no API key, network error,
bad JSON, or invalid shape) it returns a neutral fallback insight marked with
status=FALLBACK, so the user-facing request still succeeds.
"""

import logging
from dataclasses import dataclass

from app.models.insight import InsightStatus, Sentiment
from app.schemas.insight import InsightAI
from app.services.ai.client import AIClient
from app.services.ai.parsing import parse_insight
from app.services.ai.prompt import build_messages

logger = logging.getLogger("engagedash.ai")

MAX_ATTEMPTS = 2
FALLBACK_SUMMARY = (
    "AI insight could not be generated automatically. Please review the notes manually."
)


@dataclass
class GeneratedInsight:
    """The result of an insight generation attempt (success or fallback)."""

    data: InsightAI
    status: InsightStatus
    model: str | None
    raw_response: str | None


def generate_insight(notes: str) -> GeneratedInsight:
    messages = build_messages(notes)
    raw_response = None
    model = None
    last_error = None

    try:
        client = AIClient()
        model = client.model
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                raw_response = client.generate(messages)
                data = parse_insight(raw_response)
                return GeneratedInsight(data, InsightStatus.SUCCESS, model, raw_response)
            except Exception as error:
                last_error = error
                logger.warning("AI attempt %d failed: %s", attempt, error)
    except Exception as error:
        # e.g. the client could not be built (missing API key).
        last_error = error

    logger.error("AI insight generation failed, using fallback: %s", last_error)
    fallback = InsightAI(
        summary=FALLBACK_SUMMARY,
        sentiment=Sentiment.NEUTRAL,
        action_items=[],
        risks=[],
    )
    return GeneratedInsight(fallback, InsightStatus.FALLBACK, model, raw_response)
