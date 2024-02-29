from typing import Annotated

from pydantic import EmailStr, Field, Json
from webauthn.helpers.structs import (
    AuthenticationCredential,
    RegistrationCredential,
)

from app.schemas.base import BaseSchema
from app.schemas.user import UserSchema


class RegisterOptionsInput(BaseSchema):
    email: Annotated[
        EmailStr,
        Field(
            max_length=255,
        ),
    ]

    verification_code: Annotated[
        str,
        Field(
            examples=[
                "88765432",
            ],
        ),
    ]

    display_name: Annotated[
        str,
        Field(
            max_length=70,
            examples=[
                "Aryan Iyappan",
            ],
        ),
    ]


class RegisterVerificationInput(BaseSchema):
    email: Annotated[
        EmailStr,
        Field(
            max_length=255,
        ),
    ]

    display_name: Annotated[
        str,
        Field(
            max_length=70,
            examples=[
                "Aryan Iyappan",
            ],
        ),
    ]

    credential: Json[RegistrationCredential]


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


class EmailVerificationRequestInput(BaseSchema):
    email: Annotated[
        EmailStr,
        Field(
            max_length=250,
            examples=[
                "aryan@example.com",
            ],
            description="The email address to send the email verification request to.",
        ),
    ]


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
