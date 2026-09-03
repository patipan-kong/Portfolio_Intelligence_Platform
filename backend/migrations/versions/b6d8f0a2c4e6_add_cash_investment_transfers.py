"""add cash-side Investment Funding Transfer (ADR-012)

Also widens cash_account_transactions.transaction_type from VARCHAR(16) to
VARCHAR(32) — the prior width could not hold 'INVESTMENT_TRANSFER' (19
chars) on PostgreSQL, which enforces declared VARCHAR length (IFT-001).

Revision ID: b6d8f0a2c4e6
Revises: f6a8c0e2d4b6
Create Date: 2026-09-03
"""
from alembic import op
import sqlalchemy as sa


revision = "b6d8f0a2c4e6"
down_revision = "f6a8c0e2d4b6"
branch_labels = None
depends_on = None


_WIDENED_TYPE_AMOUNT_CHECK = (
    "(transaction_type IN ('INCOME', 'EXPENSE') AND amount > 0) "
    "OR (transaction_type IN ('ADJUSTMENT', 'TRANSFER', 'INVESTMENT_TRANSFER') AND amount <> 0)"
)
_PRIOR_TYPE_AMOUNT_CHECK = (
    "(transaction_type IN ('INCOME', 'EXPENSE') AND amount > 0) "
    "OR (transaction_type IN ('ADJUSTMENT', 'TRANSFER') AND amount <> 0)"
)
_COUNTERPARTY_TYPE_CHECK = "counterparty_portfolio_id IS NULL OR transaction_type = 'INVESTMENT_TRANSFER'"
_TRANSFER_LEG_TYPE_CHECK = "transfer_id IS NULL OR transaction_type = 'TRANSFER'"


def upgrade() -> None:
    # SQLite needs a batch rewrite for the new column, index, FK, and CHECK
    # constraints. Keep PostgreSQL additive, matching the f1a2b3c4d5e6
    # precedent for the same table.
    if op.get_bind().dialect.name == "sqlite":
        with op.batch_alter_table("cash_account_transactions", recreate="always") as batch_op:
            batch_op.drop_constraint("ck_cash_account_transactions_type_amount", type_="check")
            batch_op.alter_column(
                "transaction_type",
                existing_type=sa.String(16),
                type_=sa.String(32),
                existing_nullable=False,
            )
            batch_op.create_check_constraint("ck_cash_account_transactions_type_amount", _WIDENED_TYPE_AMOUNT_CHECK)
            batch_op.add_column(sa.Column("counterparty_portfolio_id", sa.Integer(), nullable=True))
            batch_op.create_index(
                "ix_cash_account_transactions_counterparty_portfolio_id",
                ["counterparty_portfolio_id"],
                unique=False,
            )
            batch_op.create_foreign_key(
                "fk_cash_account_transactions_counterparty_portfolio_id",
                "portfolios",
                ["counterparty_portfolio_id"],
                ["id"],
                ondelete="SET NULL",
            )
            batch_op.create_check_constraint(
                "ck_cash_account_transactions_counterparty_type", _COUNTERPARTY_TYPE_CHECK
            )
            batch_op.create_check_constraint(
                "ck_cash_account_transactions_transfer_leg_type", _TRANSFER_LEG_TYPE_CHECK
            )
    else:
        op.drop_constraint("ck_cash_account_transactions_type_amount", "cash_account_transactions", type_="check")
        op.alter_column(
            "cash_account_transactions",
            "transaction_type",
            existing_type=sa.String(16),
            type_=sa.String(32),
            existing_nullable=False,
        )
        op.create_check_constraint(
            "ck_cash_account_transactions_type_amount", "cash_account_transactions", _WIDENED_TYPE_AMOUNT_CHECK
        )
        op.add_column("cash_account_transactions", sa.Column("counterparty_portfolio_id", sa.Integer(), nullable=True))
        op.create_index(
            "ix_cash_account_transactions_counterparty_portfolio_id",
            "cash_account_transactions",
            ["counterparty_portfolio_id"],
            unique=False,
        )
        op.create_foreign_key(
            "fk_cash_account_transactions_counterparty_portfolio_id",
            "cash_account_transactions",
            "portfolios",
            ["counterparty_portfolio_id"],
            ["id"],
            ondelete="SET NULL",
        )
        op.create_check_constraint(
            "ck_cash_account_transactions_counterparty_type",
            "cash_account_transactions",
            _COUNTERPARTY_TYPE_CHECK,
        )
        op.create_check_constraint(
            "ck_cash_account_transactions_transfer_leg_type",
            "cash_account_transactions",
            _TRANSFER_LEG_TYPE_CHECK,
        )


def downgrade() -> None:
    if op.get_bind().dialect.name == "sqlite":
        with op.batch_alter_table("cash_account_transactions", recreate="always") as batch_op:
            batch_op.drop_constraint("ck_cash_account_transactions_transfer_leg_type", type_="check")
            batch_op.drop_constraint("ck_cash_account_transactions_counterparty_type", type_="check")
            batch_op.drop_constraint("fk_cash_account_transactions_counterparty_portfolio_id", type_="foreignkey")
            batch_op.drop_index("ix_cash_account_transactions_counterparty_portfolio_id")
            batch_op.drop_column("counterparty_portfolio_id")
            batch_op.drop_constraint("ck_cash_account_transactions_type_amount", type_="check")
            # Narrowing is safe here: any surviving INVESTMENT_TRANSFER-typed
            # row (19 chars) already fails _PRIOR_TYPE_AMOUNT_CHECK below
            # regardless of column width, so this downgrade already assumes
            # (and requires) the feature's rows are gone before it runs.
            batch_op.alter_column(
                "transaction_type",
                existing_type=sa.String(32),
                type_=sa.String(16),
                existing_nullable=False,
            )
            batch_op.create_check_constraint("ck_cash_account_transactions_type_amount", _PRIOR_TYPE_AMOUNT_CHECK)
    else:
        op.drop_constraint(
            "ck_cash_account_transactions_transfer_leg_type", "cash_account_transactions", type_="check"
        )
        op.drop_constraint(
            "ck_cash_account_transactions_counterparty_type", "cash_account_transactions", type_="check"
        )
        op.drop_constraint(
            "fk_cash_account_transactions_counterparty_portfolio_id", "cash_account_transactions", type_="foreignkey"
        )
        op.drop_index("ix_cash_account_transactions_counterparty_portfolio_id", table_name="cash_account_transactions")
        op.drop_column("cash_account_transactions", "counterparty_portfolio_id")
        op.drop_constraint("ck_cash_account_transactions_type_amount", "cash_account_transactions", type_="check")
        # Narrowing is safe here: any surviving INVESTMENT_TRANSFER-typed row
        # (19 chars) already fails _PRIOR_TYPE_AMOUNT_CHECK below regardless
        # of column width, so this downgrade already assumes (and requires)
        # the feature's rows are gone before it runs. On PostgreSQL, if a
        # value still exceeds 16 chars at this point, ALTER COLUMN TYPE
        # raises rather than silently truncating.
        op.alter_column(
            "cash_account_transactions",
            "transaction_type",
            existing_type=sa.String(32),
            type_=sa.String(16),
            existing_nullable=False,
        )
        op.create_check_constraint(
            "ck_cash_account_transactions_type_amount", "cash_account_transactions", _PRIOR_TYPE_AMOUNT_CHECK
        )
