from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from app.lib.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class ProviderType(StrEnum):
    google = "google"


class OauthAccount(Base):
    __tablename__ = "oauth_accounts"

    provider: Mapped[ProviderType] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=now(),
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="user_sessions",
    )
