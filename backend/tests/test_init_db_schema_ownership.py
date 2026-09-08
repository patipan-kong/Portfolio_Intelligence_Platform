"""ADR-017: PostgreSQL schema ownership boundary for init_db().

Covers the SQLite/PostgreSQL split in models.database.init_db():
SQLite keeps calling Base.metadata.create_all(); PostgreSQL performs a
read-only Alembic currentness check and never creates or alters schema.
"""
from __future__ import annotations

import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from sqlalchemy import create_engine, inspect as sa_inspect
from sqlalchemy.pool import StaticPool

import main  # noqa: F401  (registers all models, incl. assets, onto Base.metadata)
import models.database as dbmod
from models.database import Base, DatabaseSchemaNotCurrentError


def _fake_engine_with_connect():
    """A MagicMock engine whose .connect() works as a context manager."""
    fake_engine = MagicMock()
    fake_conn = MagicMock()
    fake_engine.connect.return_value.__enter__.return_value = fake_conn
    fake_engine.connect.return_value.__exit__.return_value = False
    return fake_engine


def _patched_alembic(db_heads, repo_heads):
    """Patch ScriptDirectory.get_heads() and MigrationContext.get_current_heads()
    to return the given revision tuples, without touching a real database."""
    script_patch = patch("alembic.script.ScriptDirectory.from_config")
    context_patch = patch("alembic.runtime.migration.MigrationContext.configure")
    return script_patch, context_patch, db_heads, repo_heads


class TestSqlitePath:
    def test_init_db_calls_create_all(self, monkeypatch):
        engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        monkeypatch.setattr(dbmod, "engine", engine)
        monkeypatch.setattr(dbmod, "_is_sqlite", True)

        dbmod.init_db()

        tables = sa_inspect(engine).get_table_names()
        assert "workspaces" in tables
        assert "portfolios" in tables

    def test_no_alembic_currentness_check_blocks_sqlite(self, monkeypatch):
        engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        monkeypatch.setattr(dbmod, "engine", engine)
        monkeypatch.setattr(dbmod, "_is_sqlite", True)

        with patch.object(dbmod, "_require_alembic_current") as require_current:
            dbmod.init_db()
            require_current.assert_not_called()


class TestPostgresPath:
    def test_current_heads_allows_startup_without_create_all(self, monkeypatch):
        monkeypatch.setattr(dbmod, "_is_sqlite", False)
        monkeypatch.setattr(dbmod, "engine", _fake_engine_with_connect())

        with patch("alembic.script.ScriptDirectory.from_config") as from_config, \
             patch("alembic.runtime.migration.MigrationContext.configure") as configure, \
             patch.object(Base.metadata, "create_all") as create_all:
            from_config.return_value.get_heads.return_value = ("h5i6j7k8l9m0",)
            configure.return_value.get_current_heads.return_value = ("h5i6j7k8l9m0",)

            dbmod.init_db()  # must not raise

            create_all.assert_not_called()

    def test_behind_database_raises_actionable_error(self, monkeypatch):
        monkeypatch.setattr(dbmod, "_is_sqlite", False)
        monkeypatch.setattr(dbmod, "engine", _fake_engine_with_connect())

        with patch("alembic.script.ScriptDirectory.from_config") as from_config, \
             patch("alembic.runtime.migration.MigrationContext.configure") as configure, \
             patch.object(Base.metadata, "create_all") as create_all:
            from_config.return_value.get_heads.return_value = ("h5i6j7k8l9m0",)
            configure.return_value.get_current_heads.return_value = ("g4h5i6j7k8l9",)

            with pytest.raises(DatabaseSchemaNotCurrentError) as exc_info:
                dbmod.init_db()

            message = str(exc_info.value)
            assert "g4h5i6j7k8l9" in message
            assert "h5i6j7k8l9m0" in message
            assert "alembic upgrade head" in message
            create_all.assert_not_called()

    def test_empty_unversioned_database_raises_without_create_all_fallback(self, monkeypatch):
        monkeypatch.setattr(dbmod, "_is_sqlite", False)
        monkeypatch.setattr(dbmod, "engine", _fake_engine_with_connect())

        with patch("alembic.script.ScriptDirectory.from_config") as from_config, \
             patch("alembic.runtime.migration.MigrationContext.configure") as configure, \
             patch.object(Base.metadata, "create_all") as create_all:
            from_config.return_value.get_heads.return_value = ("h5i6j7k8l9m0",)
            configure.return_value.get_current_heads.return_value = ()

            with pytest.raises(DatabaseSchemaNotCurrentError) as exc_info:
                dbmod.init_db()

            assert "none" in str(exc_info.value).lower()
            create_all.assert_not_called()

    def test_ahead_or_unknown_revision_raises(self, monkeypatch):
        monkeypatch.setattr(dbmod, "_is_sqlite", False)
        monkeypatch.setattr(dbmod, "engine", _fake_engine_with_connect())

        with patch("alembic.script.ScriptDirectory.from_config") as from_config, \
             patch("alembic.runtime.migration.MigrationContext.configure") as configure, \
             patch.object(Base.metadata, "create_all") as create_all:
            from_config.return_value.get_heads.return_value = ("h5i6j7k8l9m0",)
            configure.return_value.get_current_heads.return_value = ("z9z9z9z9z9z9",)

            with pytest.raises(DatabaseSchemaNotCurrentError):
                dbmod.init_db()

            create_all.assert_not_called()

    def test_multi_head_mismatch_raises(self, monkeypatch):
        monkeypatch.setattr(dbmod, "_is_sqlite", False)
        monkeypatch.setattr(dbmod, "engine", _fake_engine_with_connect())

        with patch("alembic.script.ScriptDirectory.from_config") as from_config, \
             patch("alembic.runtime.migration.MigrationContext.configure") as configure, \
             patch.object(Base.metadata, "create_all") as create_all:
            from_config.return_value.get_heads.return_value = ("h5i6j7k8l9m0", "other_head")
            configure.return_value.get_current_heads.return_value = ("h5i6j7k8l9m0",)

            with pytest.raises(DatabaseSchemaNotCurrentError):
                dbmod.init_db()

            create_all.assert_not_called()


class TestStructuralGuard:
    """Regression guard: create_all() must never fire on the PostgreSQL path,
    regardless of how init_db() is refactored in the future."""

    def test_create_all_never_called_when_not_sqlite(self, monkeypatch):
        monkeypatch.setattr(dbmod, "_is_sqlite", False)
        monkeypatch.setattr(dbmod, "engine", _fake_engine_with_connect())

        with patch("alembic.script.ScriptDirectory.from_config") as from_config, \
             patch("alembic.runtime.migration.MigrationContext.configure") as configure, \
             patch.object(Base.metadata, "create_all") as create_all:
            from_config.return_value.get_heads.return_value = ("h5i6j7k8l9m0",)
            configure.return_value.get_current_heads.return_value = ("h5i6j7k8l9m0",)
            dbmod.init_db()

            with pytest.raises(DatabaseSchemaNotCurrentError):
                configure.return_value.get_current_heads.return_value = ("behind",)
                dbmod.init_db()

            create_all.assert_not_called()
