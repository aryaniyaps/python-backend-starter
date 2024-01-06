import typing
from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base

if typing.TYPE_CHECKING:
    from app.users.models import User


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
        nullable=False,
        unique=True,
        index=True,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        nullable=False,
    )

    last_login_at: Mapped[datetime] = mapped_column(
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="password_reset_tokens",
    )
