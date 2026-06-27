"""Global exception handlers producing a consistent error envelope.

Every error response has the shape:

    {"error": {"code": "<machine_code>", "message": "<human>", "details": <any|null>}}
"""

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import get_settings
from app.core.exceptions import AppError

logger = logging.getLogger("engagedash.errors")


def _envelope(code: str, message: str, details: Any | None = None) -> dict[str, Any]:
    return {"error": {"code": code, "message": message, "details": details}}


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=_envelope(exc.code, exc.message, exc.details),
    )


async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    # Surface field-level errors in a clean, JSON-serializable form.
    return JSONResponse(
        status_code=422,
        content=_envelope(
            "validation_error",
            "Request validation failed.",
            jsonable_encoder(exc.errors()),
        ),
    )


async def http_exception_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    # Wrap framework HTTPExceptions (e.g. 404 routing, auth deps) in the envelope.
    return JSONResponse(
        status_code=exc.status_code,
        content=_envelope("http_error", str(exc.detail)),
        headers=getattr(exc, "headers", None),
    )


async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception: %s", exc)
    settings = get_settings()
    # Never leak internals in production.
    message = "Internal server error." if settings.is_production else f"{type(exc).__name__}: {exc}"
    return JSONResponse(status_code=500, content=_envelope("internal_error", message))


def register_exception_handlers(app: FastAPI) -> None:
    """Register all handlers on the FastAPI app."""
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
