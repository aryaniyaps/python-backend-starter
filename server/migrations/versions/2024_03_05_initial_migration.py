"""
initial migration

Revision ID: fd20fb42ede5
Revises: 7a23de63905c
Create Date: 2024-03-05 12:43:29.009884

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "fd20fb42ede5"
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
        unique=True,
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
        "register_flows",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column(
            "current_step",
            sa.Enum(
                "EMAIL_VERIFICATION", "WEBAUTHN_REGISTRATION", name="registerflowstep"
            ),
            nullable=False,
        ),
        sa.Column("email", postgresql.CITEXT(length=250), nullable=False),
        sa.Column("verification_code_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "verification_code_expires_at", sa.DateTime(timezone=True), nullable=False
        ),
        sa.Column("ip_address", sa.String(length=40), nullable=False),
        sa.Column("user_agent", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("register_flows_pkey")),
    )
    op.create_index(
        op.f("register_flows_email_idx"), "register_flows", ["email"], unique=False
    )
    op.create_index(
        op.f("register_flows_verification_code_hash_idx"),
        "register_flows",
        ["verification_code_hash"],
        unique=True,
    )
    op.create_table(
        "users",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("email", postgresql.CITEXT(length=255), nullable=False),
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
    op.create_table(
        "user_sessions",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("ip_address", sa.String(length=40), nullable=False),
        sa.Column("location", sa.String(length=256), nullable=False),
        sa.Column("user_agent", sa.String(), nullable=False),
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
    op.create_table(
        "webauthn_credentials",
        sa.Column("id", sa.LargeBinary(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("public_key", sa.LargeBinary(), nullable=False),
        sa.Column("sign_count", sa.Integer(), nullable=False),
        sa.Column("device_type", sa.String(), nullable=False),
        sa.Column("backed_up", sa.Boolean(), nullable=False),
        sa.Column(
            "transports",
            postgresql.ARRAY(
                postgresql.ENUM(
                    "USB",
                    "NFC",
                    "BLE",
                    "INTERNAL",
                    "CABLE",
                    "HYBRID",
                    name="authenticatortransport",
                )
            ),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("webauthn_credentials_user_id_fkey")
        ),
        sa.PrimaryKeyConstraint(
            "id", "user_id", name=op.f("webauthn_credentials_pkey")
        ),
    )


def downgrade() -> None:
    op.drop_table("webauthn_credentials")
    op.drop_index(op.f("user_sessions_user_id_idx"), table_name="user_sessions")
    op.drop_table("user_sessions")
    op.drop_index(op.f("users_email_idx"), table_name="users")
    op.drop_table("users")
    op.drop_index(
        op.f("register_flows_verification_code_hash_idx"), table_name="register_flows"
    )
    op.drop_index(op.f("register_flows_email_idx"), table_name="register_flows")
    op.drop_table("register_flows")
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
