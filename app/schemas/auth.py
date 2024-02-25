from typing import Annotated

from pydantic import EmailStr, Field, Json, SecretStr
from webauthn.helpers.structs import (
    AuthenticationCredential,
    RegistrationCredential,
    UserVerificationRequirement,
)

from app.lib.constants import MAX_USERNAME_LENGTH, MIN_USERNAME_LENGTH
from app.schemas.base import BaseSchema
from app.schemas.user import UserSchema


class RegistrationOptionsInput(BaseSchema):
    username: Annotated[
        str,
        Field(
            max_length=MAX_USERNAME_LENGTH,
            min_length=MIN_USERNAME_LENGTH,
        ),
    ]


class RegistrationVerificationInput(BaseSchema):
    username: Annotated[
        str,
        Field(
            max_length=MAX_USERNAME_LENGTH,
        ),
    ]

    credential: Json[RegistrationCredential]


class AuthenticationOptionsInput(BaseSchema):
    username: Annotated[
        str,
        Field(
            max_length=MAX_USERNAME_LENGTH,
        ),
    ]

    user_verification: UserVerificationRequirement


class AuthenticationVerificationInput(BaseSchema):
    username: Annotated[
        str,
        Field(
            max_length=MAX_USERNAME_LENGTH,
        ),
    ]

    credential: Json[AuthenticationCredential]


class LoginUserInput(BaseSchema):
    login: Annotated[
        str | EmailStr,
        Field(
            examples=[
                "aryaniyaps",
                "aryaniyaps@example.com",
            ],
            description="The identifier of the user account (username or email).",
        ),
    ]

    password: Annotated[
        SecretStr,
        Field(
            examples=[
                "super-Secret12!",
            ],
            description="The password associated with the user account.",
        ),
    ]


class LoginUserResult(BaseSchema):
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


class RegisterUserInput(BaseSchema):
    username: Annotated[
        str,
        Field(
            max_length=MAX_USERNAME_LENGTH,
            min_length=MIN_USERNAME_LENGTH,
            examples=[
                "aryaniyaps",
            ],
            description="The desired username for the new user account.",
        ),
    ]

    email: Annotated[
        EmailStr,
        Field(
            max_length=250,
            examples=[
                "aryan@example.com",
            ],
            description="The email address associated with the new user account.",
        ),
    ]

    email_verification_token: Annotated[
        SecretStr,
        Field(
            title="Email Verification Token",
            description="The verification token for the email address.",
        ),
    ]

    password: Annotated[
        SecretStr,
        Field(
            max_length=64,
            examples=[
                "super-Secret12!",
            ],
            description="The password for the new user account.",
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
