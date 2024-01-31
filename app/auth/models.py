from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import Index, UniqueConstraint
from sqlalchemy.sql.functions import now

from app.core.database import Base

if TYPE_CHECKING:
    from app.users.models import User


class LoginSession(Base):
    __tablename__ = "login_sessions"

    __table_args__ = (
        Index(
            "login_sessions_user_id_ip_address_idx",
            Column("user_id"),
            Column("ip_address"),
        ),
    )

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

    ip_address: Mapped[str] = mapped_column(
        String(40),
    )

    location: Mapped[str] = mapped_column(
        String(256),
    )

    user_agent: Mapped[str] = mapped_column(
        String(256),
    )

    logged_out_at: Mapped[datetime | None]

    created_at: Mapped[datetime] = mapped_column(
        server_default=now(),
    )

    user = relationship("User", back_populates="login_sessions")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
    )

    token_hash: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        index=True,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
    )

    expires_at: Mapped[datetime]

    created_at: Mapped[datetime] = mapped_column(
        server_default=now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="password_reset_tokens",
    )
