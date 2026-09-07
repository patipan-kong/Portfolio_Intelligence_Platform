"""add wealth_goal_context_json to recommendation_snapshots

Revision ID: e5f7a9b1c3d6
Revises: d4f6a8c0e2b4
Create Date: 2026-08-31

Phase 7.4 (Decision Intelligence Context Admission, ADR-008): adds a single
nullable wealth_goal_context_json column to recommendation_snapshots — the
sole persistence location for the frozen, context-only
wealth.decision-goal-context.v1 envelope captured for an explicitly selected
set of Wealth Goals. NULL means no capture was attempted. OptimizerHistory is
unchanged; no other schema is touched.
"""
from alembic import op
import sqlalchemy as sa

revision = "e5f7a9b1c3d6"
down_revision = "d4f6a8c0e2b4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("recommendation_snapshots") as batch_op:
        batch_op.add_column(
            sa.Column("wealth_goal_context_json", sa.Text(), nullable=True)
        )


def downgrade() -> None:
    with op.batch_alter_table("recommendation_snapshots") as batch_op:
        batch_op.drop_column("wealth_goal_context_json")
