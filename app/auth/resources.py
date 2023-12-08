from typing import Annotated
from uuid import UUID

from aioinject import Inject, inject
from falcon import HTTP_201, HTTP_204, before
from falcon.asgi import Request, Response
from user_agents import parse

from app.auth.hooks import login_required
from app.auth.services import AuthService

from .models import (
    LoginUserInput,
    PasswordResetInput,
    PasswordResetRequestInput,
    RegisterUserInput,
)


class AuthResource:
    @inject
    async def on_post_register(
        self,
        req: Request,
        resp: Response,
        auth_service: Annotated[AuthService, Inject],
    ) -> None:
        """Register a new user."""
        data = await req.media
        result = await auth_service.register_user(
            data=RegisterUserInput.model_validate(data),
        )
        resp.media = result.model_dump(mode="json")
        resp.status = HTTP_201

    @inject
    async def on_post_login(
        self,
        req: Request,
        resp: Response,
        auth_service: Annotated[AuthService, Inject],
    ) -> None:
        """Login the current user."""
        data = await req.media
        result = await auth_service.login_user(
            data=LoginUserInput.model_validate(data),
        )
        resp.media = result.model_dump(mode="json")

    @before(login_required)
    @inject
    async def on_post_logout(
        self,
        req: Request,
        resp: Response,
        auth_service: Annotated[AuthService, Inject],
    ) -> None:
        """Logout the current user."""
        current_user_id: UUID = req.context["current_user_id"]
        authentication_token: str = req.context["authentication_token"]
        await auth_service.remove_authentication_token(
            authentication_token=authentication_token,
            user_id=current_user_id,
        )
        resp.status = HTTP_204

    @inject
    async def on_post_reset_password_request(
        self,
        req: Request,
        resp: Response,
        auth_service: Annotated[AuthService, Inject],
    ) -> None:
        """Send a password reset request to the given email."""
        data = await req.media
        await auth_service.send_password_reset_request(
            data=PasswordResetRequestInput.model_validate(data),
            user_agent=parse(req.user_agent),
        )
        resp.status = HTTP_204

    @inject
    async def on_post_reset_password(
        self,
        req: Request,
        resp: Response,
        auth_service: Annotated[AuthService, Inject],
    ) -> None:
        """Reset the relevant user's password with the given credentials."""
        data = await req.media
        await auth_service.reset_password(
            data=PasswordResetInput.model_validate(data),
        )
        resp.status = HTTP_204


auth_resource = AuthResource()
