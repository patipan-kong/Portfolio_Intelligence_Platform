"""add Goal Funding Allocation Foundation

Revision ID: a2b4c6d8e0f2
Revises: h4i5j6k7l8m9
Create Date: 2026-08-26
"""
from alembic import op
import sqlalchemy as sa


revision = "a2b4c6d8e0f2"
down_revision = "h4i5j6k7l8m9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "goal_funding_allocations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("wealth_goal_id", sa.Integer(), nullable=False),
        sa.Column("cash_account_id", sa.Integer(), nullable=True),
        sa.Column("portfolio_id", sa.Integer(), nullable=True),
        sa.Column("allocated_amount", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False, server_default="THB"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "(cash_account_id IS NOT NULL AND portfolio_id IS NULL) "
            "OR (cash_account_id IS NULL AND portfolio_id IS NOT NULL)",
            name="ck_goal_funding_allocations_exactly_one_source",
        ),
        sa.CheckConstraint("allocated_amount > 0", name="ck_goal_funding_allocations_amount_positive"),
        sa.CheckConstraint("currency = 'THB'", name="ck_goal_funding_allocations_currency_thb"),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["wealth_goal_id"], ["wealth_goals.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["cash_account_id"], ["cash_accounts.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["portfolio_id"], ["portfolios.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("wealth_goal_id", "cash_account_id", name="uq_goal_funding_allocations_goal_cash"),
        sa.UniqueConstraint("wealth_goal_id", "portfolio_id", name="uq_goal_funding_allocations_goal_portfolio"),
    )
    op.create_index(
        "ix_goal_funding_allocations_workspace_goal",
        "goal_funding_allocations",
        ["workspace_id", "wealth_goal_id"],
        unique=False,
    )
    op.create_index(
        "ix_goal_funding_allocations_workspace_id",
        "goal_funding_allocations",
        ["workspace_id"],
        unique=False,
    )
    op.create_index(
        "ix_goal_funding_allocations_wealth_goal_id",
        "goal_funding_allocations",
        ["wealth_goal_id"],
        unique=False,
    )
    op.create_index(
        "ix_goal_funding_allocations_cash_account_id",
        "goal_funding_allocations",
        ["cash_account_id"],
        unique=False,
    )
    op.create_index(
        "ix_goal_funding_allocations_portfolio_id",
        "goal_funding_allocations",
        ["portfolio_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_goal_funding_allocations_portfolio_id", table_name="goal_funding_allocations")
    op.drop_index("ix_goal_funding_allocations_cash_account_id", table_name="goal_funding_allocations")
    op.drop_index("ix_goal_funding_allocations_wealth_goal_id", table_name="goal_funding_allocations")
    op.drop_index("ix_goal_funding_allocations_workspace_id", table_name="goal_funding_allocations")
    op.drop_index("ix_goal_funding_allocations_workspace_goal", table_name="goal_funding_allocations")
    op.drop_table("goal_funding_allocations")
