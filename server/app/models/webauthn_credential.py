from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now
from webauthn.helpers.structs import AuthenticatorTransport

from app.lib.database.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class WebAuthnCredential(Base):
    __tablename__ = "webauthn_credentials"

    # TODO: rename this ID to credential_id and use UUIDs as primary keys.
    # this will help in pagination and is what is done by sites like locker.io
    # [
    # {
    #    "id": "3ef13c24-41e1-42cd-b1d5-e0fc2c3e313c",
    #    "created_time": 1710044530.0,
    #    "webauthn_credential_id": "UDHFMGLY5DibnQ0ZjuQhIFD4H8picoZkSUgpzbSnupw",
    #    "webauthn_public_key": "pQECAyYgASFYIOx0ZG9JvqL6XjMWbrbdrxK84i2eKSRSE-umk1H-Nl9fIlggmair70G8ri-t-tuhnqmO0Qa0eOOshoSV5VGeNzRgp18",
    #    "name": "Other_Windows_Chrome",
    #    "last_used_time": 1710044580.0
    # }
    # ]
    id: Mapped[bytes] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )

    public_key: Mapped[bytes]

    sign_count: Mapped[int]

    device_type: Mapped[str]

    backed_up: Mapped[bool]

    transports: Mapped[list[AuthenticatorTransport] | None] = mapped_column(
        ARRAY(ENUM(AuthenticatorTransport)),
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=now(),
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="webauthn_credentials",
    )
