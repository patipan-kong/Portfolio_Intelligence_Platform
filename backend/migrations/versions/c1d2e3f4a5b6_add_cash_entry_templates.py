"""add cash entry templates

User-triggered recurring cash-entry templates: workspace-owned convenience
metadata that prefills the existing Cash Flow Add Income / Add Expense form.
Not a financial fact, not a schedule — no date/frequency/recurrence column.

Revision ID: c1d2e3f4a5b6
Revises: b6d8f0a2c4e6
Create Date: 2026-09-03
"""
from alembic import op
import sqlalchemy as sa


revision = "c1d2e3f4a5b6"
down_revision = "b6d8f0a2c4e6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cash_entry_templates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("transaction_type", sa.String(length=16), nullable=False),
        sa.Column("cash_account_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("transaction_type IN ('INCOME', 'EXPENSE')", name="ck_cash_entry_templates_type"),
        sa.CheckConstraint("amount > 0", name="ck_cash_entry_templates_amount_positive"),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        # RESTRICT, not CASCADE: CashAccount rows are archived/restored, never
        # hard-deleted through the API, so this never fires today — but a
        # template referencing an account must not silently disappear if that
        # ever changes (see Cash Flow authority, docs/architecture/ROADMAP.md).
        sa.ForeignKeyConstraint(["cash_account_id"], ["cash_accounts.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_cash_entry_templates_workspace_id", "cash_entry_templates", ["workspace_id"], unique=False)
    op.create_index("ix_cash_entry_templates_cash_account_id", "cash_entry_templates", ["cash_account_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_cash_entry_templates_cash_account_id", table_name="cash_entry_templates")
    op.drop_index("ix_cash_entry_templates_workspace_id", table_name="cash_entry_templates")
    op.drop_table("cash_entry_templates")
