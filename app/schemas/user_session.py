from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field
from pydantic.networks import IPvAnyAddress

from app.schemas.base import BaseSchema


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
            examples=[
                "192.158.1.38",
            ],
        ),
    ]

    location: Annotated[
        str,
        Field(
            description="The location of the user session.",
            examples=[
                "Los Angeles, California (US)",
            ],
        ),
    ]

    device: Annotated[
        str,
        Field(
            title="User Agent",
            description="The device of the user session.",
            examples=[
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
            ],
        ),
    ]

    logged_out_at: Annotated[
        datetime | None,
        Field(
            title="Logged Out At",
            description="When the user logged out of the session.",
        ),
    ]

    created_at: Annotated[
        datetime,
        Field(
            title="Created At",
            description="When the user session was created.",
        ),
    ]
