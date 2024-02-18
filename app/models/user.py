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
    from app.models.auth_provider import AuthProvider
    from app.models.password_reset_token import PasswordResetToken
    from app.models.user_password import UserPassword
    from app.models.user_session import UserSession


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

    email: Mapped[str] = mapped_column(
        CITEXT(250),
        unique=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=now(),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        onupdate=now(),
    )

    user_passwords: Mapped[list["UserPassword"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    password_reset_tokens: Mapped[list["PasswordResetToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    auth_providers: Mapped[list["AuthProvider"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    user_sessions: Mapped[list["UserSession"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
