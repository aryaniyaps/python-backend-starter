from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import EmailStr, Field, PrivateAttr, SecretStr, computed_field

from app.schemas.base import BaseSchema
from app.utils.avatars import generate_avatar_url


class PartialUserSchema(BaseSchema):
    id: Annotated[
        UUID,
        Field(
            description="The ID of the user.",
        ),
    ]

    # email is a private attribute and is not
    # exposed on the partial user schema. We need this field
    # to generate the gravatar URL.
    email: Annotated[
        str,
        PrivateAttr(),
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

    @computed_field(  # type: ignore[misc]
        title="Avatar URL",
        description="The Gravatar URL of the user.",
    )
    @property
    def avatar_url(self) -> str:
        """Generate a Gravatar URL for the user."""
        return generate_avatar_url(email=self.email)


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
