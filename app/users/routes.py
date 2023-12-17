from uuid import UUID

from sanic import Blueprint, Request
from sanic.response import JSONResponse, json

from app.auth.decorators import login_required
from app.users.services import UserService

users_blueprint = Blueprint(
    name="users",
    url_prefix="/users",
)


@users_blueprint.get("/@me")
@login_required
async def on_get_current_user(
    request: Request,
    user_service: UserService,
) -> JSONResponse:
    """Get the current user."""
    current_user_id: UUID = request.ctx["current_user_id"]
    result = await user_service.get_user_by_id(
        user_id=current_user_id,
    )
    return json(body=result.model_dump(mode="json"))


@users_blueprint.get("/<user_id:uuid>")
@login_required
async def on_get_user(
    _request: Request,
    user_id: UUID,
    user_service: UserService,
) -> JSONResponse:
    """Get the user with the given ID."""
    result = await user_service.get_user_by_id(user_id=user_id)
    return json(body=result.model_dump(mode="json"))
