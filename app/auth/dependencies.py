from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header

from app.auth.services import AuthService
from app.core.errors import UnauthenticatedError


async def get_authentication_token(
    x_authentication_token: Annotated[str | None, Header()] = None,
) -> str:
    """Get the authentication token."""
    if not x_authentication_token:
        raise UnauthenticatedError(
            message="Authentication token is missing.",
        )
    return x_authentication_token


async def get_current_user_id(
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=AuthService,
        ),
    ],
    authentication_token: Annotated[
        str,
        Depends(
            dependency=get_authentication_token,
        ),
    ],
) -> UUID:
    """Get the current user ID."""
    # Verify the token and get the current user ID
    user_id = await auth_service.verify_authentication_token(
        authentication_token=authentication_token,
    )

    return user_id
