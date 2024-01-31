from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import EmailStr, Field
from pydantic.networks import IPvAnyAddress

from app.core.schemas import BaseSchema
from app.users.schemas import UserSchema


class LoginSessionSchema(BaseSchema):
    id: Annotated[
        UUID,
        Field(
            description="The ID of the login session.",
        ),
    ]

    ip_address: Annotated[
        IPvAnyAddress,
        Field(
            description="The IP address of the login session.",
        ),
    ]

    location: Annotated[
        str,
        Field(
            description="The location of the login session.",
        ),
    ]

    created_at: Annotated[
        datetime,
        Field(
            description="When the login session was created.",
        ),
    ]


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
        str,
        Field(
            examples=[
                "my_super_secret",
            ],
            description="The password associated with the user account.",
        ),
    ]


class LoginUserResult(BaseSchema):
    authentication_token: Annotated[
        str,
        Field(
            examples=[
                "authentication_token",
            ],
            description="The authentication token generated upon successful login.",
        ),
    ]

    user: Annotated[
        UserSchema,
        Field(
            description="The logged in user.",
        ),
    ]


class RegisterUserInput(BaseSchema):
    username: Annotated[
        str,
        Field(
            max_length=32,
            min_length=2,
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

    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=32,
            pattern=r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W])",
            examples=[
                "my_super_secret",
            ],
            description="The password for the new user account.",
        ),
    ]


class RegisterUserResult(BaseSchema):
    authentication_token: Annotated[
        str,
        Field(
            description="The authentication token obtained after registration.",
            examples=[
                "authentication_token",
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
            description="Whether the current user's session should be remembered.",
        ),
    ] = True


class PasswordResetRequestInput(BaseSchema):
    email: Annotated[
        EmailStr,
        Field(
            max_length=250,
            examples=[
                "aryan@example.com",
            ],
            description="""The email address associated with the user account
            for which a password reset is requested.""",
        ),
    ]


class PasswordResetInput(BaseSchema):
    email: Annotated[
        EmailStr,
        Field(
            max_length=250,
            examples=[
                "aryan@example.com",
            ],
            description="""The email address associated with the user account
            for which the password is being reset.""",
        ),
    ]

    new_password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=32,
            pattern=r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W])",
            examples=[
                "my_super_secret",
            ],
            description="The new password for the user account.",
        ),
    ]

    reset_token: Annotated[
        str,
        Field(
            examples=[
                "my_reset_token",
            ],
            description="""The token used to verify the user's identity
            during the password reset process.""",
        ),
    ]
