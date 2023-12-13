from uuid import UUID

import inject
from falcon import before
from falcon.asgi import Request, Response

from app.auth.hooks import login_required

from .services import UserService


class UserResource:
    @before(login_required)
    @inject.autoparams("user_service")
    async def on_get_current_user(
        self,
        req: Request,
        resp: Response,
        user_service: UserService,
    ) -> None:
        """Get the current user."""
        current_user_id: UUID = req.context["current_user_id"]
        result = await user_service.get_user_by_id(
            user_id=current_user_id,
        )
        resp.media = result.model_dump(mode="json")

    @before(login_required)
    @inject.autoparams("user_service")
    async def on_get_user(
        self,
        _req: Request,
        resp: Response,
        user_id: UUID,
        user_service: UserService,
    ) -> None:
        """Get the user with the given ID."""
        result = await user_service.get_user_by_id(user_id=user_id)
        resp.media = result.model_dump(mode="json")


user_resource = UserResource()
