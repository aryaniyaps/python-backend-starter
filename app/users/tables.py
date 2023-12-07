from sqlalchemy import Column, DateTime, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

from app.core.database import database_metadata

users_table = Table(
    "users",
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
        "username",
        String(32),
        nullable=False,
        unique=True,
        index=True,
    ),
    Column(
        "email",
        String(250),
        nullable=False,
        unique=True,
        index=True,
    ),
    Column(
        "password_hash",
        String(128),
        nullable=False,
        unique=True,
    ),
    Column(
        "last_login_at",
        DateTime(timezone=True),
        server_default=text("now()"),
        nullable=False,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        server_default=text("now()"),
        nullable=False,
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=text("now()"),
        onupdate=text("now()"),
        nullable=False,
    ),
)
