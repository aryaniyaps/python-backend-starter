"""
create extensions

Revision ID: 7a23de63905c
Revises:
Create Date: 2024-02-10 17:35:25.715775

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7a23de63905c"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(sa.text("CREATE EXTENSION IF NOT EXISTS citext;"))


def downgrade() -> None:
    op.execute(sa.text("DROP EXTENSION IF EXISTS citext;"))
