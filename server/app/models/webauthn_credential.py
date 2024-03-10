from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now
from webauthn.helpers.structs import AuthenticatorTransport

from app.lib.database.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class WebAuthnCredential(Base):
    __tablename__ = "webauthn_credentials"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
    )

    credential_id: Mapped[bytes] = mapped_column(index=True)

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
