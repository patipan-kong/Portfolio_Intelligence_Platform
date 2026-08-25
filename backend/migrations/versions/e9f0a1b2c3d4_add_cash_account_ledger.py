"""add prospective CashAccount baseline and ledger

Revision ID: e9f0a1b2c3d4
Revises: d8e0f1a2b3c4
Create Date: 2026-08-25
"""
from alembic import op
import sqlalchemy as sa


revision = "e9f0a1b2c3d4"
down_revision = "d8e0f1a2b3c4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cash_account_baselines",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cash_account_id", sa.Integer(), nullable=False),
        sa.Column("effective_on", sa.String(length=10), nullable=False),
        sa.Column("observed_balance", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("observed_balance >= 0", name="ck_cash_account_baselines_balance_nonnegative"),
        sa.ForeignKeyConstraint(["cash_account_id"], ["cash_accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("cash_account_id"),
    )
    op.create_index("ix_cash_account_baselines_cash_account_id", "cash_account_baselines", ["cash_account_id"], unique=False)
    op.create_table(
        "cash_account_transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("cash_account_id", sa.Integer(), nullable=False),
        sa.Column("transaction_type", sa.String(length=16), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("occurred_on", sa.String(length=10), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("(transaction_type IN ('INCOME', 'EXPENSE') AND amount > 0) OR (transaction_type = 'ADJUSTMENT' AND amount <> 0)", name="ck_cash_account_transactions_type_amount"),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["cash_account_id"], ["cash_accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_cash_account_transactions_workspace_id", "cash_account_transactions", ["workspace_id"], unique=False)
    op.create_index("ix_cash_account_transactions_cash_account_id", "cash_account_transactions", ["cash_account_id"], unique=False)
    op.create_index("ix_cash_account_transactions_account_occurred", "cash_account_transactions", ["cash_account_id", "occurred_on"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_cash_account_transactions_account_occurred", table_name="cash_account_transactions")
    op.drop_index("ix_cash_account_transactions_cash_account_id", table_name="cash_account_transactions")
    op.drop_index("ix_cash_account_transactions_workspace_id", table_name="cash_account_transactions")
    op.drop_table("cash_account_transactions")
    op.drop_index("ix_cash_account_baselines_cash_account_id", table_name="cash_account_baselines")
    op.drop_table("cash_account_baselines")
