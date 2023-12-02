from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.sql import func

from app.core.database import database_metadata

password_reset_tokens_table = Table(
    "password_reset_tokens",
    database_metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
    ),
    Column(
        "token",
        String(64),
        nullable=False,
        unique=True,
    ),
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "expires_at",
        DateTime(timezone=True),
        nullable=False,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    ),
)
