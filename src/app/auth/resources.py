from falcon import before, HTTP_204
from falcon.asgi import Request, Response

from app.auth.hooks import login_required
from app.auth.services import AuthService

from .models import LoginUserInput


class AuthResource:
    async def on_post_login(
        self,
        req: Request,
        resp: Response,
    ) -> None:
        """Login the current user."""
        data = await req.stream.read()
        result = await AuthService.login_user(
            data=LoginUserInput.model_validate_json(data),
        )
        resp.media = result.model_dump_json()

    @before(login_required)
    async def on_post_logout(
        self,
        req: Request,
        resp: Response,
    ) -> None:
        """Logout the current user."""
        authentication_token = req.context["authentication_token"]
        await AuthService.remove_authentication_token(
            authentication_token=authentication_token,
        )
        resp.status = HTTP_204


auth_resource = AuthResource()
