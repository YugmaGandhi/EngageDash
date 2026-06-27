"""Database access for insights."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.insight import Insight
from app.repositories.base import BaseRepository


class InsightRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Insight, db)

    def list_for_interaction(self, interaction_id: int) -> list[Insight]:
        """Return an interaction's insights, newest first."""
        query = (
            select(Insight)
            .where(Insight.interaction_id == interaction_id)
            .order_by(Insight.created_at.desc(), Insight.id.desc())
        )
        return list(self.db.scalars(query).all())
