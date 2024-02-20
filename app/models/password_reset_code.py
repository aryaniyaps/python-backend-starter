from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from app.lib.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class PasswordResetCode(Base):
    __tablename__ = "password_reset_codes"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
    )

    code_hash: Mapped[str] = mapped_column(
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
        back_populates="password_reset_codes",
    )
