"""Turn the AI's raw text into a validated InsightAI object.

Models sometimes wrap JSON in ```code fences``` or add a sentence before/after it,
so we extract the JSON object first, then normalize and validate it.
"""

import json

from app.schemas.insight import InsightAI


def parse_insight(text: str) -> InsightAI:
    """Parse and validate the model's response. Raises ValueError if it can't."""
    json_text = _extract_json_object(text)
    data = json.loads(json_text)  # raises json.JSONDecodeError (a ValueError) if invalid

    if not isinstance(data, dict):
        raise ValueError("AI response is not a JSON object")

    data["sentiment"] = _normalize_sentiment(data.get("sentiment"))
    data["action_items"] = _as_string_list(data.get("action_items"))
    data["risks"] = _as_string_list(data.get("risks"))

    return InsightAI(**data)  # raises ValidationError if the shape is still wrong


def _extract_json_object(text: str) -> str:
    """Return the substring from the first '{' to the last '}'."""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON object found in AI response")
    return text[start : end + 1]


def _normalize_sentiment(value):
    """Lowercase/trim sentiment so 'Positive' or ' POSITIVE ' still match the enum."""
    if isinstance(value, str):
        return value.strip().lower()
    return value


def _as_string_list(value) -> list[str]:
    """Coerce the value into a clean list of non-empty strings."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return []
