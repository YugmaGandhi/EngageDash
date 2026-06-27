"""Thin wrapper around the OpenAI SDK, pointed at NVIDIA's free endpoint.

DeepSeek (a "thinking" model) returns its chain-of-thought in a separate
`reasoning` / `reasoning_content` field and the final answer in `content`.
We use `content` for the actual result and ignore the reasoning.
"""

from openai import OpenAI

from app.core.config import get_settings

# How long to wait for the AI before giving up (seconds).
AI_TIMEOUT_SECONDS = 30


class AIClient:
    def __init__(self):
        settings = get_settings()
        self.model = settings.ai_model
        self._client = OpenAI(
            base_url=settings.ai_base_url,
            api_key=settings.ai_api_key,
            timeout=AI_TIMEOUT_SECONDS,
        )

    def generate(self, messages: list[dict], temperature: float = 0.3, max_tokens: int = 2048) -> str:
        """Send chat messages to the model and return its text answer."""
        completion = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        message = completion.choices[0].message

        # Prefer the final answer; fall back to the reasoning text if content is empty.
        reasoning = getattr(message, "reasoning", None) or getattr(message, "reasoning_content", None)
        return message.content or reasoning or ""
