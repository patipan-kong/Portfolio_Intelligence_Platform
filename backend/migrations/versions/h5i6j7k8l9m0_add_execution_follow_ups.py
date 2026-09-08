"""add execution follow-up acknowledgment metadata

Revision ID: h5i6j7k8l9m0
Revises: g4h5i6j7k8l9
Create Date: 2026-09-08

Product Intelligence Slice 2: one current-state follow-up acknowledgment row
per execution decision.  The row is deliberately separate from the canonical
retrospective ExecutionReview and contains no history or task fields.
"""
from alembic import op
import sqlalchemy as sa


revision = "h5i6j7k8l9m0"
down_revision = "g4h5i6j7k8l9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "execution_follow_ups",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("execution_decision_id", sa.Integer(), nullable=False),
        sa.Column("acknowledged_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["execution_decision_id"], ["user_execution_decisions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("execution_decision_id", name="uq_execution_follow_ups_decision"),
    )
    op.create_index(
        "ix_execution_follow_ups_workspace_id",
        "execution_follow_ups",
        ["workspace_id"],
        unique=False,
    )
    op.create_index(
        "ix_execution_follow_ups_execution_decision_id",
        "execution_follow_ups",
        ["execution_decision_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_execution_follow_ups_execution_decision_id",
        table_name="execution_follow_ups",
    )
    op.drop_index(
        "ix_execution_follow_ups_workspace_id",
        table_name="execution_follow_ups",
    )
    op.drop_table("execution_follow_ups")
