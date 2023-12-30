from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path

from app.auth.dependencies import get_current_user_id
from app.core.constants import Tag
from app.users.models import User
from app.users.services import UserService

users_router = APIRouter(
    prefix="/users",
    tags=[Tag.USERS],
)


@users_router.get(
    "/@me",
    response_model=User,
    summary="Get the current user.",
    description="""Retrieves information about the currently authenticated
    user based on their user ID. Requires the authentication token to be
    included in the request headers for security validation.""",
)
async def get_current_user(
    current_user_id: Annotated[
        UUID,
        Depends(
            dependency=get_current_user_id,
        ),
    ],
    user_service: Annotated[
        UserService,
        Depends(
            dependency=UserService,
        ),
    ],
) -> User:
    """Get the current user."""
    return await user_service.get_user_by_id(
        user_id=current_user_id,
    )


@users_router.get(
    "/{user_id}",
    response_model=User,
    summary="Get the user with the given ID.",
    description="""Retrieves information about a user based on the
    provided user ID. The user ID is expected to be a valid UUID.
    This endpoint is useful for fetching details about specific users
    in the system.""",
)
async def get_user(
    user_id: Annotated[
        UUID,
        Path(
            title="The ID of the user to get.",
        ),
    ],
    user_service: Annotated[
        UserService,
        Depends(
            dependency=UserService,
        ),
    ],
) -> User:
    """Get the user with the given ID."""
    return await user_service.get_user_by_id(user_id=user_id)
