"""Investor Intent V1 migration: sole head, additive, no backfill, ORM parity."""
import importlib.util
from pathlib import Path

from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, text

BACKEND = Path(__file__).resolve().parents[1]
MIGRATION = BACKEND / "migrations" / "versions" / "o7p8q9r0s1t2_add_position_intents.py"
TABLES = ("position_intents", "position_intent_revisions")


def _load_migration():
    spec = importlib.util.spec_from_file_location("position_intent_migration", MIGRATION)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _schema(connection):
    inspector = inspect(connection)
    return {
        table: {
            "columns": {(c["name"], str(c["type"]), c["nullable"]) for c in inspector.get_columns(table)},
            "indexes": {(i["name"], tuple(i["column_names"]), bool(i["unique"])) for i in inspector.get_indexes(table)},
            "uniques": {(u["name"], tuple(u["column_names"])) for u in inspector.get_unique_constraints(table)},
        }
        for table in TABLES
    }


def test_descends_from_previous_sole_head_and_is_new_sole_head():
    module = _load_migration()
    script = ScriptDirectory.from_config(Config(str(BACKEND / "alembic.ini")))
    assert module.down_revision == "n6o7p8q9r0s1"
    assert script.get_heads() == ["o7p8q9r0s1t2"]


def test_upgrade_is_additive_without_backfill_and_downgrade_removes_only_new_tables():
    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE workspaces (id INTEGER PRIMARY KEY)"))
        connection.execute(text("CREATE TABLE portfolios (id INTEGER PRIMARY KEY, workspace_id INTEGER)"))
        connection.execute(text(
            "CREATE TABLE portfolio_items (id INTEGER PRIMARY KEY, portfolio_id INTEGER, "
            "symbol TEXT, allow_swap BOOLEAN)"))
        connection.execute(text("INSERT INTO workspaces (id) VALUES (1)"))
        connection.execute(text("INSERT INTO portfolios (id, workspace_id) VALUES (10, 1)"))
        connection.execute(text(
            "INSERT INTO portfolio_items (id, portfolio_id, symbol, allow_swap) VALUES (5, 10, 'PIS.BK', 0)"))

        module = _load_migration()
        module.op = Operations(MigrationContext.configure(connection))
        module.upgrade()

        for table in TABLES:
            assert connection.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one() == 0
        assert connection.execute(text("SELECT allow_swap FROM portfolio_items WHERE id = 5")).scalar_one() == 0

        module.downgrade()
        remaining = inspect(connection).get_table_names()
        assert not set(TABLES) & set(remaining)
        assert {"workspaces", "portfolios", "portfolio_items"} <= set(remaining)


def test_migration_schema_matches_orm_create_all():
    """ADR-017: ORM index=True must not create structure the migration lacks."""
    import models.asset  # noqa: F401
    import models.registry_finding  # noqa: F401
    from models.database import Base

    orm = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(orm, tables=[Base.metadata.tables[name] for name in
                                          ("workspaces", "portfolios", *TABLES)])
    migrated = create_engine("sqlite:///:memory:")
    with migrated.begin() as connection:
        connection.execute(text("CREATE TABLE workspaces (id INTEGER PRIMARY KEY)"))
        connection.execute(text("CREATE TABLE portfolios (id INTEGER PRIMARY KEY)"))
        module = _load_migration()
        module.op = Operations(MigrationContext.configure(connection))
        module.upgrade()
        migrated_schema = _schema(connection)
    with orm.connect() as connection:
        assert _schema(connection) == migrated_schema


def test_migration_contains_no_data_manipulation_or_allow_swap_conversion():
    import ast
    tree = ast.parse(MIGRATION.read_text(encoding="utf-8"))
    tree.body = tree.body[1:]  # drop the module docstring; check executable code only
    source = ast.unparse(tree).lower()
    for forbidden in ("op.execute", "insert(", "update(", "delete(", "bulk_insert", "portfolio_items"):
        assert forbidden not in source
