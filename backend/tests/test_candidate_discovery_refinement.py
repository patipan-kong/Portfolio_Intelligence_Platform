"""Slice 1B pure diagnostics and authority-isolation regressions."""
import copy

import pytest

from services.candidate_discovery import discover
from services.candidate_discovery_refinement import (
    candidate_sets, cumulative_pareto, dimension_leaders, exclusion_diagnosis,
    refine_capture, temporal_diagnostics,
)
from tests.test_candidate_discovery import capture, instrument, snapshot


def test_cumulative_exact_budget():
    result = cumulative_pareto([["A"], ["B"], ["C", "D", "E"], ["F"]], 5)
    assert result["symbols"] == ["A", "B", "C", "D", "E"]
    assert result["included_fronts"] == [1, 2, 3]
    assert result["actual_count"] == 5 and result["overshoot"] == 0


def test_cumulative_front_crossing_preserves_whole_front():
    fronts = [["A"], ["B"], ["C", "D", "E"], ["F", "G", "H"], ["I", "J", "K", "L", "M", "N"]]
    result = cumulative_pareto(fronts, 10)
    assert result["actual_count"] == 14 and result["overshoot"] == 4
    assert result["included_fronts"] == [1, 2, 3, 4, 5]
    assert result["overshoot_reason"] == "complete_boundary_front"
    assert not result["ties_split"]


def test_cumulative_ties_order_and_exhausted_universe():
    a = cumulative_pareto([["C", "A", "B"]], 2)
    b = cumulative_pareto([["B", "C", "A"]], 2)
    assert a == b
    assert a["symbols"] == ["A", "B", "C"]
    assert cumulative_pareto([["A"]], 10)["shortfall"] == 9
    assert cumulative_pareto([], 5)["actual_count"] == 0


@pytest.mark.parametrize("budget", [0, -1, True, 1.5])
def test_bad_budget_rejected(budget):
    with pytest.raises(ValueError):
        cumulative_pareto([], budget)


def test_duplicate_or_empty_front_rejected():
    for fronts in ([["A"], ["A"]], [[]]):
        with pytest.raises(ValueError):
            cumulative_pareto(fronts, 1)


def test_candidate_sets_input_order_invariance():
    items = [instrument("A", 7, 90), instrument("B", 6, 80),
             instrument("C", 6, 80), instrument("D", 5, 70)]
    assert candidate_sets(discover(snapshot(*items))) == candidate_sets(discover(snapshot(*reversed(items))))


def test_dimension_boundary_ties_and_union_are_explicit():
    value = discover(snapshot(instrument("A", 7, 80), instrument("B", 7, 70),
        instrument("C", 6, 90), instrument("D", 5, 90)))
    leaders = dimension_leaders(value, "fundamental", 1)
    assert [r["symbol"] for r in leaders["leaders"]] == ["A", "B"]
    assert leaders["overshoot"] == 1
    union = candidate_sets(value, (1,))["dimension_union_1"]
    assert union["symbols"] == ["A", "B", "C", "D"]
    assert union["nominal_union_bound"] == 2 and union["above_nominal_bound"] == 2
    assert union["overshoot_reason"] == "dimension_boundary_ties"


def test_dimension_leaders_empty_and_invalid_dimension():
    assert dimension_leaders(discover(snapshot()), "timing", 5)["leaders"] == []
    with pytest.raises(ValueError):
        dimension_leaders(discover(snapshot()), "fake", 5)


def test_temporal_known_and_unknown_dates_never_substitute_cache():
    value = discover(snapshot(instrument("A"), instrument("B")))
    a, b = value["candidates"]
    for row in (a, b):
        row["instrument"]["timing"]["provenance"] = (("benchmark_observed_at", "2026-10-06T00:00:00+00:00"),)
        row["instrument"]["timing"]["cached_at"] = "2026-10-07T00:00:00+00:00"
        row["instrument"]["fundamental"]["cached_at"] = "2026-10-07T00:00:00+00:00"
    a["instrument"]["timing"]["observed_at"] = "2026-10-05T00:00:00+00:00"
    diagnosis = temporal_diagnostics(value)
    assert diagnosis["timing_bar_age_days"]["min"] == 2
    assert diagnosis["timing_observation_unknown_count"] == 1
    assert diagnosis["fa_observation_unknown_count"] == 2
    assert diagnosis["benchmark_after_instrument_count"] == 1
    assert diagnosis["benchmark_different_UTC_calendar_date_count"] == 1
    assert diagnosis["candidates"][1]["timing_bar_age_days"] is None
    assert not diagnosis["current_opportunity_set"]


def test_naive_timestamp_is_unknown_not_invented_utc():
    value = discover(snapshot(instrument("A")))
    value["candidates"][0]["instrument"]["timing"]["observed_at"] = "2026-10-05T00:00:00"
    assert temporal_diagnostics(value)["timing_observation_unknown_count"] == 1


def test_same_bar_calendar_date_is_distinct_from_same_timestamp():
    value = discover(snapshot(instrument("A")))
    timing = value["candidates"][0]["instrument"]["timing"]
    timing["observed_at"] = "2026-10-05T03:00:00+00:00"
    timing["provenance"] = (("benchmark_observed_at", "2026-10-05T13:30:00+00:00"),)
    result = temporal_diagnostics(value)
    assert result["benchmark_same_UTC_calendar_date_count"] == 1
    assert result["benchmark_same_index_count"] == 0


def test_coarse_dimensions_and_joint_maximum_are_visible():
    result = refine_capture(capture())
    assert result["dimension_coarseness"]["fundamental"]["distinct_values"] == 1
    assert result["joint_dimension_maxima"] == ["A"]


@pytest.mark.parametrize("signal", ["BUY", "ACCUMULATE", "WATCH", "HOLD", "REDUCE", "SELL"])
def test_all_candidate_sets_signal_independent(signal):
    frozen = capture()
    before = refine_capture(frozen)
    frozen["analysis_cache"][0]["signal"] = signal
    after = refine_capture(frozen)
    assert before["baseline"]["standalone"] == after["baseline"]["standalone"]
    assert {n: v["symbols"] for n, v in before["candidate_sets"].items()} == {
        n: v["symbols"] for n, v in after["candidate_sets"].items()}


def test_overlay_changes_annotations_not_standalone_or_sets():
    frozen = capture()
    before = refine_capture(frozen)
    frozen["portfolios"] = [{"id": 1}]
    frozen["holdings"] = [{"portfolio_id": 1, "symbol": "A", "allow_swap": False}]
    after = refine_capture(frozen)
    assert before["baseline"]["standalone"] == after["baseline"]["standalone"]
    assert {n: v["symbols"] for n, v in before["candidate_sets"].items()} == {
        n: v["symbols"] for n, v in after["candidate_sets"].items()}
    diagnostic = after["candidate_sets"]["front_1"]["portfolio_diagnostics"][0]
    assert diagnostic["locked"] == ["A"]
    assert diagnostic["not_blocked_by_known_hard_restrictions_count"] == 0
    assert diagnostic["confirmed_current_feasible_count"] is None


def test_financial_missingness_is_not_waived_and_raw_supplement_does_not_rank():
    frozen = capture()
    frozen["agent_cache"][0]["result_json"]["debt_equity"] = None
    frozen["watchlist"][0]["sector"] = "Financial Services"
    supplement = {"requested_provider_symbols": {"A": "A"}, "rows": [
        {"symbol": "A", "payload_json": {"quoteType": "EQUITY", "industry": "Banks - Regional"}}]}
    result = refine_capture(frozen, supplement)
    assert result["eligibility_refinement"]["after_ranking_eligible"] == 0
    field = result["exclusion_diagnosis"][0]["fields"][0]
    assert field["field"] == "debt_equity"
    assert field["classification"] == "provider_missing_in_supplement_baseline_origin_unproven"
    assert field["economic_applicability"].startswith("UNKNOWN")
    changed = copy.deepcopy(supplement)
    changed["rows"][0]["payload_json"]["debtToEquity"] = 50
    assert refine_capture(frozen, changed)["baseline"]["standalone"] == result["baseline"]["standalone"]


def test_supplemental_etf_profile_is_diagnosis_not_identity_override():
    frozen = capture()
    frozen["agent_cache"][0]["result_json"] = {"fa_score": 0}
    value = refine_capture(frozen, {"rows": [{"symbol": "A", "payload_json": {"quoteType": "ETF"}}]})
    assert value["exclusion_diagnosis"][0]["profile_limitation"].startswith("provider_reports_ETF")
    assert value["baseline"]["standalone"]["candidates"][0]["instrument"]["asset_type"] is None


def _report_command():
    import importlib.util
    from services.candidate_discovery_evidence import BACKEND
    spec = importlib.util.spec_from_file_location("refinement_report_command",
        BACKEND / "scripts/shadow_candidate_discovery_refinement.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_report_handles_no_eligible_candidates_without_division_or_format_error():
    frozen = capture()
    frozen["agent_cache"][0]["result_json"] = {"fa_score": 0}
    result = refine_capture(frozen)
    report = _report_command().render_report(result)
    assert "UNKNOWN" in report
    assert result["candidate_sets"]["front_1"]["actual_count"] == 0


def test_cli_refuses_original_baseline_output_prefix(monkeypatch, tmp_path):
    import sys
    prefix = tmp_path / "baseline"
    monkeypatch.setattr(sys, "argv", ["command", "--capture", str(prefix) + ".capture.json",
        "--baseline-result", str(prefix) + ".result.json", "--output-prefix", str(prefix)])
    with pytest.raises(SystemExit) as exc:
        _report_command().main()
    assert exc.value.code == 2
    assert list(tmp_path.iterdir()) == []
