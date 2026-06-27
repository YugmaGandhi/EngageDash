"""Application exception hierarchy.

Raise these from services/routers instead of returning ad-hoc error responses.
They are translated into a consistent JSON envelope by the handlers in
`app.core.error_handlers`.
"""

class AppError(Exception):
    """Base class for errors we raise on purpose.

    Each subclass sets the HTTP `status_code` and a short `code` string.
    `message` is shown to the client; `details` can hold extra context.
    """

    status_code = 500
    code = "internal_error"

    def __init__(self, message=None, details=None):
        self.message = message or self.__class__.__name__
        self.details = details
        super().__init__(self.message)


class BadRequestError(AppError):
    status_code = 400
    code = "bad_request"


class UnauthorizedError(AppError):
    status_code = 401
    code = "unauthorized"


class PermissionDeniedError(AppError):
    status_code = 403
    code = "permission_denied"


class NotFoundError(AppError):
    status_code = 404
    code = "not_found"


class ConflictError(AppError):
    status_code = 409
    code = "conflict"
