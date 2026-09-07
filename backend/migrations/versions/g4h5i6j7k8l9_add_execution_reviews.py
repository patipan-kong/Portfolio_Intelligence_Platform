"""add execution reviews

Revision ID: g4h5i6j7k8l9
Revises: f7a9c1e3b5d7
Create Date: 2026-09-07
"""
from alembic import op
import sqlalchemy as sa


revision = "g4h5i6j7k8l9"
down_revision = "f7a9c1e3b5d7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "execution_reviews",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("execution_decision_id", sa.Integer(), nullable=False),
        sa.Column("reviewed_at", sa.DateTime(), nullable=False),
        sa.Column("outcome", sa.String(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("changed_context", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("outcome IN ('ON_TRACK', 'MIXED', 'OFF_TRACK')", name="ck_execution_reviews_outcome"),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["execution_decision_id"], ["user_execution_decisions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("execution_decision_id", name="uq_execution_reviews_decision"),
    )
    op.create_index("ix_execution_reviews_workspace_id", "execution_reviews", ["workspace_id"], unique=False)
    op.create_index("ix_execution_reviews_execution_decision_id", "execution_reviews", ["execution_decision_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_execution_reviews_execution_decision_id", table_name="execution_reviews")
    op.drop_index("ix_execution_reviews_workspace_id", table_name="execution_reviews")
    op.drop_table("execution_reviews")
