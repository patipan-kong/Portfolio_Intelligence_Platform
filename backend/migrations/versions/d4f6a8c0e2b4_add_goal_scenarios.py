"""add Named Scenario Foundation

Revision ID: d4f6a8c0e2b4
Revises: a2b4c6d8e0f2, c5d7e9f1a3b5
Create Date: 2026-08-26
"""
from alembic import op
import sqlalchemy as sa


revision = "d4f6a8c0e2b4"
down_revision = ("a2b4c6d8e0f2", "c5d7e9f1a3b5")
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "goal_scenarios",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("wealth_goal_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("monthly_contribution", sa.Float(), nullable=False),
        sa.Column("annual_return_pct", sa.Float(), nullable=False),
        sa.Column("is_archived", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("monthly_contribution >= 0", name="ck_goal_scenarios_contribution_nonnegative"),
        sa.CheckConstraint("annual_return_pct > -100", name="ck_goal_scenarios_return_above_negative_100"),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["wealth_goal_id"], ["wealth_goals.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_goal_scenarios_workspace_goal_archived",
        "goal_scenarios",
        ["workspace_id", "wealth_goal_id", "is_archived"],
        unique=False,
    )
    op.create_index("ix_goal_scenarios_workspace_id", "goal_scenarios", ["workspace_id"], unique=False)
    op.create_index("ix_goal_scenarios_wealth_goal_id", "goal_scenarios", ["wealth_goal_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_goal_scenarios_wealth_goal_id", table_name="goal_scenarios")
    op.drop_index("ix_goal_scenarios_workspace_id", table_name="goal_scenarios")
    op.drop_index("ix_goal_scenarios_workspace_goal_archived", table_name="goal_scenarios")
    op.drop_table("goal_scenarios")
