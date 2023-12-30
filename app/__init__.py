from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.auth.routes import auth_router
from app.config import settings
from app.core.constants import APP_NAME, SUPPORT_EMAIL
from app.core.error_handlers import (
    handle_invalid_input_error,
    handle_resource_not_found_error,
    handle_unauthenticated_error,
    handle_unexpected_error,
    handle_validation_error,
)
from app.core.errors import (
    InvalidInputError,
    ResourceNotFoundError,
    UnauthenticatedError,
    UnexpectedError,
)
from app.core.middleware.request_id import set_request_id
from app.core.models import ValidationErrorResult
from app.meta.routes import meta_router
from app.users.routes import users_router


def add_routes(app: FastAPI) -> None:
    """Register routes for the app."""
    app.include_router(router=meta_router)
    app.include_router(router=users_router)
    app.include_router(router=auth_router)


def add_middleware(app: FastAPI) -> None:
    """Register middleware for the app."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        BaseHTTPMiddleware,
        dispatch=set_request_id,
    )


def add_error_handlers(app: FastAPI) -> None:
    """Register error handlers for the app."""
    app.add_exception_handler(
        RequestValidationError,
        handler=handle_validation_error,  # type: ignore
    )
    app.add_exception_handler(
        InvalidInputError,
        handler=handle_invalid_input_error,  # type: ignore
    )
    app.add_exception_handler(
        ResourceNotFoundError,
        handler=handle_resource_not_found_error,  # type: ignore
    )
    app.add_exception_handler(
        UnauthenticatedError,
        handler=handle_unauthenticated_error,  # type: ignore
    )
    app.add_exception_handler(
        UnexpectedError,
        handler=handle_unexpected_error,  # type: ignore
    )


def create_app() -> FastAPI:
    """Initialize an app instance."""
    app = FastAPI(
        version="0.0.1",
        debug=settings.debug,
        default_response_class=ORJSONResponse,
        openapi_url=settings.openapi_url,
        redoc_url=None,
        title=APP_NAME,
        swagger_ui_parameters={
            "syntaxHighlight.theme": "nord",
            "displayRequestDuration": True,
        },
        responses={
            status.HTTP_422_UNPROCESSABLE_ENTITY: {
                "model": ValidationErrorResult,
                "description": "Validation Error",
            }
        },
        contact={
            "email": SUPPORT_EMAIL,
        },
    )
    add_middleware(app)
    add_error_handlers(app)
    add_routes(app)
    return app
