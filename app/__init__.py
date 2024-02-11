from http import HTTPStatus

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app.auth.routes import auth_router
from app.config import settings
from app.core.constants import APP_NAME, SUPPORT_EMAIL
from app.core.error_handlers import (
    handle_http_exception,
    handle_invalid_input_error,
    handle_ratelimit_exceeded_error,
    handle_resource_not_found_error,
    handle_unauthenticated_error,
    handle_unexpected_error,
    handle_validation_error,
)
from app.core.errors import (
    InvalidInputError,
    RateLimitExceededError,
    ResourceNotFoundError,
    UnauthenticatedError,
    UnexpectedError,
)
from app.core.middleware.rate_limiter import rate_limiter_middleware
from app.core.schemas import (
    RateLimitExceededErrorResult,
    UnexpectedErrorResult,
    ValidationErrorResult,
)
from app.health.routes import health_router
from app.oauth.routes import oauth_router
from app.users.routes import users_router


def add_routes(app: FastAPI) -> None:
    """Register routes for the app."""
    app.include_router(health_router)
    app.include_router(users_router)
    app.include_router(auth_router)
    app.include_router(oauth_router)


def add_middleware(app: FastAPI) -> None:
    """Register middleware for the app."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_headers=[
            "X-Requested-With",
            "X-Request-ID",
        ],
        expose_headers=[
            "*",
        ],
    )
    app.add_middleware(GZipMiddleware)
    app.add_middleware(
        BaseHTTPMiddleware,
        dispatch=rate_limiter_middleware,
    )
    app.add_middleware(
        CorrelationIdMiddleware,
        header_name="X-Request-ID",
    )


def create_app() -> FastAPI:
    """Initialize an app instance."""
    app = FastAPI(
        version="0.0.1",
        debug=settings.debug,
        default_response_class=ORJSONResponse,
        openapi_url=settings.openapi_url,
        title=f"{APP_NAME} HTTP API",
        servers=[
            {
                "url": settings.server_url,
            },
        ],
        swagger_ui_parameters={
            "syntaxHighlight.theme": "monokai",
            "displayRequestDuration": True,
        },
        responses={
            HTTPStatus.TOO_MANY_REQUESTS: {
                "model": RateLimitExceededErrorResult,
                "description": "Rate Limit Exceeded Error",
            },
            HTTPStatus.INTERNAL_SERVER_ERROR: {
                "model": UnexpectedErrorResult,
                "description": "Internal Server Error",
            },
            HTTPStatus.UNPROCESSABLE_ENTITY: {
                "model": ValidationErrorResult,
                "description": "Validation Error",
            },
        },
        # TODO @aryaniyaps: add error handlers via `app.add_exception_handler` after
        # a generic ExceptionHandler type is implemented.
        # https://github.com/encode/starlette/pull/2403
        exception_handlers={
            RequestValidationError: handle_validation_error,
            HTTPException: handle_http_exception,
            InvalidInputError: handle_invalid_input_error,
            ResourceNotFoundError: handle_resource_not_found_error,
            UnauthenticatedError: handle_unauthenticated_error,
            UnexpectedError: handle_unexpected_error,
            RateLimitExceededError: handle_ratelimit_exceeded_error,
        },
        contact={
            "email": SUPPORT_EMAIL,
        },
    )
    add_middleware(app)
    add_routes(app)
    return app
