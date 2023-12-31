from typing import Annotated

from pydantic import EmailStr, Field

from app.core.schemas import BaseSchema
from app.users.schemas import UserSchema


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
            # TODO: fix regex issues with pydantic
            # pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_+=]).+",
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
