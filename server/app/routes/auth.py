from http import HTTPStatus
from typing import Annotated

import user_agents
from fastapi import APIRouter, Depends, Header
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
    CreateWebAuthnCredentialInput,
    LoginOptionsInput,
    LoginVerificationInput,
    LogoutInput,
    RegisterFlowStartInput,
    RegisterFlowStartResult,
    RegisterFlowVerifyInput,
    RegisterFlowVerifyResult,
    RegisterFlowWebAuthnFinishInput,
    RegisterFlowWebAuthnStartInput,
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
    "/register/flow/start",
    response_model=RegisterFlowStartResult,
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    summary="Start a register flow.",
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="15/hour",
            ),
        ),
    ],
)
async def start_register_flow(
    data: RegisterFlowStartInput,
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
) -> RegisterFlowStartResult:
    """Start a register flow."""
    register_flow = await auth_service.start_register_flow(
        email=data.email,
        user_agent=user_agents.parse(user_agent),
        request_ip=request_ip,
    )

    return RegisterFlowStartResult(
        flow_id=register_flow.id,
    )


@auth_router.post(
    "/register/flow/verify",
    response_model=RegisterFlowVerifyResult,
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    summary="Verify a register flow.",
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="15/hour",
            ),
        ),
    ],
)
async def verify_register_flow(
    data: RegisterFlowVerifyInput,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> RegisterFlowVerifyResult:
    """Verify a register flow."""
    register_flow = await auth_service.verify_register_flow(
        flow_id=data.flow_id,
        verification_code=data.verification_code,
    )

    return RegisterFlowVerifyResult(
        flow_id=register_flow.id,
    )


@auth_router.post(
    "/register/flow/webauthn-start",
    response_model=PublicKeyCredentialCreationOptions,
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    summary="Start the webauthn registration in the register flow.",
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="15/hour",
            ),
        ),
    ],
)
async def start_webauthn_register_flow(
    data: RegisterFlowWebAuthnStartInput,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> PublicKeyCredentialCreationOptions:
    """Start the webauthn registration in the register flow."""
    return await auth_service.webauthn_start_register_flow(
        flow_id=data.flow_id,
        display_name=data.display_name,
    )


@auth_router.post(
    "/register/flow/webauthn-finish",
    response_model=AuthenticationResult,
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    summary="Finish the webauthn registration in the register flow.",
    dependencies=[
        Depends(
            dependency=RateLimiter(
                limit="15/hour",
            ),
        ),
    ],
)
async def finish_webauthn_register_flow(
    data: RegisterFlowWebAuthnFinishInput,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> AuthenticationResult:
    """Finish the webauthn registration in the register flow."""
    return await auth_service.webauthn_finish_register_flow(
        flow_id=data.flow_id,
        display_name=data.display_name,
        credential=data.credential,
    )


@auth_router.post(
    "/login/start",
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
    "/login/finish",
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
        user_agent=user_agents.parse(user_agent),
    )


@auth_router.post("/webauthn-credentials")
async def create_webauthn_credential(_data: CreateWebAuthnCredentialInput) -> None:
    """Create a new webauthn credential."""


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
