from http import HTTPStatus

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse, Response
from starlette.exceptions import HTTPException

from app.core.errors import (
    InvalidInputError,
    RateLimitExceededError,
    ResourceNotFoundError,
    UnauthenticatedError,
    UnexpectedError,
)


async def handle_validation_error(
    _request: Request,
    exception: RequestValidationError,
) -> Response:
    """Handle ValidationError exceptions."""
    return ORJSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content={
            "message": "Invalid input detected.",
            "errors": jsonable_encoder(exception.errors()),
        },
    )


async def handle_ratelimit_exceeded_error(
    _request: Request,
    exception: RateLimitExceededError,
) -> Response:
    """Handle RateLimitExceededError expections."""
    return ORJSONResponse(
        content={
            "message": exception.message,
        },
        status_code=HTTPStatus.TOO_MANY_REQUESTS,
    )


async def handle_http_exception(
    _request: Request,
    exception: HTTPException,
) -> Response:
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
) -> Response:
    """Handle InvalidInputError expections."""
    return ORJSONResponse(
        content={
            "message": exception.message,
        },
        status_code=HTTPStatus.BAD_REQUEST,
    )


async def handle_resource_not_found_error(
    _request: Request,
    exception: ResourceNotFoundError,
) -> Response:
    """Handle ResourceNotFound expections."""
    return ORJSONResponse(
        content={
            "message": exception.message,
        },
        status_code=HTTPStatus.NOT_FOUND,
    )


async def handle_unauthenticated_error(
    _request: Request,
    exception: UnauthenticatedError,
) -> Response:
    """Handle UnauthenticatedError expections."""
    return ORJSONResponse(
        content={
            "message": exception.message,
        },
        status_code=HTTPStatus.UNAUTHORIZED,
    )


async def handle_unexpected_error(
    _request: Request,
    exception: UnexpectedError,
) -> Response:
    """Handle UnexpectedError expections."""
    return ORJSONResponse(
        content={
            "message": exception.message,
        },
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
