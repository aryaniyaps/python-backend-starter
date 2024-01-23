from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import Index
from sqlalchemy.sql import func
from sqlalchemy.sql.functions import now

from app.core.database import Base

if TYPE_CHECKING:
    from app.auth.models import PasswordResetToken


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        Index(
            "users_email_case_insensitive_idx",
            func.lower(Column("email")),
            unique=True,
        ),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
    )

    username: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(250),
        unique=True,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(128),
    )

    last_login_at: Mapped[datetime] = mapped_column(
        server_default=now(),
    )

    last_login_ip: Mapped[str] = mapped_column(
        String(40),
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=now(),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        onupdate=now(),
    )

    password_reset_tokens: Mapped[list["PasswordResetToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
