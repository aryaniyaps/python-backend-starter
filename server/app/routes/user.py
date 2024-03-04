from http import HTTPStatus
from typing import Annotated
from uuid import UUID

import user_agents
from fastapi import APIRouter, Depends, Header, Path

from app.dependencies.auth import get_viewer_info
from app.dependencies.ip_address import get_ip_address
from app.dependencies.user import get_user_service
from app.lib.constants import OpenAPITag
from app.models.user import User
from app.schemas.errors import InvalidInputErrorResult, ResourceNotFoundErrorResult
from app.schemas.user import (
    ChangeUserEmailInput,
    ChangeUserEmailRequestInput,
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
        display_name=data.display_name,
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
        user_agent=user_agents.parse(user_agent),
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
        verification_code=data.verification_code.get_secret_value(),
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
