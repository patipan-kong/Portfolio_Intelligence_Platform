# Shadow Candidate Discovery — Slice 1

This is an offline experiment, not a shipped recommendation authority. Production
Stock Analysis, optimizer, policy, funding, sizing, accounting, APIs and UI are
unchanged. No production consumer imports these modules.

## Contract and experiment

- Contract: `wealth.shadow-discovery.v1`.
- Capture: `wealth.shadow-capture.v1`; comparison: `wealth.shadow-comparison.v1`.
- Experiment: `fa-timing-pareto.v1`.
- Pure core: `backend/services/candidate_discovery.py`.
- Captured-evidence adapters: `backend/services/candidate_discovery_evidence.py`.
- Explicit offline command: `backend/scripts/shadow_candidate_discovery.py`.

Input includes universe identity, UTC as-of/capture times, listing and optional
canonical identity, evidence values/inputs, observation/cache times, provenance,
limitations and source versions where known. `as_of` is the read-only transaction
capture boundary, **not** an assertion that every market fact was observed then.

FA uses saved `AgentCache.fundamental` output, not a new formula. Its actual
scoring version and financial observation date were not recorded by the cache;
the manifest's current fundamental-source digest does not prove that version
produced the historical cached value. Timing reuses the canonical
`timing_intelligence` indicator extraction and pure scoring functions over saved
`MarketDataCache` split-JSON history. SPY's saved `history:3mo:1d` is the existing
benchmark. No fetch function, cache helper, provider or AI client is called.

The adapter loads an explicit allowlist of canonical pure definitions from source
AST. It does not import executable production module setup. The source digests
must match the saved manifest for replay. This is a bounded offline dependency
mechanism; changes to the canonical definitions require deliberate review.

## Eligibility and mathematical semantics

Research needs an identified listing and at least one available supported
observation. A watchlist symbol identifies a listing; it does not invent a stable
asset ID. Asset IDs come from existing captured bindings. Canonical DR links come
only from effective `DEPOSITARY_RECEIPT_OF` records. Cached FA provider-parent
symbols remain explicitly noncanonical references.

Ranking requires stock-compatible evidence and complete FA and timing scoring
components for this experiment. FA components are PE, growth, ROE, debt/equity.
Timing components are price, SMA20, SMA50, RSI, current/average volume, stock
20-day return and SPY 20-day return. SMA200 is preserved but not required by the
numeric score. A raw default score can remain inspectable while availability is
false or inputs incomplete; it cannot enter ranking as an average observation.
Complete-case FA eligibility is experimental and can disproportionately exclude
banks whose debt/equity is absent. No claim is made that this is appropriate
production eligibility.

Cache expiry is reported, not converted to a new Discovery freshness threshold.
Expired and mixed-epoch observations are retained for **snapshot diagnostics**;
ranking eligibility does not establish current investment readiness. Benchmark
and instrument observation-date mismatches are explicit.

Over the eligible universe, each dimension reports competition rank and midrank
percentile: `100 * (strictly lower count + equal count / 2) / N`. Higher is
stronger. A singleton or all-equal universe is 50. Ties are preserved. Pareto
dominance requires at least as strong on both dimensions and strictly stronger
on one. Fronts peel nondominated sets. Symbols sort output only; they never
break score ties. The experimental shortlist is the entire first front, uncapped.
It does not mean BUY, allocation, expected outperformance or deployment readiness.

Portfolio overlay is returned separately. Captured current holdings and existing
`allow_swap=false` locks are authoritative facts; no Investor Intent is created.
Historic canonical valuation/policy snapshots are copied with source identities
and cannot assert current feasibility. Unknown policy returns `unknown`, not
unblocked. The pure overlay also accepts explicitly supplied current canonical
caps/weights and annotates reached caps without changing ranks. It does not
compute valuation or resolve a new policy.

## Offline commands

From repository root, PowerShell:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
.\.venv\Scripts\python.exe -B backend/scripts/shadow_candidate_discovery.py --capture-current --workspace-id 1 --output-prefix artifacts/shadow-discovery/2026-10-07-watchlist
.\.venv\Scripts\python.exe -B backend/scripts/shadow_candidate_discovery.py --input artifacts/shadow-discovery/2026-10-07-watchlist.capture.json --output-prefix artifacts/shadow-discovery/replay
```

Current capture supports configured PostgreSQL through `--env-file` (default
`backend/.env`). It uses one `REPEATABLE READ`, `READ ONLY` transaction, SELECTs
only, rollback and close. No credentials enter the artifacts. The command writes
only the requested local JSON/Markdown artifacts; it never updates DB/cache state.
Replay needs neither a database nor a network connection. Artifacts contain
local captured portfolio/evidence facts and remain uncommitted in this task.

Legacy comparison reuses `_compress_for_layer1` and `_L1_BUY_SIGNALS` from current
source. It reports captured-input gate/FA+TA order and unrestricted FA+TA order.
Exact current runtime selection is **UNPROVEN**: runtime can refresh expired agent
facts, source settings are not replayed, and its unordered watchlist query can
produce different cutoff ties. The offline capture fixes watchlist ID order.

## Validation

```powershell
$env:PYTHONPATH='backend'
$env:PYTHONDONTWRITEBYTECODE='1'
.\.venv\Scripts\python.exe -B -m pytest backend/tests/test_candidate_discovery.py -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m pytest backend/tests/test_timing_intelligence.py -q -p no:cacheprovider -k 'not regression'
git diff --check
```

Tests cover mathematical cases, missingness/defaults, order invariance, uncapped
ties, signal independence, overlay separation, actual registry relationship
vocabulary, producer source drift, legacy semantics and runtime import isolation.
The timing regression tests are excluded here because their fixture invokes a
native `pandas.date_range` path that crashes in this local environment. Canonical
pure timing tests and the new cached-history adapter tests pass independently.

## Initial 89-symbol diagnostic

Capture: 2026-10-07 06:54:51 UTC. Research eligible: 89. Ranking eligible: 79.
Ten have incomplete FA inputs, including one with no observed FA scoring
components; timing inputs are complete for all 89. All timing histories are
expired. Benchmark dates differ from every instrument's last close timestamp.

Legacy opinions: ACCUMULATE 58, WATCH 24, HOLD 7; gate eligible: 82.
Captured-input legacy top ten: CATL01.BK, PTT.BK, AMATA.BK, HMPRO.BK, AMZN01.BK,
GOOGL01.BK, AAPL01.BK, MSFT01.BK, META01.BK, PTTEP.BK.

Pareto fronts: 1, 1, 3, 3, 6, 6, 8, 7, 2, 4, 6, 9, 7, 7, 5, 2, 2.
First-front shortlist: MICRON01.BK (FA 7, timing 90), Technology, already held
in portfolio TA. Overlap with captured legacy top ten: zero. Eligible pairs:
2,103 dominance, 932 incomparable, 46 exact ties. These are differences in
evidence structure, not evidence of superior recommendations.

Review complete-case sector bias, observation alignment, FA coarseness and
shortlist breadth before advancing. No production ranking algorithm or shortlist
semantics have been chosen.
