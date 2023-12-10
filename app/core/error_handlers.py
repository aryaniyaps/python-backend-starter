import logging

from falcon import HTTP_400, HTTP_401, HTTP_404, HTTP_500
from falcon.asgi import Request, Response
from pydantic import ValidationError

from app.core.errors import (
    InvalidInputError,
    ResourceNotFoundError,
    UnauthenticatedError,
    UnexpectedError,
)


async def handle_validation_error(
    _req: Request,
    resp: Response,
    ex: ValidationError,
    _params,
) -> None:
    """Handle ValidationError exceptions."""
    resp.status = HTTP_400
    resp.media = {
        "message": "Invalid input detected.",
        "errors": ex.errors(
            include_url=False,
            include_context=False,
            include_input=False,
        ),
    }


async def handle_invalid_input_error(
    _req: Request,
    resp: Response,
    ex: InvalidInputError,
    _params,
) -> None:
    """Handle InvalidInputError expections."""
    resp.status = HTTP_400
    resp.media = {
        "message": ex.message,
    }


async def handle_resource_not_found_error(
    _req: Request,
    resp: Response,
    ex: ResourceNotFoundError,
    _params,
) -> None:
    """Handle ResourceNotFound expections."""
    resp.status = HTTP_404
    resp.media = {
        "message": ex.message,
    }


async def handle_unauthenticated_error(
    _req: Request,
    resp: Response,
    ex: UnauthenticatedError,
    _params,
) -> None:
    """Handle UnauthenticatedError expections."""
    resp.status = HTTP_401
    resp.media = {
        "message": ex.message,
    }


async def handle_unexpected_error(
    _req: Request,
    resp: Response,
    ex: UnexpectedError,
    _params,
) -> None:
    """Handle UnexpectedError expections."""
    resp.status = HTTP_500
    resp.media = {
        "message": ex.message,
    }


async def handle_uncaught_exception(
    _req: Request,
    resp: Response,
    ex: Exception,
    _params,
) -> None:
    """Handle uncaught expections."""
    logging.error(ex, stack_info=True, stacklevel=2)
    resp.status = HTTP_500
    resp.media = {
        "message": "An unexpected error occurred.",
    }
