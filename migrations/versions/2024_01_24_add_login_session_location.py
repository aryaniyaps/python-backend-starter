"""
add login session location

Revision ID: 27097746b44f
Revises: 98fa494ae1a0
Create Date: 2024-01-24 16:58:06.304008

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "27097746b44f"
down_revision: str | None = "98fa494ae1a0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "login_sessions", sa.Column("location", sa.String(length=256), nullable=False)
    )


def downgrade() -> None:
    op.drop_column("login_sessions", "location")
