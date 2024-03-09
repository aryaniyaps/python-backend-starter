from datetime import datetime
from typing import Annotated

from pydantic import Field
from webauthn.helpers.structs import AuthenticatorTransport

from app.schemas.base import BaseSchema


class WebAuthnCredentialSchema(BaseSchema):
    id: Annotated[
        bytes,
        Field(
            description="The ID of the WebAuthn credential.",
        ),
    ]

    public_key: Annotated[
        bytes,
        Field(
            description="The public key of the WebAuthn credential.",
        ),
    ]

    sign_count: Annotated[
        int,
        Field(
            description="The sign count of the WebAuthn credential.",
        ),
    ]

    device_type: Annotated[
        str,
        Field(
            description="The device type of the WebAuthn credential.",
        ),
    ]

    backed_up: Annotated[
        bool,
        Field(
            description="Whether the WebAuthn credential has been backed up.",
        ),
    ]

    transports: Annotated[
        list[AuthenticatorTransport] | None,
        Field(
            description="The transports of the WebAuthn credential.",
        ),
    ]

    created_at: Annotated[
        datetime,
        Field(
            title="Created At",
            description="When the user session was created.",
        ),
    ]
