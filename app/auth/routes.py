from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, status
from user_agents import parse

from app.auth.dependencies import get_authentication_token, get_current_user_id
from app.auth.models import (
    LoginUserInput,
    LoginUserResult,
    PasswordResetInput,
    PasswordResetRequestInput,
    RegisterUserInput,
    RegisterUserResult,
)
from app.auth.services import AuthService

auth_router = APIRouter(
    prefix="/auth",
)


@auth_router.post(
    "/register",
    response_model=RegisterUserResult,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    data: RegisterUserInput,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=AuthService,
        ),
    ],
) -> RegisterUserResult:
    """Register a new user."""
    return await auth_service.register_user(
        data=RegisterUserInput.model_validate(data),
    )


@auth_router.post(
    "/login",
    response_model=LoginUserResult,
)
async def login_user(
    data: LoginUserInput,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=AuthService,
        ),
    ],
) -> LoginUserResult:
    """Login the current user."""
    return await auth_service.login_user(
        data=LoginUserInput.model_validate(data),
    )


@auth_router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout_user(
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
    current_user_id: Annotated[
        UUID,
        Depends(
            dependency=get_current_user_id,
        ),
    ],
) -> None:
    """Logout the current user."""
    await auth_service.remove_authentication_token(
        authentication_token=authentication_token,
        user_id=current_user_id,
    )


@auth_router.post(
    "/reset-password-request",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def request_password_reset(
    data: PasswordResetRequestInput,
    user_agent: Annotated[str, Header()],
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=AuthService,
        ),
    ],
) -> None:
    """Send a password reset request to the given email."""
    await auth_service.send_password_reset_request(
        data=PasswordResetRequestInput.model_validate(data),
        user_agent=parse(user_agent),
    )


@auth_router.post(
    "/reset-password",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def reset_password(
    data: PasswordResetInput,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=AuthService,
        ),
    ],
) -> None:
    """Send a password reset request to the given email."""
    await auth_service.reset_password(
        data=PasswordResetInput.model_validate(data),
    )
