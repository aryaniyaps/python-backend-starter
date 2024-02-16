from http import HTTPStatus

from fastapi import Request
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
from app.schemas.base import BaseSchema
from app.schemas.errors import (
    HTTPExceptionResult,
    InvalidInputErrorResult,
    RateLimitExceededErrorResult,
    ResourceNotFoundErrorResult,
    UnauthenticatedErrorResult,
    UnexpectedErrorResult,
    ValidationErrorResult,
)


def _create_error_response(
    error_result: BaseSchema,
    status_code: HTTPStatus | int,
) -> ORJSONResponse:
    """Create an error response from the given error result."""
    return ORJSONResponse(
        status_code=status_code,
        content=error_result.model_dump(mode="json"),
    )


async def handle_validation_error(
    _request: Request,
    exception: RequestValidationError,
) -> Response:
    """Handle ValidationError exceptions."""
    return _create_error_response(
        error_result=ValidationErrorResult(
            message="Invalid input detected.",
            errors=exception.errors(),
        ),
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
    )


async def handle_ratelimit_exceeded_error(
    _request: Request,
    exception: RateLimitExceededError,
) -> Response:
    """Handle RateLimitExceededError expections."""
    return _create_error_response(
        error_result=RateLimitExceededErrorResult(
            message=str(exception),
            is_primary=exception.is_primary,
        ),
        status_code=HTTPStatus.TOO_MANY_REQUESTS,
    )


async def handle_http_exception(
    _request: Request,
    exception: HTTPException,
) -> Response:
    """Handle HTTPException exceptions."""
    return _create_error_response(
        error_result=HTTPExceptionResult(
            message=exception.detail,
        ),
        status_code=exception.status_code,
    )


async def handle_invalid_input_error(
    _request: Request,
    exception: InvalidInputError,
) -> Response:
    """Handle InvalidInputError expections."""
    return _create_error_response(
        error_result=InvalidInputErrorResult(
            message=str(exception),
        ),
        status_code=HTTPStatus.BAD_REQUEST,
    )


async def handle_resource_not_found_error(
    _request: Request,
    exception: ResourceNotFoundError,
) -> Response:
    """Handle ResourceNotFound expections."""
    return _create_error_response(
        error_result=ResourceNotFoundErrorResult(
            message=str(exception),
        ),
        status_code=HTTPStatus.NOT_FOUND,
    )


async def handle_unauthenticated_error(
    _request: Request,
    exception: UnauthenticatedError,
) -> Response:
    """Handle UnauthenticatedError expections."""
    return _create_error_response(
        error_result=UnauthenticatedErrorResult(
            message=str(exception),
        ),
        status_code=HTTPStatus.UNAUTHORIZED,
    )


async def handle_unexpected_error(
    _request: Request,
    exception: UnexpectedError,
) -> Response:
    """Handle UnexpectedError expections."""
    return _create_error_response(
        error_result=UnexpectedErrorResult(
            message=str(exception),
        ),
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
