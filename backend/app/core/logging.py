"""Logging configuration with per-request correlation IDs.

`request_id_ctx` is populated by the request-logging middleware and injected into
every log record via `RequestIdFilter`, so all logs emitted while handling a
request carry its id.
"""

import logging
from contextvars import ContextVar
from logging.config import dictConfig

from app.core.config import get_settings

# Holds the current request's id; "-" when outside a request context.
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    """Attach the current request id to each log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx.get()
        return True


def configure_logging() -> None:
    """Configure application logging from settings (idempotent)."""
    settings = get_settings()
    level = settings.log_level.upper()

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "request_id": {"()": "app.core.logging.RequestIdFilter"},
            },
            "formatters": {
                "standard": {
                    "format": "%(asctime)s | %(levelname)-8s | %(name)s | "
                    "rid=%(request_id)s | %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "filters": ["request_id"],
                },
            },
            "root": {"handlers": ["console"], "level": level},
            "loggers": {
                # Tame access-log noise; our middleware logs requests instead.
                "uvicorn.access": {"handlers": ["console"], "level": "WARNING", "propagate": False},
                "uvicorn.error": {"handlers": ["console"], "level": level, "propagate": False},
            },
        }
    )
