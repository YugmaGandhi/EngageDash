"""EngageDash backend — application entrypoint.

This is the minimal skeleton (Phase 0). Full OpenAPI metadata, routers, middleware,
database, Redis, and error handling are layered in from Phase 1 onward.
"""

from fastapi import FastAPI

from app.core.error_handlers import register_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import RequestLoggingMiddleware

# Configure logging before anything emits logs.
configure_logging()

app = FastAPI(
    title="EngageDash API",
    version="0.1.0",
    description="AI-powered Customer Success Insights Dashboard — API.",
)

app.add_middleware(RequestLoggingMiddleware)
register_exception_handlers(app)


@app.get("/health", tags=["health"], summary="Health check")
def health() -> dict[str, str]:
    """Liveness probe used by Docker healthchecks and uptime monitoring."""
    return {"status": "ok"}
