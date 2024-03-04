from typing import Annotated
from uuid import UUID

from pydantic import EmailStr, Field, Json, RootModel
from webauthn.helpers.structs import (
    AuthenticationCredential,
    PublicKeyCredentialCreationOptions,
)

from app.lib.enums import RegisterFlowStep
from app.schemas.base import BaseSchema
from app.schemas.user import UserSchema


class RegisterFlowSchema(BaseSchema):
    id: UUID

    current_step: RegisterFlowStep

    email: Annotated[
        str,
        Field(
            examples=[
                "a********s@example.com",
            ],
        ),
    ]


class RegisterFlowStartInput(BaseSchema):
    email: Annotated[
        EmailStr,
        Field(
            max_length=255,
        ),
    ]


class RegisterFlowStartResult(BaseSchema):
    register_flow: RegisterFlowSchema


class RegisterFlowVerifyInput(BaseSchema):
    verification_code: Annotated[
        str,
        Field(
            examples=[
                "87996502",
            ],
        ),
    ]


class RegisterFlowVerifyResult(BaseSchema):
    register_flow: RegisterFlowSchema


class RegisterFlowWebAuthnStartResult(BaseSchema):
    register_flow: RegisterFlowSchema

    options: PublicKeyCredentialCreationOptions


class RegisterFlowWebAuthnFinishInput(BaseSchema):
    # FIXME: the client sends client data json under the key clientDataJSON, while we
    # expect it to be clientDataJson. we need to fix this naming issue
    credential: Json


RegisterFlowWebAuthnFinishResult = RootModel[UserSchema]

AuthenticateUserResult = RootModel[UserSchema]


class LoginOptionsInput(BaseSchema):
    email: Annotated[
        EmailStr,
        Field(
            max_length=255,
        ),
    ]


class LoginVerificationInput(BaseSchema):
    credential: Json[AuthenticationCredential]


class CreateWebAuthnCredentialInput(BaseSchema):
    pass


class LogoutInput(BaseSchema):
    remember_session: Annotated[
        bool,
        Field(
            title="Remember Session",
            description="Whether the current user's session should be remembered.",
        ),
    ] = True
