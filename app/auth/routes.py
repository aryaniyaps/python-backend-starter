from typing import Annotated, Any

from fastapi import APIRouter, Depends, Header, Security, status
from sqlalchemy import ScalarResult
from user_agents import parse

from app.auth.dependencies import (
    authentication_token_header,
    get_auth_service,
    get_user_info,
)
from app.auth.models import LoginSession
from app.auth.schemas import (
    LoginSessionSchema,
    LoginUserInput,
    LoginUserResult,
    LogoutInput,
    PasswordResetInput,
    PasswordResetRequestInput,
    RegisterUserInput,
    RegisterUserResult,
)
from app.auth.services import AuthService
from app.auth.types import UserInfo
from app.core.constants import OpenAPITag
from app.core.dependencies import get_ip_address

auth_router = APIRouter(
    prefix="/auth",
    tags=[OpenAPITag.AUTHENTICATION],
)


@auth_router.post(
    "/register",
    response_model=RegisterUserResult,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user.",
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
    "/sessions",
    response_model=LoginUserResult,
    summary="Login the current user.",
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


@auth_router.delete(
    "/sessions/@me",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout the current user.",
)
async def delete_current_login_session(
    data: LogoutInput,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
    authentication_token: Annotated[
        str,
        Security(
            authentication_token_header,
        ),
    ],
    user_info: Annotated[
        UserInfo,
        Depends(
            dependency=get_user_info,
        ),
    ],
) -> None:
    """Logout the current user."""
    await auth_service.logout_user(
        authentication_token=authentication_token,
        login_session_id=user_info.login_session_id,
        user_id=user_info.user_id,
        remember_session=data.remember_session,
    )


@auth_router.get(
    "/sessions",
    summary="Get the current user's login sessions.",
    response_model=list[LoginSessionSchema],
)
async def get_login_sessions(
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
    user_info: Annotated[
        UserInfo,
        Depends(
            dependency=get_user_info,
        ),
    ],
) -> ScalarResult[LoginSession]:
    """Get the current user's login sessions."""
    return await auth_service.get_login_sessions(user_id=user_info.user_id)


@auth_router.delete(
    "/sessions/",
    summary="Logout every other session except for the current session.",
)
async def delete_login_sessions(
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
    user_info: Annotated[
        UserInfo,
        Depends(
            dependency=get_user_info,
        ),
    ],
) -> None:
    """Logout every other session except for the current session."""
    await auth_service.delete_login_sessions(
        user_id=user_info.user_id,
        except_login_session_id=user_info.login_session_id,
    )


@auth_router.post(
    "/reset-password-request",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Send a password reset request.",
    response_model=None,
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
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Reset user password.",
    response_model=None,
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
    """Send a password reset request to the given email."""
    await auth_service.reset_password(
        reset_token=data.reset_token,
        email=data.email,
        new_password=data.new_password,
        request_ip=request_ip,
        user_agent=parse(user_agent),
    )
