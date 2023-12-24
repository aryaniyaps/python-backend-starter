from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.auth.routes import auth_router
from app.config import Settings
from app.core.constants import APP_NAME
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
from app.users.routes import users_router


def add_routes(app: FastAPI) -> None:
    """Register routes for the app."""
    app.include_router(router=users_router)
    app.include_router(router=auth_router)


def add_middleware(app: FastAPI, settings: Settings) -> None:
    """Register middleware for the app."""
    app.add_middleware(
        BaseHTTPMiddleware,
        dispatch=set_request_id,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def add_error_handlers(app: FastAPI) -> None:
    """Register error handlers for the app."""
    app.add_exception_handler(
        RequestValidationError,
        handler=handle_validation_error,
    )
    app.add_exception_handler(
        InvalidInputError,
        handler=handle_invalid_input_error,
    )
    app.add_exception_handler(
        ResourceNotFoundError,
        handler=handle_resource_not_found_error,
    )
    app.add_exception_handler(
        UnauthenticatedError,
        handler=handle_unauthenticated_error,
    )
    app.add_exception_handler(
        UnexpectedError,
        handler=handle_unexpected_error,
    )


def create_app(settings: Settings) -> FastAPI:
    """Initialize an app instance."""
    app = FastAPI(
        debug=settings.debug,
        default_response_class=ORJSONResponse,
        title=APP_NAME,
    )
    add_middleware(app, settings)
    add_error_handlers(app)
    add_routes(app)
    return app
