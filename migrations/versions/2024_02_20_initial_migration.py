"""
initial migration

Revision ID: f3ca079c5282
Revises: 7a23de63905c
Create Date: 2024-02-20 18:53:21.257289

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "f3ca079c5282"
down_revision: str | None = "7a23de63905c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "email_verification_codes",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("email", postgresql.CITEXT(length=250), nullable=False),
        sa.Column("code_hash", sa.String(length=255), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("email_verification_codes_pkey")),
    )
    op.create_index(
        op.f("email_verification_codes_code_hash_idx"),
        "email_verification_codes",
        ["code_hash"],
        unique=False,
    )
    op.create_index(
        "email_verification_codes_email_code_hash_idx",
        "email_verification_codes",
        ["email", "code_hash"],
        unique=False,
    )
    op.create_index(
        op.f("email_verification_codes_email_idx"),
        "email_verification_codes",
        ["email"],
        unique=False,
    )
    op.create_table(
        "user_emails",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("email_address", postgresql.CITEXT(length=250), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("user_emails_user_id_fkey")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("user_emails_pkey")),
        sa.UniqueConstraint("user_id", name=op.f("user_emails_user_id_key")),
    )
    op.create_table(
        "users",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("username", postgresql.CITEXT(length=32), nullable=False),
        sa.Column("primary_email_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["primary_email_id"],
            ["user_emails.id"],
            name=op.f("users_primary_email_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("users_pkey")),
    )
    op.create_index(
        op.f("users_primary_email_id_idx"), "users", ["primary_email_id"], unique=False
    )
    op.create_index(op.f("users_username_idx"), "users", ["username"], unique=True)
    op.create_table(
        "auth_providers",
        sa.Column(
            "provider",
            sa.Enum("facebook", "google", "email_password", name="authprovidertype"),
            nullable=False,
        ),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("auth_providers_user_id_fkey")
        ),
        sa.PrimaryKeyConstraint(
            "provider", "user_id", name=op.f("auth_providers_pkey")
        ),
    )
    op.create_table(
        "password_reset_codes",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("code_hash", sa.String(length=128), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("password_reset_codes_user_id_fkey")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("password_reset_codes_pkey")),
    )
    op.create_index(
        op.f("password_reset_codes_code_hash_idx"),
        "password_reset_codes",
        ["code_hash"],
        unique=True,
    )
    op.create_table(
        "user_passwords",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("hash", sa.String(length=128), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("user_passwords_user_id_fkey")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("user_passwords_pkey")),
        sa.UniqueConstraint("user_id", name=op.f("user_passwords_user_id_key")),
    )
    op.create_table(
        "user_sessions",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("ip_address", sa.String(length=40), nullable=False),
        sa.Column("location", sa.String(length=256), nullable=False),
        sa.Column("device", sa.String(length=256), nullable=False),
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


def downgrade() -> None:
    op.drop_index(op.f("user_sessions_user_id_idx"), table_name="user_sessions")
    op.drop_table("user_sessions")
    op.drop_table("user_passwords")
    op.drop_index(
        op.f("password_reset_codes_code_hash_idx"), table_name="password_reset_codes"
    )
    op.drop_table("password_reset_codes")
    op.drop_table("auth_providers")
    op.drop_index(op.f("users_username_idx"), table_name="users")
    op.drop_index(op.f("users_primary_email_id_idx"), table_name="users")
    op.drop_table("users")
    op.drop_table("user_emails")
    op.drop_index(
        op.f("email_verification_codes_email_idx"),
        table_name="email_verification_codes",
    )
    op.drop_index(
        "email_verification_codes_email_code_hash_idx",
        table_name="email_verification_codes",
    )
    op.drop_index(
        op.f("email_verification_codes_code_hash_idx"),
        table_name="email_verification_codes",
    )
    op.drop_table("email_verification_codes")
