from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from app.core.models import CoreModel


class User(CoreModel):
    id: UUID

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
