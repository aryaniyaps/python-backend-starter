from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from app.lib.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class UserEmail(Base):
    __tablename__ = "user_emails"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
    )

    email_address: Mapped[str] = mapped_column(
        CITEXT(250),
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=now(),
    )

    # TODO: add attribute is_verified?

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="user_emails",
    )
