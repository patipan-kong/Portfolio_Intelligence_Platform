# Shadow Discovery — Slice 1B refinement

Replay-only diagnostics extend Slice 1; no runtime consumer, new eligibility,
scoring formula, Investor Intent or production shortlist has been introduced.
Original Slice 1 source computations and capture/result/report remain intact.

## Findings before eligibility changes

All ten FA exclusions were inspected before changing anything. Eight provider
EQUITY profiles (five regional banks, two life insurers, one credit-services
business) lack debtToEquity. AIA06.BK's cached parent AIA and GOLDM01.BK's cached
parent GLDM have provider ETF profiles. AIA lacks growth/ROE/debt; GLDM also lacks
PE. Their stock/DR binding and corporate-FA profile warrant separate review.

The frozen capture does not contain raw provider info or industry. A separate
SELECT-only, repeatable-read/read-only supplemental capture obtained already
local raw fundamental cache rows for these ten symbols. It is bound to the
original capture hash, is diagnostic only, and never contributes ranking facts.
Missing fields are absent/null in those rows, not lost by the Discovery adapter.
This does not prove those rows were the original inputs to the baseline FA agent.
Publication/observation times for the baseline financial metrics remain unknown.

Source `agents/fundamental.py` obtains PE from trailingPE or forwardPE, growth from
revenueGrowth, ROE from returnOnEquity and debt/equity from debtToEquity. It skips
missing metrics and has no sector-specific applicability contract. Therefore no
financial-sector exception is implemented: research/ranking eligibility stays
89/79. Provider missingness is evidenced; economic inapplicability is unresolved.

## Versioned diagnostics

`wealth.shadow-discovery-refinement.v1` lives in
`backend/services/candidate_discovery_refinement.py`. It reports:

- FA/Timing leaders, boundary ties, percentiles and held/new annotations.
- Dimension distinct-value/tie counts and joint maxima.
- Pareto front sizes, cumulative sizes, pair relationships and sectors.
- Timing bar-age distributions and benchmark/index/calendar-date differences.
- Unknown FA observation/reporting/scoring epochs; no freshness classification.
- Candidate-set comparisons and full difference lists against the captured
  legacy gate/top ten and unrestricted FA+TA top ten. Full unrestricted ordering
  remains in the embedded baseline.
- Important cases, diagnostic-only label distributions, and portfolio annotations.

Last history index is a daily-bar label, not proven close-event time. All 89
baseline timing caches expired; 68 instruments share the benchmark's UTC calendar
date, 21 do not, and no instrument has the same index timestamp as SPY. Intraday
label differences cannot themselves prove session misalignment. No market-calendar
or new freshness policy is invented. Full aligned point-in-time/current-opportunity
comparison is unsupported, although structural captured-score comparisons work.

## Candidate-set experiments

There is no default candidate set.

1. Front 1 only: diagnostic baseline, not the default shortlist.
2. Cumulative Pareto: include entire fronts until the TOTAL requested budget is
   reached, preserving the complete boundary front and reporting overshoot.
3. Dimension-leader union: union the top requested count PER DIMENSION, preserving
   all boundary ties. Nominal union bound is twice the per-dimension budget before
   duplicate removal; boundary ties can exceed it. This parameter is explicitly
   different from the cumulative total budget. No weighted score is introduced.

Budgets 5/10/15 are experiments, not recommendations. Cumulative actual counts
are 5/14/20 (overshoot 0/4/5). Dimension-union counts are 14/26/30, with nominal
bound excess 4/6/0. Front 1 contains MICRON01.BK alone because it has maximum FA
and ties maximum timing in the eligible captured cohort. Mathematical dominance
is not expected outperformance or portfolio suitability.

Portfolio counts after known hard restrictions are not confirmed feasible:
current policy/exposure cannot be reconstructed from historical annotations.
Existing PIS.BK lock is preserved. No portfolio context changes relative results.

## Reproduce without database or network access

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
.\.venv\Scripts\python.exe -B backend/scripts/shadow_candidate_discovery_refinement.py --capture artifacts/shadow-discovery/2026-10-07-watchlist.capture.json --baseline-result artifacts/shadow-discovery/2026-10-07-watchlist.result.json --supplement artifacts/shadow-discovery/2026-10-07-slice1b.fa-supplement.json --budgets 5 10 15 --output-prefix artifacts/shadow-discovery/2026-10-07-slice1b
$env:PYTHONPATH='backend'
.\.venv\Scripts\python.exe -B -m pytest backend/tests/test_candidate_discovery.py backend/tests/test_candidate_discovery_refinement.py -q -p no:cacheprovider
git diff --check
```

The command verifies that canonical source/dependency versions still match the
capture and that baseline replay equals the saved Slice 1 result. It refuses to
overwrite original baseline inputs/report. The new artifacts are named separately.

No expected-return superiority is established. Resolve identity/profile concerns,
FA applicability and temporal provenance before advancing to Slice 2 or introducing
another dimension merely to force a preferred result.
