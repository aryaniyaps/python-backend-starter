"""initial migration

Revision ID: a41c3d075424
Revises:
Create Date: 2024-01-12 09:40:24.343263

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a41c3d075424"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("username", sa.String(length=32), nullable=False),
        sa.Column("email", sa.String(length=250), nullable=False),
        sa.Column("password_hash", sa.String(length=128), nullable=False),
        sa.Column(
            "last_login_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("users_pkey")),
    )
    op.create_index(op.f("users_email_idx"), "users", ["email"], unique=True)
    op.create_index(op.f("users_username_idx"), "users", ["username"], unique=True)
    op.create_table(
        "password_reset_tokens",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("token_hash", sa.String(length=128), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("expires_at", postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("last_login_at", postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
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


def downgrade() -> None:
    op.drop_index(
        op.f("password_reset_tokens_token_hash_idx"), table_name="password_reset_tokens"
    )
    op.drop_table("password_reset_tokens")
    op.drop_index(op.f("users_username_idx"), table_name="users")
    op.drop_index(op.f("users_email_idx"), table_name="users")
    op.drop_table("users")
