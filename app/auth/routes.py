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
from app.core.constants import Tag

auth_router = APIRouter(
    prefix="/auth",
    tags=[Tag.AUTHENTICATION],
)


@auth_router.post(
    "/register",
    response_model=RegisterUserResult,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user.",
    description="""Allows users to register a new account by providing the
    required user registration information. Upon successful registration,
    it returns details about the registered user.""",
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
    summary="Login the current user.",
    description="""Handles user login by validating the provided login credentials.
    If the credentials are valid, it returns information about the authenticated user,
    including an authentication token for future requests.""",
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
    summary="Logout the current user.",
    description="""Logs out the currently authenticated user by invalidating
    the authentication token associated with the user. Requires the user's
    authentication token and user ID for security validation.""",
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
    summary="Send a password reset request.",
    description="""Initiates the process of resetting a user's password
    by sending a reset request to the provided email address. The user
    agent information is also captured for security purposes.""",
    response_model=None,
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
    summary="Reset user password.",
    description="""Allows users to reset their password by providing the
    necessary information, including a valid reset token. After successful
    validation, the user's password is updated.""",
    response_model=None,
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
