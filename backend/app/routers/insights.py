"""AI insight endpoints, nested under an interaction."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.insight import InsightResponse
from app.services.insight_service import InsightService

router = APIRouter(prefix="/interactions", tags=["insights"])


@router.post(
    "/{interaction_id}/insights",
    response_model=InsightResponse,
    status_code=201,
    summary="Generate an AI insight from the interaction's notes",
    responses={403: {"description": "Not allowed"}, 404: {"description": "Interaction not found"}},
)
def generate_insight(
    interaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Run the AI on the interaction's notes and store the result. Calling this
    again generates a new insight (the newest is the latest). If the AI fails,
    a fallback insight is stored with status='fallback'."""
    return InsightService(db).generate_for_interaction(current_user, interaction_id)


@router.get(
    "/{interaction_id}/insights",
    response_model=list[InsightResponse],
    summary="List AI insights for an interaction (newest first)",
    responses={403: {"description": "Not allowed"}, 404: {"description": "Interaction not found"}},
)
def list_insights(
    interaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return InsightService(db).list_for_interaction(current_user, interaction_id)
