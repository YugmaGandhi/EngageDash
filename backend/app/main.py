"""EngageDash backend — application entrypoint.

This is the minimal skeleton (Phase 0). Full OpenAPI metadata, routers, middleware,
database, Redis, and error handling are layered in from Phase 1 onward.
"""

from fastapi import FastAPI

app = FastAPI(
    title="EngageDash API",
    version="0.1.0",
    description="AI-powered Customer Success Insights Dashboard — API.",
)


@app.get("/health", tags=["health"], summary="Health check")
def health() -> dict[str, str]:
    """Liveness probe used by Docker healthchecks and uptime monitoring."""
    return {"status": "ok"}
