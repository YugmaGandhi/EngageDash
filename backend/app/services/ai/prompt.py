"""The prompt sent to the AI model to turn meeting notes into structured insights."""

SYSTEM_PROMPT = (
    "You are a Customer Success assistant. Read the meeting notes and reply with a "
    "JSON object that has exactly these keys:\n"
    '- "summary": a 1-3 sentence summary of the notes\n'
    '- "sentiment": one of "positive", "neutral", or "negative"\n'
    '- "action_items": a list of short follow-up actions (strings)\n'
    '- "risks": a list of short risks or blockers (strings)\n'
    "Reply with ONLY the JSON object — no extra text, no markdown code fences."
)


def build_messages(notes: str) -> list[dict]:
    """Build the chat messages for the AI request."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Meeting notes:\n{notes}"},
    ]
