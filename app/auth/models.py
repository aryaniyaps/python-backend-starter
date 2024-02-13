from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import Index
from sqlalchemy.sql.functions import now

from app.core.database import Base

if TYPE_CHECKING:
    from app.users.models import User


class UserSession(Base):
    __tablename__ = "user_sessions"

    __table_args__ = (
        Index(
            "user_sessions_user_id_ip_address_idx",
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

    user: Mapped["User"] = relationship(
        "User",
        back_populates="user_sessions",
    )


class EmailVerificationToken(Base):
    __tablename__ = "email_verification_tokens"

    __table_args__ = (
        Index(
            "email_verification_tokens_email_token_hash_idx",
            Column("email"),
            Column("token_hash"),
        ),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
    )

    email: Mapped[str] = mapped_column(
        CITEXT(250),
        index=True,
    )

    token_hash: Mapped[str] = mapped_column(
        String(255),
        index=True,
    )

    expires_at: Mapped[datetime]


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
