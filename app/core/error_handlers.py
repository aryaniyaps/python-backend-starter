from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.exceptions import HTTPException

from app.core.errors import (
    InvalidInputError,
    ResourceNotFoundError,
    UnauthenticatedError,
    UnexpectedError,
)


async def handle_validation_error(
    _request: Request,
    exception: RequestValidationError,
) -> ORJSONResponse:
    """Handle ValidationError exceptions."""
    return ORJSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Invalid input detected.",
            "errors": jsonable_encoder(exception.errors()),
        },
    )


async def handle_http_exception(
    _request: Request,
    exception: HTTPException,
) -> ORJSONResponse:
    """Handle HTTPExceptions."""
    return ORJSONResponse(
        status_code=exception.status_code,
        content={
            "message": exception.detail,
        },
    )


async def handle_invalid_input_error(
    _request: Request,
    exception: InvalidInputError,
) -> ORJSONResponse:
    """Handle InvalidInputError expections."""
    return ORJSONResponse(
        content={
            "message": exception.message,
        },
        status_code=status.HTTP_400_BAD_REQUEST,
    )


async def handle_resource_not_found_error(
    _request: Request,
    exception: ResourceNotFoundError,
) -> ORJSONResponse:
    """Handle ResourceNotFound expections."""
    return ORJSONResponse(
        content={
            "message": exception.message,
        },
        status_code=status.HTTP_404_NOT_FOUND,
    )


async def handle_unauthenticated_error(
    _request: Request,
    exception: UnauthenticatedError,
) -> ORJSONResponse:
    """Handle UnauthenticatedError expections."""
    return ORJSONResponse(
        content={
            "message": exception.message,
        },
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


async def handle_unexpected_error(
    _request: Request,
    exception: UnexpectedError,
) -> ORJSONResponse:
    """Handle UnexpectedError expections."""
    return ORJSONResponse(
        content={
            "message": exception.message,
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
