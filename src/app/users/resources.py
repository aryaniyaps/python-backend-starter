from falcon import Request, Response, HTTP_201, before

from app.auth.hooks import login_required
from app.users.models import CreateUserInput, User

from .services import UserService


class UserResource:
    async def on_post(
        self,
        req: Request,
        resp: Response,
    ) -> None:
        """Create a new user."""
        data = await req.media
        result = await UserService.create_user(
            data=CreateUserInput.model_validate_json(data),
        )
        resp.media = result.model_dump_json()
        resp.status = HTTP_201

    @before(login_required)
    async def on_get_current_user(
        self,
        req: Request,
        resp: Response,
    ) -> None:
        """Get the current user."""
        current_user_id: int = req.context["current_user_id"]
        result = await UserService.get_user_by_id(
            user_id=current_user_id,
        )
        resp.media = result.model_dump_json()

    @before(login_required)
    async def on_get_user(
        self,
        req: Request,
        resp: Response,
        user_id: int,
    ) -> None:
        """Get the user with the given ID."""
        result = await UserService.get_user_by_id(user_id=user_id)
        resp.media = result.model_dump_json()


user_resource = UserResource()
