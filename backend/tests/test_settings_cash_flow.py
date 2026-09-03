"""Focused tests for the workspace-scoped /settings/cash-flow preference."""
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.database import Base, Settings, Workspace
import models.asset  # noqa: F401 — registers Asset tables referenced by ledger models.
import models.registry_finding  # noqa: F401 — registers registry tables referenced by Base metadata.
import main


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def get_settings(db):
    return asyncio.run(main.get_cash_flow_settings(db))


def update_settings(db, target_coverage_months):
    body = main.CashFlowSettingsBody(target_coverage_months=target_coverage_months)
    return asyncio.run(main.update_cash_flow_settings(body, db))


def test_missing_setting_returns_null_not_404():
    db = make_session()
    result = get_settings(db)
    assert result == {"target_coverage_months": None}


def test_patch_persists_and_get_reflects_it():
    db = make_session()
    saved = update_settings(db, 6)
    assert saved == {"target_coverage_months": 6.0}
    assert get_settings(db) == {"target_coverage_months": 6.0}


def test_patch_null_clears_the_target():
    db = make_session()
    update_settings(db, 6)
    cleared = update_settings(db, None)
    assert cleared == {"target_coverage_months": None}
    assert get_settings(db) == {"target_coverage_months": None}
    ws = main._ws_id(db)
    row = db.query(Settings).filter(
        Settings.workspace_id == ws,
        Settings.key == "cash_flow_target_coverage_months",
    ).first()
    assert row is None


def test_rejects_zero():
    with pytest.raises(ValidationError):
        main.CashFlowSettingsBody(target_coverage_months=0)


def test_rejects_negative():
    with pytest.raises(ValidationError):
        main.CashFlowSettingsBody(target_coverage_months=-3)


def test_rejects_non_finite_values():
    with pytest.raises(ValidationError):
        main.CashFlowSettingsBody(target_coverage_months=float("nan"))
    with pytest.raises(ValidationError):
        main.CashFlowSettingsBody(target_coverage_months=float("inf"))
    with pytest.raises(ValidationError):
        main.CashFlowSettingsBody(target_coverage_months=float("-inf"))


def test_rejects_non_numeric_string():
    with pytest.raises(ValidationError):
        main.CashFlowSettingsBody(target_coverage_months="six")


def test_workspace_isolation():
    db = make_session()
    from models.database import get_default_workspace

    ws_a = get_default_workspace(db)
    ws_b = Workspace(name="Second")
    db.add(ws_b)
    db.commit()
    db.refresh(ws_b)

    main._upsert_setting(db, ws_a.id, "cash_flow_target_coverage_months", "6.0")
    db.commit()

    assert main._get_cash_flow_settings(db, ws_a.id) == {"target_coverage_months": 6.0}
    assert main._get_cash_flow_settings(db, ws_b.id) == {"target_coverage_months": None}
