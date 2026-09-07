"""add standalone cash accounts

Revision ID: d8e0f1a2b3c4
Revises: b7d9f1a3c5e7
Create Date: 2026-08-25
"""
from alembic import op
import sqlalchemy as sa


revision = "d8e0f1a2b3c4"
down_revision = "b7d9f1a3c5e7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cash_accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("institution", sa.String(), nullable=True),
        sa.Column("currency", sa.String(length=3), nullable=False, server_default="THB"),
        sa.Column("balance", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("is_archived", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("currency = 'THB'", name="ck_cash_accounts_currency_thb"),
        sa.CheckConstraint("balance >= 0", name="ck_cash_accounts_balance_nonnegative"),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_cash_accounts_workspace_archived",
        "cash_accounts",
        ["workspace_id", "is_archived"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_cash_accounts_workspace_archived", table_name="cash_accounts")
    op.drop_table("cash_accounts")
