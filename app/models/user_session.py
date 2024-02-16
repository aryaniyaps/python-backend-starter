from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import Index
from sqlalchemy.sql.functions import now

from app.lib.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class UserSession(Base):
    __tablename__ = "user_sessions"

    __table_args__ = (
        Index(
            "user_sessions_user_id_ip_address_idx",
            Column("user_id"),
            Column("ip_address"),
        ),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    ip_address: Mapped[str] = mapped_column(
        String(40),
    )

    subdivision_geoname_id: Mapped[int]

    location: Mapped[str] = mapped_column(
        String(256),
    )

    user_agent: Mapped[str] = mapped_column(
        String(256),
    )

    device: Mapped[str] = mapped_column(
        String(256),
    )

    logged_out_at: Mapped[datetime | None]

    created_at: Mapped[datetime] = mapped_column(
        server_default=now(),
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="user_sessions",
    )
