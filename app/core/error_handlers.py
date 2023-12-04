from falcon import (
    HTTPBadRequest,
    HTTPInternalServerError,
    HTTPNotFound,
    HTTPUnauthorized,
)
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
    raise HTTPBadRequest(
        description=ex.json(),
    )


async def handle_invalid_input_error(
    req: Request,
    resp: Response,
    ex: InvalidInputError,
    params,
) -> None:
    """Handle InvalidInputError expections."""
    raise HTTPBadRequest(
        description=ex.message,
    )


async def handle_resource_not_found_error(
    req: Request,
    resp: Response,
    ex: ResourceNotFoundError,
    params,
) -> None:
    """Handle ResourceNotFound expections."""
    raise HTTPNotFound(
        description=ex.message,
    )


async def handle_unauthenticated_error(
    req: Request,
    resp: Response,
    ex: UnauthenticatedError,
    params,
) -> None:
    """Handle UnauthenticatedError expections."""
    raise HTTPUnauthorized(
        description=ex.message,
    )


async def handle_unexpected_error(
    req: Request,
    resp: Response,
    ex: UnexpectedError,
    params,
) -> None:
    """Handle Unexpected expections."""
    raise HTTPInternalServerError(
        description=ex.message,
    )
