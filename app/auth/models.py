import typing
from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

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
        unique=True,
        index=True,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
    )

    expires_at: Mapped[datetime]

    last_login_at: Mapped[datetime]

    created_at: Mapped[datetime] = mapped_column(
        server_default=now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="password_reset_tokens",
    )

    __mapper_args__ = {"eager_defaults": True}
