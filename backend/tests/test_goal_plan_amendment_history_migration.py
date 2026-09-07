import importlib.util
from pathlib import Path

from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, text


BACKEND = Path(__file__).resolve().parents[1]
MIGRATION = BACKEND / "migrations" / "versions" / "f7a9c1e3b5d7_add_goal_plan_amendment_history.py"


def _load_migration():
    spec = importlib.util.spec_from_file_location("goal_plan_amendment_migration", MIGRATION)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_revision_descends_from_immediate_predecessor_and_is_sole_head():
    module = _load_migration()
    script = ScriptDirectory.from_config(Config(str(BACKEND / "alembic.ini")))
    assert module.down_revision == "e4f6a8b0c2d4"
    assert script.get_heads() == ["f7a9c1e3b5d7"]


def test_upgrade_from_predecessor_shape_is_empty_and_downgrade_removes_only_new_table():
    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE workspaces (id INTEGER PRIMARY KEY)"))
        connection.execute(text("CREATE TABLE wealth_goals (id INTEGER PRIMARY KEY, workspace_id INTEGER)"))
        connection.execute(text("INSERT INTO workspaces (id) VALUES (1)"))
        connection.execute(text("INSERT INTO wealth_goals (id, workspace_id) VALUES (1, 1)"))
        module = _load_migration()
        module.op = Operations(MigrationContext.configure(connection))
        module.upgrade()

        inspector = inspect(connection)
        assert "goal_plan_amendment_history" in inspector.get_table_names()
        columns = {column["name"] for column in inspector.get_columns("goal_plan_amendment_history")}
        assert columns == {
            "id", "workspace_id", "wealth_goal_id", "previous_target_amount", "resulting_target_amount",
            "previous_target_date", "resulting_target_date", "previous_priority", "resulting_priority", "recorded_at",
        }
        assert connection.execute(text("SELECT COUNT(*) FROM goal_plan_amendment_history")).scalar_one() == 0
        assert "ix_goal_plan_amendment_history_workspace_goal_recorded" in {
            index["name"] for index in inspector.get_indexes("goal_plan_amendment_history")
        }

        module.downgrade()
        assert "goal_plan_amendment_history" not in inspect(connection).get_table_names()
        assert connection.execute(text("SELECT COUNT(*) FROM wealth_goals")).scalar_one() == 1


def test_migration_contains_no_data_manipulation_or_backfill():
    source = MIGRATION.read_text(encoding="utf-8").lower()
    for forbidden in ("op.execute", "insert(", "update(", "delete(", "bulk_insert"):
        assert forbidden not in source
