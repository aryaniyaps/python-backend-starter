from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from app.lib.constants import MAX_USERNAME_LENGTH
from app.lib.database import Base

if TYPE_CHECKING:
    from app.models.user_session import UserSession
    from app.models.webauthn_credential import WebAuthnCredential


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
    )

    username: Mapped[str] = mapped_column(
        CITEXT(MAX_USERNAME_LENGTH),
        unique=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=now(),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        onupdate=now(),
    )

    webauthn_credentials: Mapped[set["WebAuthnCredential"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    user_sessions: Mapped[set["UserSession"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
