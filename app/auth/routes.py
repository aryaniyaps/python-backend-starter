from uuid import UUID

from sanic import Blueprint, Request
from sanic.response import HTTPResponse, JSONResponse, empty, json

from app.auth.decorators import login_required
from app.auth.models import LoginUserInput, RegisterUserInput
from app.auth.services import AuthService

auth_blueprint = Blueprint(
    name="auth",
    url_prefix="/auth",
)


@auth_blueprint.post("/register")
async def register_user(
    request: Request,
    auth_service: AuthService,
) -> JSONResponse:
    """Register a new user."""
    result = await auth_service.register_user(
        data=RegisterUserInput.model_validate(request.json),
    )
    return json(body=result.model_dump(mode="json"))


@auth_blueprint.post("/login")
async def login_user(
    request: Request,
    auth_service: AuthService,
) -> JSONResponse:
    """Login the current user."""
    result = await auth_service.login_user(
        data=LoginUserInput.model_validate(request.json),
    )
    return json(body=result.model_dump(mode="json"))


@auth_blueprint.post("/logout")
@login_required
async def logout_user(
    request: Request,
    auth_service: AuthService,
) -> HTTPResponse:
    """Logout the current user."""
    current_user_id: UUID = request.ctx["current_user_id"]
    authentication_token: str = request.ctx["authentication_token"]
    await auth_service.remove_authentication_token(
        authentication_token=authentication_token,
        user_id=current_user_id,
    )

    return empty()
