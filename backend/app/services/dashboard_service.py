"""Builds the dashboard metrics.

Everything is scoped by role: admins and managers see numbers across all
customers, while a CSM only sees numbers for the customers assigned to them.
"""

from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.deps.auth import is_admin_or_manager
from app.models.customer import Customer, CustomerStatus
from app.models.insight import Insight, InsightStatus, Sentiment
from app.models.interaction import Interaction
from app.models.user import User

RECENT_DAYS = 7
RECENT_INTERACTIONS_LIMIT = 5

# All dashboard cache keys start with this, so they are easy to clear together.
CACHE_KEY_PREFIX = "dashboard:"


class DashboardService:
    def __init__(self, db: Session, cache=None):
        self.db = db
        self.cache = cache  # a RedisCache, or None to skip caching

    def get_dashboard(self, user: User) -> dict:
        """Return metrics from the cache if present, otherwise compute and cache them."""
        if self.cache is None:
            return self.compute_metrics(user)

        key = self._cache_key(user)
        cached = self.cache.get_json(key)
        if cached is not None:
            return cached

        metrics = self.compute_metrics(user)
        ttl = get_settings().dashboard_cache_ttl_seconds
        self.cache.set_json(key, metrics, ttl=ttl)
        return metrics

    def _cache_key(self, user: User) -> str:
        # Admins and managers share the global view; each CSM has their own key.
        if is_admin_or_manager(user):
            return f"{CACHE_KEY_PREFIX}all"
        return f"{CACHE_KEY_PREFIX}csm:{user.id}"

    def compute_metrics(self, user: User) -> dict:
        # owner_id = None means "no filter" (admins/managers see everything).
        owner_id = None if is_admin_or_manager(user) else user.id

        return {
            "total_customers": self._total_customers(owner_id),
            "customers_by_status": self._customers_by_status(owner_id),
            "at_risk_customers": self._customers_by_status(owner_id).get("at_risk", 0),
            "total_interactions": self._total_interactions(owner_id),
            "interactions_last_7_days": self._recent_interaction_count(owner_id),
            "sentiment_breakdown": self._sentiment_breakdown(owner_id),
            "recent_interactions": self._recent_interactions(owner_id),
        }

    # ---- customers ----

    def _total_customers(self, owner_id: int | None) -> int:
        query = select(func.count()).select_from(Customer)
        if owner_id is not None:
            query = query.where(Customer.assigned_csm_id == owner_id)
        return self.db.scalar(query) or 0

    def _customers_by_status(self, owner_id: int | None) -> dict:
        query = select(Customer.status, func.count()).group_by(Customer.status)
        if owner_id is not None:
            query = query.where(Customer.assigned_csm_id == owner_id)

        # Start every status at 0 so the response always has all of them.
        counts = {status.value: 0 for status in CustomerStatus}
        for status, count in self.db.execute(query).all():
            counts[status.value] = count
        return counts

    # ---- interactions ----

    def _total_interactions(self, owner_id: int | None) -> int:
        query = select(func.count()).select_from(Interaction)
        if owner_id is not None:
            query = query.join(Customer, Interaction.customer_id == Customer.id).where(
                Customer.assigned_csm_id == owner_id
            )
        return self.db.scalar(query) or 0

    def _recent_interaction_count(self, owner_id: int | None) -> int:
        since = datetime.now(timezone.utc) - timedelta(days=RECENT_DAYS)
        query = select(func.count()).select_from(Interaction).where(Interaction.occurred_at >= since)
        if owner_id is not None:
            query = query.join(Customer, Interaction.customer_id == Customer.id).where(
                Customer.assigned_csm_id == owner_id
            )
        return self.db.scalar(query) or 0

    def _recent_interactions(self, owner_id: int | None) -> list[dict]:
        query = select(Interaction)
        if owner_id is not None:
            query = query.join(Customer, Interaction.customer_id == Customer.id).where(
                Customer.assigned_csm_id == owner_id
            )
        query = query.order_by(Interaction.occurred_at.desc()).limit(RECENT_INTERACTIONS_LIMIT)

        return [
            {
                "id": interaction.id,
                "customer_id": interaction.customer_id,
                "type": interaction.type.value,
                "title": interaction.title,
                "occurred_at": interaction.occurred_at,
            }
            for interaction in self.db.scalars(query).all()
        ]

    # ---- insights ----

    def _sentiment_breakdown(self, owner_id: int | None) -> dict:
        query = select(Insight.sentiment, func.count())
        if owner_id is not None:
            # Join insight -> interaction -> customer to scope by the CSM.
            query = (
                query.join(Interaction, Insight.interaction_id == Interaction.id)
                .join(Customer, Interaction.customer_id == Customer.id)
                .where(Customer.assigned_csm_id == owner_id)
            )
        # Only count successful AI results. Fallback insights default to "neutral"
        # because generation failed, so they aren't real sentiment.
        query = query.where(Insight.status == InsightStatus.SUCCESS).group_by(Insight.sentiment)

        counts = {sentiment.value: 0 for sentiment in Sentiment}
        for sentiment, count in self.db.execute(query).all():
            counts[sentiment.value] = count
        return counts
