"""Slice 1C frozen replay/report. No database or live market mode."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))
from services.candidate_discovery_integrity import investigate
from services.candidate_discovery_evidence import compare_capture
from services.candidate_discovery_refinement import refine_capture


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_preservation(manifest):
    for name, expected in manifest.items():
        if digest(Path(name)) != expected:
            raise ValueError(f'preserved input changed: {name}')


def render_report(result):
    lines = ['# Shadow Discovery — Slice 1C Evidence Integrity', '',
        'Structural sensitivity research only. All scoring, percentiles, dominance, fronts, budgets and extraction functions frozen. '
        'No investment, execution or production authority.', '',
        '## A. Entry/worktree state', '',
        'Branch: feature/wealth-os-shadow-candidate-discovery. HEAD: 653a3ed75247342c88b7b7ca2a78ff6dcf4aec4a. '
        'Local origin/main: a04a02b7bfb0a33aede40f5ac30d163d3f297563. No fetch.',
        'Pre-existing tracked change: backend/ai-model.json. Slice 1/1B files/artifacts were untracked. '
        'Full entry and final status/validation are in the implementation note.', '',
        '## B. Preservation proof', '',
        'Every prior artifact, prior scoring/discovery/adapter/refinement/CLI file and ai-model.json verified against SHA-256 manifest. '
        'Frozen Slice 1 replay equals its saved result. Frozen Slice 1B replay equals its saved result (excluding file-checksum metadata).',
        '', '```json', json.dumps(result.get('preserved_sha256', {}), indent=2), '```', '',
        '## C. Slice 1C files', '',
        'New offline integrity service, replay CLI, read-only supplement CLI, focused tests, implementation note, '
        'preservation manifest, separate local supplement/result/report. Only prior-file edit is the offline import-guard allowlist in Slice 1 tests.', '',
        '## D. Identity lineage', '',
        str(result['identity_summary']), '',
        'A = canonical evidence identity supported; B = provider agreement without canonical economic binding; '
        'C = concrete conflict or unsupported source identity. ETF profile alone is not C. '
        'An unbound matching registry row does not create a binding.', '',
        '| Listing | Mapping source | Provider / FA / Timing | Provider type / name | Canonical ID; unbound matches | Class / category | Economic exposure |',
        '|---|---|---|---|---|---|---|']
    for r in result['identity']:
        lines.append(f"| {r['symbol']} | {r['mapping_source']} | {r['provider_symbol']} / {r['fa_source_identity']} / "
            f"{r['timing_source_identity']} | {r['provider_quote_type']} / {r['provider_name']} | "
            f"{r['canonical_asset_id']}; {r['unbound_symbol_matches']} | {r['classification']} / {r['consistency_category']} | {r['same_economic_exposure']} |")
    lines.extend(['', 'All normalized paths, parent sources, listing forms, binding/relationship evidence, profile fetch times '
        'and limitations are recorded per symbol in result JSON. Source paths: fundamental.py:25 → normalize_dr_symbol:617 → '
        'symbol_resolver.resolve_yfinance_symbol; Timing uses frozen get_yfinance_symbol output and saved history keys.', '',
        '## E. FA applicability', '', str(result['FA_producer_semantics']), '',
        'Canonical producer begins score=0, adds branches only for non-None PE/growth/ROE/debt-equity, and returns a score '
        'for any nonempty info object. Missing contributions are skipped; no values are imputed and no partial normalization occurs. '
        'No sector branch, mandatory component contract, explicit not-applicable flag or bank/insurer replacement metric was found '
        'in the producer, provider adaptation, focused tests or inspected architecture docs. Raw metadata can describe an industry, '
        'but it does not establish economic applicability.', '',
        '| Symbol with incomplete FA | Sector | Saved score | Missing fields | Producer / applicability |', '|---|---|---:|---|---|'])
    for r in result['FA_applicability']:
        if not r['complete']:
            missing = ', '.join(f"{f['field']} ({f['observation_class']})" for f in r['fields'] if f['observation_class'] != 'observed')
            lines.append(f"| {r['symbol']} | {r['sector']} | {r['saved_score']} | {missing} | optional / unknown |")
    lines.extend(['', 'Provider missing remains separate from economically not applicable. Canonical current-source validity '
        'does not establish the cached scoring version, stock-economic applicability or comparability of partial and complete scores.', '',
        '## F. FA sensitivity scenarios', '',
        'A = frozen strict eligibility. B = successful finite persisted FA score admitted under current canonical optional-component '
        'behavior; input missingness retained in evidence inputs and diagnostic records. Even an all-missing-components persisted score '
        'is admitted if successful: this is producer behavior, not invented zero imputation. B is deliberately not a production decision.', '',
        '| Scenario | Eligible | Added / removed | Front sizes | Sector coverage |', '|---|---:|---|---|---|'])
    for name, scenario in result['scenarios'].items():
        lines.append(f"| {name} | {scenario['standalone']['coverage']['ranking_eligible']} | {scenario['eligible_added']} / "
            f"{scenario['eligible_removed']} | {scenario['standalone']['front_sizes']} | {scenario['eligible_sector_coverage']} |")
    lines.extend(['', '## G. Temporal provenance map', '',
        '| Field | Meaning | May establish observation epoch? |', '|---|---|---|',
        '| AgentCache.cached_at | Saved agent result cache time | No |',
        '| MarketDataCache.fetched_at / expires_at | Cache acquisition / TTL boundary | No |',
        '| History index | Market bar label; session/close event time unverified | Calendar label only |',
        '| SPY history index | Benchmark bar label | Calendar label only |',
        '| mostRecentQuarter / lastFiscalYearEnd | Provider period metadata in later supplement | No baseline metric/publication linkage |',
        '| AnalysisHistory.analyzed_at | Stock Analysis calculation time | No underlying FA observation lineage |',
        '| Capture timestamps | Read-only transaction boundaries | No market/financial epoch |',
        '| FA publication/observation/calculation/scoring version | Unrecorded in baseline | UNKNOWN |', '',
        'Baseline temporal diagnosis: ' + str({k:v for k,v in result['temporal_baseline'].items() if k not in ('candidates','timing_date_distribution')}), '',
        'Provider reporting dates, cache dates and full timing endpoints are retained in result JSON. No timestamp substitutes for another.',
        str(result['capture_provenance']), '',
        '## H. Common epoch reconstruction', '',
        '```json', json.dumps({k:v for k,v in result['common_epoch'].items() if k != 'endpoints'}, indent=2), '```', '',
        str(result['FA_temporal_alignment']), '',
        'BANPU constrains the latest shared date: its frozen 1y daily history contains no saved bars between August 11 '
        'and October 5; both its last valid Close and Volume are on October 5. CATL/300750.SZ ends September 30. '
        'The intersection therefore stops at August 11. Limiter witnesses above show the exact shared date possible '
        'without each limiting series. There is no observed instrument Close/Volume endpoint mismatch. '
        'The cause of the missing saved bars is UNPROVEN; no production scorer or cache was repaired.', '',
        'Alternative already-local BANPU histories were inspected: ' + str(result['alternative_history_diagnosis']), '',
        'The one-month history has one saved row; the three-month history has 28 valid Close rows, insufficient for SMA50; '
        'the five-year history ends June 30. None independently establishes a later complete Timing epoch. '
        'Splicing caches would need adjustment/version consistency not established here and was not attempted.', '',
        'Saved current cache history can be truncated. The local catalogue and AnalysisHistory metadata were inspected; '
        'AgentCache/MarketDataCache have unique current keys and no companion historical cache tables were found. '
        'AnalysisHistory stores aggregate analysis scores/times, not replayable underlying FA components and their observation dates. '
        'No full FA point-in-time reconstruction is justified.', '',
        '| History | Last row label | Last valid Close | Last valid Volume | Latest joint date |', '|---|---|---|---|---|'])
    for r in result['common_epoch'].get('endpoints', []):
        if r['last_valid_Close'] != r['last_valid_Volume'] or r['symbol'] == 'SPY':
            lines.append(f"| {r['symbol']} | {r['last_index']} | {r['last_valid_Close']} | {r['last_valid_Volume']} | {r['latest_joint_date']} |")
    lines.extend(['', '## I–J. Temporal sensitivity and candidate-set stability', '',
        'T0 uses original endpoints. T1 uses the latest shared UTC calendar date with complete canonical Timing inputs for all 89 '
        'listings and SPY. FA frozen. Algorithms and rolling observation-count windows unchanged. Combined B/T1 exposes interactions.', '',
        'T1 deliberately changes the market bar date to an earlier epoch. Churn therefore includes historical market movement; '
        'it cannot isolate a provenance-only effect or establish algorithm failure/outperformance. It establishes that baseline '
        'membership is not invariant to this defensible local-evidence scenario.', '',
        '| Scenario | Set | Actual | Intersection / union | Jaccard | Added | Removed |', '|---|---|---:|---|---:|---|---|'])
    for name, scenario in result['scenarios'].items():
        for set_name, c in scenario['comparisons'].items():
            lines.append(f"| {name} | {set_name} | {c['candidate_count']} | {c['intersection_count']} / {c['union_count']} | "
                f"{c['jaccard']:.4f} | {', '.join(c['added'])} | {', '.join(c['removed'])} |")
            lines.append(f"\nMembership: {scenario['candidate_sets'][set_name]['symbols']}. Sectors before/after: {c['sector_before']} / {c['sector_after']}.\n")
    for name, group in result['stability'].items():
        lines.extend([f"{name}: stable core ({group['stable_core_count']}): {group['stable_core']}; "
            f"sensitive edge ({group['sensitive_edge_count']}): {group['sensitive_edge']}.", ''])
    lines.extend(['Excluded/unresolved economic identities: all symbols lacking category A. Membership stability and evidence confidence '
        'are independent; a stable core does not clear unknown bindings or FA dates.', '',
        '## K. Important-case stability', '',
        'C5/C10/C15 triplets are Y/N. Final epistemic status can remain unresolved despite stable or sensitive membership.', '',
        '| Symbol | Identity | FA | Membership status / final status | Scenario: front, Timing, C5/C10/C15 |', '|---|---|---|---|---|'])
    for r in result['important_cases']:
        positions = '; '.join(f"{n}: F{p['front']}, T{p['timing']}, " + '/'.join('Y' if v else 'N' for v in p['memberships'])
                              for n,p in r['scenarios'].items())
        lines.append(f"| {r['symbol']} | {r['identity']} | {r['FA']} | {r['membership_status']} / {r['diagnostic_status']} | {positions} |")
    lines.extend(['', 'All important cases share unknown FA epoch/version and calendar-only Timing replay limitations. '
        'Every symbol’s raw score, percentile and Pareto front before/after is recorded under scenario movement.', '',
        '## L. Portfolio annotations', '',
        '| Scenario / set | Portfolio | Before held/new | After held/new | Locks |', '|---|---|---|---|---|'])
    for name, scenario in result['scenarios'].items():
        for set_name, comparison in scenario['comparisons'].items():
            for p in comparison['portfolio_annotations']:
                lines.append(f"| {name} / {set_name} | {p['portfolio_id']} | {len(p['before_held'])}/{len(p['before_new'])} | "
                    f"{len(p['after_held'])}/{len(p['after_new'])} | {p['locked']} |")
    lines.extend(['', 'Current feasibility UNPROVEN. Supplied historical holdings, locks and policy annotate candidates only. '
        'No valuation, position sizing, policy change or portfolio-aware ranking.', '',
        '## M. Production isolation', '',
        'Only explicit offline CLIs import this service. No runtime API, production agent or consumer imports/reads Discovery. '
        'Source AST loading reuses pure canonical definitions without initializing data_fetcher, AI clients or models.database. '
        'Supplement connection is REPEATABLE READ, READ ONLY; SELECT only; rollback and close in finally.', '',
        '## N. Validation', '', 'Exact commands and pass counts are recorded in SHADOW_CANDIDATE_DISCOVERY_SLICE1C.md. '
        'Preservation checks and both prior replays are enforced by this CLI before writing a separate result.', '',
        '## O. Open questions', '',
        '- Intended economic binding of all unbound listings, especially AIA06 and foreign-linked instruments.',
        '- Whether partial FA score cross-sectional comparability warrants a separate input contract.',
        '- FA observation/publication dates, component periods and cached scoring versions.',
        '- BANPU missing saved daily bars; calendar alignment versus economic session alignment.',
        '- Historical adjusted-price revisions and portfolio feasibility.', '',
        '## P. Decision questions', '',
        'Q1: Provider mappings agree locally but are canonically unbound; suspicious ETF identities remain unresolved, not proven mismatches.',
        'Q2: Strict complete-case is stricter than producer semantics. It is an experimental comparability constraint, not a canonical requirement.',
        'Q3: Existing optional-component behavior improves financial-sector admission in B without sector logic; validity does not prove comparability.',
        'Q4: A shared calendar-bar epoch is reconstructible from frozen local histories if reported supported above. Exact market-close epoch is UNPROVEN.',
        'Q5: FA point-in-time alignment is unsupported by current provenance.',
        'Q6: The exact C5/C10/C15 Jaccard and churn values are reported above for every supported scenario, including combined B/T1.',
        'Q7: Stable core sizes and members are reported separately per budget above; these are membership diagnostics.',
        'Q8: FA admission alone barely changes top candidate membership. Calendar alignment materially changes membership and '
        'Front 1 becomes MICRON/PTTEP; additive-score/Pareto structure remains intact. Earlier-date market movement is a confounder.',
        'Q9: Freeze algorithms for continued shadow research. Evidence/admission semantics remain unsettled; do not declare the shadow input contract mature.',
        'Q10: Investor Intent Slice 2 remains blocked; no production authority granted.', '',
        '## Q. Git state', '', 'No commits, staging, pushes, fetches, pulls or rebases. Final exact git status is in the implementation note.', '',
        '## R. Recommendation', '', result['verdict'], ''])
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capture', type=Path, required=True)
    parser.add_argument('--slice1-result', type=Path, required=True)
    parser.add_argument('--slice1b-result', type=Path, required=True)
    parser.add_argument('--slice1b-supplement', type=Path, required=True)
    parser.add_argument('--supplement', type=Path, required=True)
    parser.add_argument('--alternative-history', type=Path)
    parser.add_argument('--preservation', type=Path, required=True)
    parser.add_argument('--output-prefix', type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.preservation.read_text())
    validate_preservation(manifest)
    protected = {Path(n).resolve() for n in manifest} | {v.resolve() for k,v in vars(args).items()
        if isinstance(v, Path) and k != 'output_prefix'}
    outputs = [Path(str(args.output_prefix) + suffix) for suffix in ('.result.json', '.md')]
    if any(p.resolve() in protected for p in outputs):
        raise ValueError('cannot overwrite preserved inputs')
    capture = json.loads(args.capture.read_text())
    supplement = json.loads(args.supplement.read_text())
    if supplement['baseline_sha256'] != digest(args.capture):
        raise ValueError('supplement bound to another capture')
    if json.loads(json.dumps(compare_capture(capture))) != json.loads(args.slice1_result.read_text()):
        raise ValueError('Slice 1 replay changed')
    prior = json.loads(args.slice1b_result.read_text())
    replay = json.loads(json.dumps(refine_capture(capture, json.loads(args.slice1b_supplement.read_text()))))
    # Only checksum metadata, not semantic output, is added by Slice 1B CLI.
    if replay != {k:v for k,v in prior.items() if k not in ('baseline_capture_sha256', 'baseline_result_sha256')}:
        raise ValueError('Slice 1B replay changed')
    alternative = json.loads(args.alternative_history.read_text()) if args.alternative_history else None
    if alternative and alternative['baseline_sha256'] != digest(args.capture):
        raise ValueError('alternative history bound to another capture')
    result = investigate(capture, supplement, alternative)
    result['preserved_sha256'] = manifest
    result['supplement_sha256'] = digest(args.supplement)
    result['alternative_history_sha256'] = digest(args.alternative_history) if args.alternative_history else None
    outputs[0].write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    outputs[1].write_text(render_report(result), encoding='utf-8')
    validate_preservation(manifest)
    print(json.dumps({'version': result['integrity_version'], 'identity': result['identity_summary'],
        'common_epoch': {k:v for k,v in result['common_epoch'].items() if k != 'endpoints'},
        'stability': {k:{n:v for n,v in g.items() if n != 'excluded_unresolved'} for k,g in result['stability'].items()}}, indent=2))


if __name__ == '__main__':
    main()
