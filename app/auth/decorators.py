from functools import wraps
from typing import Annotated, Awaitable, Callable

from fastapi import Depends, Header, Request

from app.auth.services import AuthService
from app.core.errors import UnauthenticatedError


def login_required(callable: Callable[..., Awaitable]) -> Callable[..., Awaitable]:
    """Ensure that the current user is logged in."""

    @wraps(callable)
    async def protected_route(
        request: Request,
        auth_service: Annotated[
            AuthService,
            Depends(
                dependency=AuthService,
            ),
        ],
        x_authentication_token: Annotated[str | None, Header()] = None,
        *args,
        **kwargs,
    ) -> Awaitable:
        if not x_authentication_token:
            raise UnauthenticatedError(
                message="Authentication token is missing.",
            )

        # Verify the token and get the current user ID
        user_id = await auth_service.verify_authentication_token(
            authentication_token=x_authentication_token,
        )

        # Put the user ID and authentication token
        # in the request context
        request.state.current_user_id = user_id
        request.state.authentication_token = x_authentication_token

        # run the handler method and return the response
        return await callable(request, *args, **kwargs)

    return protected_route
