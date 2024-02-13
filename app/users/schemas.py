from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import EmailStr, Field, SecretStr

from app.core.schemas import BaseSchema


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


class ChangeUserPasswordInput(BaseSchema):
    new_password: Annotated[
        SecretStr,
        Field(
            min_length=8,
            max_length=64,
            pattern=r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W])",
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


class UpdateUserInput(BaseSchema):
    username: Annotated[
        str | None,
        Field(
            max_length=32,
            min_length=2,
            examples=[
                "aryaniyaps_new",
            ],
            description="The new username for the user.",
        ),
    ] = None
