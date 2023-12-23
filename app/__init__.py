from di import Container, ScopeState
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
from app.core.listeners.setup_routes import setup_routes
from app.core.middleware.request_id import set_request_id
from app.users.routes import users_blueprint


def configure_app(app: Sanic, settings: Settings) -> None:
    """Configure settings for the given app."""
    app.config.update(
        {
            "DEBUG": settings.debug,
            "FALLBACK_ERROR_FORMAT": "json",
        }
    )


def add_routes(app: Sanic) -> None:
    """Register routes for the app."""
    app.blueprint(blueprint=auth_blueprint)
    app.blueprint(blueprint=users_blueprint)


def add_middleware(app: Sanic) -> None:
    """Register middleware for the app."""
    app.on_request(middleware=set_request_id)


def add_listeners(
    app: Sanic,
    app_state: ScopeState,
    container: Container,
) -> None:
    """Register listeners for the app."""
    app.before_server_start(
        listener=setup_routes(
            app_state=app_state,
            container=container,
        ),
    )


def add_error_handlers(app: Sanic) -> None:
    """Register error handlers for the app."""
    app.error_handler.add(
        exception=ValidationError,
        handler=handle_validation_error,
    )
    app.error_handler.add(
        exception=InvalidInputError,
        handler=handle_invalid_input_error,
    )
    app.error_handler.add(
        exception=ResourceNotFoundError,
        handler=handle_resource_not_found_error,
    )
    app.error_handler.add(
        exception=UnauthenticatedError,
        handler=handle_unauthenticated_error,
    )
    app.error_handler.add(
        exception=UnexpectedError,
        handler=handle_unexpected_error,
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
    add_middleware(app)
    add_listeners(app, app_state, container)
    add_error_handlers(app)
    add_routes(app)
    return app
