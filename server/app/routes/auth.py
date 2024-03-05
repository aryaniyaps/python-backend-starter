from http import HTTPStatus
from typing import Annotated, Any
from uuid import UUID

import user_agents
from fastapi import APIRouter, Depends, Header, Path, Response
from webauthn.helpers import (
    parse_authentication_credential_json,
    parse_registration_credential_json,
)
from webauthn.helpers.structs import (
    PublicKeyCredentialRequestOptions,
)

from app.config import settings
from app.dependencies.auth import (
    authentication_token_cookie,
    get_auth_service,
    get_viewer_info,
)
from app.dependencies.ip_address import get_ip_address
from app.lib.constants import AUTHENTICATION_TOKEN_COOKIE, OpenAPITag
from app.models.register_flow import RegisterFlow
from app.models.user import User
from app.models.user_session import UserSession
from app.schemas.auth import (
    AuthenticateOptionsInput,
    AuthenticateOptionsResult,
    AuthenticateUserResult,
    AuthenticateVerificationInput,
    CreateWebAuthnCredentialInput,
    LogoutInput,
    RegisterFlowSchema,
    RegisterFlowStartInput,
    RegisterFlowStartResult,
    RegisterFlowVerifyInput,
    RegisterFlowVerifyResult,
    RegisterFlowWebAuthnFinishInput,
    RegisterFlowWebAuthnFinishResult,
    RegisterFlowWebAuthnStartResult,
)
from app.schemas.errors import InvalidInputErrorResult, ResourceNotFoundErrorResult
from app.schemas.user_session import UserSessionSchema
from app.services.auth import AuthService
from app.types.auth import UserInfo

auth_router = APIRouter(
    prefix="/auth",
    tags=[OpenAPITag.AUTHENTICATION],
)


@auth_router.get(
    "/register/flows/{flow_id}",
    response_model=RegisterFlowSchema,
    responses={
        HTTPStatus.NOT_FOUND: {
            "model": ResourceNotFoundErrorResult,
            "description": "Resource Not Found Error",
        },
    },
    summary="Get a register flow.",
)
async def get_register_flow(
    flow_id: Annotated[
        UUID,
        Path(
            title="The ID of the register flow.",
        ),
    ],
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> RegisterFlow:
    """Get a register flow."""
    return await auth_service.get_register_flow(flow_id=flow_id)


@auth_router.post(
    "/register/flows/start",
    response_model=RegisterFlowStartResult,
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    summary="Start a register flow.",
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
) -> dict[str, Any]:
    """Start a register flow."""
    register_flow = await auth_service.start_register_flow(
        email=data.email,
        user_agent=user_agents.parse(user_agent),
        request_ip=request_ip,
    )

    return {"register_flow": register_flow}


@auth_router.post(
    "/register/flows/{flow_id}/cancel",
    response_model=None,
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    summary="Cancel a register flow.",
)
async def cancel_register_flow(
    flow_id: Annotated[
        UUID,
        Path(
            title="The ID of the register flow.",
        ),
    ],
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> None:
    """Cancel a register flow."""
    await auth_service.cancel_register_flow(
        flow_id=flow_id,
    )


@auth_router.post(
    "/register/flows/{flow_id}/resend-verification",
    response_model=None,
    status_code=HTTPStatus.ACCEPTED,
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    summary="Resend email verification in the register flow.",
)
async def resend_verification_register_flow(
    flow_id: Annotated[
        UUID,
        Path(
            title="The ID of the register flow.",
        ),
    ],
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
    """Resend email verification in the register flow."""
    await auth_service.resend_verification_register_flow(
        flow_id=flow_id,
        user_agent=user_agents.parse(user_agent),
        request_ip=request_ip,
    )


@auth_router.post(
    "/register/flows/{flow_id}/verify",
    response_model=RegisterFlowVerifyResult,
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    summary="Verify a register flow.",
)
async def verify_register_flow(
    flow_id: Annotated[
        UUID,
        Path(
            title="The ID of the register flow.",
        ),
    ],
    data: RegisterFlowVerifyInput,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> dict[str, Any]:
    """Verify a register flow."""
    register_flow = await auth_service.verify_register_flow(
        flow_id=flow_id,
        verification_code=data.verification_code,
    )

    return {"register_flow": register_flow}


@auth_router.post(
    "/register/flows/{flow_id}/webauthn-start",
    response_model=RegisterFlowWebAuthnStartResult,
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    summary="Start the webauthn registration in the register flow.",
)
async def start_webauthn_register_flow(
    flow_id: Annotated[
        UUID,
        Path(
            title="The ID of the register flow.",
        ),
    ],
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> dict[str, Any]:
    """Start the webauthn registration in the register flow."""
    register_flow, options = await auth_service.webauthn_start_register_flow(
        flow_id=flow_id,
    )

    return {
        "register_flow": register_flow,
        "options": options,
    }


@auth_router.post(
    "/register/flows/{flow_id}/webauthn-finish",
    response_model=RegisterFlowWebAuthnFinishResult,
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": InvalidInputErrorResult,
            "description": "Invalid Input Error",
        },
    },
    summary="Finish the webauthn registration in the register flow.",
)
async def finish_webauthn_register_flow(
    flow_id: Annotated[
        UUID,
        Path(
            title="The ID of the register flow.",
        ),
    ],
    data: RegisterFlowWebAuthnFinishInput,
    response: Response,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> User:
    """Finish the webauthn registration in the register flow."""
    authentication_token, user = await auth_service.webauthn_finish_register_flow(
        flow_id=flow_id,
        credential=parse_registration_credential_json(data.credential),
    )

    # set authentication token in a cookie
    response.set_cookie(
        key=AUTHENTICATION_TOKEN_COOKIE,
        value=authentication_token,
        secure=settings.is_production(),
    )

    return user


@auth_router.post(
    "/login/start",
    response_model=AuthenticateOptionsResult,
)
async def generate_authentication_options(
    data: AuthenticateOptionsInput,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> AuthenticateOptionsResult:
    """Generate options for retrieving a credential."""
    options = await auth_service.generate_authentication_options(
        email=data.email,
    )

    return AuthenticateOptionsResult(options=options)


@auth_router.post(
    "/login/finish",
    response_model=AuthenticateUserResult,
)
async def verify_authentication_response(
    data: AuthenticateVerificationInput,
    user_agent: Annotated[str, Header()],
    request_ip: Annotated[
        str,
        Depends(
            dependency=get_ip_address,
        ),
    ],
    response: Response,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
) -> User:
    """Verify the authenticator's response for login."""
    authentication_token, user = await auth_service.verify_authentication_response(
        credential=parse_authentication_credential_json(data.credential),
        request_ip=request_ip,
        user_agent=user_agents.parse(user_agent),
    )

    # set authentication token in a cookie
    response.set_cookie(
        key=AUTHENTICATION_TOKEN_COOKIE,
        value=authentication_token,
        secure=settings.is_production(),
    )

    return user


@auth_router.post("/webauthn-credentials")
async def create_webauthn_credential(_data: CreateWebAuthnCredentialInput) -> None:
    """Create a new webauthn credential."""


@auth_router.post(
    "/logout",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Logout the current user.",
)
async def delete_current_user_session(
    data: LogoutInput,
    response: Response,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
    authentication_token: Annotated[
        str,
        Depends(
            authentication_token_cookie,
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

    # remove authentication token from cookie
    response.delete_cookie(AUTHENTICATION_TOKEN_COOKIE)


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
