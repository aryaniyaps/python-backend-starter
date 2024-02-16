from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Path
from user_agents import parse

from app.dependencies.auth import get_viewer_info
from app.dependencies.ip_address import get_ip_address
from app.dependencies.rate_limiter import RateLimiter
from app.dependencies.user import get_user_service
from app.lib.constants import OpenAPITag
from app.models.user import User
from app.schemas.errors import InvalidInputErrorResult, ResourceNotFoundErrorResult
from app.schemas.user import (
    ChangeUserEmailInput,
    ChangeUserEmailRequestInput,
    ChangeUserPasswordInput,
    PartialUserSchema,
    UpdateUserInput,
    UserSchema,
)
from app.services.user import UserService
from app.types.auth import UserInfo

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
    summary="Change the current user's password.",
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="15/hour",
            ),
        ),
    ],
)
async def change_current_user_password(
    data: ChangeUserPasswordInput,
    request_ip: Annotated[
        str,
        Depends(
            dependency=get_ip_address,
        ),
    ],
    user_agent: Annotated[str, Header()],
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
    """Change the current user's password."""
    return await user_service.update_user_password(
        user_id=viewer_info.user_id,
        current_password=data.current_password.get_secret_value(),
        new_password=data.new_password.get_secret_value(),
        request_ip=request_ip,
        user_agent=parse(user_agent),
    )


@users_router.post(
    "/@me/email-change-request",
    response_model=None,
    status_code=HTTPStatus.ACCEPTED,
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    summary="Send an email change request.",
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="15/hour",
            ),
        ),
    ],
)
async def request_current_user_email_change(
    data: ChangeUserEmailRequestInput,
    user_agent: Annotated[str, Header()],
    request_ip: Annotated[
        str,
        Depends(
            dependency=get_ip_address,
        ),
    ],
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
    """Send an email change request."""
    await user_service.send_change_email_request(
        user_id=viewer_info.user_id,
        email=data.email,
        current_password=data.current_password.get_secret_value(),
        user_agent=parse(user_agent),
        request_ip=request_ip,
    )


@users_router.patch(
    "/@me/email",
    response_model=UserSchema,
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    summary="Change the current user's email.",
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="15/hour",
            ),
        ),
    ],
)
async def change_current_user_email(
    data: ChangeUserEmailInput,
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
    """Change the current user's email."""
    return await user_service.update_user_email(
        user_id=viewer_info.user_id,
        email_verification_token=data.email_verification_token.get_secret_value(),
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
