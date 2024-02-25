from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Header
from user_agents import parse
from webauthn.helpers.structs import (
    PublicKeyCredentialCreationOptions,
    PublicKeyCredentialRequestOptions,
)

from app.dependencies.auth import (
    authentication_token_header,
    get_auth_service,
    get_viewer_info,
)
from app.dependencies.ip_address import get_ip_address
from app.dependencies.rate_limiter import RateLimiter
from app.lib.constants import OpenAPITag
from app.models.user_session import UserSession
from app.schemas.auth import (
    AuthenticateUserResult,
    EmailVerificationRequestInput,
    LoginOptionsInput,
    LoginVerificationInput,
    LogoutInput,
    RegisterOptionsInput,
    RegisterUserResult,
    RegisterVerificationInput,
)
from app.schemas.errors import InvalidInputErrorResult
from app.schemas.user_session import UserSessionSchema
from app.services.auth import AuthService
from app.types.auth import AuthenticationResult, UserInfo

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
    "/register/options",
    response_model=PublicKeyCredentialCreationOptions,
)
async def registration_options(
    data: RegisterOptionsInput,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> PublicKeyCredentialCreationOptions:
    """Generate options for registering a credential."""
    return await auth_service.generate_registration_options(
        email=data.email,
        verification_code=data.verification_code,
    )


@auth_router.post(
    "/register/verification",
    response_model=RegisterUserResult,
)
async def registration_verification(
    data: RegisterVerificationInput,
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
) -> AuthenticationResult:
    """Verify the authenticator's response for registration."""
    return await auth_service.verify_registration_response(
        email=data.email,
        credential=data.credential,
        request_ip=request_ip,
        user_agent=parse(user_agent),
    )


@auth_router.post(
    "/login/options",
    response_model=PublicKeyCredentialRequestOptions,
)
async def login_options(
    data: LoginOptionsInput,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> PublicKeyCredentialRequestOptions:
    """Generate options for retrieving a credential."""
    return await auth_service.generate_login_options(
        email=data.email,
    )


@auth_router.post(
    "/login/verification",
    response_model=AuthenticateUserResult,
)
async def login_verification(
    data: LoginVerificationInput,
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
) -> AuthenticationResult:
    """Verify the authenticator's response for login."""
    return await auth_service.verify_login_response(
        credential=data.credential,
        request_ip=request_ip,
        user_agent=parse(user_agent),
    )


@auth_router.delete("/credentials/{credential_id}")
async def delete_credential() -> None:
    pass


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
) -> list[UserSession]:
    """Get the current user's user sessions."""
    return await auth_service.get_user_sessions(
        user_id=viewer_info.user_id,
    )
