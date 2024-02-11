from http import HTTPStatus
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Header
from sqlalchemy import ScalarResult
from user_agents import parse

from app.auth.dependencies import (
    authentication_token_header,
    get_auth_service,
    get_viewer_info,
)
from app.auth.models import UserSession
from app.auth.schemas import (
    EmailVerificationInput,
    EmailVerificationRequestInput,
    EmailVerificationResult,
    LoginUserInput,
    LoginUserResult,
    LogoutInput,
    PasswordResetInput,
    PasswordResetRequestInput,
    RegisterUserInput,
    RegisterUserResult,
    UserSessionSchema,
)
from app.auth.services import AuthService
from app.auth.types import UserInfo
from app.core.constants import OpenAPITag
from app.core.dependencies import get_ip_address
from app.core.rate_limiter import RateLimiter

auth_router = APIRouter(
    prefix="/auth",
    tags=[OpenAPITag.AUTHENTICATION],
)


@auth_router.post(
    "/email-verification-request",
    response_model=None,
    status_code=HTTPStatus.NO_CONTENT,
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
    "/verify-email",
    summary="Verify user email.",
    response_model=EmailVerificationResult,
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="20/hour",
            ),
        ),
    ],
)
async def verify_email(
    data: EmailVerificationInput,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> EmailVerificationResult:
    """Verify the user's email."""
    verification_token = await auth_service.verify_email(
        verification_token=data.verification_token,
        email=data.email,
    )

    return EmailVerificationResult(
        verification_token_id=verification_token.id,
    )


@auth_router.post(
    "/register",
    response_model=RegisterUserResult,
    status_code=HTTPStatus.CREATED,
    summary="Register a new user.",
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
        username=data.username,
        password=data.password,
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
        password=data.password,
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


@auth_router.delete(
    "/sessions/",
    summary="Logout every other session for the user except for the current session.",
)
async def delete_user_sessions(
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
) -> None:
    """Logout every other session except for the current session."""
    await auth_service.delete_user_sessions(
        user_id=viewer_info.user_id,
        except_user_session_id=viewer_info.user_session_id,
    )


@auth_router.post(
    "/reset-password-request",
    status_code=HTTPStatus.NO_CONTENT,
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
        reset_token=data.reset_token,
        email=data.email,
        new_password=data.new_password,
        request_ip=request_ip,
        user_agent=parse(user_agent),
    )
