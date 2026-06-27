"""HTTP middleware: request/response logging with correlation IDs."""

import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import request_id_ctx

logger = logging.getLogger("engagedash.request")

REQUEST_ID_HEADER = "X-Request-ID"


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Assign a request id, log the request/response, and time it."""

    async def dispatch(self, request: Request, call_next) -> Response:
        # Reuse an inbound id (e.g. from a gateway) or mint a new one.
        request_id = request.headers.get(REQUEST_ID_HEADER) or uuid.uuid4().hex
        token = request_id_ctx.set(request_id)

        start = time.perf_counter()
        try:
            response = await call_next(request)
            duration_ms = (time.perf_counter() - start) * 1000
            # Log while the request id context is still set so rid is populated.
            logger.info(
                "%s %s -> %d (%.1fms)",
                request.method,
                request.url.path,
                response.status_code,
                duration_ms,
            )
            response.headers[REQUEST_ID_HEADER] = request_id
            return response
        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000
            logger.exception(
                "%s %s -> unhandled error (%.1fms)", request.method, request.url.path, duration_ms
            )
            raise
        finally:
            request_id_ctx.reset(token)
