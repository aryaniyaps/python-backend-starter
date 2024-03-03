"""
remove user display name

Revision ID: 801b0dd65ef7
Revises: 8d370a31c5aa
Create Date: 2024-03-03 14:31:30.888037

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "801b0dd65ef7"
down_revision: str | None = "8d370a31c5aa"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_column("users", "display_name")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "display_name", postgresql.CITEXT(), autoincrement=False, nullable=False
        ),
    )
