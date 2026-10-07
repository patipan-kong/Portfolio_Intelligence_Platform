"""add position intents (Investor Intent V1)

Revision ID: o7p8q9r0s1t2
Revises: n6o7p8q9r0s1
Create Date: 2026-10-07

Investor Intent V1: owner-authored, position-scoped hard restrictions and a
soft preference, plus append-only revision history. Additive only — no
backfill, and no conversion of portfolio_items.allow_swap.
"""
from alembic import op
import sqlalchemy as sa

revision = "o7p8q9r0s1t2"
down_revision = "n6o7p8q9r0s1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "position_intents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("portfolio_id", sa.Integer(), nullable=False),
        sa.Column("position_symbol", sa.String(), nullable=False),
        sa.Column("increase_prohibited", sa.Boolean(), nullable=False),
        sa.Column("decrease_prohibited", sa.Boolean(), nullable=False),
        sa.Column("soft_preference", sa.String(length=16), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("author_kind", sa.String(length=16), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["portfolio_id"], ["portfolios.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("portfolio_id", "position_symbol", name="uq_position_intents_portfolio_symbol"),
        sa.CheckConstraint(
            "soft_preference IN ('NONE', 'PREFER_KEEP', 'PREFER_EXIT')",
            name="ck_position_intents_soft_preference",
        ),
        sa.CheckConstraint("author_kind IN ('OWNER')", name="ck_position_intents_author_kind"),
        sa.CheckConstraint("revision >= 1", name="ck_position_intents_revision_positive"),
    )
    op.create_index("ix_position_intents_workspace_id", "position_intents", ["workspace_id"], unique=False)
    op.create_index("ix_position_intents_portfolio_id", "position_intents", ["portfolio_id"], unique=False)

    op.create_table(
        "position_intent_revisions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("position_intent_id", sa.Integer(), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("increase_prohibited", sa.Boolean(), nullable=False),
        sa.Column("decrease_prohibited", sa.Boolean(), nullable=False),
        sa.Column("soft_preference", sa.String(length=16), nullable=False),
        sa.Column("author_kind", sa.String(length=16), nullable=False),
        sa.Column("recorded_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["position_intent_id"], ["position_intents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "position_intent_id", "revision",
            name="uq_position_intent_revisions_intent_revision",
        ),
        sa.CheckConstraint(
            "soft_preference IN ('NONE', 'PREFER_KEEP', 'PREFER_EXIT')",
            name="ck_position_intent_revisions_soft_preference",
        ),
        sa.CheckConstraint("author_kind IN ('OWNER')", name="ck_position_intent_revisions_author_kind"),
        sa.CheckConstraint("revision >= 1", name="ck_position_intent_revisions_revision_positive"),
    )
    op.create_index(
        "ix_position_intent_revisions_workspace_id", "position_intent_revisions", ["workspace_id"], unique=False,
    )
    op.create_index(
        "ix_position_intent_revisions_position_intent_id", "position_intent_revisions",
        ["position_intent_id"], unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_position_intent_revisions_position_intent_id", table_name="position_intent_revisions")
    op.drop_index("ix_position_intent_revisions_workspace_id", table_name="position_intent_revisions")
    op.drop_table("position_intent_revisions")
    op.drop_index("ix_position_intents_portfolio_id", table_name="position_intents")
    op.drop_index("ix_position_intents_workspace_id", table_name="position_intents")
    op.drop_table("position_intents")
