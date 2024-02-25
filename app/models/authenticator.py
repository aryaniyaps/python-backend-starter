from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from app.lib.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Authenticator(Base):
    __tablename__ = "authenticators"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
    )

    credential_id: Mapped[str] = mapped_column(
        unique=True,
        index=True,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    credential_public_key: Mapped[str]

    sign_count: Mapped[int]

    credential_device_type: Mapped[str]

    credential_backed_up: Mapped[bool]

    transports: Mapped[str | None]

    created_at: Mapped[datetime] = mapped_column(
        server_default=now(),
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="authenticators",
    )
