from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import EmailStr, Field, SecretStr

from app.schemas.base import BaseSchema


class PartialUserSchema(BaseSchema):
    id: Annotated[
        UUID,
        Field(
            description="The ID of the user.",
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

    verification_code: Annotated[
        SecretStr,
        Field(
            examples=[
                "43569923",
            ],
            title="Verification Code",
            description="The verification code for the email.",
        ),
    ]


class UpdateUserInput(BaseSchema):
    display_name: Annotated[
        str | None,
        Field(
            max_length=250,
            min_length=2,
            examples=[
                "aryaniyaps_new",
            ],
            description="The new username for the user.",
        ),
    ] = None
