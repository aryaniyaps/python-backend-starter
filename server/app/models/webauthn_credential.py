from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now
from webauthn.helpers.structs import AuthenticatorTransport

from app.lib.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class WebAuthnCredential(Base):
    __tablename__ = "webauthn_credentials"

    id: Mapped[str] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )

    public_key: Mapped[str]

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
