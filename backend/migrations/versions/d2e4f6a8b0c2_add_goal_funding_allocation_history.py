"""add goal funding allocation designation history

Revision ID: d2e4f6a8b0c2
Revises: c1d2e3f4a5b6
Create Date: 2026-09-04
"""
from alembic import op
import sqlalchemy as sa


revision = "d2e4f6a8b0c2"
down_revision = "c1d2e3f4a5b6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "goal_funding_allocation_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("wealth_goal_id", sa.Integer(), nullable=False),
        sa.Column("source_kind", sa.String(length=16), nullable=False),
        # Deliberately scalar snapshots: normal Portfolio deletion must not
        # delete history, and later source renames must not rewrite evidence.
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("source_name", sa.String(), nullable=False),
        sa.Column("action", sa.String(length=16), nullable=False),
        sa.Column("previous_designated_amount", sa.Float(), nullable=True),
        sa.Column("resulting_designated_amount", sa.Float(), nullable=True),
        sa.Column("currency", sa.String(length=3), nullable=False, server_default="THB"),
        sa.Column("recorded_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("source_kind IN ('CASH_ACCOUNT', 'PORTFOLIO')", name="ck_goal_funding_allocation_history_source_kind"),
        sa.CheckConstraint("action IN ('CREATE', 'UPDATE', 'REMOVE')", name="ck_goal_funding_allocation_history_action"),
        sa.CheckConstraint("currency = 'THB'", name="ck_goal_funding_allocation_history_currency_thb"),
        sa.CheckConstraint(
            "(action = 'CREATE' AND previous_designated_amount IS NULL AND resulting_designated_amount > 0) "
            "OR (action = 'UPDATE' AND previous_designated_amount > 0 AND resulting_designated_amount > 0 "
            "AND previous_designated_amount <> resulting_designated_amount) "
            "OR (action = 'REMOVE' AND previous_designated_amount > 0 AND resulting_designated_amount IS NULL)",
            name="ck_goal_funding_allocation_history_transition",
        ),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["wealth_goal_id"], ["wealth_goals.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_goal_funding_allocation_history_workspace_id", "goal_funding_allocation_history", ["workspace_id"], unique=False)
    op.create_index("ix_goal_funding_allocation_history_wealth_goal_id", "goal_funding_allocation_history", ["wealth_goal_id"], unique=False)
    op.create_index(
        "ix_goal_funding_allocation_history_workspace_goal_recorded",
        "goal_funding_allocation_history",
        ["workspace_id", "wealth_goal_id", "recorded_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_goal_funding_allocation_history_workspace_goal_recorded", table_name="goal_funding_allocation_history")
    op.drop_index("ix_goal_funding_allocation_history_wealth_goal_id", table_name="goal_funding_allocation_history")
    op.drop_index("ix_goal_funding_allocation_history_workspace_id", table_name="goal_funding_allocation_history")
    op.drop_table("goal_funding_allocation_history")
