from functools import wraps
from typing import Awaitable, Callable

from sanic import Request

from app.auth.services import AuthService
from app.core.errors import UnauthenticatedError


async def login_required(
    callable: Callable[..., Awaitable]
) -> Callable[..., Awaitable]:
    """Ensure that the current user is logged in."""

    @wraps(callable)
    async def protected_route(
        request: Request,
        auth_service: AuthService,
        *args,
        **kwargs,
    ) -> Awaitable:
        authentication_token = request.headers.get("X-Authentication-Token")
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
        request.ctx["current_user_id"] = user_id
        request.ctx["authentication_token"] = authentication_token

        # run the handler method and return the response
        return await callable(request, *args, **kwargs)

    return protected_route
