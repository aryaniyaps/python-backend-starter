from di import Container, ScopeState
from falcon import CORSMiddleware
from orjson import dumps, loads
from pydantic import ValidationError
from sanic import Sanic

from app.auth.routes import auth_blueprint
from app.config import Settings
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
from app.core.middleware.container import ContainerMiddleware
from app.users.routes import users_blueprint


def configure_app(app: Sanic, settings: Settings) -> None:
    """Configure settings for the given app."""
    app.config.DEBUG = settings.debug


def add_routes(app: Sanic) -> None:
    """Register routes for the app."""
    app.blueprint(blueprint=auth_blueprint)
    app.blueprint(blueprint=users_blueprint)


def add_middleware(
    app: Sanic,
    settings: Settings,
    app_state: ScopeState,
    container: Container,
) -> None:
    """Register middleware for the app."""
    app.add_middleware(
        middleware=CORSMiddleware(
            allow_origins=settings.cors_allow_origins,
        )
    )
    # add the container middleware at last
    # as it skips the execution of consequent
    # middleware
    app.add_middleware(
        middleware=ContainerMiddleware(
            container=container,
            app_state=app_state,
        )
    )


def add_error_handlers(app: Sanic) -> None:
    """Register error handlers for the app."""
    app.error_handler.add(
        ValidationError,
        handle_validation_error,
    )
    app.error_handler.add(
        InvalidInputError,
        handle_invalid_input_error,
    )
    app.error_handler.add(
        ResourceNotFoundError,
        handle_resource_not_found_error,
    )
    app.error_handler.add(
        UnauthenticatedError,
        handle_unauthenticated_error,
    )
    app.error_handler.add(
        UnexpectedError,
        handle_unexpected_error,
    )


def create_app(
    container: Container,
    app_state: ScopeState,
    settings: Settings,
) -> Sanic:
    """Initialize an app instance."""
    app = Sanic(
        name=__name__,
        dumps=dumps,
        loads=loads,
    )
    configure_app(app, settings)
    add_middleware(
        app,
        settings=settings,
        app_state=app_state,
        container=container,
    )
    add_error_handlers(app)
    add_routes(app)
    return app
