from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, Index, String, text
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column

from app.lib.database import Base


class EmailVerificationToken(Base):
    __tablename__ = "email_verification_tokens"

    __table_args__ = (
        Index(
            "email_verification_tokens_email_token_hash_idx",
            Column("email"),
            Column("token_hash"),
        ),
    )

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

    token_hash: Mapped[str] = mapped_column(
        String(255),
        index=True,
    )

    expires_at: Mapped[datetime]
