"""Focused BANPU-WP1 schema and migration contract tests."""
from __future__ import annotations

import importlib
import sys
from datetime import datetime
from pathlib import Path

import pytest
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateIndex, CreateTable

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from models import database as database_models
from models.database import Transaction


MIGRATION_MODULE = "migrations.versions.b7d9f1a3c5e7_add_position_conversion_payload"
INDEX_NAME = "uq_tx_position_conversion_portfolio_predecessor_date"
CONSTRAINT_NAME = "ck_tx_position_conversion_identity_date"


def _transactions_table(metadata: sa.MetaData) -> sa.Table:
    return sa.Table(
        "transactions",
        metadata,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("portfolio_id", sa.Integer, nullable=False),
        sa.Column("asset_id", sa.Integer, nullable=True),
        # Nullable here so the focused test proves the conversion-specific
        # constraint rather than relying on the production column's broader
        # NOT NULL declaration.
        sa.Column("transaction_date", sa.DateTime, nullable=True),
        sa.Column("transaction_type", sa.String, nullable=False),
    )


@pytest.fixture
def migrated_connection():
    engine = sa.create_engine("sqlite:///:memory:")
    with engine.begin() as connection:
        transactions = _transactions_table(sa.MetaData())
        transactions.create(connection)
        connection.execute(
            transactions.insert().values(
                id=100,
                portfolio_id=1,
                asset_id=27,
                transaction_date=datetime(2025, 9, 1),
                transaction_type="BUY",
            )
        )
        migration = importlib.import_module(MIGRATION_MODULE)
        original_op = migration.op
        migration.op = Operations(MigrationContext.configure(connection))
        try:
            migration.upgrade()
            yield connection, migration
        finally:
            migration.op = original_op


def test_orm_uses_json_on_sqlite_and_jsonb_on_postgresql():
    column_type = Transaction.__table__.c.conversion_payload.type

    assert isinstance(column_type.dialect_impl(sqlite.dialect()), sa.JSON)
    assert isinstance(column_type.dialect_impl(postgresql.dialect()), postgresql.JSONB)


def test_orm_declares_conversion_only_partial_unique_index():
    index = next(index for index in Transaction.__table__.indexes if index.name == INDEX_NAME)

    assert index.unique
    assert [column.name for column in index.columns] == [
        "portfolio_id", "asset_id", "transaction_date"
    ]
    assert "POSITION_CONVERSION" in str(index.dialect_options["sqlite"]["where"])
    assert "POSITION_CONVERSION" in str(index.dialect_options["postgresql"]["where"])
    assert "WHERE transaction_type = 'POSITION_CONVERSION'" in str(
        CreateIndex(index).compile(dialect=sqlite.dialect())
    )
    assert "WHERE transaction_type = 'POSITION_CONVERSION'" in str(
        CreateIndex(index).compile(dialect=postgresql.dialect())
    )


def test_orm_declares_dialect_equivalent_conversion_constraints():
    create_table = CreateTable(
        Transaction.__table__,
        include_foreign_key_constraints=[],
    )
    sqlite_ddl = str(create_table.compile(dialect=sqlite.dialect()))
    postgres_ddl = str(
        create_table.compile(dialect=postgresql.dialect())
    )

    assert sqlite_ddl.count(f"CONSTRAINT {CONSTRAINT_NAME}") == 1
    assert "typeof(transaction_date) = 'text'" in sqlite_ddl
    assert "date_trunc" not in sqlite_ddl
    assert postgres_ddl.count(f"CONSTRAINT {CONSTRAINT_NAME}") == 1
    assert "transaction_date = date_trunc('day', transaction_date)" in postgres_ddl
    assert "typeof(transaction_date)" not in postgres_ddl


def test_migration_postgresql_path_selects_jsonb_and_partial_predicate():
    migration = importlib.import_module(MIGRATION_MODULE)

    class _Bind:
        dialect = postgresql.dialect()

    class _Batch:
        def __init__(self, fake_op):
            self.fake_op = fake_op

        def __enter__(self):
            return self

        def __exit__(self, *_):
            return False

        def add_column(self, column):
            self.fake_op.column = column

        def create_check_constraint(self, name, condition):
            self.fake_op.constraint = (name, condition)

    class _PostgresOp:
        column = None
        constraint = None
        index_kwargs = None

        def get_bind(self):
            return _Bind()

        def batch_alter_table(self, _):
            return _Batch(self)

        def create_index(self, *args, **kwargs):
            self.index_kwargs = (args, kwargs)

    fake_op = _PostgresOp()
    original_op = migration.op
    original_columns = migration._column_names
    original_indexes = migration._index_names
    original_constraints = migration._check_constraint_names
    migration.op = fake_op
    migration._column_names = lambda _: set()
    migration._index_names = lambda _: set()
    migration._check_constraint_names = lambda _: set()
    try:
        migration.upgrade()
    finally:
        migration.op = original_op
        migration._column_names = original_columns
        migration._index_names = original_indexes
        migration._check_constraint_names = original_constraints

    assert isinstance(fake_op.column.type, postgresql.JSONB)
    assert fake_op.constraint is not None
    constraint_name, constraint_sql = fake_op.constraint
    assert constraint_name == CONSTRAINT_NAME
    assert "date_trunc('day', transaction_date)" in str(constraint_sql)
    assert fake_op.index_kwargs is not None
    _, kwargs = fake_op.index_kwargs
    assert "POSITION_CONVERSION" in str(kwargs["postgresql_where"])


def test_upgrade_is_additive_null_and_repeatable(migrated_connection):
    connection, migration = migrated_connection
    columns = {column["name"]: column for column in sa.inspect(connection).get_columns("transactions")}

    assert columns["conversion_payload"]["nullable"]
    assert connection.execute(
        sa.text("SELECT conversion_payload FROM transactions WHERE id = 100")
    ).scalar_one() is None

    migration.upgrade()
    assert list({index["name"] for index in sa.inspect(connection).get_indexes("transactions")}).count(INDEX_NAME) == 1
    assert list(
        constraint["name"]
        for constraint in sa.inspect(connection).get_check_constraints("transactions")
    ).count(CONSTRAINT_NAME) == 1


def test_legacy_sqlite_compatibility_adds_wp1_schema_idempotently(monkeypatch):
    engine = sa.create_engine("sqlite:///:memory:")
    database_models.Workspace.__table__.create(engine)
    database_models.Portfolio.__table__.create(engine)
    legacy_transactions = _transactions_table(sa.MetaData())
    legacy_transactions.append_column(sa.Column("workspace_id", sa.Integer, nullable=False))
    legacy_transactions.create(engine)

    with engine.begin() as connection:
        connection.execute(
            database_models.Workspace.__table__.insert().values(id=1, name="Default")
        )
        connection.execute(
            database_models.Portfolio.__table__.insert().values(
                id=1, workspace_id=1, name="Main"
            )
        )
        connection.execute(
            legacy_transactions.insert().values(
                id=100,
                workspace_id=1,
                portfolio_id=1,
                asset_id=27,
                transaction_date=datetime(2025, 9, 1),
                transaction_type="BUY",
            )
        )

    monkeypatch.setattr(database_models, "engine", engine)
    monkeypatch.setattr(database_models, "SessionLocal", sessionmaker(bind=engine))
    monkeypatch.setattr(database_models, "_is_sqlite", True)

    database_models.migrate_legacy_data()
    database_models.migrate_legacy_data()

    inspector = sa.inspect(engine)
    assert "conversion_payload" in {
        column["name"] for column in inspector.get_columns("transactions")
    }
    assert INDEX_NAME in {
        index["name"] for index in inspector.get_indexes("transactions")
    }
    with engine.connect() as connection:
        assert connection.execute(
            sa.text("SELECT conversion_payload FROM transactions WHERE id = 100")
        ).scalar_one() is None
        triggers = {
            name
            for name in connection.execute(
                sa.text(
                    "SELECT name FROM sqlite_master "
                    "WHERE type = 'trigger' AND name LIKE :prefix"
                ),
                {"prefix": f"{CONSTRAINT_NAME}_%"},
            ).scalars()
        }
        assert triggers == {
            f"{CONSTRAINT_NAME}_insert",
            f"{CONSTRAINT_NAME}_update",
        }

        with pytest.raises(IntegrityError, match=CONSTRAINT_NAME):
            connection.execute(
                sa.text(
                    "INSERT INTO transactions "
                    "(id, workspace_id, portfolio_id, asset_id, transaction_date, transaction_type) "
                    "VALUES (101, 1, 1, 27, '2025-10-01 09:30:00', 'POSITION_CONVERSION')"
                )
            )
        connection.execute(
            sa.text(
                "INSERT INTO transactions "
                "(id, workspace_id, portfolio_id, asset_id, transaction_date, transaction_type) "
                "VALUES (102, 1, 1, NULL, '2025-10-01 09:30:00', 'BUY')"
            )
        )
        with pytest.raises(IntegrityError, match=CONSTRAINT_NAME):
            connection.execute(
                sa.text(
                    "UPDATE transactions SET transaction_type = 'POSITION_CONVERSION' "
                    "WHERE id = 102"
                )
            )


def test_partial_index_rejects_duplicate_conversion_only(migrated_connection):
    connection, _ = migrated_connection
    insert = sa.text(
        "INSERT INTO transactions "
        "(id, portfolio_id, asset_id, transaction_date, transaction_type) "
        "VALUES (:id, 2, 27, '2025-10-01 00:00:00', :type)"
    )
    connection.execute(insert, {"id": 1, "type": "BUY"})
    connection.execute(insert, {"id": 2, "type": "BUY"})
    connection.execute(insert, {"id": 3, "type": "POSITION_CONVERSION"})

    with pytest.raises(IntegrityError):
        connection.execute(insert, {"id": 4, "type": "POSITION_CONVERSION"})


@pytest.mark.parametrize(
    ("asset_id", "transaction_date"),
    [
        (None, "2025-10-01 00:00:00"),
        (27, None),
        (27, "2025-10-01 09:30:00"),
        (27, "2025-10-01T00:00:00"),
        (27, "2025-10-01 00:00:00+07:00"),
        (27, "2025-09-30 17:00:00Z"),
    ],
)
def test_conversion_insert_rejects_missing_or_noncanonical_identity_date(
    migrated_connection,
    asset_id,
    transaction_date,
):
    connection, _ = migrated_connection

    with pytest.raises(IntegrityError, match=CONSTRAINT_NAME):
        connection.execute(
            sa.text(
                "INSERT INTO transactions "
                "(id, portfolio_id, asset_id, transaction_date, transaction_type) "
                "VALUES (1, 2, :asset_id, :transaction_date, 'POSITION_CONVERSION')"
            ),
            {"asset_id": asset_id, "transaction_date": transaction_date},
        )


@pytest.mark.parametrize(
    ("assignment", "parameters"),
    [
        ("asset_id = NULL", {}),
        ("transaction_date = NULL", {}),
        ("transaction_date = :value", {"value": "2025-10-01 09:30:00"}),
        ("transaction_date = :value", {"value": "2025-10-01 00:00:00+07:00"}),
    ],
)
def test_conversion_update_rejects_missing_or_noncanonical_identity_date(
    migrated_connection,
    assignment,
    parameters,
):
    connection, _ = migrated_connection
    connection.execute(
        sa.text(
            "INSERT INTO transactions "
            "(id, portfolio_id, asset_id, transaction_date, transaction_type) "
            "VALUES (1, 2, 27, '2025-10-01 00:00:00', 'POSITION_CONVERSION')"
        )
    )

    with pytest.raises(IntegrityError, match=CONSTRAINT_NAME):
        connection.execute(
            sa.text(f"UPDATE transactions SET {assignment} WHERE id = 1"),
            parameters,
        )


def test_same_date_different_time_cannot_bypass_conversion_identity(
    migrated_connection,
):
    connection, _ = migrated_connection
    connection.execute(
        sa.text(
            "INSERT INTO transactions "
            "(id, portfolio_id, asset_id, transaction_date, transaction_type) "
            "VALUES (1, 2, 27, '2025-10-01 00:00:00', 'POSITION_CONVERSION')"
        )
    )

    with pytest.raises(IntegrityError, match=CONSTRAINT_NAME):
        connection.execute(
            sa.text(
                "INSERT INTO transactions "
                "(id, portfolio_id, asset_id, transaction_date, transaction_type) "
                "VALUES (2, 2, 27, '2025-10-01 09:30:00', 'POSITION_CONVERSION')"
            )
        )


def test_non_conversion_rows_keep_null_asset_and_intraday_timestamp(
    migrated_connection,
):
    connection, _ = migrated_connection
    connection.execute(
        sa.text(
            "INSERT INTO transactions "
            "(id, portfolio_id, asset_id, transaction_date, transaction_type) "
            "VALUES (1, 2, NULL, '2025-10-01 09:30:00', 'DEPOSIT')"
        )
    )
    connection.execute(
        sa.text(
            "UPDATE transactions SET transaction_date = '2025-10-01 14:45:00' "
            "WHERE id = 1"
        )
    )

    assert connection.execute(
        sa.text(
            "SELECT asset_id, transaction_date FROM transactions WHERE id = 1"
        )
    ).one() == (None, "2025-10-01 14:45:00")


def test_downgrade_refuses_while_conversion_rows_exist(migrated_connection):
    connection, migration = migrated_connection
    connection.execute(
        sa.text(
            "INSERT INTO transactions "
            "(id, portfolio_id, asset_id, transaction_date, transaction_type) "
            "VALUES (1, 2, 27, '2025-10-01 00:00:00', 'POSITION_CONVERSION')"
        )
    )

    with pytest.raises(RuntimeError, match="Refusing to remove"):
        migration.downgrade()

    assert "conversion_payload" in {
        column["name"] for column in sa.inspect(connection).get_columns("transactions")
    }


def test_empty_downgrade_removes_wp1_schema_and_is_repeatable(migrated_connection):
    connection, migration = migrated_connection

    migration.downgrade()
    migration.downgrade()

    inspector = sa.inspect(connection)
    assert "conversion_payload" not in {column["name"] for column in inspector.get_columns("transactions")}
    assert INDEX_NAME not in {index["name"] for index in inspector.get_indexes("transactions")}
    assert CONSTRAINT_NAME not in {
        constraint["name"]
        for constraint in inspector.get_check_constraints("transactions")
    }
