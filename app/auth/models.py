from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import EmailStr, Field

from app.core.models import CoreModel
from app.users.models import User


class LoginUserInput(CoreModel):
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


class LoginUserResult(CoreModel):
    authentication_token: Annotated[
        str,
        Field(
            examples=[
                "authentication_token",
            ],
            description="The authentication token generated upon successful login.",
        ),
    ]
    user: User


class RegisterUserInput(CoreModel):
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
            # TODO: fix regex issues with pydantic
            # pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_+=]).+",
            examples=[
                "my_super_secret",
            ],
            description="The password for the new user account.",
        ),
    ]


class RegisterUserResult(CoreModel):
    authentication_token: Annotated[
        str,
        Field(
            description="The authentication token obtained after registration.",
            examples=[
                "authentication_token",
            ],
        ),
    ]
    user: User


class PasswordResetRequestInput(CoreModel):
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


class PasswordResetInput(CoreModel):
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
            # TODO: fix regex issues with pydantic
            # pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_+=]).+",
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


class PasswordResetToken(CoreModel):
    id: UUID
    user_id: Annotated[
        UUID,
        Field(
            description="The ID of the user associated with the password reset token.",
        ),
    ]
    token_hash: Annotated[
        str,
        Field(
            exclude=True,
        ),
    ]
    last_login_at: Annotated[
        datetime,
        Field(
            description="""When the user associated with the password
            reset token last logged in.""",
        ),
    ]
    created_at: Annotated[
        datetime,
        Field(
            description="When the password reset token was created.",
        ),
    ]
    expires_at: Annotated[
        datetime,
        Field(
            description="When the password reset token expires.",
        ),
    ]
