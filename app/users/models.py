from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import EmailStr, Field

from app.core.models import CoreModel


class User(CoreModel):
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

    email: Annotated[
        str,
        Field(
            examples=[
                "aryaniyaps@example.com",
            ],
            description="The email of the user.",
        ),
    ]

    password_hash: Annotated[
        str,
        Field(
            exclude=True,
        ),
    ]

    last_login_at: Annotated[
        datetime,
        Field(
            description="When the user last logged in.",
        ),
    ]

    created_at: Annotated[
        datetime,
        Field(
            description="When the user was created.",
        ),
    ]

    updated_at: Annotated[
        datetime,
        Field(
            description="When the user was last updated.",
        ),
    ]


class UpdateUserInput(CoreModel):
    username: Annotated[
        str | None,
        Field(
            default=None,
            max_length=32,
            min_length=2,
            examples=[
                "aryaniyaps_new",
            ],
            description="The new username for the user.",
        ),
    ]

    email: Annotated[
        EmailStr | None,
        Field(
            default=None,
            max_length=250,
            examples=[
                "aryan_new@example.com",
            ],
            description="The new email address for the user.",
        ),
    ]

    password: Annotated[
        str | None,
        Field(
            default=None,
            min_length=8,
            max_length=32,
            # TODO: fix regex issues with pydantic
            # pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_+=]).+",
            examples=[
                "my_new_super_secret",
            ],
            description="The new password for the user.",
        ),
    ]
