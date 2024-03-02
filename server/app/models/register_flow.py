from datetime import datetime
from uuid import UUID

from sqlalchemy import String, text
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column

from app.lib.database import Base


class RegisterFlow(Base):
    __tablename__ = "register_flows"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
    )

    email: Mapped[str] = mapped_column(
        CITEXT(250),
        index=True,
    )

    verification_code_hash: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )

    is_verified: Mapped[bool] = mapped_column(
        default=False,
    )

    expires_at: Mapped[datetime]
