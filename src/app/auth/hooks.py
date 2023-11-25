from falcon import Response, Request
from app.auth.services import AuthService

from app.core.errors import UnauthenticatedError


async def login_required(
    req: Request,
    resp: Response,
    resource,
    params,
) -> None:
    """Ensure that the current user is logged in."""
    authentication_token = req.get_header("X-Authentication-Token")
    if not authentication_token:
        raise UnauthenticatedError(
            message="Authentication token is missing",
        )

    # Verify the token and get the current user
    user_id = await AuthService.verify_authentication_token(
        authentication_token=authentication_token,
    )

    # Put the user ID in the request context
    req.context["current_user_id"] = user_id
