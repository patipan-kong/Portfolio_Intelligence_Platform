"""Focused offline authority, missingness and mathematical correctness tests."""
import ast
import sys
from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from services.candidate_discovery import (
    DiscoveryInput, Evidence, Holding, Instrument, PortfolioOverlayInput,
    discover, portfolio_overlay,
)
from services.candidate_discovery_evidence import (
    BACKEND, FA_SOURCE, LEGACY_SOURCE, TIMING_SOURCE, adapt_capture, compare_capture,
    source_digest,
)


def evidence(value, **kwargs):
    return Evidence(value, value is not None, "captured producer", scoring_version="fixture.v1", **kwargs)


def instrument(symbol, fa=3, timing=60, **kwargs):
    return Instrument(symbol, evidence(fa), evidence(timing), asset_type="EQUITY",
                      identity_source="captured listing", **kwargs)


def snapshot(*items):
    return DiscoveryInput("test-universe", "2026-10-07T00:00:00+00:00",
                          "2026-10-07T00:00:00+00:00", tuple(items))


def rows(result):
    return {r["instrument"]["symbol"]: r for r in result["candidates"]}


def capture():
    import pandas as pd
    index = pd.to_datetime([datetime(2025, 1, 1, tzinfo=timezone.utc) + timedelta(days=i)
                            for i in range(250)], utc=True)
    frame = pd.DataFrame({"Close": [100 + i * .1 for i in range(250)],
                          "Volume": [1000] * 250}, index=index)
    payload = {"json_split": frame.to_json(orient="split", date_format="iso")}
    now = "2026-10-07T00:00:00+00:00"
    return {"capture_version": "wealth.shadow-capture.v1", "universe_id": "fixture",
        "as_of": now, "captured_at": now,
        "source_digests": {"fundamental": source_digest(FA_SOURCE),
            "timing": source_digest(TIMING_SOURCE), "legacy": source_digest(LEGACY_SOURCE)},
        "watchlist": [{"id": 1, "symbol": "A", "asset_id": None, "sector": "Tech",
                       "timing_fetch_symbol": "A"}],
        "agent_cache": [{"symbol": "A", "agent": "fundamental", "cached_at": now,
            "result_json": {"fa_score": 3, "pe_ratio": 15, "roe": .1,
                            "revenue_growth": .05, "debt_equity": 80}},
            {"symbol": "A", "agent": "technical", "cached_at": now, "result_json": {"ta_score": 2}}],
        "market_cache": [{"symbol": s, "cache_type": typ, "payload_json": payload,
                          "fetched_at": now, "expires_at": now}
            for s, typ in (("A", "history:1y:1d"), ("SPY", "history:3mo:1d"))],
        "analysis_cache": [{"symbol": "A", "signal": "ACCUMULATE"}],
        "assets": [], "relationships": [], "portfolios": [], "holdings": []}


def test_determinism_and_order_invariance():
    value = snapshot(instrument("A", 5, 80), instrument("B", 2, 50), instrument("C", 4, 90))
    assert discover(value) == discover(value)
    assert discover(value) == discover(replace(value, instruments=tuple(reversed(value.instruments))))


@pytest.mark.parametrize("dimension", ["fundamental", "timing"])
def test_missing_is_not_neutral(dimension):
    item = replace(instrument("A"), **{dimension: evidence(None)})
    result = discover(snapshot(item, instrument("B")))
    assert rows(result)["A"]["relative"] is None
    assert f"missing_{dimension}_evidence" in rows(result)["A"]["ranking_eligibility"]["reasons"]
    assert result["coverage"]["ranking_eligible"] == 1
    assert rows(result)["B"]["relative"]["fundamental"]["midrank_percentile"] == 50


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), True])
def test_invalid_numeric_observations_excluded(bad):
    assert discover(snapshot(instrument("A", bad)))["coverage"]["ranking_eligible"] == 0


def test_percentile_order_ties_and_competition_rank():
    result = rows(discover(snapshot(instrument("A", 1), instrument("B", 3), instrument("C", 3))))
    assert result["A"]["relative"]["fundamental"]["midrank_percentile"] == pytest.approx(16.666667)
    assert result["B"]["relative"]["fundamental"]["midrank_percentile"] == pytest.approx(66.666667)
    assert result["B"]["relative"]["fundamental"]["ties"] == ["B", "C"]
    assert result["A"]["relative"]["fundamental"]["rank_best_first"] == 3


def test_pareto_fronts_dominance_incomparability_and_ties():
    result = discover(snapshot(instrument("A", 5, 80), instrument("B", 4, 90),
        instrument("C", 5, 80), instrument("D", 3, 70), instrument("E", 2, 60)))
    assert result["pareto_fronts"] == [["A", "B", "C"], ["D"], ["E"]]
    assert result["experimental_shortlist"]["symbols"] == ["A", "B", "C"]
    assert rows(result)["A"]["relative"]["joint_ties"] == ["C"]
    assert rows(result)["D"]["relative"]["dominated_by"] == ["A", "B", "C"]
    assert "B" not in rows(result)["A"]["relative"]["dominates"]


def test_empty_and_singleton():
    assert discover(snapshot())["pareto_fronts"] == []
    assert discover(snapshot())["coverage"]["ranking_coverage_fraction"] is None
    assert rows(discover(snapshot(instrument("A"))))["A"]["relative"]["timing"]["midrank_percentile"] == 50


def test_large_tied_front_is_uncapped():
    result = discover(snapshot(*(instrument(str(i)) for i in range(20))))
    assert result["front_sizes"] == [20]
    assert len(result["experimental_shortlist"]["symbols"]) == 20
    assert result["experimental_shortlist"]["cap"] is None


def test_research_ranking_and_consideration_are_distinct():
    item = instrument("A", timing=None)
    result = rows(discover(snapshot(item)))["A"]
    assert result["research_eligibility"]["eligible"]
    assert not result["ranking_eligibility"]["eligible"]
    overlay = portfolio_overlay(snapshot(item), PortfolioOverlayInput("p", "now", ()))
    assert overlay["candidates"][0]["portfolio_add_consideration"]["status"] == "constrained"


def test_unsupported_asset_and_missing_identity():
    item = replace(instrument("A"), asset_type="BOND", identity_source=None)
    reason = rows(discover(snapshot(item)))["A"]["ranking_eligibility"]["reasons"]
    assert "unsupported_asset_type" in reason and "missing_identity" in reason


def test_versions_and_duplicate_listing_rejected():
    with pytest.raises(ValueError):
        discover(replace(snapshot(), contract_version="future"))
    with pytest.raises(ValueError):
        discover(snapshot(instrument("A"), instrument("A")))


def test_overlay_never_changes_rank_and_applies_existing_lock():
    value = snapshot(instrument("A", 5, 90))
    before = discover(value)
    context = PortfolioOverlayInput("p", "now", (Holding("A", allow_swap=False),))
    overlay = portfolio_overlay(value, context)
    assert discover(value) == before
    assert overlay["candidates"][0]["portfolio_add_consideration"]["reasons"] == ["existing_position_locked"]
    assert before["experimental_shortlist"]["symbols"] == ["A"]


def test_unknown_policy_does_not_mean_unblocked():
    overlay = portfolio_overlay(snapshot(instrument("A")), PortfolioOverlayInput("p", "now", ()))
    assert overlay["candidates"][0]["portfolio_add_consideration"]["status"] == "unknown"


def test_supplied_current_policy_overlay():
    item = instrument("A", sector="Tech", asset_id=1)
    context = PortfolioOverlayInput("p", "now", (Holding("A", asset_id=1, weight_pct=20),),
        sector_weights=(("Tech", 40),), sector_caps=(("Tech", 40),),
        position_cap=20, constraints_current=True)
    reasons = portfolio_overlay(snapshot(item), context)["candidates"][0]["portfolio_add_consideration"]["reasons"]
    assert reasons == ["position_cap_reached", "sector_cap_reached"]


def test_adapter_complete_evidence_and_no_production_imports():
    value, _ = adapt_capture(capture())
    assert discover(value)["coverage"]["ranking_eligible"] == 1
    assert value.instruments[0].timing.value is not None
    assert "services.data_fetcher" not in sys.modules
    assert "models.database" not in sys.modules


@pytest.mark.parametrize("signal", ["BUY", "ACCUMULATE", "WATCH", "HOLD", "REDUCE", "SELL"])
def test_stock_analysis_independence(signal):
    frozen = capture()
    baseline = compare_capture(frozen)["standalone"]
    frozen["analysis_cache"][0]["signal"] = signal
    assert compare_capture(frozen)["standalone"] == baseline


def test_adapter_all_missing_fa_preserves_raw_zero_without_ranking():
    frozen = capture()
    frozen["agent_cache"][0]["result_json"] = {"fa_score": 0}
    value, _ = adapt_capture(frozen)
    assert value.instruments[0].fundamental.value == 0
    assert not value.instruments[0].fundamental.available
    assert discover(value)["coverage"]["ranking_eligible"] == 0


def test_adapter_missing_history_and_benchmark_not_neutral():
    frozen = capture()
    frozen["market_cache"] = []
    value, _ = adapt_capture(frozen)
    assert value.instruments[0].timing.value is None
    assert not value.instruments[0].timing.available
    assert discover(value)["coverage"]["ranking_eligible"] == 0


def test_adapter_partial_timing_defaults_are_visible_but_excluded():
    frozen = capture()
    frozen["market_cache"] = [r for r in frozen["market_cache"] if r["symbol"] != "SPY"]
    value, _ = adapt_capture(frozen)
    assert value.instruments[0].timing.value is not None
    assert not value.instruments[0].timing.available
    assert "benchmark_return_20d" in value.instruments[0].timing.missing_inputs


def test_cache_expiry_is_limitation_without_invented_threshold():
    frozen = capture()
    for row in frozen["market_cache"]:
        row["expires_at"] = "2025-01-01T00:00:00+00:00"
    value, _ = adapt_capture(frozen)
    assert "cache_expired_snapshot_diagnostic_only" in value.instruments[0].timing.limitations
    assert discover(value)["coverage"]["ranking_eligible"] == 1


def test_canonical_relationship_only_and_provider_parent_not_identity():
    frozen = capture()
    frozen["watchlist"][0]["asset_id"] = 10
    frozen["assets"] = [{"id": 10, "asset_type": "EQUITY", "tradable": True}]
    frozen["relationships"] = [{"from_asset_id": 10, "to_asset_id": 20,
        "relationship_type": "DEPOSITARY_RECEIPT_OF", "effective_date": None}]
    frozen["portfolios"] = [{"id": 1}]
    frozen["holdings"] = [{"portfolio_id": 1, "symbol": "PARENT", "asset_id": 20,
                           "allow_swap": True}]
    value, contexts = adapt_capture(frozen)
    assert value.instruments[0].related_asset_ids == (20,)
    assert portfolio_overlay(value, contexts[0])["candidates"][0]["related_exposure"][0]["asset_id"] == 20
    frozen["relationships"] = []
    frozen["agent_cache"][0]["result_json"]["parent_symbol"] = "PARENT"
    value, contexts = adapt_capture(frozen)
    assert not value.instruments[0].related_asset_ids
    assert not portfolio_overlay(value, contexts[0])["candidates"][0]["related_exposure"]


def test_capture_source_version_mismatch_rejected():
    frozen = capture()
    frozen["source_digests"]["timing"] = "old"
    with pytest.raises(ValueError, match="source changed"):
        adapt_capture(frozen)


def test_capture_dependency_drift_rejected():
    frozen = capture()
    frozen["runtime_versions"] = {"pandas": "impossible-version"}
    with pytest.raises(ValueError, match="dependency changed"):
        adapt_capture(frozen)


@pytest.mark.parametrize("query_fails", [False, True])
def test_current_capture_connection_is_read_only_and_always_rolled_back(monkeypatch, query_fails):
    import importlib.util
    import psycopg2
    import dotenv
    spec = importlib.util.spec_from_file_location("offline_shadow_command", BACKEND / "scripts/shadow_candidate_discovery.py")
    command = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(command)
    statements = []

    class Cursor:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def execute(self, sql, params):
            assert sql.startswith("SELECT ")
            statements.append(sql)
            if query_fails and "FROM watchlist" in sql:
                raise RuntimeError("offline simulated read failure")

        def fetchall(self):
            if statements[-1] == "SELECT transaction_timestamp() AS timestamp":
                return [{"timestamp": datetime(2026, 10, 7, tzinfo=timezone.utc)}]
            return []

    class Connection:
        rolled_back = closed = False

        def set_session(self, **kwargs):
            assert kwargs == {"isolation_level": "REPEATABLE READ", "readonly": True, "autocommit": False}

        def cursor(self, **kwargs):
            return Cursor()

        def rollback(self):
            self.rolled_back = True

        def close(self):
            self.closed = True

    connection = Connection()
    monkeypatch.setattr(psycopg2, "connect", lambda *args, **kwargs: connection)
    monkeypatch.setattr(dotenv, "dotenv_values", lambda path: {"DATABASE_URL": "postgresql://offline-test"})
    if query_fails:
        with pytest.raises(RuntimeError, match="simulated read failure"):
            command.capture_current(1, BACKEND / ".env")
    else:
        result = command.capture_current(1, BACKEND / ".env")
        assert result["watchlist"] == []
        assert any("FROM market_data_cache" in statement for statement in statements)
    assert any("FROM watchlist" in statement for statement in statements)
    assert connection.rolled_back and connection.closed


def test_legacy_comparison_reuses_actual_gate_and_order():
    report = compare_capture(capture())
    assert report["legacy"]["captured_order_top_10"] == ["A"]
    assert report["legacy"]["l1_gate"] == ["ACCUMULATE", "BUY", "WATCH"]
    assert report["legacy"]["exact_current_runtime_result"] == "UNPROVEN"


def test_production_isolation_import_guard():
    touched = {"candidate_discovery.py", "candidate_discovery_evidence.py", "shadow_candidate_discovery.py",
               "candidate_discovery_refinement.py", "shadow_candidate_discovery_refinement.py",
               "candidate_discovery_integrity.py", "shadow_candidate_discovery_integrity.py",
               "capture_candidate_discovery_integrity.py",
               "test_candidate_discovery.py"}
    paths = list(BACKEND.glob("*.py"))
    for directory in ("agents", "services", "models", "routers", "scripts", "migrations"):
        paths.extend((BACKEND / directory).rglob("*.py"))
    for path in paths:
        if path.name in touched or "tests" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [node.module or ""] if isinstance(node, ast.ImportFrom) else [n.name for n in node.names]
                assert not any("candidate_discovery" in n for n in names), str(path)
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                assert "candidate_discovery" not in node.value, str(path)
