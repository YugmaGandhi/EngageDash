"""EngageDash backend — application entrypoint.

This is the minimal skeleton (Phase 0). Full OpenAPI metadata, routers, middleware,
database, Redis, and error handling are layered in from Phase 1 onward.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.error_handlers import register_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import RequestLoggingMiddleware
from app.routers import auth, customers, dashboard, insights, interactions, users

# Configure logging before anything emits logs.
configure_logging()

settings = get_settings()

# Short descriptions for each group of endpoints. These show up as sections
# in the Swagger UI (/docs) and ReDoc (/redoc).
tags_metadata = [
    {"name": "health", "description": "Service health and readiness checks."},
    {"name": "auth", "description": "Register, login, token refresh, and profile."},
    {"name": "users", "description": "User management (admin only)."},
    {"name": "customers", "description": "Manage customers."},
    {"name": "interactions", "description": "Manage customer meetings and interactions."},
    {"name": "insights", "description": "AI-generated insights from meeting notes."},
    {"name": "dashboard", "description": "Aggregated business metrics."},
]

app = FastAPI(
    title="EngageDash API",
    version="0.1.0",
    description=(
        "AI-powered Customer Success Insights Dashboard.\n\n"
        "Manage customers and interactions, generate AI insights from meeting notes, "
        "and view operational metrics."
    ),
    openapi_tags=tags_metadata,
    contact={"name": "EngageDash", "email": "support@engagedash.example"},
    license_info={"name": "MIT"},
)

# Allow the frontend (origins from settings) to call the API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)
register_exception_handlers(app)


@app.get("/health", tags=["health"], summary="Health check")
def health() -> dict[str, str]:
    """Liveness probe used by Docker healthchecks and uptime monitoring."""
    return {"status": "ok"}


# Feature routers.
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(customers.router)
app.include_router(interactions.router)
app.include_router(insights.router)
app.include_router(dashboard.router)
