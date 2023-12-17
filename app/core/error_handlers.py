from pydantic import ValidationError
from sanic import Request
from sanic.response import JSONResponse, json

from app.core.errors import (
    InvalidInputError,
    ResourceNotFoundError,
    UnauthenticatedError,
    UnexpectedError,
)


async def handle_validation_error(
    _request: Request,
    exception: ValidationError,
) -> JSONResponse:
    """Handle ValidationError exceptions."""
    return json(
        body={
            "message": "Invalid input detected.",
            "errors": exception.errors(
                include_url=False,
                include_context=False,
                include_input=False,
            ),
        },
        status=422,
    )


async def handle_invalid_input_error(
    _request: Request,
    exception: InvalidInputError,
) -> JSONResponse:
    """Handle InvalidInputError expections."""
    return json(
        body={
            "message": exception.message,
        },
        status=400,
    )


async def handle_resource_not_found_error(
    _request: Request,
    exception: ResourceNotFoundError,
) -> JSONResponse:
    """Handle ResourceNotFound expections."""
    return json(
        body={
            "message": exception.message,
        },
        status=404,
    )


async def handle_unauthenticated_error(
    _request: Request,
    exception: UnauthenticatedError,
) -> JSONResponse:
    """Handle UnauthenticatedError expections."""
    return json(
        body={
            "message": exception.message,
        },
        status=401,
    )


async def handle_unexpected_error(
    _request: Request,
    exception: UnexpectedError,
) -> JSONResponse:
    """Handle UnexpectedError expections."""
    return json(
        body={
            "message": exception.message,
        },
        status=500,
    )
