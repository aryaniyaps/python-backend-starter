"""
initial migration

Revision ID: 6a6f953b7c2f
Revises: 7a23de63905c
Create Date: 2024-02-10 17:36:07.254921

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "6a6f953b7c2f"
down_revision: str | None = "7a23de63905c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("username", postgresql.CITEXT(length=32), nullable=False),
        sa.Column("email", postgresql.CITEXT(length=250), nullable=False),
        sa.Column("password_hash", sa.String(length=128), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("users_pkey")),
    )
    op.create_index(op.f("users_email_idx"), "users", ["email"], unique=True)
    op.create_index(op.f("users_username_idx"), "users", ["username"], unique=True)
    op.create_table(
        "password_reset_tokens",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("token_hash", sa.String(length=128), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("password_reset_tokens_user_id_fkey")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("password_reset_tokens_pkey")),
    )
    op.create_index(
        op.f("password_reset_tokens_token_hash_idx"),
        "password_reset_tokens",
        ["token_hash"],
        unique=True,
    )
    op.create_table(
        "user_sessions",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("ip_address", sa.String(length=40), nullable=False),
        sa.Column("location", sa.String(length=256), nullable=False),
        sa.Column("user_agent", sa.String(length=256), nullable=False),
        sa.Column("logged_out_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("user_sessions_user_id_fkey")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("user_sessions_pkey")),
    )
    op.create_index(
        op.f("user_sessions_user_id_idx"), "user_sessions", ["user_id"], unique=False
    )
    op.create_index(
        "user_sessions_user_id_ip_address_idx",
        "user_sessions",
        ["user_id", "ip_address"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("user_sessions_user_id_ip_address_idx", table_name="user_sessions")
    op.drop_index(op.f("user_sessions_user_id_idx"), table_name="user_sessions")
    op.drop_table("user_sessions")
    op.drop_index(
        op.f("password_reset_tokens_token_hash_idx"), table_name="password_reset_tokens"
    )
    op.drop_table("password_reset_tokens")
    op.drop_index(op.f("users_username_idx"), table_name="users")
    op.drop_index(op.f("users_email_idx"), table_name="users")
    op.drop_table("users")
