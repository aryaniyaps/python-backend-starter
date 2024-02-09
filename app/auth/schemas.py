from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import EmailStr, Field
from pydantic.networks import IPvAnyAddress

from app.core.schemas import BaseSchema
from app.users.schemas import UserSchema


class UserSessionSchema(BaseSchema):
    id: Annotated[
        UUID,
        Field(
            description="The ID of the user session.",
        ),
    ]

    ip_address: Annotated[
        IPvAnyAddress,
        Field(
            title="IP Address",
            description="The IP address of the user session.",
        ),
    ]

    location: Annotated[
        str,
        Field(
            description="The location of the user session.",
        ),
    ]

    user_agent: Annotated[
        str,
        Field(
            title="User Agent",
            description="The user agent of the user session.",
        ),
    ]

    created_at: Annotated[
        datetime,
        Field(
            title="Created At",
            description="When the user session was created.",
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
                "authentication_token",
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
            max_length=64,
            pattern=r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W])",
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
            title="Remember Session",
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
            max_length=64,
            pattern=r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W])",
            examples=[
                "super-Secret12!",
            ],
            title="New Password",
            description="The new password for the user account.",
        ),
    ]

    reset_token: Annotated[
        str,
        Field(
            examples=[
                "my_reset_token",
            ],
            title="Reset Token",
            description="""The token used to verify the user's identity
            during the password reset process.""",
        ),
    ]
