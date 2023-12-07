from uuid import UUID

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
    async def on_post_register(
        self,
        req: Request,
        resp: Response,
    ) -> None:
        """Register a new user."""
        data = await req.media
        result = await AuthService.register_user(
            data=RegisterUserInput.model_validate(data),
        )
        resp.media = result.model_dump()
        resp.status = HTTP_201

    async def on_post_login(
        self,
        req: Request,
        resp: Response,
    ) -> None:
        """Login the current user."""
        data = await req.media
        result = await AuthService.login_user(
            data=LoginUserInput.model_validate(data),
        )
        resp.media = result.model_dump()

    @before(login_required)
    async def on_post_logout(
        self,
        req: Request,
        resp: Response,
    ) -> None:
        """Logout the current user."""
        current_user_id: UUID = req.context["current_user_id"]
        authentication_token: str = req.context["authentication_token"]
        await AuthService.remove_authentication_token(
            authentication_token=authentication_token,
            user_id=current_user_id,
        )
        resp.status = HTTP_204

    async def on_post_reset_password_request(
        self,
        req: Request,
        resp: Response,
    ) -> None:
        """Send a password reset request to the given email."""
        data = await req.media
        await AuthService.send_password_reset_request(
            data=PasswordResetRequestInput.model_validate(data),
            user_agent=parse(req.user_agent),
        )
        resp.status = HTTP_204

    async def on_post_reset_password(
        self,
        req: Request,
        resp: Response,
    ) -> None:
        """Reset the relevant user's password with the given credentials."""
        data = await req.media
        await AuthService.reset_password(
            data=PasswordResetInput.model_validate(data),
        )
        resp.status = HTTP_204


auth_resource = AuthResource()
