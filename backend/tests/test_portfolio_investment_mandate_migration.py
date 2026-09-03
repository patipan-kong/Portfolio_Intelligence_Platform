import importlib.util
from pathlib import Path

from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, text


BACKEND = Path(__file__).resolve().parents[1]
MIGRATION = BACKEND / "migrations" / "versions" / "f6a8c0e2d4b6_add_portfolio_investment_mandates.py"


def _load_migration():
    spec = importlib.util.spec_from_file_location("mandate_migration", MIGRATION)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_revision_descends_from_sole_predecessor_and_repository_has_one_head():
    module = _load_migration()
    script = ScriptDirectory.from_config(Config(str(BACKEND / "alembic.ini")))
    assert module.down_revision == "e5f7a9b1c3d6"
    # The repository's sole head has since advanced to b6d8f0a2c4e6
    # (Investment Funding Transfer / ADR-012), chained directly onto this
    # migration; this test's original intent — "the repository has exactly
    # one head" — is preserved by asserting that current head instead.
    assert script.get_heads() == ["b6d8f0a2c4e6"]


def test_upgrade_is_empty_no_backfill_and_downgrade_removes_only_new_structure():
    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE workspaces (id INTEGER PRIMARY KEY)"))
        connection.execute(text("CREATE TABLE portfolios (id INTEGER PRIMARY KEY, workspace_id INTEGER, goal_type TEXT, goal_target_value FLOAT)"))
        connection.execute(text("CREATE TABLE wealth_goals (id INTEGER PRIMARY KEY, workspace_id INTEGER)"))
        connection.execute(text("CREATE TABLE goal_funding_allocations (id INTEGER PRIMARY KEY, workspace_id INTEGER, wealth_goal_id INTEGER, portfolio_id INTEGER, allocated_amount FLOAT)"))
        connection.execute(text("INSERT INTO workspaces (id) VALUES (1)"))
        connection.execute(text("INSERT INTO portfolios (id, workspace_id, goal_type, goal_target_value) VALUES (10, 1, 'RETIREMENT', 1000000)"))
        connection.execute(text("INSERT INTO wealth_goals (id, workspace_id) VALUES (20, 1)"))
        connection.execute(text("INSERT INTO goal_funding_allocations (id, workspace_id, wealth_goal_id, portfolio_id, allocated_amount) VALUES (30, 1, 20, 10, 500000)"))

        module = _load_migration()
        module.op = Operations(MigrationContext.configure(connection))
        module.upgrade()

        inspector = inspect(connection)
        assert "portfolio_investment_mandates" in inspector.get_table_names()
        columns = {column["name"] for column in inspector.get_columns("portfolio_investment_mandates")}
        assert columns == {"id", "workspace_id", "portfolio_id", "wealth_goal_id", "created_at"}
        assert connection.execute(text("SELECT COUNT(*) FROM portfolio_investment_mandates")).scalar_one() == 0
        assert connection.execute(text("SELECT COUNT(*) FROM goal_funding_allocations")).scalar_one() == 1

        module.downgrade()
        remaining = inspect(connection).get_table_names()
        assert "portfolio_investment_mandates" not in remaining
        assert {"workspaces", "portfolios", "wealth_goals", "goal_funding_allocations"}.issubset(remaining)
        assert connection.execute(text("SELECT goal_target_value FROM portfolios WHERE id = 10")).scalar_one() == 1000000


def test_migration_contains_no_data_manipulation_or_backfill():
    source = MIGRATION.read_text(encoding="utf-8").lower()
    for forbidden in ("op.execute", "insert(", "update(", "delete(", "bulk_insert"):
        assert forbidden not in source
