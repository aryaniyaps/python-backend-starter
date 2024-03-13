from typing import Annotated
from uuid import UUID

from pydantic import EmailStr, Field, Json, RootModel, field_serializer
from webauthn.helpers.structs import (
    PublicKeyCredentialCreationOptions,
    PublicKeyCredentialRequestOptions,
)

from app.lib.enums import RegisterFlowStep
from app.schemas.base import BaseSchema
from app.schemas.user import UserSchema
from app.utils.formatting import redact_email


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

    @field_serializer("email")
    @classmethod
    def serialize_email(cls, email: str) -> str:
        """Redact the given email (for security purposes)."""
        return redact_email(email=email)


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
    credential: Json


RegisterFlowWebAuthnFinishResult = RootModel[UserSchema]

AuthenticateUserResult = RootModel[UserSchema]


class AuthenticateOptionsInput(BaseSchema):
    email: Annotated[
        EmailStr,
        Field(
            max_length=255,
        ),
    ]


class AuthenticateOptionsResult(BaseSchema):
    options: PublicKeyCredentialRequestOptions


class AuthenticateVerificationInput(BaseSchema):
    credential: Json


class CreateWebAuthnCredentialInput(BaseSchema):
    pass


class RegisterOptionsResult(BaseSchema):
    options: PublicKeyCredentialCreationOptions


class LogoutInput(BaseSchema):
    remember_session: Annotated[
        bool,
        Field(
            title="Remember Session",
            description="Whether the current user's session should be remembered.",
        ),
    ] = True
