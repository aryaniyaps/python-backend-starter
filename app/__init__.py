from falcon import CORSMiddleware
from falcon.asgi import App

from app.auth.resources import auth_resource
from app.config import settings
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


def create_app() -> App:
    """Create the ASGI app."""
    app = App()
    add_middleware(app)
    add_routes(app)
    return app
