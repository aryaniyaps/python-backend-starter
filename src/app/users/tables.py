from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.core.database import database_metadata

users_table = Table(
    "users",
    database_metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
    ),
    Column(
        "username",
        String(32),
        nullable=False,
        unique=True,
    ),
    Column(
        "email",
        String(250),
        nullable=False,
        unique=True,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    ),
)
