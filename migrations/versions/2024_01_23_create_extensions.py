"""
create extensions

Revision ID: e404ef6a54b5
Revises:
Create Date: 2024-01-23 09:42:17.516135

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e404ef6a54b5"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(sa.text("CREATE EXTENSION IF NOT EXISTS citext;"))


def downgrade() -> None:
    op.execute(sa.text("DROP EXTENSION IF EXISTS citext;"))
