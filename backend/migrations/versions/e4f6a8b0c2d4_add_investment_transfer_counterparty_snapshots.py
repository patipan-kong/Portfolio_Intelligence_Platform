"""add documentary Investment Funding Transfer counterparty snapshots

Revision ID: e4f6a8b0c2d4
Revises: d2e4f6a8b0c2
Create Date: 2026-09-04
"""
from alembic import op
import sqlalchemy as sa


revision = "e4f6a8b0c2d4"
down_revision = "d2e4f6a8b0c2"
branch_labels = None
depends_on = None


_SNAPSHOT_PAIR_CHECK = (
    "(counterparty_portfolio_id_snapshot IS NULL AND counterparty_portfolio_name_snapshot IS NULL) "
    "OR (counterparty_portfolio_id_snapshot IS NOT NULL AND counterparty_portfolio_name_snapshot IS NOT NULL)"
)
_SNAPSHOT_TYPE_CHECK = (
    "(counterparty_portfolio_id_snapshot IS NULL AND counterparty_portfolio_name_snapshot IS NULL) "
    "OR transaction_type = 'INVESTMENT_TRANSFER'"
)


def upgrade() -> None:
    # Existing Investment Funding Transfer rows intentionally remain NULL: this
    # migration must not invent a historical counterparty identity. SQLite
    # needs a batch rewrite to add CHECK constraints.
    if op.get_bind().dialect.name == "sqlite":
        with op.batch_alter_table("cash_account_transactions", recreate="always") as batch_op:
            batch_op.add_column(sa.Column("counterparty_portfolio_id_snapshot", sa.Integer(), nullable=True))
            batch_op.add_column(sa.Column("counterparty_portfolio_name_snapshot", sa.String(), nullable=True))
            batch_op.create_check_constraint(
                "ck_cash_account_transactions_counterparty_snapshot_pair", _SNAPSHOT_PAIR_CHECK
            )
            batch_op.create_check_constraint(
                "ck_cash_account_transactions_counterparty_snapshot_type", _SNAPSHOT_TYPE_CHECK
            )
    else:
        op.add_column("cash_account_transactions", sa.Column("counterparty_portfolio_id_snapshot", sa.Integer(), nullable=True))
        op.add_column("cash_account_transactions", sa.Column("counterparty_portfolio_name_snapshot", sa.String(), nullable=True))
        op.create_check_constraint(
            "ck_cash_account_transactions_counterparty_snapshot_pair",
            "cash_account_transactions",
            _SNAPSHOT_PAIR_CHECK,
        )
        op.create_check_constraint(
            "ck_cash_account_transactions_counterparty_snapshot_type",
            "cash_account_transactions",
            _SNAPSHOT_TYPE_CHECK,
        )


def downgrade() -> None:
    if op.get_bind().dialect.name == "sqlite":
        with op.batch_alter_table("cash_account_transactions", recreate="always") as batch_op:
            batch_op.drop_constraint("ck_cash_account_transactions_counterparty_snapshot_type", type_="check")
            batch_op.drop_constraint("ck_cash_account_transactions_counterparty_snapshot_pair", type_="check")
            batch_op.drop_column("counterparty_portfolio_name_snapshot")
            batch_op.drop_column("counterparty_portfolio_id_snapshot")
    else:
        op.drop_constraint(
            "ck_cash_account_transactions_counterparty_snapshot_type",
            "cash_account_transactions",
            type_="check",
        )
        op.drop_constraint(
            "ck_cash_account_transactions_counterparty_snapshot_pair",
            "cash_account_transactions",
            type_="check",
        )
        op.drop_column("cash_account_transactions", "counterparty_portfolio_name_snapshot")
        op.drop_column("cash_account_transactions", "counterparty_portfolio_id_snapshot")
