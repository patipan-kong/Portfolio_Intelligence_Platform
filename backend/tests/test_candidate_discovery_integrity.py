"""Focused Slice 1C evidence semantics and scenario isolation tests."""
import copy
import json
from dataclasses import replace
from pathlib import Path

import pytest

from services.candidate_discovery import discover
from services.candidate_discovery_evidence import adapt_capture
from services.candidate_discovery_integrity import (
    common_epoch, fa_applicability, identity_lineage, investigate,
    producer_partial_supported, producer_valid_snapshot, set_difference, stability_groups,
)
from scripts.capture_candidate_discovery_integrity import capture_integrity
from scripts.shadow_candidate_discovery_integrity import validate_preservation
from tests.test_candidate_discovery import capture


def bound_capture():
    c = capture()
    c['watchlist'][0]['asset_id'] = 1
    c['assets'] = [{'id': 1, 'canonical_symbol': 'A', 'asset_type': 'EQUITY', 'tradable': True}]
    c['agent_cache'][0]['result_json']['symbol'] = 'A'
    return c


def dr_capture():
    c = capture()
    c['watchlist'][0].update(symbol='AAPL01.BK', timing_fetch_symbol='AAPL')
    c['agent_cache'][0]['symbol'] = 'AAPL01.BK'
    c['agent_cache'][0]['result_json'].update(symbol='AAPL01.BK', parent_symbol='AAPL', is_dr=True)
    c['market_cache'][0]['symbol'] = 'AAPL'
    return c


def test_exact_supported_listing():
    row = identity_lineage(bound_capture())[0]
    assert row['classification'] == 'exact_listing_supported'
    assert row['consistency_category'] == 'A'


def test_provider_parent_only_not_economic_binding():
    row = identity_lineage(dr_capture())[0]
    assert row['classification'] == 'provider_parent_mapping_only'
    assert row['consistency_category'] == 'B'
    assert row['same_provider_identity'] is True
    assert row['same_economic_exposure'] == 'UNPROVEN'


def test_explicit_underlying_binding():
    c = dr_capture()
    c['watchlist'][0]['asset_id'] = 1
    c['assets'] = [{'id': 1, 'canonical_symbol': 'AAPL01.BK', 'asset_type': 'EQUITY'},
                   {'id': 2, 'canonical_symbol': 'AAPL', 'asset_type': 'EQUITY'}]
    c['relationships'] = [{'from_asset_id': 1, 'to_asset_id': 2,
        'relationship_type': 'DEPOSITARY_RECEIPT_OF', 'effective_date': None}]
    assert identity_lineage(c)[0]['classification'] == 'explicit_underlying_binding_supported'
    c['relationships'][0]['effective_date'] = '2099-01-01'
    assert identity_lineage(c)[0]['consistency_category'] == 'B'


def test_missing_binding_does_not_use_symbol_match():
    c = bound_capture()
    c['watchlist'][0]['asset_id'] = None
    row = identity_lineage(c)[0]
    assert row['classification'] == 'canonical_binding_missing'
    assert row['canonical_asset_id'] is None and row['unbound_symbol_matches'] == [1]


@pytest.mark.parametrize('kind', ['parent', 'timing', 'binding', 'profile', 'result'])
def test_conflict_risk(kind):
    c = dr_capture()
    supplement = None
    if kind == 'parent':
        c['agent_cache'][0]['result_json']['parent_symbol'] = 'OTHER'
    elif kind == 'timing':
        c['watchlist'][0]['timing_fetch_symbol'] = 'OTHER'
    elif kind == 'binding':
        c['watchlist'][0]['asset_id'] = 100
    elif kind == 'result':
        c['agent_cache'][0]['result_json']['symbol'] = 'OTHER'
    else:
        supplement = {'profiles': [{'symbol': 'AAPL', 'payload_json': {'symbol': 'OTHER'}}]}
    row = identity_lineage(c, supplement)[0]
    assert row['consistency_category'] == 'C' and row['integrity_risks']


def test_unsupported_identity():
    c = capture()
    c['agent_cache'] = []
    assert identity_lineage(c)[0]['classification'] == 'unsupported_identity'


def test_ETF_profile_is_review_not_mismatch():
    row = identity_lineage(dr_capture(), {'profiles': [
        {'symbol': 'AAPL', 'payload_json': {'quoteType': 'ETF'}}]})[0]
    assert row['consistency_category'] == 'B'
    assert row['profile_review'] and not row['integrity_risks']


def test_provider_missing_is_not_not_applicable():
    c = capture()
    c['agent_cache'][0]['result_json']['debt_equity'] = None
    snap, _ = adapt_capture(c)
    row = fa_applicability(snap, c, {'profiles': [{'symbol': 'A', 'payload_json': {}}]})[0]
    field = next(f for f in row['fields'] if f['field'] == 'debt_equity')
    assert field['observation_class'] == 'provider_missing_in_supplement'
    assert field['applicability_class'] == 'applicability_unknown'
    assert not field['not_applicable_explicit']


def test_current_producer_proves_partial_and_all_missing_semantics():
    result = producer_partial_supported()
    assert result['PE_only_score'] == 2 and result['empty_nonempty_info_score'] == 0
    assert result['all_components_optional'] and not result['imputation']
    assert result['baseline_completeness_relation'] == 'stricter_than_producer'


@pytest.mark.parametrize('all_missing', [False, True])
def test_producer_scenario_retains_saved_score_and_missing_inputs_no_imputation(all_missing):
    c = capture()
    fa = c['agent_cache'][0]['result_json']
    for name in (['pe_ratio', 'roe', 'revenue_growth', 'debt_equity'] if all_missing else ['debt_equity']):
        fa[name] = None
    fa['fa_score'] = 0 if all_missing else 3
    snap, _ = adapt_capture(c)
    before = discover(snap)
    scenario = producer_valid_snapshot(snap, c)
    assert discover(snap) == before and before['coverage']['ranking_eligible'] == 0
    assert discover(scenario)['coverage']['ranking_eligible'] == 1
    assert scenario.instruments[0].fundamental.value == fa['fa_score']
    assert dict(scenario.instruments[0].fundamental.inputs)['debt_equity'] is None


def test_error_or_absent_score_not_admitted():
    c = capture()
    c['agent_cache'][0]['result_json'] = {'error': 'no data'}
    snap, _ = adapt_capture(c)
    assert discover(producer_valid_snapshot(snap, c))['coverage']['ranking_eligible'] == 0


def test_epoch_truncates_only_saved_bars_not_fetch_timestamp():
    c = capture()
    before = copy.deepcopy(c)
    info, aligned = common_epoch(c)
    assert info['supported'] and not info['timestamp_alignment']
    assert c == before
    assert aligned['market_cache'][0]['fetched_at'] == c['market_cache'][0]['fetched_at']
    snap, _ = adapt_capture(aligned)
    assert snap.instruments[0].fundamental.observed_at is None
    assert snap.instruments[0].timing.observed_at != c['captured_at']


def test_unknown_or_missing_history_stays_unsupported():
    c = capture()
    c['market_cache'] = []
    info, aligned = common_epoch(c)
    assert info['supported'] is False and aligned is None


def test_aligned_scenario_freezes_FA_and_bar_date_is_not_exact_timestamp():
    c = capture()
    c['market_cache'][1]['payload_json'] = copy.deepcopy(c['market_cache'][1]['payload_json'])
    payload = c['market_cache'][1]['payload_json']
    data = json.loads(payload['json_split'])
    data['index'] = [s.replace('T00:', 'T01:') for s in data['index']]
    payload['json_split'] = json.dumps(data)
    before, _ = adapt_capture(c)
    info, aligned = common_epoch(c)
    after, _ = adapt_capture(aligned)
    assert info['supported'] and not info['timestamp_alignment']
    assert before.instruments[0].fundamental == after.instruments[0].fundamental
    timing = after.instruments[0].timing
    assert timing.observed_at != dict(timing.provenance)['benchmark_observed_at']


def test_history_score_sentiment_is_not_a_timestamp():
    result = investigate(bound_capture(), {'analysis_history_metadata': [
        {'symbol': 'A', 'scores': {'news_sentiment': 50, 'fundamental_score': 75}}]})
    assert result['FA_temporal_alignment']['analysis_history_timestamp_or_period_score_keys'] == {}


def test_nonmatching_dates_do_not_synthesize_epoch():
    c = capture()
    row = c['market_cache'][1]
    row['payload_json'] = copy.deepcopy(row['payload_json'])
    payload = row['payload_json']
    data = json.loads(payload['json_split'])
    data['index'] = [s.replace('2025-', '2020-') for s in data['index']]
    payload['json_split'] = json.dumps(data)
    info, aligned = common_epoch(c)
    assert info['reason'] == 'no_common_saved_calendar_bar_date' and aligned is None


def test_insufficient_common_history_not_admitted():
    c = capture()
    payload = c['market_cache'][1]['payload_json']
    data = json.loads(payload['json_split'])
    data['index'], data['data'] = data['index'][:5], data['data'][:5]
    payload['json_split'] = json.dumps(data)
    info, aligned = common_epoch(c)
    assert not info['supported'] and aligned is None


def test_shared_date_limiter_is_a_saved_bar_gap_not_the_last_Close_endpoint():
    c = capture()
    instrument_payload = json.loads(c['market_cache'][0]['payload_json']['json_split'])
    benchmark_payload = copy.deepcopy(instrument_payload)
    instrument_payload['index'] = instrument_payload['index'][:200] + instrument_payload['index'][-1:]
    instrument_payload['data'] = instrument_payload['data'][:200] + instrument_payload['data'][-1:]
    benchmark_payload['index'] = benchmark_payload['index'][:-1]
    benchmark_payload['data'] = benchmark_payload['data'][:-1]
    c['market_cache'][0]['payload_json'] = {'json_split': json.dumps(instrument_payload)}
    c['market_cache'][1]['payload_json'] = {'json_split': json.dumps(benchmark_payload)}
    info, aligned = common_epoch(c)
    assert info['supported']
    assert info['epoch_UTC_calendar_date'] == instrument_payload['index'][199][:10]
    endpoint = next(r for r in info['endpoints'] if r['symbol'] == 'A')
    assert endpoint['last_valid_Close'][:10] > info['epoch_UTC_calendar_date']
    assert info['instrument_Close_Volume_endpoint_mismatch_count'] == 0
    assert info['limiter_witnesses'][0]['symbol'] == 'A'


@pytest.mark.parametrize('before,after,jaccard,added,removed', [
    (['A','B'], ['B','C'], 1/3, ['C'], ['A']),
    ([], [], 1, [], []), (['A'], [], 0, [], ['A']),
])
def test_stability_metrics(before, after, jaccard, added, removed):
    result = set_difference(before, after)
    assert result['jaccard'] == jaccard
    assert result['added'] == added and result['removed'] == removed


def test_stable_core_sensitive_edge_and_unresolved_distinct():
    groups = stability_groups([['A','B'], ['B','C']], ['A','Z'])
    assert groups['stable_core'] == ['B'] and groups['sensitive_edge'] == ['A','C']
    assert groups['excluded_unresolved'] == ['A','Z']


def test_scenario_determinism_order_and_baseline_isolation():
    c = bound_capture()
    before = copy.deepcopy(c)
    a = investigate(c)
    assert c == before and investigate(c) == a
    c['watchlist'].reverse()
    c['agent_cache'].reverse()
    c['market_cache'].reverse()
    assert investigate(c) == a
    assert a['baseline_standalone'] == a['scenarios']['A.strict.T0.v1']['standalone']


@pytest.mark.parametrize('label', ['BUY','ACCUMULATE','WATCH','HOLD','REDUCE','SELL'])
def test_legacy_labels_cannot_change_any_integrity_or_stability(label):
    c = bound_capture()
    baseline = investigate(c)
    c['analysis_cache'][0]['signal'] = label
    assert investigate(c) == baseline


def test_portfolio_context_only_changes_annotations():
    c = bound_capture()
    before = investigate(c)
    c['portfolios'] = [{'id': 1, 'name': 'fixture'}]
    c['holdings'] = [{'portfolio_id': 1, 'symbol': 'A', 'asset_id': 1,
        'allow_swap': False, 'shares': 1, 'sector': None}]
    after = investigate(c)
    assert before['baseline_standalone'] == after['baseline_standalone']
    assert before['stability'] == after['stability']
    for name in before['scenarios']:
        assert before['scenarios'][name]['standalone'] == after['scenarios'][name]['standalone']
    assert after['scenarios']['A.strict.T0.v1']['comparisons']['cumulative_5']['portfolio_annotations'][0]['locked'] == ['A']


def test_C_risk_scenario_separate_and_B_retained():
    c = bound_capture()
    c['watchlist'][0]['asset_id'] = 404
    result = investigate(c)
    assert result['baseline_standalone']['coverage']['ranking_eligible'] == 1
    assert result['scenarios']['I.exclude-C.T0.v1']['standalone']['coverage']['ranking_eligible'] == 0
    assert not investigate(dr_capture())['identity_summary']['identity_C_exclusion_tested']


def test_preservation_detects_change(tmp_path):
    import hashlib
    path = tmp_path / 'baseline'
    path.write_text('baseline')
    manifest = {str(path): hashlib.sha256(path.read_bytes()).hexdigest()}
    validate_preservation(manifest)
    path.write_text('changed')
    with pytest.raises(ValueError, match='preserved input changed'):
        validate_preservation(manifest)


@pytest.mark.parametrize('fail', [False, True])
def test_supplement_SELECT_only_readonly_and_rollback(monkeypatch, fail):
    import psycopg2
    import dotenv
    class Cursor:
        queries = []
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def execute(self, sql, params):
            assert sql.startswith('SELECT')
            self.queries.append(sql)
            if fail: raise RuntimeError('fixture failure')
        def fetchall(self):
            return [{'t': '2026-10-07T00:00:00+00:00'}] if len(self.queries) == 1 else []
    class Connection:
        rolled_back = False
        closed = False
        def set_session(self, **kwargs):
            assert kwargs == {'isolation_level': 'REPEATABLE READ', 'readonly': True, 'autocommit': False}
        def cursor(self, **kwargs): return Cursor()
        def rollback(self): self.rolled_back = True
        def close(self): self.closed = True
    connection = Connection()
    monkeypatch.setattr(psycopg2, 'connect', lambda *a, **k: connection)
    monkeypatch.setattr(dotenv, 'dotenv_values', lambda path: {'DATABASE_URL': 'fixture'})
    c = capture()
    c['workspace_id'] = 1
    if fail:
        with pytest.raises(RuntimeError): capture_integrity(c, Path('fixture'))
    else:
        capture_integrity(c, Path('fixture'))
    assert connection.rolled_back and connection.closed
