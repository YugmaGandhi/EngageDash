"""Small helper for clearing cached data after changes.

Centralizing this here means every place that changes customers, interactions,
or insights clears the dashboard cache the same way, so the dashboard never
shows stale numbers.
"""

from app.services.dashboard_service import CACHE_KEY_PREFIX


class CacheService:
    def __init__(self, cache=None):
        self.cache = cache  # a RedisCache, or None (e.g. in some tests)

    def invalidate_dashboard(self) -> None:
        """Remove every cached dashboard so the next request recomputes."""
        if self.cache is not None:
            self.cache.delete_pattern(f"{CACHE_KEY_PREFIX}*")
