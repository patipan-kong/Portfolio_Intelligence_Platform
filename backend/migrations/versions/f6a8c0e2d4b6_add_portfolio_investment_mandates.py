"""add portfolio investment mandates

Revision ID: f6a8c0e2d4b6
Revises: e5f7a9b1c3d6
Create Date: 2026-09-01
"""
from alembic import op
import sqlalchemy as sa


revision = "f6a8c0e2d4b6"
down_revision = "e5f7a9b1c3d6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "portfolio_investment_mandates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("portfolio_id", sa.Integer(), nullable=False),
        sa.Column("wealth_goal_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["portfolio_id"], ["portfolios.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["wealth_goal_id"], ["wealth_goals.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "portfolio_id",
            "wealth_goal_id",
            name="uq_portfolio_investment_mandates_portfolio_goal",
        ),
    )
    op.create_index(
        "ix_portfolio_investment_mandates_workspace_id",
        "portfolio_investment_mandates",
        ["workspace_id"],
        unique=False,
    )
    op.create_index(
        "ix_portfolio_investment_mandates_portfolio_id",
        "portfolio_investment_mandates",
        ["portfolio_id"],
        unique=False,
    )
    op.create_index(
        "ix_portfolio_investment_mandates_wealth_goal_id",
        "portfolio_investment_mandates",
        ["wealth_goal_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_portfolio_investment_mandates_wealth_goal_id",
        table_name="portfolio_investment_mandates",
    )
    op.drop_index(
        "ix_portfolio_investment_mandates_portfolio_id",
        table_name="portfolio_investment_mandates",
    )
    op.drop_index(
        "ix_portfolio_investment_mandates_workspace_id",
        table_name="portfolio_investment_mandates",
    )
    op.drop_table("portfolio_investment_mandates")
