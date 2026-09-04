"""add goal plan amendment history

Revision ID: f7a9c1e3b5d7
Revises: e4f6a8b0c2d4
Create Date: 2026-09-04
"""
from alembic import op
import sqlalchemy as sa


revision = "f7a9c1e3b5d7"
down_revision = "e4f6a8b0c2d4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "goal_plan_amendment_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("wealth_goal_id", sa.Integer(), nullable=False),
        sa.Column("previous_target_amount", sa.Float(), nullable=False),
        sa.Column("resulting_target_amount", sa.Float(), nullable=False),
        sa.Column("previous_target_date", sa.String(), nullable=True),
        sa.Column("resulting_target_date", sa.String(), nullable=True),
        sa.Column("previous_priority", sa.String(length=16), nullable=False),
        sa.Column("resulting_priority", sa.String(length=16), nullable=False),
        sa.Column("recorded_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("previous_target_amount > 0", name="ck_goal_plan_amendment_history_previous_amount_positive"),
        sa.CheckConstraint("resulting_target_amount > 0", name="ck_goal_plan_amendment_history_resulting_amount_positive"),
        sa.CheckConstraint("previous_priority IN ('HIGH', 'MEDIUM', 'LOW')", name="ck_goal_plan_amendment_history_previous_priority"),
        sa.CheckConstraint("resulting_priority IN ('HIGH', 'MEDIUM', 'LOW')", name="ck_goal_plan_amendment_history_resulting_priority"),
        sa.CheckConstraint(
            "previous_target_amount <> resulting_target_amount "
            "OR (previous_target_date IS NULL AND resulting_target_date IS NOT NULL) "
            "OR (previous_target_date IS NOT NULL AND resulting_target_date IS NULL) "
            "OR previous_target_date <> resulting_target_date "
            "OR previous_priority <> resulting_priority",
            name="ck_goal_plan_amendment_history_material_change",
        ),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["wealth_goal_id"], ["wealth_goals.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_goal_plan_amendment_history_workspace_id", "goal_plan_amendment_history", ["workspace_id"], unique=False)
    op.create_index("ix_goal_plan_amendment_history_wealth_goal_id", "goal_plan_amendment_history", ["wealth_goal_id"], unique=False)
    op.create_index(
        "ix_goal_plan_amendment_history_workspace_goal_recorded",
        "goal_plan_amendment_history",
        ["workspace_id", "wealth_goal_id", "recorded_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_goal_plan_amendment_history_workspace_goal_recorded", table_name="goal_plan_amendment_history")
    op.drop_index("ix_goal_plan_amendment_history_wealth_goal_id", table_name="goal_plan_amendment_history")
    op.drop_index("ix_goal_plan_amendment_history_workspace_id", table_name="goal_plan_amendment_history")
    op.drop_table("goal_plan_amendment_history")
