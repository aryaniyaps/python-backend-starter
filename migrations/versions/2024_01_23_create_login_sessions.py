"""
create login sessions

Revision ID: b973f8d5f5b7
Revises: eaa0144fd294
Create Date: 2024-01-23 09:56:39.824257

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b973f8d5f5b7"
down_revision: str | None = "eaa0144fd294"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "login_sessions",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("ip_address", sa.String(length=40), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("login_sessions_user_id_fkey")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("login_sessions_pkey")),
    )


def downgrade() -> None:
    op.drop_table("login_sessions")
