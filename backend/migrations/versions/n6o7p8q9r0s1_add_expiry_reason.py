"""add expiry_reason to user_execution_decisions

Revision ID: n6o7p8q9r0s1
Revises: h5i6j7k8l9m0
Create Date: 2026-09-10

Decision & Execution Lifecycle Completeness Slice 2: adds expiry_reason
("superseded" | "aged_out" | NULL) to user_execution_decisions.  Nullable,
additive, no backfill — existing EXPIRED rows remain NULL.
"""
from alembic import op
import sqlalchemy as sa

revision = "n6o7p8q9r0s1"
down_revision = "h5i6j7k8l9m0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("user_execution_decisions") as batch_op:
        batch_op.add_column(sa.Column("expiry_reason", sa.String(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("user_execution_decisions") as batch_op:
        batch_op.drop_column("expiry_reason")
