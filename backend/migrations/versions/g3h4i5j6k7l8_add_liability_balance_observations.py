"""add Liability Balance Observations (Phase 5)

Revision ID: g3h4i5j6k7l8
Revises: g2h3i4j5k6l7
Create Date: 2026-08-25
"""
from alembic import op
import sqlalchemy as sa


revision = "g3h4i5j6k7l8"
down_revision = "g2h3i4j5k6l7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "liability_balance_observations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("liability_id", sa.Integer(), nullable=False),
        sa.Column("balance", sa.Float(), nullable=False),
        sa.Column("observed_on", sa.String(length=10), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("balance >= 0", name="ck_liability_balance_observations_balance_nonnegative"),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["liability_id"], ["liabilities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("liability_id", "observed_on", name="uq_liability_balance_observations_liability_date"),
    )
    op.create_index(
        "ix_liability_balance_observations_workspace_id",
        "liability_balance_observations",
        ["workspace_id"],
        unique=False,
    )
    op.create_index(
        "ix_liability_balance_observations_liability_id",
        "liability_balance_observations",
        ["liability_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_liability_balance_observations_liability_id", table_name="liability_balance_observations")
    op.drop_index("ix_liability_balance_observations_workspace_id", table_name="liability_balance_observations")
    op.drop_table("liability_balance_observations")
