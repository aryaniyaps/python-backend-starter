from uuid import UUID

from falcon import before
from falcon.asgi import Request, Response
from lagom import bind_to_container, injectable

from app.auth.hooks import login_required
from app.core.containers import context_container

from .services import UserService


class UserResource:
    @before(login_required)
    @bind_to_container(container=context_container)
    async def on_get_current_user(
        self,
        req: Request,
        resp: Response,
        user_service: UserService = injectable,
    ) -> None:
        """Get the current user."""
        current_user_id: UUID = req.context["current_user_id"]
        result = await user_service.get_user_by_id(
            user_id=current_user_id,
        )
        resp.media = result.model_dump()

    @before(login_required)
    @bind_to_container(container=context_container)
    async def on_get_user(
        self,
        req: Request,
        resp: Response,
        user_id: UUID,
        user_service: UserService = injectable,
    ) -> None:
        """Get the user with the given ID."""
        result = await user_service.get_user_by_id(user_id=user_id)
        resp.media = result.model_dump()


user_resource = UserResource()
