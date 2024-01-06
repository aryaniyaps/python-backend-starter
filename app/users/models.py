import typing
from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import FetchedValue, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base

if typing.TYPE_CHECKING:
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
        String(32),
        nullable=False,
        unique=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(250),
        nullable=False,
        unique=True,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    last_login_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=FetchedValue(),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=func.now(),
        server_default=FetchedValue(),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        # nullable=False,
        onupdate=func.now(),
        server_default=FetchedValue(),
        server_onupdate=FetchedValue(),
    )

    password_reset_tokens: Mapped[List["PasswordResetToken"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    __mapper_args__ = {"eager_defaults": True}
