from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import EmailStr, Field, SecretStr

from app.lib.constants import MAX_USERNAME_LENGTH, MIN_USERNAME_LENGTH
from app.schemas.base import BaseSchema


class PartialUserSchema(BaseSchema):
    id: Annotated[
        UUID,
        Field(
            description="The ID of the user.",
        ),
    ]

    username: Annotated[
        str,
        Field(
            examples=[
                "aryaniyaps",
            ],
            description="The username of the user.",
        ),
    ]

    created_at: Annotated[
        datetime,
        Field(
            title="Created At",
            description="When the user was created.",
        ),
    ]

    updated_at: Annotated[
        datetime | None,
        Field(
            title="Updated At",
            description="When the user was last updated.",
        ),
    ]


class UserSchema(PartialUserSchema):
    email: Annotated[
        str,
        Field(
            examples=[
                "aryaniyaps@example.com",
            ],
            description="The email of the user.",
        ),
    ]

    has_password: Annotated[
        bool,
        Field(
            description="Whether the user has their password set.",
        ),
    ]


class ChangeUserPasswordInput(BaseSchema):
    new_password: Annotated[
        SecretStr,
        Field(
            max_length=64,
            examples=[
                "new-super-Secret12!",
            ],
            description="The new password for the user.",
        ),
    ]

    current_password: Annotated[
        SecretStr,
        Field(
            examples=[
                "super-Secret12!",
            ],
            title="Current Password",
            description="The password associated with the user.",
        ),
    ]


class ChangeUserEmailRequestInput(BaseSchema):
    email: Annotated[
        EmailStr,
        Field(
            max_length=250,
            examples=[
                "aryan_new@example.com",
            ],
            description="The new email address for the user.",
        ),
    ]

    current_password: Annotated[
        SecretStr,
        Field(
            examples=[
                "super-Secret12!",
            ],
            description="The password associated with the user.",
        ),
    ]


class ChangeUserEmailInput(BaseSchema):
    email: Annotated[
        EmailStr,
        Field(
            max_length=250,
            examples=[
                "aryan_new@example.com",
            ],
            description="The new email address for the user.",
        ),
    ]

    email_verification_token: Annotated[
        SecretStr,
        Field(
            title="Email Verification Token",
            description="The verification token for the email.",
        ),
    ]


class UpdateUserInput(BaseSchema):
    username: Annotated[
        str | None,
        Field(
            max_length=MAX_USERNAME_LENGTH,
            min_length=MIN_USERNAME_LENGTH,
            examples=[
                "aryaniyaps_new",
            ],
            description="The new username for the user.",
        ),
    ] = None
