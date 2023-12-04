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
    req: Request,
    resp: Response,
    ex: ValidationError,
    params,
) -> None:
    """Handle ValidationError exceptions."""
    resp.status = HTTP_400
    resp.media = {
        "message": "Invalid input detected.",
        "errors": ex.errors(),
    }


async def handle_invalid_input_error(
    req: Request,
    resp: Response,
    ex: InvalidInputError,
    params,
) -> None:
    """Handle InvalidInputError expections."""
    resp.status = HTTP_400
    resp.media = {
        "message": ex.message,
    }


async def handle_resource_not_found_error(
    req: Request,
    resp: Response,
    ex: ResourceNotFoundError,
    params,
) -> None:
    """Handle ResourceNotFound expections."""
    resp.status = HTTP_404
    resp.media = {
        "message": ex.message,
    }


async def handle_unauthenticated_error(
    req: Request,
    resp: Response,
    ex: UnauthenticatedError,
    params,
) -> None:
    """Handle UnauthenticatedError expections."""
    resp.status = HTTP_401
    resp.media = {
        "message": ex.message,
    }


async def handle_unexpected_error(
    req: Request,
    resp: Response,
    ex: UnexpectedError,
    params,
) -> None:
    """Handle Unexpected expections."""
    resp.status = HTTP_500
    resp.media = {
        "message": ex.message,
    }
