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

# Configure logging before anything emits logs.
configure_logging()

settings = get_settings()

app = FastAPI(
    title="EngageDash API",
    version="0.1.0",
    description="AI-powered Customer Success Insights Dashboard — API.",
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
