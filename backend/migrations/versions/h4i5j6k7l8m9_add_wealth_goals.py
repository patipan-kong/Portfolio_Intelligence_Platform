"""add Wealth Goals Foundation v1

Revision ID: h4i5j6k7l8m9
Revises: g3h4i5j6k7l8
Create Date: 2026-08-26
"""
from alembic import op
import sqlalchemy as sa


revision = "h4i5j6k7l8m9"
down_revision = "g3h4i5j6k7l8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "wealth_goals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("goal_type", sa.String(length=32), nullable=False),
        sa.Column("target_amount", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False, server_default="THB"),
        sa.Column("target_date", sa.String(), nullable=True),
        sa.Column("priority", sa.String(length=16), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("is_archived", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "goal_type IN ('RETIREMENT', 'HOUSE', 'WEDDING', 'EDUCATION', 'VACATION', 'EMERGENCY_FUND', 'FIRE', 'OTHER')",
            name="ck_wealth_goals_type",
        ),
        sa.CheckConstraint("priority IN ('HIGH', 'MEDIUM', 'LOW')", name="ck_wealth_goals_priority"),
        sa.CheckConstraint("currency = 'THB'", name="ck_wealth_goals_currency_thb"),
        sa.CheckConstraint("target_amount > 0", name="ck_wealth_goals_target_amount_positive"),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_wealth_goals_workspace_archived",
        "wealth_goals",
        ["workspace_id", "is_archived"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_wealth_goals_workspace_archived", table_name="wealth_goals")
    op.drop_table("wealth_goals")
