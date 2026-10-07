"""Slice 1C offline evidence diagnostics. Frozen scoring and ranking functions.

Scenarios alter evidence admission or truncate saved bars, never the algorithm.
No label, AI, live data, database or production consumer dependency.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import replace
from pathlib import Path

from services.candidate_discovery import discover, portfolio_overlay
from services.candidate_discovery_evidence import (
    FA_SOURCE, _definitions, _finite, _history, _payload, _timing_functions, adapt_capture, source_digest,
)
from services.candidate_discovery_refinement import (
    FA_FIELDS, IMPORTANT_SYMBOLS, candidate_sets, temporal_diagnostics,
)
from services.symbol_resolver import YFINANCE_SYMBOL_MAP, is_dr, resolve_yfinance_symbol

VERSION = 'wealth.shadow-evidence-integrity.v1'
BUDGETS = (5, 10, 15)


def identity_lineage(capture: dict, supplement: dict | None = None) -> list[dict]:
    profiles = {r['symbol']: r for r in (supplement or {}).get('profiles', [])}
    agents = {r['symbol']: _payload(r, 'result_json') for r in capture['agent_cache']
              if r['agent'] == 'fundamental'}
    assets = {r['id']: r for r in capture['assets']}
    result = []
    for watch in sorted(capture['watchlist'], key=lambda w: w['symbol']):
        symbol = watch['symbol']
        normalized = symbol.strip().upper()
        provider = resolve_yfinance_symbol(symbol)
        base = normalized.removesuffix('.BK')
        mapping = ('explicit_YFINANCE_SYMBOL_MAP' if base in YFINANCE_SYMBOL_MAP else
                   'generic_DR_suffix_removal' if is_dr(symbol) else 'unchanged_listing')
        fa = agents.get(symbol, {})
        parent = fa.get('parent_symbol')
        fa_identity = parent if parent else fa.get('symbol')
        timing_identity = watch.get('timing_fetch_symbol')
        profile_row = profiles.get(provider)
        profile = _payload(profile_row, 'payload_json')
        asset = assets.get(watch.get('asset_id'))
        # A registry row with the same symbol is not a Watchlist binding.
        unbound_matches = sorted(a['id'] for a in assets.values()
                                 if a['canonical_symbol'] == normalized)
        relations = sorted({r['to_asset_id'] for r in capture['relationships']
            if asset and r['from_asset_id'] == asset['id']
            and r['relationship_type'] == 'DEPOSITARY_RECEIPT_OF'
            and (not r.get('effective_date') or r['effective_date'] <= capture['as_of'])})
        targets = [assets.get(i) for i in relations]
        risks = []
        if watch.get('asset_id') is not None and asset is None:
            risks.append('dangling_canonical_binding')
        if asset and asset['canonical_symbol'] != normalized:
            risks.append('bound_listing_symbol_conflict')
        if fa.get('symbol') and fa['symbol'] != symbol:
            risks.append('cached_FA_result_symbol_conflict')
        if fa_identity and fa_identity != provider:
            risks.append('cached_FA_identity_disagrees_with_current_resolver')
        if timing_identity and timing_identity != provider:
            risks.append('captured_timing_identity_disagrees_with_current_resolver')
        if profile.get('symbol') and profile['symbol'] != provider:
            risks.append('provider_profile_symbol_conflict')
        if targets and (len(targets) != 1 or targets[0] is None
                        or targets[0]['canonical_symbol'] != provider):
            risks.append('canonical_underlying_binding_conflict_or_unverifiable')
        agreed = bool(fa_identity and fa_identity == timing_identity == provider)
        if risks:
            classification, category = 'conflicting_identity_evidence', 'C'
        elif not agreed:
            classification, category = 'unsupported_identity', 'C'
            risks.append('evidence_source_identity_not_established')
        elif parent:
            classification = ('explicit_underlying_binding_supported' if asset and targets
                              else 'provider_parent_mapping_only')
            category = 'A' if asset and targets else 'B'
        else:
            classification = 'exact_listing_supported' if asset else 'canonical_binding_missing'
            category = 'A' if asset else 'B'
        result.append({
            'symbol': symbol, 'normalized_symbol': normalized,
            'listing_type': asset['asset_type'] if asset else
                'cached_FA_is_dr_true; canonical_listing_type_UNPROVEN' if fa.get('is_dr') else 'UNPROVEN',
            'normalization_path': 'data_fetcher.normalize_dr_symbol -> symbol_resolver.resolve_yfinance_symbol',
            'mapping_source': mapping, 'provider_symbol': provider,
            'parent_symbol': parent, 'parent_evidence_source': 'captured AgentCache.result_json.parent_symbol',
            'provider_quote_type': profile.get('quoteType'), 'provider_name': profile.get('shortName'),
            'profile_fetched_at': (profile_row or {}).get('fetched_at'),
            'profile_original_baseline_response': 'UNPROVEN',
            'canonical_asset_id': asset['id'] if asset else None,
            'watchlist_asset_id': watch.get('asset_id'), 'unbound_symbol_matches': unbound_matches,
            'canonical_underlying_asset_ids': relations,
            'fa_source_identity': fa_identity, 'fa_source': 'AgentCache.fundamental saved score/metrics',
            'timing_source_identity': timing_identity, 'timing_source': 'captured MarketDataCache history:1y:1d',
            'same_provider_identity': agreed,
            'same_economic_exposure': 'canonical_relationship_supported' if category == 'A' else 'UNPROVEN',
            'classification': classification, 'consistency_category': category, 'integrity_risks': sorted(risks),
            'profile_review': 'ETF profile; intended underlying identity UNPROVEN, mismatch not established'
                if profile.get('quoteType') == 'ETF' and parent else None,
            'limitation': 'Current resolver agreement cannot prove historical fetch or issuer/economic binding',
        })
    return result


def producer_partial_supported() -> dict:
    """Execute canonical producer AST with controlled local info, no module imports.

    This demonstrates skipped missing components, including a successful score
    when all four are absent. It does not prove cached score version or validity.
    """
    from typing import TypedDict
    namespace = _definitions(FA_SOURCE, {'FundamentalResult', 'analyze_fundamental'}, {
        'TypedDict': TypedDict, 'fetch_info': lambda symbol: {'sector': 'fixture'},
        'normalize_dr_symbol': lambda symbol: symbol, 'is_dr_symbol': lambda symbol: False})
    empty = namespace['analyze_fundamental']('fixture')
    namespace['fetch_info'] = lambda symbol: {'trailingPE': 10}
    partial = namespace['analyze_fundamental']('fixture')
    valid = (empty['fa_score'] == 0 and partial['fa_score'] == 2
             and all(empty[k] is None for k in FA_FIELDS)
             and partial['debt_equity'] is None)
    if not valid:
        raise ValueError('canonical missing-component behavior changed; scenario B unsupported')
    return {'source': 'backend/agents/fundamental.py:analyze_fundamental',
        'all_components_optional': True, 'absent_component_behavior': 'skip additive branch',
        'empty_nonempty_info_score': empty['fa_score'], 'PE_only_score': partial['fa_score'],
        'imputation': False, 'partial_normalization': False, 'sector_profile': None,
        'economic_not_applicable_contract': None,
        'baseline_completeness_relation': 'stricter_than_producer',
        'cached_scoring_version': 'UNPROVEN; current-source behavior supports sensitivity only'}


def fa_applicability(snapshot, capture: dict, supplement: dict | None = None) -> list[dict]:
    profiles = {r['symbol']: _payload(r, 'payload_json') for r in (supplement or {}).get('profiles', [])}
    rows = []
    for item in sorted(snapshot.instruments, key=lambda i: i.symbol):
        inputs = dict(item.fundamental.inputs)
        profile = profiles.get(resolve_yfinance_symbol(item.symbol))
        fields = []
        for name, keys in FA_FIELDS.items():
            observed = _finite(inputs.get(name))
            missing_provider = profile is not None and all(profile.get(k) is None for k in keys)
            fields.append({'field': name, 'captured_value': inputs.get(name),
                'observation_class': 'observed' if observed else
                    'provider_missing_in_supplement' if missing_provider else 'baseline_missing_provider_origin_UNPROVEN',
                'producer_class': 'producer_optional', 'applicability_class': 'applicability_unknown',
                'not_applicable_explicit': False,
                'provider_keys': list(keys), 'provider_original_baseline_response': 'UNPROVEN'})
        rows.append({'symbol': item.symbol, 'sector': item.sector,
            'complete': not item.fundamental.missing_inputs,
            'saved_score': item.fundamental.value,
            'all_components_missing': len(item.fundamental.missing_inputs) == len(FA_FIELDS),
            'fields': fields})
    return rows


def producer_valid_snapshot(snapshot, capture: dict):
    producer_partial_supported()
    agents = {r['symbol']: _payload(r, 'result_json') for r in capture['agent_cache']
              if r['agent'] == 'fundamental'}
    items = []
    for item in snapshot.instruments:
        fa = agents.get(item.symbol, {})
        # Retain persisted raw score. Never synthesize a value for missing inputs.
        valid = bool(fa and 'error' not in fa and _finite(fa.get('fa_score')))
        evidence = replace(item.fundamental, available=valid,
            missing_inputs=() if valid else item.fundamental.missing_inputs,
            limitations=item.fundamental.limitations +
                ('scenario_B_admits_saved_partial_score_components_remain_in_inputs',))
        items.append(replace(item, fundamental=evidence))
    return replace(snapshot, instruments=tuple(items))


def common_epoch(capture: dict) -> tuple[dict, dict | None]:
    """Exact UTC calendar date shared by valid Close/Volume bars, not close time.

    Entire original universe and SPY constrain the epoch, including excluded FA.
    Preserve canonical rolling observation-count windows and all original data
    before the endpoint. No calendar imputation or adjusted-price PIT claim.
    """
    market = {(r['symbol'], r['cache_type']): r for r in capture['market_cache']}
    keys = sorted({(w['timing_fetch_symbol'], 'history:1y:1d') for w in capture['watchlist']}
                  | {('SPY', 'history:3mo:1d')})
    frames, date_sets, endpoints = {}, [], []
    for key in keys:
        frame = _history(market.get(key))
        if frame is None or 'Close' not in frame:
            return {'supported': False, 'reason': 'missing_saved_Close_history', 'symbol': key[0]}, None
        valid = frame['Close'].map(_finite)
        if key[0] != 'SPY':
            if 'Volume' not in frame:
                return {'supported': False, 'reason': 'missing_saved_Volume', 'symbol': key[0]}, None
            valid = valid & frame['Volume'].map(_finite)
        dates = {i.date() for i in frame.index[valid]}
        if not dates:
            return {'supported': False, 'reason': 'no_valid_joint_bar', 'symbol': key[0]}, None
        frames[key] = frame
        date_sets.append(dates)
        close = frame['Close'].dropna()
        volume = frame['Volume'].dropna() if 'Volume' in frame else None
        endpoints.append({'symbol': key[0], 'cache_type': key[1], 'rows': len(frame),
            'last_index': frame.index[-1].isoformat(), 'last_valid_Close': close.index[-1].isoformat() if len(close) else None,
            'last_valid_Volume': volume.index[-1].isoformat() if volume is not None and len(volume) else None,
            'joint_bar_count': len(dates), 'latest_joint_date': max(dates).isoformat()})
    dates = set.intersection(*date_sets)
    if not dates:
        return {'supported': False, 'reason': 'no_common_saved_calendar_bar_date', 'endpoints': endpoints}, None
    # Try latest shared dates first, requiring complete canonical scoring inputs.
    functions = _timing_functions()
    for day in sorted(dates, reverse=True):
        trimmed = {key: frame[[i.date() <= day for i in frame.index]].copy() for key, frame in frames.items()}
        benchmark = trimmed[('SPY', 'history:3mo:1d')]['Close'].dropna()
        if len(benchmark) < 21 or benchmark.iloc[-21] == 0:
            continue
        benchmark_return = float((benchmark.iloc[-1] / benchmark.iloc[-21] - 1) * 100)
        if not _finite(benchmark_return):
            continue
        required = ('price', 'sma20', 'sma50', 'rsi', 'current_volume', 'avg_volume_20d', 'stock_return_20d')
        if any(not all(_finite(v.get(k)) for k in required)
               for key, frame in trimmed.items() if key[0] != 'SPY'
               for v in [functions['_extract_indicators'](frame)]):
            continue
        # Copy whole capture and replace only serialized history payloads. Original
        # fetch/expiry times remain acquisition metadata, never rewritten epochs.
        aligned = json.loads(json.dumps(capture))
        for row in aligned['market_cache']:
            key = (row['symbol'], row['cache_type'])
            if key in trimmed:
                payload = _payload(row, 'payload_json').copy()
                payload['json_split'] = trimmed[key].to_json(orient='split', date_format='iso')
                row['payload_json'] = payload
        witnesses = []
        for index, key in enumerate(keys):
            other_dates = set.intersection(*(values for n, values in enumerate(date_sets) if n != index))
            if other_dates and max(other_dates) > day:
                witnesses.append({'symbol': key[0], 'cache_type': key[1],
                    'latest_common_date_without_this_series': max(other_dates).isoformat(),
                    'saved_joint_dates_after_chosen_epoch': sorted(d.isoformat() for d in date_sets[index] if d > day)})
        return {'supported': True, 'scenario_id': 'T1.common-calendar-bars.v1',
            'epoch_UTC_calendar_date': day.isoformat(), 'shared_dates_count': len(dates),
            'limiter_witnesses': witnesses,
            'instrument_Close_Volume_endpoint_mismatch_count': sum(
                r['last_valid_Close'] != r['last_valid_Volume'] for r in endpoints if r['symbol'] != 'SPY'),
            'scope': 'all captured 89 listings plus SPY; valid Close/Volume on shared date',
            'benchmark_return_20d': benchmark_return, 'endpoints': endpoints,
            'timestamp_alignment': False, 'financial_point_in_time_alignment': False,
            'limitations': ['Calendar bar date only; different exchanges have different session times',
                'Historical replay uses later-acquired provider bars; revisions/adjustments UNPROVEN',
                'Rolling 20-observation returns may span different calendar windows',
                'FA frozen; publication/observation epoch and cached scoring version unknown']}, aligned
    return {'supported': False, 'reason': 'shared_dates_have_insufficient_complete_scoring_history',
            'shared_dates_count': len(dates), 'endpoints': endpoints}, None


def set_difference(before, after) -> dict:
    a, b = set(before), set(after)
    return {'candidate_count': len(b), 'intersection': sorted(a & b), 'intersection_count': len(a & b),
        'union': sorted(a | b), 'union_count': len(a | b),
        'jaccard': len(a & b) / len(a | b) if a | b else 1.0,
        'added': sorted(b - a), 'removed': sorted(a - b), 'churn_count': len(a ^ b)}


def stability_groups(sets: list[list[str]], unresolved: list[str]) -> dict:
    cohorts = [set(s) for s in sets]
    core = set.intersection(*cohorts) if cohorts else set()
    union = set.union(*cohorts) if cohorts else set()
    return {'stable_core': sorted(core), 'stable_core_count': len(core),
        'sensitive_edge': sorted(union - core), 'sensitive_edge_count': len(union - core),
        'excluded_unresolved': sorted(set(unresolved)),
        'interpretation': 'Membership stability only; identity/FA temporal uncertainty is not resolved by stability'}


def _rows(standalone):
    return {r['instrument']['symbol']: r for r in standalone['candidates']}


def _sectors(standalone, symbols):
    rows = _rows(standalone)
    return dict(sorted(Counter(rows[s]['instrument']['sector'] or 'UNKNOWN' for s in symbols).items()))


def evaluate_scenario(identifier, snapshot, baseline, contexts, explanation):
    standalone = discover(snapshot)
    sets = candidate_sets(standalone, BUDGETS)
    base_sets = candidate_sets(baseline, BUDGETS)
    overlays = [portfolio_overlay(snapshot, c) for c in contexts]
    rows, base_rows = _rows(standalone), _rows(baseline)
    comparisons = {}
    for budget in BUDGETS:
        name = f'cumulative_{budget}'
        before, after = base_sets[name]['symbols'], sets[name]['symbols']
        comparison = set_difference(before, after)
        comparison['sector_before'] = _sectors(baseline, before)
        comparison['sector_after'] = _sectors(standalone, after)
        portfolios = []
        for overlay in overlays:
            held = {r['symbol'] for r in overlay['candidates'] if r['already_held']}
            selected = [r for r in overlay['candidates'] if r['symbol'] in after]
            portfolios.append({'portfolio_id': overlay['portfolio_id'],
                'exposure_source': overlay['exposure_source'], 'policy_source': overlay['policy_source'],
                'constraints_current': overlay['constraints_current'],
                'before_held': sorted(set(before) & held), 'after_held': sorted(set(after) & held),
                'before_new': sorted(set(before) - held), 'after_new': sorted(set(after) - held),
                'locked': sorted(r['symbol'] for r in selected if 'existing_position_locked'
                    in r['portfolio_add_consideration']['reasons']),
                'current_feasibility': 'UNPROVEN', 'annotations': selected})
        comparison['portfolio_annotations'] = portfolios
        comparisons[name] = comparison
    before_eligible = {s for s, r in base_rows.items() if r['relative']}
    after_eligible = {s for s, r in rows.items() if r['relative']}
    movement = {s: {'before_front': base_rows[s]['relative']['pareto_front'] if base_rows[s]['relative'] else None,
                    'after_front': rows[s]['relative']['pareto_front'] if rows[s]['relative'] else None,
                    'before_timing': base_rows[s]['instrument']['timing']['value'],
                    'after_timing': rows[s]['instrument']['timing']['value'],
                    'before_timing_percentile': base_rows[s]['relative']['timing']['midrank_percentile']
                        if base_rows[s]['relative'] else None,
                    'after_timing_percentile': rows[s]['relative']['timing']['midrank_percentile']
                        if rows[s]['relative'] else None} for s in sorted(rows)}
    return {'scenario_id': identifier, 'explanation': explanation, 'standalone': standalone,
        'candidate_sets': sets, 'eligible_added': sorted(after_eligible - before_eligible),
        'eligible_removed': sorted(before_eligible - after_eligible),
        'eligible_sector_coverage': _sectors(standalone, after_eligible),
        'comparisons': comparisons, 'movement': movement}


def investigate(capture: dict, supplement: dict | None = None, alternative_history: dict | None = None) -> dict:
    snapshot, contexts = adapt_capture(capture)
    baseline = discover(snapshot)
    identity = identity_lineage(capture, supplement)
    applicability = fa_applicability(snapshot, capture, supplement)
    producer = producer_partial_supported()
    temporal, aligned = common_epoch(capture)
    alternate_diagnosis = []
    for row in (alternative_history or {}).get('rows', []):
        frame = _history(row)
        indicators = _timing_functions()['_extract_indicators'](frame)
        close = frame['Close'].dropna() if frame is not None and 'Close' in frame else []
        alternate_diagnosis.append({'symbol': row['symbol'], 'cache_type': row['cache_type'],
            'fetched_at': row.get('fetched_at'), 'expires_at': row.get('expires_at'),
            'saved_rows': len(frame) if frame is not None else 0,
            'valid_Close_rows': len(close),
            'last_Close_bar_label': close.index[-1].isoformat() if len(close) else None,
            'missing_canonical_Timing_inputs': [k for k in ('price','sma20','sma50','rsi',
                'current_volume','avg_volume_20d','stock_return_20d') if not _finite(indicators.get(k))],
            'used_for_scenario': False,
            'reason': 'Alternative period; no history splicing or unproven adjustment compatibility',
        })
    partial = producer_valid_snapshot(snapshot, capture)
    definitions = [
        ('A.strict.T0.v1', snapshot, 'Frozen Slice 1 complete-case FA and original captured Timing'),
        ('B.producer-valid.T0.v1', partial,
         'Successful finite persisted FA scores, including partial/all-missing components; no score change or imputation'),
    ]
    if aligned is not None:
        aligned_snapshot, _ = adapt_capture(aligned)
        definitions.extend([
            ('A.strict.T1.v1', aligned_snapshot, 'Strict FA unchanged; saved histories truncated to common UTC calendar bar date'),
            ('B.producer-valid.T1.v1', producer_valid_snapshot(aligned_snapshot, capture),
             'Combined producer-valid admission and common-calendar Timing replay'),
        ])
    risks = {r['symbol'] for r in identity if r['consistency_category'] == 'C'}
    # Only test risk exclusion when concrete C evidence exists. B never excluded.
    if risks:
        definitions.append(('I.exclude-C.T0.v1', replace(snapshot, instruments=tuple(
            replace(i, fundamental=replace(i.fundamental, invalid_reason='identity_integrity_risk'))
            if i.symbol in risks else i for i in snapshot.instruments)),
            'Independent identity-C exclusion sensitivity; baseline untouched'))
    scenarios = {identifier: evaluate_scenario(identifier, value, baseline, contexts, explanation)
                 for identifier, value, explanation in definitions}
    evaluated = {r['instrument']['symbol'] for scenario in scenarios.values()
                 for r in scenario['standalone']['candidates'] if r['relative']}
    # Keep source-binding uncertainty distinct from membership sensitivity.
    unresolved = sorted(r['symbol'] for r in identity if r['consistency_category'] != 'A'
                        or r['symbol'] not in evaluated)
    groups = {f'cumulative_{budget}': stability_groups([
        s['candidate_sets'][f'cumulative_{budget}']['symbols'] for s in scenarios.values()], unresolved)
        for budget in BUDGETS}
    important_symbols = set(IMPORTANT_SYMBOLS) | risks | {
        r['symbol'] for r in applicability if not r['complete']}
    by_identity = {r['symbol']: r for r in identity}
    by_fa = {r['symbol']: r for r in applicability}
    important = []
    for symbol in sorted(important_symbols & set(by_identity)):
        positions = {identifier: {'front': scenario['movement'][symbol]['after_front'],
            'memberships': [symbol in scenario['candidate_sets'][f'cumulative_{b}']['symbols'] for b in BUDGETS],
            'timing': scenario['movement'][symbol]['after_timing'],
            'timing_percentile': scenario['movement'][symbol]['after_timing_percentile']}
            for identifier, scenario in scenarios.items()}
        sensitive = len({tuple(p['memberships']) for p in positions.values()}) > 1
        status = 'sensitive' if sensitive else 'stable'
        # Membership can be stable despite unresolved economic binding. Surface
        # both facts; final epistemic status must not erase that uncertainty.
        important.append({'symbol': symbol, 'identity': by_identity[symbol]['classification'],
            'FA': 'complete' if by_fa[symbol]['complete'] else 'partial/all-missing; producer_optional; applicability_unknown',
            'temporal_limitation': 'FA epoch/version unknown; later-acquired bar replay; no exact close-time alignment',
            'scenarios': positions, 'membership_status': status,
            'diagnostic_status': 'unresolved' if symbol in unresolved else status})
    history = (supplement or {}).get('analysis_history_metadata', [])
    history_period_keys = Counter()
    history_by_symbol = {}
    for row in history:
        history_by_symbol.setdefault(row['symbol'], []).append(row.get('analyzed_at'))
        scores = row.get('scores')
        if isinstance(scores, str):
            try:
                scores = json.loads(scores)
            except ValueError:
                scores = {}
        if isinstance(scores, dict):
            history_period_keys.update(k for k in scores if re.search(
                r'(^|_)(date|time|timestamp|period|observed|observation|published|publication|version|at)($|_)', k.lower()))
    return {'integrity_version': VERSION, 'shadow_only': True, 'algorithm_changed': False,
        'capture_provenance': {'baseline_capture_at': capture['captured_at'],
            'local_supplement_capture_at': (supplement or {}).get('captured_at'),
            'alternative_history_capture_at': (alternative_history or {}).get('captured_at'),
            'offline_calculation_timestamp': None,
            'offline_calculation_timestamp_semantics': 'unrecorded; reproducible calculation is not a historical observation'},
        'current_resolver_source_sha256': source_digest(Path(__file__).with_name('symbol_resolver.py')),
        'current_resolver_historical_version': 'UNPROVEN; source digest describes current diagnostic resolver only',
        'baseline_standalone': baseline, 'identity': identity,
        'identity_summary': {'classification_counts': dict(sorted(Counter(r['classification'] for r in identity).items())),
            'consistency_counts': dict(sorted(Counter(r['consistency_category'] for r in identity).items())),
            'ETF_profile_review_symbols': [r['symbol'] for r in identity if r['profile_review']],
            'identity_C_exclusion_tested': bool(risks)},
        'FA_producer_semantics': producer, 'FA_applicability': applicability,
        'temporal_baseline': temporal_diagnostics(baseline), 'common_epoch': temporal,
        'alternative_history_diagnosis': alternate_diagnosis,
        'FA_temporal_alignment': {'supported': False,
            'reason': 'AgentCache contains cache time, not metric reporting/publication/observation dates or scoring version',
            'analysis_history_rows_inspected': len(history),
            'analysis_history_timestamp_or_period_score_keys': dict(history_period_keys),
            'analysis_history_role': 'AI analysis time/scores do not prove FA observation epoch or reconstruct source metrics',
            'local_table_catalogue': (supplement or {}).get('history_table_catalogue', []),
            'history_semantics': 'AgentCache/MarketDataCache unique current rows; no history tables in captured catalogue'},
        'analysis_history_calculation_dates': [{
            'symbol': s, 'rows': len(dates),
            'first_analyzed_at': min(d for d in dates if d) if any(dates) else None,
            'last_analyzed_at': max(d for d in dates if d) if any(dates) else None,
            'meaning': 'AI Stock Analysis calculation timestamps, not FA observations'}
            for s, dates in sorted(history_by_symbol.items())],
        'provider_reporting_metadata': [{
            'symbol': r['symbol'], 'fetched_at': r.get('fetched_at'), 'expires_at': r.get('expires_at'),
            'mostRecentQuarter_unix': _payload(r, 'payload_json').get('mostRecentQuarter'),
            'lastFiscalYearEnd_unix': _payload(r, 'payload_json').get('lastFiscalYearEnd'),
            'other_provider_date_fields_raw': {k:v for k,v in _payload(r, 'payload_json').items()
                if any(t in k.lower() for t in ('timestamp','date','time','quarter','yearend'))},
            'publication_or_observation_date': None,
            'meaning': 'provider period/quote/earnings/corporate-event date fields in later local supplement; '
                'none establishes baseline metric publication/observation lineage'}
            for r in (supplement or {}).get('profiles', [])],
        'local_market_history_catalogue': (supplement or {}).get('market_history_catalogue', []),
        'scenarios': scenarios, 'stability': groups, 'important_cases': important,
        'verdict': 'EVIDENCE INTEGRITY MIXED — CONTINUE SHADOW DISCOVERY RESEARCH'}
