# Slice 1C — Evidence integrity and candidate-set stability

Implemented October 7, 2026, on `feature/wealth-os-shadow-candidate-discovery`.
Shadow-only, offline evidence investigation. No algorithm redesign or production integration.

The complete A–R evidence report is `artifacts/shadow-discovery/2026-10-07-slice1c.md`.
The machine-readable report is the sibling `.result.json`. All 89 identity lineages,
field classifications, scenario inputs/results, relative positions, front movement,
membership differences, sector composition, and portfolio annotations are retained there.

## A. Entry/worktree state

HEAD: `653a3ed75247342c88b7b7ca2a78ff6dcf4aec4a`.
Locally known origin/main: `a04a02b7bfb0a33aede40f5ac30d163d3f297563`; no fetch.
Entry status:

```text
 M backend/ai-model.json
?? artifacts/
?? backend/scripts/shadow_candidate_discovery.py
?? backend/scripts/shadow_candidate_discovery_refinement.py
?? backend/services/candidate_discovery.py
?? backend/services/candidate_discovery_evidence.py
?? backend/services/candidate_discovery_refinement.py
?? backend/tests/test_candidate_discovery.py
?? backend/tests/test_candidate_discovery_refinement.py
?? docs/implementation/SHADOW_CANDIDATE_DISCOVERY_SLICE1.md
?? docs/implementation/SHADOW_CANDIDATE_DISCOVERY_SLICE1B.md
```

Existing artifacts: `2026-10-07-watchlist.capture.json`, `.result.json`, `.md`,
and `2026-10-07-slice1b.fa-supplement.json`, `.result.json`, `.md`.

## B. Baseline preservation

`2026-10-07-slice1c.preservation.json` records SHA-256 of all six prior artifacts,
all five prior offline service/CLI files, and ai-model.json before edits.
The replay CLI validates every checksum both before and after writing distinct Slice 1C outputs.
Original Slice 1 and 1B semantic replays must equal saved JSON. Tuple serialization
is normalized through JSON; only Slice 1B's two file-checksum metadata keys are excluded.
No result fields are omitted from that comparison.

ai-model.json SHA-256 remains
`DB39FDA7F8ED717D1C17AD597526FB1CA477BA5E64360F7CA6152AFD561FA256`.
Baseline: universe/research 89, ranking 79, excluded 10; labels 58 ACCUMULATE,
24 WATCH, 7 HOLD. All original scores, fronts, extraction semantics and legacy comparisons preserved.

## C. Added/changed files

- `backend/services/candidate_discovery_integrity.py`: pure offline identity,
  producer-semantics, applicability, epoch reconstruction and scenario/stability diagnostics.
- `backend/scripts/shadow_candidate_discovery_integrity.py`: frozen replay and full A–R report;
  baseline/checksum verification and protected output paths.
- `backend/scripts/capture_candidate_discovery_integrity.py`: optional local-only supplemental
  SELECT capture; repeatable-read READ ONLY transaction, rollback/close even on error.
- `backend/tests/test_candidate_discovery_integrity.py`: 39 focused tests.
- This implementation note and five Slice 1C artifacts: preservation manifest,
  local supplement, BANPU alternative-history supplement, result JSON and report Markdown.
- Only prior-file change: three offline module names added to the production import-guard
  allowlist in `backend/tests/test_candidate_discovery.py`. No prior implementation file changed.

## D–F. Identity and FA authority

All 89 watchlist asset_id fields are null. Registry rows sharing listing symbols
do not establish bindings. Captured relationships are empty. Counts: 68
canonical_binding_missing, 21 provider_parent_mapping_only; all category B,
zero category A or C. Agreement between saved FA parent and saved Timing provider
key supports provider consistency, not canonical economic equivalence.

All 21 foreign-linked cases appear in the full report. MICRON→MU, INTEL→INTC,
CATL→300750.SZ, SMIC→0981.HK and GOLDM→GLDM use explicit resolver mappings;
other captured DR parent mappings use generic suffix removal. PIS.BK remains PIS.BK.
Profiles identify AIA as iShares Asia 50 ETF, GLDM as SPDR Gold MiniShares Trust.
Neither ETF profile proves a mismatch with an intended underlying absent canonical evidence.
No category-C exclusion scenario is justified for the captured universe.

Concrete FA path: provider.get_fundamentals → fetch_info(normalize_dr_symbol(listing))
→ analyze_fundamental → AgentCache.result_json.{fa_score,pe_ratio,revenue_growth,roe,debt_equity}
→ offline adapter Evidence → complete-case admission → discover percentiles/fronts
→ cumulative candidate sets. Historical provider-response linkage and cached scorer version UNPROVEN.
New supplemental provider metadata is used for diagnostics only, never scores or admission.

`backend/agents/fundamental.py` starts score at zero and skips each missing component.
It fails only for empty info, and can return a successful score with all four components absent
when info contains other metadata. Source AST execution with controlled local info proves PE-only
score 2 and all-component-missing score 0; it never fetches data. Missing metric values remain None.
No sector applicability/mandatory metric or sector replacement profile exists in this producer.
YahooChartProvider delegates fundamentals to its legacy provider; YahooProvider returns ticker.info.
Neither supplies producer-level missing versus not-applicable classification.
Repository tests and inspected architecture docs do not supply an alternative financial-sector scorer.

Strict complete-case is therefore stricter than canonical producer semantics. B admits successful
finite persisted scores unchanged, including GOLDM's saved zero, while retaining component missingness
in inputs and the separate applicability report. This is sensitivity admission, not new scoring,
imputation, economic suitability or evidence that partial and complete scores are comparable.
Financial Services coverage rises 7→15; AIA and GOLDM retain their captured sector fallback values
(Financial and Other). No sector taxonomy repair was made.

## G–I. Temporal findings

Cache time, fetch time, expiry, market/benchmark bar labels, provider financial period metadata,
Stock Analysis analyzed_at, capture time and unknown historical FA calculation dates remain distinct.
All 89 baseline FA observation dates and scorer versions are unknown; all 89 Timing caches are expired.
8,758 local AnalysisHistory rows contain aggregate technical/fundamental/news/risk/valuation scores.
They do not reconstruct source FA metrics, observation dates or scorer versions.
The local table catalogue has agent_cache, market_data_cache and analysis_history;
the cache models use unique current keys, with no historical companion cache tables found.

T1 uses all 89 captured listings plus SPY, requiring a shared UTC calendar date with
valid Close and Volume on instrument bars, sufficient canonical rolling inputs and a valid SPY return.
Latest supported common date: **2026-08-11**, among 27 shared dates.
Canonical _extract_indicators/compute_timing_score run over original saved histories truncated at that date.
Original FA remains identical; scoring/percentiles/Pareto and budgets remain identical algorithms.
Different exchange session times, observation-count return windows, provider adjustments and later acquisition
prevent exact synchronous or full point-in-time interpretation.

BANPU's frozen 1y history has no saved bars between August 11 and October 5; both its last valid
Close and Volume are on October 5. CATL/300750.SZ ends September 30. The full-universe intersection
therefore stops at August 11. Excluding BANPU's series from the intersection permits September 30,
which is recorded as a diagnostic limiter witness, not an exclusion scenario.
No instrument in the capture has an observed Close/Volume endpoint mismatch. The cause of the saved
history gap is UNPROVEN; no scorer or cache was repaired.

A distinct local supplement inspects alternative BANPU daily histories: 1mo contains one row;
3mo contains 28 valid Close rows and lacks SMA50; 5y ends June 30. None independently
supports a later complete canonical Timing epoch. No cache splicing, backfill or fresh fetch occurred.
T1 is a historical calendar-bar replay: churn includes market movement across dates and does not
isolate a provenance-only effect or establish algorithm quality/outperformance.
FA alignment remains unsupported.

## J–K. Stability

All four scenarios are isolated copies. Algorithms remain frozen.

| Scenario | Eligible | C5 count/Jaccard | C10 count/Jaccard | C15 count/Jaccard |
|---|---:|---|---|---|
| A.strict.T0.v1 | 79 | 5 / 1.0000 | 14 / 1.0000 | 20 / 1.0000 |
| B.producer-valid.T0.v1 | 89 | 5 / 1.0000 | 14 / 1.0000 | 21 / 0.9524 |
| A.strict.T1.v1 | 79 | 7 / 0.0909 | 14 / 0.2727 | 24 / 0.3750 |
| B.producer-valid.T1.v1 | 89 | 8 / 0.0833 | 16 / 0.2500 | 16 / 0.2414 |

Stable cores across all four:

- C5: MICRON01.BK (1).
- C10: AMZN01.BK, MICRON01.BK, NVDA01.BK, PTT.BK, PTTEP.BK, TOP.BK (6).
- C15: those six plus CATL01.BK (7).

Sensitive edges contain 11/18/28 symbols respectively. Economic binding remains unresolved for all 89;
membership stability does not remove that uncertainty. Every requested important case has identity,
FA completeness/applicability, temporal limitation, per-scenario front/raw Timing/percentile/membership,
membership status and separate final epistemic diagnostic status in the full report/JSON.
The final status is unresolved where canonical economic binding is unavailable, even for stable membership.
Front 1 changes from MICRON alone to MICRON/PTTEP in T1. FA-only admission does not change Front 1.

## L–M. Portfolio and production isolation

Holdings, locks and captured policy/exposure annotate standalone results only. The full report gives
before/after held/new by portfolio and budget for every scenario. Current feasibility is UNPROVEN.
PIS's lock in portfolio 3 remains an annotation whenever PIS is selected.
No valuation, cash, NAV, position sizing, policy or allocation recalculation occurs.

Stock-level absolute FA/Timing evidence feeds cross-sectional percentile/Pareto diagnostics.
Portfolio awareness is an independent annotation, not ranking authority. No fields are serialized
into AI prompts, displayed in a production UI or delivered to any 3L layer.
No Stock Analysis label affects identity, applicability, fronts, membership or stability.
Production import/read guards examine backend runtime source, including string paths.
Read-only supplemental capture tests assert SELECT only and cleanup on both success and failure.
No API/schema/frontend/production consumer changed. No paid AI or live market call occurred.

## N. Tests and validation

Commands run sequentially from the repository, with these environment variables:

```powershell
$env:PYTHONPATH='backend'
$env:PYTHONDONTWRITEBYTECODE='1'
.\.venv\Scripts\python.exe -B -m pytest backend/tests/test_candidate_discovery.py backend/tests/test_candidate_discovery_refinement.py backend/tests/test_candidate_discovery_integrity.py -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m pytest backend/tests/test_timing_intelligence.py backend/tests/test_symbol_resolver.py -k 'not regression' -q -p no:cacheprovider
```

Results: **99 passed** (34 Slice 1 + 26 Slice 1B + 39 Slice 1C), one existing pandas_ta deprecation warning.
Existing pure Timing/resolver checks: **64 passed, 3 deselected**, three dependency/deprecation warnings.
The three deselected regressions use the known native-crashing date-range fixture; no full suite run.
Canonical FA behavior is validated through source AST in focused Slice 1C tests.

Frozen replay command:

```powershell
.\.venv\Scripts\python.exe -B backend/scripts/shadow_candidate_discovery_integrity.py --capture artifacts/shadow-discovery/2026-10-07-watchlist.capture.json --slice1-result artifacts/shadow-discovery/2026-10-07-watchlist.result.json --slice1b-result artifacts/shadow-discovery/2026-10-07-slice1b.result.json --slice1b-supplement artifacts/shadow-discovery/2026-10-07-slice1b.fa-supplement.json --supplement artifacts/shadow-discovery/2026-10-07-slice1c.local-supplement.json --alternative-history artifacts/shadow-discovery/2026-10-07-slice1c.banpu-history-supplement.json --preservation artifacts/shadow-discovery/2026-10-07-slice1c.preservation.json --output-prefix artifacts/shadow-discovery/2026-10-07-slice1c
```

Initial local supplement command:

```powershell
.\.venv\Scripts\python.exe -B backend/scripts/capture_candidate_discovery_integrity.py --capture artifacts/shadow-discovery/2026-10-07-watchlist.capture.json --output artifacts/shadow-discovery/2026-10-07-slice1c.local-supplement.json
```

The BANPU alternative supplement was captured with an explicit ephemeral Python SELECT script,
repeatable-read READ ONLY, rollback/close, three daily history keys only; no writes or refresh.
Both supplement files state their reason, transaction boundary and original capture checksum.

Syntax/import validation, deterministic frozen replay, all manifest checksums, new-file whitespace check,
`git -c safe.directory=G:/work/ta/stock-analysis diff --check`, and `graphify update .` completed.
Replay imports do not initialize services.data_fetcher or models.database.
No parallel test runners or subagents used.

## O–P. Open questions and decision answers

Q1: Provider identities agree locally but economic bindings remain unproven. ETF cases are unresolved,
not demonstrated mismatches.

Q2: Strict completeness is stricter than producer semantics; it is a research comparability choice.

Q3: Existing optional-component semantics increase financial coverage, without invented sector finance logic.
Whether partial raw scores deserve cross-sectional authority remains unresolved.

Q4: Calendar-bar alignment is supported at August 11; exact synchronous close-time alignment is unproven.

Q5: FA point-in-time alignment cannot be established from available provenance.

Q6: FA-only C5/C10 remain unchanged; C15 adds AIA. T1 produces substantial churn, with exact Jaccards above.
Combined admission/time scenarios expose further boundary changes. This is sensitivity, not a winner decision.

Q7: Stable cores contain 1/6/7 members for C5/C10/C15, all still economically unbound.

Q8: Admission alone scarcely alters top sets. Calendar-date replay materially alters memberships and Front 1,
while preserving the same mathematical structure. Date movement is a confounder.

Q9: Keep algorithms frozen for shadow research, but do not declare the evidence/admission contract mature
or ready for a production-authority second-opinion milestone. A review can inspect these unresolved findings.

Q10: Investor Intent Slice 2 remains blocked.

Open questions: issuer/underlying registry lineage, partial-score comparability, component periods and publication dates,
cached scorer versions, missing saved daily bars, adjustment history and current portfolio feasibility.

## Q. Final git status

```text
 M backend/ai-model.json
?? artifacts/
?? backend/scripts/capture_candidate_discovery_integrity.py
?? backend/scripts/shadow_candidate_discovery.py
?? backend/scripts/shadow_candidate_discovery_integrity.py
?? backend/scripts/shadow_candidate_discovery_refinement.py
?? backend/services/candidate_discovery.py
?? backend/services/candidate_discovery_evidence.py
?? backend/services/candidate_discovery_integrity.py
?? backend/services/candidate_discovery_refinement.py
?? backend/tests/test_candidate_discovery.py
?? backend/tests/test_candidate_discovery_integrity.py
?? backend/tests/test_candidate_discovery_refinement.py
?? docs/implementation/SHADOW_CANDIDATE_DISCOVERY_SLICE1.md
?? docs/implementation/SHADOW_CANDIDATE_DISCOVERY_SLICE1B.md
?? docs/implementation/SHADOW_CANDIDATE_DISCOVERY_SLICE1C.md
```

Branch/HEAD unchanged. No staging, commits, pushes, fetches, pulls or rebases.

## R. Recommendation

EVIDENCE INTEGRITY MIXED — CONTINUE SHADOW DISCOVERY RESEARCH

## S. Errata — adversarial review corrections (2026-10-07, documentation only)

Applied after the second-reviewer adversarial review. No algorithm, score,
admission rule, artifact or frozen function was changed, and no new research
was run. Every number below is read from the existing
`2026-10-07-slice1c.result.json` (SHA-256 in
`SHADOW_CANDIDATE_DISCOVERY_ARTIFACT_MANIFEST.md`). Where this section
conflicts with sections above, this section governs.

1. **Freeze candidate.** Only the strict scenario (`A.strict.T0.v1`) is a
   freeze candidate. Producer-valid scenarios (`B.*`) are diagnostic and
   non-authoritative and must not become an admission contract.
2. **No-data FA admission (correction to "no imputation").**
   `producer_valid_snapshot` admits any finite saved `fa_score`, including a
   score computed from zero observed components. `GOLDM01.BK` (FA 0, all four
   components absent) is admitted, and in `B.producer-valid.T1.v1` it sits on
   Pareto front 3 and enters C5 and C10. The B-scenario test
   (`all_missing=True`) codifies this; it documents behaviour, not a valid
   ranking feature.
3. **Missing-component scoring, described accurately.** `analyze_fundamental`
   starts at 0 and adds nothing for an absent component. Because 0 is also a
   real bucket value (P/E 25–40, revenue growth 0–5%, ROE 0–10%, D/E 50–200),
   a missing component is scored as the middle bucket — functionally
   zero-imputation of the score contribution. Score ranges therefore differ by
   observed-component set (all four: −4…7; D/E missing: −3…6; none: always 0).
   In addition, P/E is `trailingPE or forwardPE`, so even "complete" rows mix
   two metrics that `missing_inputs` cannot distinguish. Partial and complete
   FA scores are not shown to be cross-sectionally comparable.
4. **Same-epoch admission sensitivity (correction to Q8).** "Admission alone
   scarcely alters top sets" holds at T0 only. Comparing `A.strict.T1.v1` with
   `B.producer-valid.T1.v1` (same epoch; not reported above because scenarios
   were only compared with A.T0): C5 Jaccard 0.875 (+GOLDM01), C10 0.875
   (+GOLDM01, +TISCO), **C15 0.538** — C15 shrinks from 24 to 16 members and
   drops ABNB06, AMATA, AP, ASML01, ASP, BDMS, HMPRO, KTC, PIS, RATCH. Adding
   instruments can shrink a cumulative-front set.
5. **Producer-valid T0 C15 change.** The C15 Jaccard of 0.952 at T0 is caused
   solely by admitting `AIA06.BK`, scored on P/E alone.
6. **Identity check is not independent (correction to D–F and Q1).** The
   "agreement" between FA parent, Timing symbol and provider symbol compares
   three values all produced by `symbol_resolver.resolve_yfinance_symbol`.
   It can detect resolver drift, not a consistently wrong mapping. "Zero
   category C" does not establish the absence of identity conflicts.
7. **AIA06.BK — suspected identity risk.** Generic suffix stripping maps it
   to `AIA`, which the provider profile names "iShares Asia 50 ETF"; the cached
   FA has `market_cap=None` and only P/E present (ETF-consistent), while the
   watchlist and FA sector say "Financial". Treat as a suspected category-C
   identity risk, excluded from any authoritative use. (If production
   resolves it the same way, production Stock Analysis for AIA06 may analyse
   the wrong instrument — a separate production follow-up, not fixed here.)
8. **GOLDM01.BK — asset-type/admission leak.** The explicit mapping to `GLDM`
   is plausibly correct economically, but it is an ETF ranked on corporate FA.
   `supported_stock_evidence` treats "an FA cache row exists" as supported
   equity evidence when `asset_type` is unknown, so the asset-type gate does
   not exclude ETFs.
9. **Timing benchmark (limitation not stated above).** Every instrument,
   including SET listings and CNY-quoted `300750.SZ`, uses SPY for the
   relative-strength component (inherited from production); DR Timing uses the
   foreign parent's price series, not the THB DR. This is a cross-sectional
   comparability limit between SET and foreign-parent instruments.
10. **Replay.** FA used in the 2026-08-11 replay was cached 2026-10-06/07
    (look-ahead, consistent with "FA frozen"); daily bars are labelled at
    session open, so the UTC calendar date equals the local session date (no
    date-offset defect). Current FA combined with historical Timing is
    therefore not a point-in-time investment backtest.

Status: algorithms frozen; prior artifact checksums unchanged (verified against
`2026-10-07-slice1c.preservation.json`). The Discovery experimental track is
complete as a shadow record subject to these corrections.
