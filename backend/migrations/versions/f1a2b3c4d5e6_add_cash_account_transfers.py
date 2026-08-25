"""add logical CashAccount transfers and linked ledger legs

Revision ID: f1a2b3c4d5e6
Revises: e9f0a1b2c3d4
Create Date: 2026-08-25
"""
from alembic import op
import sqlalchemy as sa


revision = "f1a2b3c4d5e6"
down_revision = "e9f0a1b2c3d4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cash_account_transfers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("source_cash_account_id", sa.Integer(), nullable=False),
        sa.Column("destination_cash_account_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("occurred_on", sa.String(length=10), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "source_cash_account_id <> destination_cash_account_id",
            name="ck_cash_account_transfers_distinct_accounts",
        ),
        sa.CheckConstraint("amount > 0", name="ck_cash_account_transfers_amount_positive"),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_cash_account_id"], ["cash_accounts.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["destination_cash_account_id"], ["cash_accounts.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_cash_account_transfers_workspace_occurred",
        "cash_account_transfers",
        ["workspace_id", "occurred_on"],
        unique=False,
    )
    op.create_index(
        "ix_cash_account_transfers_workspace_id",
        "cash_account_transfers",
        ["workspace_id"],
        unique=False,
    )
    op.create_index(
        "ix_cash_account_transfers_source_cash_account_id",
        "cash_account_transfers",
        ["source_cash_account_id"],
        unique=False,
    )
    op.create_index(
        "ix_cash_account_transfers_destination_cash_account_id",
        "cash_account_transfers",
        ["destination_cash_account_id"],
        unique=False,
    )

    # SQLite needs a batch rewrite for the nullable category and new FK. Keep
    # PostgreSQL additive so this migration never rewrites the ledger table.
    if op.get_bind().dialect.name == "sqlite":
        with op.batch_alter_table("cash_account_transactions", recreate="always") as batch_op:
            batch_op.drop_constraint("ck_cash_account_transactions_type_amount", type_="check")
            batch_op.create_check_constraint(
                "ck_cash_account_transactions_type_amount",
                "(transaction_type IN ('INCOME', 'EXPENSE') AND amount > 0) "
                "OR (transaction_type IN ('ADJUSTMENT', 'TRANSFER') AND amount <> 0)",
            )
            batch_op.alter_column("category", existing_type=sa.String(), nullable=True)
            batch_op.add_column(sa.Column("transfer_id", sa.Integer(), nullable=True))
            batch_op.create_index("ix_cash_account_transactions_transfer_id", ["transfer_id"], unique=False)
            batch_op.create_foreign_key(
                "fk_cash_account_transactions_transfer_id",
                "cash_account_transfers",
                ["transfer_id"],
                ["id"],
                ondelete="SET NULL",
            )
    else:
        op.drop_constraint("ck_cash_account_transactions_type_amount", "cash_account_transactions", type_="check")
        op.create_check_constraint(
            "ck_cash_account_transactions_type_amount",
            "cash_account_transactions",
            "(transaction_type IN ('INCOME', 'EXPENSE') AND amount > 0) "
            "OR (transaction_type IN ('ADJUSTMENT', 'TRANSFER') AND amount <> 0)",
        )
        op.alter_column("cash_account_transactions", "category", existing_type=sa.String(), nullable=True)
        op.add_column("cash_account_transactions", sa.Column("transfer_id", sa.Integer(), nullable=True))
        op.create_index("ix_cash_account_transactions_transfer_id", "cash_account_transactions", ["transfer_id"], unique=False)
        op.create_foreign_key(
            "fk_cash_account_transactions_transfer_id",
            "cash_account_transactions",
            "cash_account_transfers",
            ["transfer_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    if op.get_bind().dialect.name == "sqlite":
        with op.batch_alter_table("cash_account_transactions", recreate="always") as batch_op:
            batch_op.drop_constraint("ck_cash_account_transactions_type_amount", type_="check")
            batch_op.create_check_constraint(
                "ck_cash_account_transactions_type_amount",
                "(transaction_type IN ('INCOME', 'EXPENSE') AND amount > 0) "
                "OR (transaction_type = 'ADJUSTMENT' AND amount <> 0)",
            )
            batch_op.drop_constraint("fk_cash_account_transactions_transfer_id", type_="foreignkey")
            batch_op.drop_index("ix_cash_account_transactions_transfer_id")
            batch_op.drop_column("transfer_id")
            batch_op.alter_column("category", existing_type=sa.String(), nullable=False)
    else:
        op.drop_constraint("fk_cash_account_transactions_transfer_id", "cash_account_transactions", type_="foreignkey")
        op.drop_index("ix_cash_account_transactions_transfer_id", table_name="cash_account_transactions")
        op.drop_column("cash_account_transactions", "transfer_id")
        op.alter_column("cash_account_transactions", "category", existing_type=sa.String(), nullable=False)
        op.drop_constraint("ck_cash_account_transactions_type_amount", "cash_account_transactions", type_="check")
        op.create_check_constraint(
            "ck_cash_account_transactions_type_amount",
            "cash_account_transactions",
            "(transaction_type IN ('INCOME', 'EXPENSE') AND amount > 0) "
            "OR (transaction_type = 'ADJUSTMENT' AND amount <> 0)",
        )
    op.drop_index("ix_cash_account_transfers_destination_cash_account_id", table_name="cash_account_transfers")
    op.drop_index("ix_cash_account_transfers_source_cash_account_id", table_name="cash_account_transfers")
    op.drop_index("ix_cash_account_transfers_workspace_id", table_name="cash_account_transfers")
    op.drop_index("ix_cash_account_transfers_workspace_occurred", table_name="cash_account_transfers")
    op.drop_table("cash_account_transfers")
