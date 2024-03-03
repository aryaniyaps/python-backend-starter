from typing import Annotated
from uuid import UUID

from pydantic import EmailStr, Field, Json
from webauthn.helpers.structs import (
    AuthenticationCredential,
    PublicKeyCredentialCreationOptions,
    RegistrationCredential,
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


class RegisterFlowResendVerificationInput(BaseSchema):
    flow_id: UUID


class RegisterFlowCancelInput(BaseSchema):
    flow_id: UUID


class RegisterFlowVerifyInput(BaseSchema):
    flow_id: UUID

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


class RegisterFlowWebAuthnStartInput(BaseSchema):
    flow_id: UUID

    display_name: Annotated[
        str,
        Field(
            max_length=75,
            examples=[
                "My webauthn credential",
            ],
        ),
    ]


class RegisterFlowWebAuthnStartResult(BaseSchema):
    register_flow: RegisterFlowSchema

    options: PublicKeyCredentialCreationOptions


class RegisterFlowWebAuthnFinishInput(BaseSchema):
    flow_id: UUID

    display_name: Annotated[
        str,
        Field(
            max_length=70,
            examples=[
                "Aryan Iyappan",
            ],
        ),
    ]

    # FIXME: the client sends client data json under the key clientDataJSON, while we
    # expect it to be clientDataJson. we need to fix this naming issue
    credential: Json[RegistrationCredential]


class RegisterFlowWebAuthnFinishResult(BaseSchema):
    user: UserSchema

    authentication_token: Annotated[
        str,
        Field(
            examples=[
                "6fa74977e2a810ea95ef22f5f09d887337070ae0aacdf19d411bbe78fb98bdfa",
            ],
            title="Authentication Token",
            description="The authentication token generated upon successful registration.",
        ),
    ]


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


class AuthenticateUserResult(BaseSchema):
    authentication_token: Annotated[
        str,
        Field(
            examples=[
                "6fa74977e2a810ea95ef22f5f09d887337070ae0aacdf19d411bbe78fb98bdfa",
            ],
            title="Authentication Token",
            description="The authentication token generated upon successful login.",
        ),
    ]

    user: Annotated[
        UserSchema,
        Field(
            description="The logged in user.",
        ),
    ]


class RegisterUserResult(BaseSchema):
    authentication_token: Annotated[
        str,
        Field(
            title="Authentication Token",
            description="The authentication token obtained after registration.",
            examples=[
                "6fa74977e2a810ea95ef22f5f09d887337070ae0aacdf19d411bbe78fb98bdfa",
            ],
        ),
    ]

    user: Annotated[
        UserSchema,
        Field(
            description="The registered user.",
        ),
    ]


class LogoutInput(BaseSchema):
    remember_session: Annotated[
        bool,
        Field(
            title="Remember Session",
            description="Whether the current user's session should be remembered.",
        ),
    ] = True
