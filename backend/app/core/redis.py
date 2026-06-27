"""Redis client and small JSON cache helpers.

A single connection-pooled client is shared across the app. `RedisCache` wraps it
with JSON (de)serialization, TTL support, and pattern-based invalidation used by
the dashboard caching layer.
"""

import json
from collections.abc import Generator
from typing import Any

import redis

from app.core.config import get_settings

settings = get_settings()

# `decode_responses=True` -> values come back as str, not bytes.
redis_client: redis.Redis = redis.from_url(
    settings.redis_url,
    decode_responses=True,
)


class RedisCache:
    """Thin JSON-aware wrapper over a Redis client."""

    def __init__(self, client: redis.Redis) -> None:
        self._client = client

    def get_json(self, key: str) -> Any | None:
        """Return the deserialized value at `key`, or None if absent/corrupt."""
        raw = self._client.get(key)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return None

    def set_json(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Store `value` as JSON, optionally with a TTL (seconds)."""
        payload = json.dumps(value, default=str)
        if ttl and ttl > 0:
            self._client.set(key, payload, ex=ttl)
        else:
            self._client.set(key, payload)

    def delete(self, *keys: str) -> int:
        """Delete one or more keys; returns the count removed."""
        if not keys:
            return 0
        return self._client.delete(*keys)

    def delete_pattern(self, pattern: str) -> int:
        """Delete every key matching `pattern` (e.g. 'dashboard:*'). Returns count."""
        deleted = 0
        # scan_iter avoids blocking Redis the way KEYS would on large datasets.
        keys = list(self._client.scan_iter(match=pattern, count=500))
        if keys:
            deleted = self._client.delete(*keys)
        return deleted

    def ping(self) -> bool:
        """Return True if the Redis server responds."""
        return bool(self._client.ping())


# Shared cache instance.
cache = RedisCache(redis_client)


def get_redis() -> Generator[RedisCache, None, None]:
    """FastAPI dependency yielding the shared cache wrapper."""
    yield cache
