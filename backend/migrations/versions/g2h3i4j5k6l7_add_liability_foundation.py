"""add Liability Foundation v1

Revision ID: g2h3i4j5k6l7
Revises: f1a2b3c4d5e6
Create Date: 2026-08-25
"""
from alembic import op
import sqlalchemy as sa


revision = "g2h3i4j5k6l7"
down_revision = "f1a2b3c4d5e6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "liabilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("liability_type", sa.String(length=32), nullable=False),
        sa.Column("lender", sa.String(), nullable=True),
        sa.Column("balance", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("currency", sa.String(length=3), nullable=False, server_default="THB"),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("is_archived", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "liability_type IN ('MORTGAGE', 'AUTO_LOAN', 'PERSONAL_LOAN', 'CREDIT_CARD', 'STUDENT_LOAN', 'OTHER')",
            name="ck_liabilities_type",
        ),
        sa.CheckConstraint("currency = 'THB'", name="ck_liabilities_currency_thb"),
        sa.CheckConstraint("balance >= 0", name="ck_liabilities_balance_nonnegative"),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_liabilities_workspace_archived",
        "liabilities",
        ["workspace_id", "is_archived"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_liabilities_workspace_archived", table_name="liabilities")
    op.drop_table("liabilities")
