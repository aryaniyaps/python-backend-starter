from typing import Annotated

from aioinject import Inject, inject
from falcon.asgi import Request, Response

from app.auth.services import AuthService
from app.core.errors import UnauthenticatedError


@inject
async def login_required(
    req: Request,
    resp: Response,
    resource,
    params,
    auth_service: Annotated[AuthService, Inject],
) -> None:
    """Ensure that the current user is logged in."""
    authentication_token = req.get_header("X-Authentication-Token")
    if not authentication_token:
        raise UnauthenticatedError(
            message="Authentication token is missing.",
        )

    # Verify the token and get the current user ID
    user_id = await auth_service.verify_authentication_token(
        authentication_token=authentication_token,
    )

    # Put the user ID and authentication token
    # in the request context
    req.context["current_user_id"] = user_id
    req.context["authentication_token"] = authentication_token
