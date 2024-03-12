from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from app.lib.database.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.webauthn_credential import WebAuthnCredential


class UserSession(Base):
    __tablename__ = "user_sessions"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    webauthn_credential_id: Mapped[UUID] = mapped_column(
        ForeignKey("webauthn_credentials.id"),
    )

    ip_address: Mapped[str] = mapped_column(
        String(40),
    )

    location: Mapped[str] = mapped_column(
        String(256),
    )

    user_agent: Mapped[str]

    logged_out_at: Mapped[datetime | None]

    created_at: Mapped[datetime] = mapped_column(
        server_default=now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="user_sessions",
    )

    webauthn_credential: Mapped["WebAuthnCredential"] = relationship(
        back_populates="user_sessions",
    )
