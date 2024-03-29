from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseSchema


class WebAuthnCredentialSchema(BaseSchema):
    id: Annotated[
        UUID,
        Field(
            description="The ID of the WebAuthn credential.",
        ),
    ]

    credential_id: Annotated[
        bytes,
        Field(
            description="The credential ID of the WebAuthn credential.",
        ),
    ]

    public_key: Annotated[
        bytes,
        Field(
            description="The public key of the WebAuthn credential.",
        ),
    ]

    device_type: Annotated[
        str,
        Field(
            description="The device type of the WebAuthn credential.",
        ),
    ]

    created_at: Annotated[
        datetime,
        Field(
            title="Created At",
            description="When the user session was created.",
        ),
    ]
