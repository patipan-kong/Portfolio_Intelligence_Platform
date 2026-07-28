# M43-WP1 — Roadmap and Current-State Reconciliation

**Milestone:** M43 — Portfolio Analytics Contract Foundation
**Work package:** M43-WP1 only
**Artifact class:** Specification and current-state evidence
**Status:** `CORRECTED AFTER INDEPENDENT REVIEW — REQUIRES INDEPENDENT CONFIRMATION`
**Runtime authority:** `NONE`
**Source-code authority:** `NONE`
**Persistence/API/UI authority:** `NONE`
**Implementation authority:** `NONE`
**Provider authority:** `NONE`
**Production-method authority:** `NONE`
**Executable-validation authority:** `NONE`

## 1. Controlling authority and scope

This artifact implements only the current-state and roadmap-reconciliation
portion of the frozen
[M43 Architecture and Implementation Plan](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
§9, WP1. It must be read with the companion
[M43-WP1 Portfolio Analytics Vocabulary and Ownership Register](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md).
The commissioning authority’s `COMPLETE AND FROZEN` architecture status and
Independent Constitutional Confirmation `APPROVED` record, together with the
repository-local status-synchronization limitation, are recorded in the
companion register §1.

The governing baseline is:

- the Platform Architecture Laws 1–15 and domain allocations, especially
  §§6.2, 6.3, 6.5, 6.7, 6.8, and 6.9;
- frozen M34 decisions, especially `M34-D-0004`, `M34-D-0005`, and
  `M34-D-0010`;
- frozen M39 observation contracts;
- frozen M40–M41 Market Measure vocabulary and contracts;
- frozen M42 Portfolio vocabulary, contracts, and closeout;
- ADR-001 through ADR-005; and
- [Portfolio Calculation Rules](../investment/PORTFOLIO_CALCULATION_RULES.md).

This document inventories deployed reality under Constitution G6. Nothing in
the inventory is an architectural precedent, an admission, a compatibility
promise, or permission to preserve a behavior.

## 2. Roadmap reconciliation

M43 remains the specification-only bridge from M42 Portfolio Composition to a
future, separately authorized Portfolio Analytics implementation:

```text
M39 Market Observation
        +
M40–M41 Market Measure
        +
M42 Portfolio Composition
        ↓
M43 non-production Portfolio Analytics contracts
```

The roadmap findings are:

| Roadmap concern | WP1 finding | Consequence |
| --- | --- | --- |
| Rolling Analytics | Vocabulary may be established, but no rolling method, formula, registry entry, endpoint, or implementation is admitted | No capability-completion mark |
| Advanced Risk Metrics | Vocabulary may be established, but no risk method or statistical convention is admitted | No capability-completion mark |
| Position Attribution | Vocabulary may be established, but no contribution or attribution method is admitted | No capability-completion mark |
| Sector Attribution Timeline | Vocabulary may be established, but no grouping choice, method, or timeline contract is admitted | No capability-completion mark |
| M42 Portfolio Composition | Remains the only permitted governed Portfolio subject | No legacy ORM object or Current Selection may substitute |
| Future executable analytics | Remains a successor-milestone concern | No runtime, source, persistence, API, or UI authority arises here |

`docs/architecture/ROADMAP.md` must not be changed by WP1. M43 deploys none of
the four roadmap capabilities.

## 3. Current-state source inventory

### 3.1 Accounting-derived period evidence

| Source | Current behavior | Architectural disposition |
| --- | --- | --- |
| `backend/services/portfolio_metrics.py` | Sole current implementation of the nine period-return `PortfolioSnapshot` fields, including `investment_return_pct` and its `daily_return_pct` alias | `CHARACTERIZE`; current code has no M43 contract or production-method admission |
| `backend/services/portfolio_snapshots.py` | Supplies the live incremental window and persists snapshot derivatives | `CHARACTERIZE`; Ledger-derived evidence only |
| `backend/services/portfolio_rebuilder.py` | Supplies replay windows and delegates period arithmetic | `CHARACTERIZE`; no Portfolio Analytics authority |
| `backend/services/snapshot_return_recovery.py` | Recalculates return fields and delegates period arithmetic | `CHARACTERIZE`; repair/recovery is not an M43 method |
| `backend/services/snapshot_repair.py` | Repairs snapshot derivatives and delegates return calculations | `CHARACTERIZE`; no result-contract precedent |
| `backend/models/database.py::PortfolioSnapshot` | Persists NAV and period-return-related fields; `daily_return_pct` and `investment_return_pct` are currently semantic aliases | `LEGACY EVIDENCE`; not an immutable M43 Portfolio Measure Result |

ADR-004 establishes one current implementation of the period-return fields.
It does not determine the constitutional semantic owner of a Portfolio
performance measure. The ownership finding is recorded in the companion
register §7.

### 3.2 Portfolio analytics formulas and duplicate rules

| Source | Formula or behavior found | Collision or duplication finding |
| --- | --- | --- |
| `backend/services/analytics/quant_engine.py` | TWR, annualized return, maximum drawdown, volatility, Sharpe, monthly win rate, alpha, beta, correlation, tracking error, information ratio, sector contribution, concentration, equity curve, rolling returns | Multiple Portfolio analytics rules in one legacy module; no Definition identity, Method Version identity, closed manifest, result identity, or provenance contract |
| `backend/services/analytics/attribution_engine.py` | A separate TWR chain in `_compute_twr()`, a normalized Portfolio return series in `compute_actual_indexed_series()` with a raw two-point NAV-ratio fallback, maximum drawdown, annualized volatility, Portfolio/shadow comparison, timing/fee/override effects, and residual reconciliation | Duplicates period return, normalized return-series construction, drawdown, and volatility; the raw-NAV fallback is rejected as precedent; the module also combines Portfolio contribution with Trust & Evaluation and human-vs-AI semantics that M43 excludes |
| `backend/services/timing_performance.py` | A separate TWR chain, benchmark return, excess return, and maximum drawdown | Duplicates TWR and drawdown; uses an ambient current date and a default request benchmark |
| `backend/services/decision_memory/attribution.py` | BHB-labeled attribution stub and stored alpha components | BHB and benchmark-relative attribution are explicitly excluded from M43; current stub is not precedent |
| `backend/services/decision_memory/shadow_tracker.py` | `_benchmark_return_pct()` independently calculates benchmark return | Additional benchmark-return implementation; `CHARACTERIZE` only and not precedent |
| `backend/main.py` performance-comparison path | Rebuilds a normalized Portfolio return series, falls back from `investment_return_pct` to `daily_return_pct`, then to `0.0` | Parallel return-series composition and silent flat-return fallback; inadmissible as canonical M43 behavior |
| `frontend/components/EquityCurveChart.tsx` | Computes drawdown from a high-water mark in the Experience layer | Direct conflict with Platform Architecture §6.9; presentation may render but must not compute |
| `frontend/components/analytics/EquityCurveChart.tsx` | Computes drawdown and daily-return tooltip values | Direct Experience-layer calculation; current-state defect, not precedent |

The duplicate-rule map is therefore:

| Rule family | Current locations with independent logic | WP1 classification |
| --- | --- | --- |
| Period return | `portfolio_metrics.py` (canonical current implementation); `quant_engine.py`, `timing_performance.py`, and `attribution_engine.py::_compute_twr()` chain returns; `attribution_engine.py::compute_actual_indexed_series()` and `main.py` also build normalized Portfolio return series | Existing lower-level rule plus multiple independent chains and consumers; ownership resolved in companion register, call-site design deferred to WP9 |
| Maximum drawdown | `quant_engine.py`; `attribution_engine.py`; `timing_performance.py`; frontend chart components | Duplicate implementation confirmed |
| Volatility | `quant_engine.py`; `attribution_engine.py` | Duplicate implementation confirmed |
| Benchmark return/alignment | `quant_engine.py`; `timing_performance.py`; `main.py`; `decision_memory/attribution.py`; `decision_memory/shadow_tracker.py::_benchmark_return_pct()` | Duplicate and inconsistent alignment/default behavior confirmed |
| Attribution | `analytics/attribution_engine.py`; `decision_memory/attribution.py`; related evaluation consumers | Semantic overlap across Portfolio Intelligence and Trust & Evaluation confirmed |
| Sector contribution/grouping | `quant_engine.py`; attribution paths; presentation consumers | Classification versus Analytical Grouping authority is not explicit |

This map does not select a future call site, package, library, or method. That
would be WP9 implementation-design authority.

### 3.3 Defaults, fallbacks, ambient state, and provider knowledge

| Current behavior | Evidence | Canonical M43 disposition |
| --- | --- | --- |
| Hard-coded annualization basis | `quant_engine.py` uses `252` and `sqrt(252)` | `REJECT AS PRECEDENT`; WP4 must establish a governed authority and binding rule |
| Hard-coded risk-free rate | `calculate_sharpe_ratio(..., risk_free_rate=0.025)` | `REJECT AS PRECEDENT`; not caller-defaultable or ambient |
| Short-history threshold | `_MIN_DAYS_FOR_ANNUALIZATION = 30` | `CHARACTERIZE ONLY`; no M43 threshold admitted |
| Raw-NAV fallback | `quant_engine.py::_daily_returns()` falls back to `total_value.pct_change()`; `attribution_engine.py::compute_actual_indexed_series()` falls back to a raw two-point `last.total_value / first.total_value` ratio | `REJECT AS PRECEDENT`; no fallback from missing cash-flow-adjusted evidence |
| Legacy alias fallback | several paths use `investment_return_pct` or `daily_return_pct` | `CHARACTERIZE ONLY`; no equivalence is admitted by M43 |
| Flat-return fallback | performance comparison substitutes `0.0` when both return fields are absent | `REJECT`; absence must be loud |
| Request-selected benchmarks | `/analytics/performance-comparison`, `/analytics/performance-stats`, and timing endpoints accept benchmark symbols | `LEGACY EXPLORATORY ONLY`; cannot replace Portfolio Benchmark Declaration |
| Default benchmark symbols | `^SET.BK`, `QQQ`, `^GSPC` appear as defaults in routes and services | `REJECT AS CANONICAL INPUT` |
| Provider identifiers and fetches | `benchmark_service.py` stores/fetches Yahoo Finance symbols through `yfinance` | Provider-level evidence path only; never a canonical Portfolio calculation input |
| Wall-clock dates | `date.today()` and `datetime.utcnow()` define windows or result timestamps in legacy analytics | `REJECT AS CANONICAL SEMANTIC INPUT`; exact governed time evidence is required |
| Forward fill / LOCF | performance comparison carries benchmark values across missing dates | `CHARACTERIZE ONLY`; no M43 missing-data method admitted |
| Sector fallback | current paths use static maps, cached provider fields, or `"Other"` | `REJECT AS ATTRIBUTION AUTHORITY`; exact Asset Classification or Analytical Grouping authority is required |

### 3.4 Caches, persistence, and operational behavior

| Surface | Current state | WP1 finding |
| --- | --- | --- |
| Analytics cache | `quant_engine.py` owns a process-local 15-minute cache keyed by Portfolio and group | Private cache confirmed; no M43 cache authority |
| Snapshot persistence | `PortfolioSnapshot` stores NAV, period returns, holdings, and sector breakdown | Ledger-derived disposable evidence, not an M43 result store |
| Benchmark persistence | `BenchmarkPrice` stores provider-symbol-indexed prices and sync state | Legacy Market evidence store; no canonical identity or manifest conclusion |
| Attribution persistence | `AttributionMetric` and `ShadowPortfolioSnapshot` store alpha, drawdown, and attribution-related values | Existing runtime reality only; no M43 result identity, method version, or lineage admission |
| Schedulers | snapshot scheduler computes attribution and fetches benchmarks | Operational behavior remains untouched and non-precedential |
| Repair/admin routes | benchmark backfill, snapshot repair, and validation routes exist | No migration, backfill, or repair authority enters M43 |

### 3.5 APIs and consumers

The principal current Portfolio-analytics-facing APIs are:

- `GET /analytics/performance-comparison`;
- `GET /analytics/performance-stats`;
- `GET /analytics/factor-exposure`;
- `GET /analytics/attribution/{shadow_id}`;
- `GET /analytics/attribution-summary`;
- `GET /analytics/timing-performance`;
- `GET /analytics/timing-scores`;
- `GET /analytics/timing-regime-attribution`; and
- related shadow, evaluation, and human-vs-AI analytics endpoints.

Principal consumers include:

- `frontend/app/analytics/page.tsx`;
- `frontend/components/analytics/*`;
- `frontend/app/ai-analytics/(hub)/attribution/page.tsx`;
- `frontend/app/ai-analytics/(hub)/portfolios/page.tsx`;
- `frontend/components/AttributionPanel.tsx`;
- `frontend/components/ShadowPortfolioPanel.tsx`; and
- `frontend/lib/api.ts` analytics contracts.

Every endpoint and consumer is legacy runtime reality. None is declared
canonical, renamed, removed, adapted, or preserved by WP1.

## 4. Legacy-to-canonical disposition matrix

| Legacy surface or phrase | WP1 disposition | Reason |
| --- | --- | --- |
| “portfolio metrics” response bundle | `REJECT` as a canonical contract noun | It mixes unrelated method families, signal analytics, allocation analytics, and presentation-ready data |
| ORM-shaped snapshot lists as calculation input | `REJECT` | M43 requires one exact Portfolio Composition and a closed manifest |
| Request-selected benchmark analytics | `REJECT` as declared-benchmark analytics | A caller symbol cannot override M42 Portfolio Benchmark Declaration |
| Private analytics cache | `REJECT` as canonical authority | Cache state is not semantic input, identity, or truth |
| Existing calculated dictionaries | `REJECT` as Portfolio Measure Results | They lack method-version, manifest, identity, canonical serialization, and complete lineage |
| `status`, `data_status`, `insufficient_data`, `unavailable`, and similar local tokens | `REJECT` as M43 vocabulary precedent | Existing strings do not define Portfolio Computation Outcome or Degraded State |
| `AttributionMetric` BHB fields | `REJECT` as M43 attribution precedent | BHB and benchmark-relative attribution are excluded |
| Human-vs-AI, override, recommendation, and regime attribution | `REJECT` from M43 | Trust & Evaluation or Decision Intelligence meaning |
| Current TWR chaining of stored period returns | `CHARACTERIZE` | The dependency pattern is relevant, but no production method or formula is admitted |
| Existing immutable M40–M41 patterns | `REUSE PATTERN ONLY` | Market Intelligence-owned types cannot accept Portfolio subjects |
| Existing M42 Portfolio Composition | `REUSE` | Exact frozen governed subject; no reinterpretation |

## 5. Negative corpus

The following statements are invalid in every WP1 artifact and in every
downstream reliance on WP1:

1. “The current analytics endpoint is the canonical Portfolio Analytics API.”
2. “A PortfolioSnapshot is a Portfolio Measure Result.”
3. “A request benchmark symbol establishes the Portfolio Benchmark
   Declaration.”
4. “`^SET.BK`, `QQQ`, `^GSPC`, 2.5%, 252, 30 days, or a current date is a
   permitted ambient default.”
5. “Missing adjusted return may fall back to raw NAV percentage change or
   zero.”
6. “A provider symbol or live provider answer is canonical calculation
   evidence.”
7. “A process cache hit is part of result identity or provenance.”
8. “Existing `status` strings are Portfolio Computation Outcome values.”
9. “`UNAVAILABLE` is a Portfolio Computation Outcome.”
10. “Portfolio Degraded State is a new state axis.”
11. “Market Intelligence’s Market Measure types may be relabeled to accept a
    Portfolio subject.”
12. “Portfolio Composition carries NAV, return, risk, attribution, or
    exposure.”
13. “Current classification labels establish Asset Classification or
    Analytical Grouping authority.”
14. “Experience may recompute drawdown, return, contribution, or any other
    business value.”
15. “M43 admits BHB, benchmark-relative attribution, recommendation
    attribution, causal attribution, or human-vs-AI attribution.”
16. “A documented formula, example, fixture, or version is a production
    method.”
17. “Current persistence implies an M43 persistence design.”
18. “WP1 authorizes a module, registry, kernel, adapter, API, migration,
    scheduler, cache, or UI change.”
19. “Portfolio Analytics is cross-portfolio or household analytics.”
20. “Current code ownership determines constitutional semantic ownership.”
21. “M43 admits Portfolio Policy or any renamed equivalent.”
22. “M43 may determine Investment Universe membership or eligibility.”
23. “M43 may infer a missing Portfolio Base Currency, Portfolio Lifecycle
    State, or Provenance coordinate.”

## 6. Reconciliation result

Current behavior confirms the exact gap M43 was frozen to address:

- formulas and states exist without canonical Portfolio contracts;
- defaults and fallbacks are ambient;
- benchmark selection can be request-driven;
- duplicate rules exist;
- Portfolio, Decision, and Evaluation semantics overlap in current modules;
- result identity, method-version identity, manifest closure, and lineage are
  absent; and
- Experience currently performs some calculations.

These findings justify the WP1 vocabulary boundary but authorize no fix.
Repository code, runtime behavior, APIs, persistence, and consumers remain
unchanged.

## 7. Completion gate for this artifact

This reconciliation is ready for independent review when:

1. the roadmap has no M43 capability-completion claim;
2. the source inventory covers formulas, endpoints, defaults, fallbacks,
   caches, persistence, and consumers;
3. duplicate rules are explicitly mapped without choosing a future
   implementation;
4. legacy behavior is treated as evidence, never precedent;
5. the negative corpus covers all frozen M43 exclusions; and
6. no source, runtime, schema, API, UI, operational, or production-method
   authority is asserted.

Independent confirmation of this artifact and its companion register is
required before any downstream work package relies on a WP1 candidate noun.
