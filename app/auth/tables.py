from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, text
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import database_metadata

password_reset_tokens_table = Table(
    "password_reset_tokens",
    database_metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
    ),
    Column(
        "token_hash",
        String(128),
        nullable=False,
        unique=True,
        index=True,
    ),
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    ),
    Column(
        "expires_at",
        DateTime(timezone=True),
        nullable=False,
    ),
    Column(
        "last_login_at",
        DateTime(timezone=True),
        nullable=False,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        server_default=text("now()"),
        nullable=False,
    ),
)
