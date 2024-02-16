from http import HTTPStatus
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Header
from sqlalchemy import ScalarResult
from user_agents import parse

from app.core.constants import OpenAPITag
from app.core.rate_limiter import RateLimiter
from app.dependencies.auth import (
    authentication_token_header,
    get_auth_service,
    get_viewer_info,
)
from app.dependencies.ip_address import get_ip_address
from app.models.user_session import UserSession
from app.schemas.auth import (
    EmailVerificationRequestInput,
    LoginUserInput,
    LoginUserResult,
    LogoutInput,
    PasswordResetInput,
    PasswordResetRequestInput,
    RegisterUserInput,
    RegisterUserResult,
)
from app.schemas.errors import InvalidInputErrorResult
from app.schemas.user_session import UserSessionSchema
from app.services.auth import AuthService
from app.types.auth import UserInfo

auth_router = APIRouter(
    prefix="/auth",
    tags=[OpenAPITag.AUTHENTICATION],
)


@auth_router.post(
    "/email-verification-request",
    response_model=None,
    status_code=HTTPStatus.ACCEPTED,
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    summary="Send an email verification request.",
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="15/hour",
            ),
        ),
    ],
)
async def request_email_verification(
    data: EmailVerificationRequestInput,
    user_agent: Annotated[str, Header()],
    request_ip: Annotated[
        str,
        Depends(
            dependency=get_ip_address,
        ),
    ],
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> None:
    """Send an email verification request."""
    await auth_service.send_email_verification_request(
        email=data.email,
        user_agent=parse(user_agent),
        request_ip=request_ip,
    )


@auth_router.post(
    "/register",
    response_model=RegisterUserResult,
    status_code=HTTPStatus.CREATED,
    summary="Register a new user.",
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="15/hour",
            ),
        ),
    ],
)
async def register_user(
    data: RegisterUserInput,
    user_agent: Annotated[str, Header()],
    request_ip: Annotated[
        str,
        Depends(
            dependency=get_ip_address,
        ),
    ],
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> dict[str, Any]:
    """Register a new user."""
    authentication_token, user = await auth_service.register_user(
        email=data.email,
        email_verification_token=data.email_verification_token.get_secret_value(),
        username=data.username,
        password=data.password.get_secret_value(),
        request_ip=request_ip,
        user_agent=parse(user_agent),
    )

    return {
        "authentication_token": authentication_token,
        "user": user,
    }


@auth_router.post(
    "/login",
    response_model=LoginUserResult,
    summary="Login the current user.",
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="100/hour",
            ),
        ),
    ],
)
async def login_user(
    data: LoginUserInput,
    user_agent: Annotated[str, Header()],
    request_ip: Annotated[
        str,
        Depends(
            dependency=get_ip_address,
        ),
    ],
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> dict[str, Any]:
    """Login the current user."""
    authentication_token, user = await auth_service.login_user(
        login=data.login,
        password=data.password.get_secret_value(),
        user_agent=parse(user_agent),
        request_ip=request_ip,
    )
    return {
        "authentication_token": authentication_token,
        "user": user,
    }


@auth_router.post(
    "/logout",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Logout the current user.",
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="50/hour",
            ),
        ),
    ],
)
async def delete_current_user_session(
    data: LogoutInput,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
    authentication_token: Annotated[
        str,
        Depends(
            authentication_token_header,
        ),
    ],
    viewer_info: Annotated[
        UserInfo,
        Depends(
            dependency=get_viewer_info,
        ),
    ],
) -> None:
    """Logout the current user."""
    await auth_service.logout_user(
        authentication_token=authentication_token,
        user_session_id=viewer_info.user_session_id,
        user_id=viewer_info.user_id,
        remember_session=data.remember_session,
    )


@auth_router.get(
    "/sessions",
    summary="Get the current user's sessions.",
    response_model=list[UserSessionSchema],
)
async def get_user_sessions(
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
    viewer_info: Annotated[
        UserInfo,
        Depends(
            dependency=get_viewer_info,
        ),
    ],
) -> ScalarResult[UserSession]:
    """Get the current user's user sessions."""
    return await auth_service.get_user_sessions(user_id=viewer_info.user_id)


@auth_router.post(
    "/reset-password-request",
    status_code=HTTPStatus.ACCEPTED,
    summary="Send a password reset request.",
    response_model=None,
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="20/hour",
            ),
        ),
    ],
)
async def request_password_reset(
    data: PasswordResetRequestInput,
    request_ip: Annotated[
        str,
        Depends(
            dependency=get_ip_address,
        ),
    ],
    user_agent: Annotated[str, Header()],
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> None:
    """Send a password reset request to the given email."""
    await auth_service.send_password_reset_request(
        email=data.email,
        user_agent=parse(user_agent),
        request_ip=request_ip,
    )


@auth_router.post(
    "/reset-password",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Reset user password.",
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    response_model=None,
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="20/hour",
            ),
        ),
    ],
)
async def reset_password(
    data: PasswordResetInput,
    request_ip: Annotated[
        str,
        Depends(
            dependency=get_ip_address,
        ),
    ],
    user_agent: Annotated[str, Header()],
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> None:
    """Reset the user's password."""
    await auth_service.reset_password(
        reset_token=data.reset_token.get_secret_value(),
        email=data.email,
        new_password=data.new_password.get_secret_value(),
        request_ip=request_ip,
        user_agent=parse(user_agent),
    )
