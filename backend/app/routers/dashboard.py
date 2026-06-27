"""Dashboard endpoint: aggregated business metrics for the logged-in user."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.redis import RedisCache, get_redis
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get(
    "",
    response_model=DashboardResponse,
    summary="Get dashboard metrics (scoped to your role)",
)
def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    cache: RedisCache = Depends(get_redis),
):
    return DashboardService(db, cache).get_dashboard(current_user)
