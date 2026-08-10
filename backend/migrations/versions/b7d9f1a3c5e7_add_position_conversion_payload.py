"""add POSITION_CONVERSION payload and duplicate-prevention index

Revision ID: b7d9f1a3c5e7
Revises: f8a0c2e4b6d8
Create Date: 2026-08-06

BANPU-WP1 adds one nullable structured payload, a conversion-specific
identity/date constraint, and a partial unique index over the canonical
conversion identity. The migration is inert for existing non-conversion rows
and is safe to invoke repeatedly. Downgrade is deliberately guarded:
append-only conversion facts must never be made unreadable.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "b7d9f1a3c5e7"
down_revision = "f8a0c2e4b6d8"
branch_labels = None
depends_on = None

_INDEX_NAME = "uq_tx_position_conversion_portfolio_predecessor_date"
_CONSTRAINT_NAME = "ck_tx_position_conversion_identity_date"
_POSTGRESQL_CONSTRAINT = (
    "transaction_type <> 'POSITION_CONVERSION' OR "
    "(asset_id IS NOT NULL AND transaction_date IS NOT NULL AND "
    "transaction_date = date_trunc('day', transaction_date))"
)
_SQLITE_CONSTRAINT = """
transaction_type <> 'POSITION_CONVERSION' OR (
    asset_id IS NOT NULL
    AND transaction_date IS NOT NULL
    AND typeof(transaction_date) = 'text'
    AND (
        transaction_date GLOB
            '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] 00:00:00'
        OR transaction_date GLOB
            '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] 00:00:00.000000'
    )
    AND date(transaction_date) = substr(transaction_date, 1, 10)
)
""".strip()


def _column_names(bind) -> set[str]:
    return {column["name"] for column in sa.inspect(bind).get_columns("transactions")}


def _index_names(bind) -> set[str]:
    return {index["name"] for index in sa.inspect(bind).get_indexes("transactions")}


def _check_constraint_names(bind) -> set[str]:
    return {
        constraint["name"]
        for constraint in sa.inspect(bind).get_check_constraints("transactions")
        if constraint["name"] is not None
    }


def upgrade() -> None:
    bind = op.get_bind()
    missing_payload = "conversion_payload" not in _column_names(bind)
    missing_constraint = _CONSTRAINT_NAME not in _check_constraint_names(bind)
    if missing_payload or missing_constraint:
        with op.batch_alter_table("transactions") as batch_op:
            if missing_payload:
                payload_type = (
                    postgresql.JSONB()
                    if bind.dialect.name == "postgresql"
                    else sa.JSON()
                )
                batch_op.add_column(
                    sa.Column("conversion_payload", payload_type, nullable=True)
                )
            if missing_constraint:
                constraint_sql = (
                    _POSTGRESQL_CONSTRAINT
                    if bind.dialect.name == "postgresql"
                    else _SQLITE_CONSTRAINT
                )
                batch_op.create_check_constraint(
                    _CONSTRAINT_NAME,
                    sa.text(constraint_sql),
                )

    if _INDEX_NAME not in _index_names(bind):
        predicate = sa.text("transaction_type = 'POSITION_CONVERSION'")
        op.create_index(
            _INDEX_NAME,
            "transactions",
            ["portfolio_id", "asset_id", "transaction_date"],
            unique=True,
            sqlite_where=predicate,
            postgresql_where=predicate,
        )


def downgrade() -> None:
    bind = op.get_bind()
    if "conversion_payload" not in _column_names(bind):
        return

    conversion_count = bind.execute(
        sa.text(
            "SELECT COUNT(*) FROM transactions "
            "WHERE transaction_type = 'POSITION_CONVERSION'"
        )
    ).scalar_one()
    if conversion_count:
        raise RuntimeError(
            "Refusing to remove transactions.conversion_payload while "
            "POSITION_CONVERSION rows exist"
        )

    if _INDEX_NAME in _index_names(bind):
        op.drop_index(_INDEX_NAME, table_name="transactions")
    with op.batch_alter_table("transactions") as batch_op:
        if _CONSTRAINT_NAME in _check_constraint_names(bind):
            batch_op.drop_constraint(_CONSTRAINT_NAME, type_="check")
        batch_op.drop_column("conversion_payload")
