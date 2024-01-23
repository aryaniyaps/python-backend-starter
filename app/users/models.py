from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, text
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from app.core.database import Base

if TYPE_CHECKING:
    from app.auth.models import PasswordResetToken


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
    )

    username: Mapped[str] = mapped_column(
        CITEXT(32),
        unique=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        CITEXT(250),
        unique=True,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(128),
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
