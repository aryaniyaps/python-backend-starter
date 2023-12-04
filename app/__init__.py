from falcon import CORSMiddleware
from falcon.asgi import App
from pydantic import ValidationError

from app.auth.resources import auth_resource
from app.config import settings
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
from app.users.resources import user_resource


def add_routes(app: App) -> None:
    """Register routes for the app."""
    app.add_route(
        "/users/@me",
        user_resource,
        suffix="current_user",
    )
    app.add_route(
        "/users/{user_id:int}",
        user_resource,
        suffix="user",
    )
    app.add_route(
        "/auth/login",
        auth_resource,
        suffix="login",
    )
    app.add_route(
        "/auth/register",
        auth_resource,
        suffix="register",
    )
    app.add_route(
        "/auth/logout",
        auth_resource,
        suffix="logout",
    )
    app.add_route(
        "/auth/reset-password-request",
        auth_resource,
        suffix="reset_password_request",
    )
    app.add_route(
        "/auth/reset-password",
        auth_resource,
        suffix="reset_password",
    )


def add_middleware(app: App) -> None:
    """Register middleware for the app."""
    app.add_middleware(
        middleware=CORSMiddleware(
            allow_origins=settings.cors_allow_origins,
        )
    )


def add_error_handlers(app: App) -> None:
    """Register error handlers for the app."""
    app.add_error_handler(
        ValidationError,
        handle_validation_error,
    )
    app.add_error_handler(
        InvalidInputError,
        handle_invalid_input_error,
    )
    app.add_error_handler(
        ResourceNotFoundError,
        handle_resource_not_found_error,
    )
    app.add_error_handler(
        UnauthenticatedError,
        handle_unauthenticated_error,
    )
    app.add_error_handler(
        UnexpectedError,
        handle_unexpected_error,
    )


def create_app() -> App:
    """Initialize an ASGI app instance."""
    app = App()
    add_middleware(app)
    add_error_handlers(app)
    add_routes(app)
    return app
