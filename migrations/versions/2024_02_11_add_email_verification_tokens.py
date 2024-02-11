"""
add email verification tokens

Revision ID: 4532e1253dae
Revises: 6a6f953b7c2f
Create Date: 2024-02-11 14:18:23.292923

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "4532e1253dae"
down_revision: str | None = "6a6f953b7c2f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "email_verification_tokens",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("email", postgresql.CITEXT(length=250), nullable=False),
        sa.Column("token_hash", sa.String(length=255), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("email_verification_tokens_pkey")),
    )
    op.create_index(
        op.f("email_verification_tokens_email_idx"),
        "email_verification_tokens",
        ["email"],
        unique=False,
    )
    op.create_index(
        op.f("email_verification_tokens_token_hash_idx"),
        "email_verification_tokens",
        ["token_hash"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("email_verification_tokens_token_hash_idx"),
        table_name="email_verification_tokens",
    )
    op.drop_index(
        op.f("email_verification_tokens_email_idx"),
        table_name="email_verification_tokens",
    )
    op.drop_table("email_verification_tokens")
