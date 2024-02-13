from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path

from app.auth.dependencies import get_viewer_info
from app.auth.types import UserInfo
from app.core.constants import OpenAPITag
from app.core.rate_limiter import RateLimiter
from app.core.schemas import InvalidInputErrorResult, ResourceNotFoundErrorResult
from app.users.dependencies import get_user_service
from app.users.models import User
from app.users.schemas import (
    PartialUserSchema,
    UpdateUserEmailInput,
    UpdateUserInput,
    UpdateUserPasswordInput,
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
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
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
    """Update the current user."""
    return await user_service.update_user(
        user_id=viewer_info.user_id,
        username=data.username,
    )


@users_router.patch(
    "/@me/password",
    response_model=UserSchema,
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    summary="Update the current user's password.",
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="15/hour",
            ),
        ),
    ],
)
async def update_current_user_password(
    data: UpdateUserPasswordInput,
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
    """Update the current user's password."""
    return await user_service.update_user_password(
        user_id=viewer_info.user_id,
        current_password=data.current_password,
        new_password=data.new_password,
    )


# TODO: maybe rename this route to request email change
@users_router.patch(
    "/@me/email",
    response_model=None,
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    summary="Update the current user's email.",
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="15/hour",
            ),
        ),
    ],
)
async def update_current_user_email(
    data: UpdateUserEmailInput,
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
) -> None:
    """Update the current user's email."""
    await user_service.update_user_email(
        user_id=viewer_info.user_id,
        email=data.email,
    )


@users_router.get(
    "/{user_id}",
    response_model=PartialUserSchema,
    summary="Get the user with the given ID.",
    responses={
        HTTPStatus.NOT_FOUND: {
            "model": ResourceNotFoundErrorResult,
            "description": "Resource Not Found Error",
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
