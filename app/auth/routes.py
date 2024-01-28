from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Path, Security, status
from user_agents import parse

from app.auth.dependencies import (
    authentication_token_header,
    get_auth_service,
    get_current_user_id,
)
from app.auth.schemas import (
    LoginUserInput,
    LoginUserResult,
    PasswordResetInput,
    PasswordResetRequestInput,
    RegisterUserInput,
    RegisterUserResult,
)
from app.auth.services import AuthService
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
    )

    return {
        "authentication_token": authentication_token,
        "user": user,
    }


@auth_router.post(
    "/login",
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


@auth_router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout the current user.",
)
async def logout_user(
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


@auth_router.get(
    "/sessions",
    summary="Get the current user's login sessions.",
)
async def get_login_sessions(
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
    current_user_id: Annotated[
        UUID,
        Depends(
            dependency=get_current_user_id,
        ),
    ],
) -> None:
    """Get the current user's login sessions."""
    raise NotImplementedError


@auth_router.delete(
    "/sessions/{session_id}",
    summary="Delete the login session with the given ID.",
)
async def delete_login_session(
    session_id: Annotated[
        UUID,
        Path(
            title="The ID of the login session to delete.",
        ),
    ],
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
    current_user_id: Annotated[
        UUID,
        Depends(
            dependency=get_current_user_id,
        ),
    ],
) -> None:
    """Delete the login session with the given ID."""
    raise NotImplementedError


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
    )
