from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path

from app.auth.dependencies import get_viewer_info
from app.auth.types import UserInfo
from app.core.constants import OpenAPITag
from app.core.rate_limiter import RateLimiter
from app.core.schemas import ResourceNotFoundErrorResult
from app.users.dependencies import get_user_service
from app.users.models import User
from app.users.schemas import (
    PartialUserSchema,
    UpdateUserInput,
    UserSchema,
)
from app.users.services import UserService

users_router = APIRouter(
    prefix="/users",
    tags=[OpenAPITag.USERS],
)


@users_router.get(
    "/@me",
    response_model=UserSchema,
    summary="Get the current user.",
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="1000/hour",
            ),
        ),
    ],
)
async def get_current_user(
    viewer_info: Annotated[
        UserInfo,
        Depends(
            dependency=get_viewer_info,
        ),
    ],
    user_service: Annotated[
        UserService,
        Depends(
            dependency=get_user_service,
        ),
    ],
) -> User:
    """Get the current user."""
    return await user_service.get_user_by_id(
        user_id=viewer_info.user_id,
    )


@users_router.patch(
    "/@me",
    response_model=UserSchema,
    summary="Update the current user.",
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="100/hour",
            ),
        ),
    ],
)
async def update_current_user(
    data: UpdateUserInput,
    viewer_info: Annotated[
        UserInfo,
        Depends(
            dependency=get_viewer_info,
        ),
    ],
    user_service: Annotated[
        UserService,
        Depends(
            dependency=get_user_service,
        ),
    ],
) -> User:
    """Get the current user."""
    return await user_service.update_user(
        user_id=viewer_info.user_id,
        username=data.username,
        email=data.email,
        new_password=data.password,
        current_password=data.current_password,
    )


@users_router.get(
    "/{user_id}",
    response_model=PartialUserSchema,
    summary="Get the user with the given ID.",
    responses={
        HTTPStatus.NOT_FOUND: {
            "description": "Resource Not Found Error",
            "model": ResourceNotFoundErrorResult,
        },
    },
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="2500/hour",
            ),
        ),
    ],
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
            dependency=get_user_service,
        ),
    ],
) -> User:
    """Get the user with the given ID."""
    return await user_service.get_user_by_id(user_id=user_id)
