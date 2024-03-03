from http import HTTPStatus

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
from ratelimit import RateLimitMiddleware
from ratelimit.auths.ip import client_ip
from starlette.exceptions import HTTPException

from app.config import settings
from app.lib.constants import APP_NAME, SUPPORT_EMAIL
from app.lib.error_handlers import (
    handle_http_exception,
    handle_invalid_input_error,
    handle_rate_limit_exceeded_error,
    handle_resource_not_found_error,
    handle_unauthenticated_error,
    handle_unexpected_error,
    handle_validation_error,
)
from app.lib.errors import (
    InvalidInputError,
    RateLimitExceededError,
    ResourceNotFoundError,
    UnauthenticatedError,
    UnexpectedError,
)
from app.lib.openapi import generate_operation_id
from app.lib.rate_limit import rate_limit_backend, rate_limit_config
from app.routes.auth import auth_router
from app.routes.health import health_router
from app.routes.user import users_router
from app.schemas.errors import (
    RateLimitExceededErrorResult,
    UnexpectedErrorResult,
    ValidationErrorResult,
)


def add_routes(app: FastAPI) -> None:
    """Register routes for the app."""
    app.include_router(health_router)
    app.include_router(users_router)
    app.include_router(auth_router)


def add_middleware(app: FastAPI) -> None:
    """Register middleware for the app."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_headers=["*"],
        allow_methods=["*"],
        expose_headers=["*"],
    )
    app.add_middleware(GZipMiddleware)
    app.add_middleware(
        RateLimitMiddleware,
        authenticate=client_ip,
        backend=rate_limit_backend,
        config=rate_limit_config,
    )
    app.add_middleware(
        CorrelationIdMiddleware,
        header_name="X-Request-ID",
    )


def create_app() -> FastAPI:
    """Initialize an app instance."""
    app = FastAPI(
        version="0.0.1",
        root_path=settings.root_path,
        debug=settings.debug,
        default_response_class=ORJSONResponse,
        openapi_url=settings.openapi_url,
        title=f"{APP_NAME} HTTP API",
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
        generate_unique_id_function=generate_operation_id,
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
            RateLimitExceededError: handle_rate_limit_exceeded_error,
        },
        contact={
            "email": SUPPORT_EMAIL,
        },
    )
    add_routes(app)
    add_middleware(app)
    return app
