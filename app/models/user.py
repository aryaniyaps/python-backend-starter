from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from app.lib.constants import MAX_USERNAME_LENGTH
from app.lib.database import Base
from app.models.user_email import UserEmail

if TYPE_CHECKING:
    from app.models.authenticator import Authenticator
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

    primary_email_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_emails.id"),
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=now(),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        onupdate=now(),
    )

    user_emails: Mapped[set["UserEmail"]] = relationship(
        back_populates="user",
        primaryjoin=lambda: User.id == UserEmail.user_id,
        cascade="all, delete-orphan",
    )

    primary_email: Mapped["UserEmail"] = relationship(
        back_populates="user",
        primaryjoin=lambda: User.primary_email_id == UserEmail.id,
        uselist=False,
        cascade="all, delete-orphan",
    )

    authenticators: Mapped[set["Authenticator"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    user_sessions: Mapped[set["UserSession"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
