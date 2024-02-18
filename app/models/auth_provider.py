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
    email = "email"


class AuthProvider(Base):
    __tablename__ = "auth_providers"

    provider: Mapped[ProviderType] = mapped_column(
        primary_key=True,
    )

    provider_user_id: Mapped[str] = mapped_column(
        primary_key=True,
    )

    # password hash is only set when the provider is `email`
    # or maybe generate random password string when user signs up with
    # oauth2? this is how fief, django auth, zoom etc do it.
    password_hash: Mapped[str | None]

    created_at: Mapped[datetime] = mapped_column(
        server_default=now(),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="user_sessions",
    )
