"""Insight business logic: generate and list AI insights for an interaction.

Access is enforced through the interaction (and therefore its customer), reusing
InteractionService so the rules stay in one place.
"""

from sqlalchemy.orm import Session

from app.models.insight import Insight
from app.models.user import User
from app.repositories.insight import InsightRepository
from app.services.ai.generator import generate_insight
from app.services.interaction_service import InteractionService


class InsightService:
    def __init__(self, db: Session):
        self.repo = InsightRepository(db)
        self.interactions = InteractionService(db)

    def generate_for_interaction(self, current_user: User, interaction_id: int) -> Insight:
        # Raises 403/404 if the user can't access this interaction.
        interaction = self.interactions.get_interaction(current_user, interaction_id)

        # generate_insight never raises; it returns a success or fallback result.
        result = generate_insight(interaction.notes)

        return self.repo.create(
            {
                "interaction_id": interaction.id,
                "summary": result.data.summary,
                "sentiment": result.data.sentiment,
                "action_items": result.data.action_items,
                "risks": result.data.risks,
                "status": result.status,
                "model": result.model,
                "raw_response": result.raw_response,
            }
        )

    def list_for_interaction(self, current_user: User, interaction_id: int) -> list[Insight]:
        # Access check first.
        self.interactions.get_interaction(current_user, interaction_id)
        return self.repo.list_for_interaction(interaction_id)
