# Wealth OS — Agent Handoff

This file is the lightweight source of truth for the current Wealth OS working state.
Keep it short. Update it whenever the active track, branch, agent/session, or next action changes.

## Current Work

- Project: Wealth OS / Portfolio Intelligence Platform
- Repository: `patipan-kong/Portfolio_Intelligence_Platform`
- Current track: UX-01 Slice 1 (Overview hierarchy + navigation continuity) — implemented on branch `feature/wealth-os-ux01-overview-hierarchy`; targeted tests + TypeScript pass; manually browser-validated; ready to commit and push for PR review.
- Main baseline: `a688f5875` (docs: rebaseline Wealth OS roadmap after dogfood (#48)), matching fetched `origin/main` on 2026-09-21 before this implementation pass.
- Current phase: **ROADMAP REBASELINE COMPLETE — PRODUCT FEATURE PAUSE → bounded UX reopening. UX-01 recon complete (verdict: IMPLEMENTATION READY); Slice 1 implemented and manually browser-validated, ready for PR review.**
- Latest active coding agent/session: Claude (Sonnet 5) — UX-01 reconnaissance, then UX-01 Slice 1 implementation, then manual browser validation.
- Last completed step: Implemented UX-01 Slice 1 only: added a semantic `<h2>Wealth Summary</h2>` heading to the headline wealth block (previously heading-less); promoted the existing `NetWorthChangeAttributionCard` to render immediately after the wealth summary instead of after the four history cards; added a plain-language disclosure that live headline figures and latest-complete-snapshot history figures can briefly differ; added Wealth Overview (`/`) to `NAV_GROUPS` under the Wealth group (previously reachable only via the brand-logo link) and updated the now-stale Navbar comment; added a "← Wealth Overview" return link on `/review`. No backend, calculation, formula, or database change. No new API request. Targeted Vitest suites (Dashboard, WealthOverview, Navbar, ReviewPage, DashboardPeriodicReviewLink, NetWorthChangeAttributionCard, NetWorthReviewSection — 138 tests) pass; `tsc --noEmit` shows the same 9 pre-existing unrelated errors as before this change (0 new). Manual browser validation subsequently completed by the user: desktop Wealth Overview composition, Wealth nav discoverability/active state, Periodic Review → Overview continuity, responsive layout at ~390-430px, and basic keyboard/focus behavior all passed with no blocking defect found.
- Next action / current authorized next work: Commit and push branch `feature/wealth-os-ux01-overview-hierarchy` for manual PR review. UX-01 is NOT complete: the "anything needing attention" composite and the four-history-card collapse/demotion remain candidate Slice 2 work, not yet started and not authorized by this pass.
- Dogfood delivery state: DOGFOOD-01 through DOGFOOD-05 are merged; no pending dogfood implementation branch or PR is part of the current handoff. DOGFOOD-06 is investigated / no product defect / no code fix (see below).

## Product Priorities and Reopening Boundary

1. Phase 8 — UX vNext + continued dogfood.
2. Phase 9 — Goal Needs Planning.
3. Phase 10 — Fund Foundation.
4. Phase 11 — Tax / Protection factual foundations; Tax-Fund semantics require both Fund Foundation and tax factual/rule authority.
5. Phase 12 — Deterministic Life Cases.
6. Phase 13 — Probabilistic / deeper advisory work: deferred, no implementation scheduled.

The [roadmap](architecture/ROADMAP.md) records bounded reopening: continued
dogfood correctness fixes, evidence-backed UX improvements after scoped recon,
and approved tracks one at a time. It does not reopen the general feature
backlog. UX-01 implementation requires a subsequent scoped decision; the next
authorized activity is reconnaissance only. No broad analytics, speculative AI,
autonomous financial actions, cross-goal optimizer authority, Monte Carlo,
giant scenario engine, tax advice, insurance recommendations or broad
multi-asset expansion is authorized merely by the rebaseline.

Continue real usage on Goals/funding, Liabilities, Mandates, Cash, scenarios,
linked execution and Reviews/Follow-ups. Sparse data limits inference; empty
tables do not mean shipped capabilities need reimplementation. SA35 contract
alignment remains optional governance work, not the next product track.

## Dogfood History — Current Status Verified Against Main

| Item | Status | Main commit / PR | Finding |
| --- | --- | --- | --- |
| DOGFOOD-01 | MERGED | `c338460` / #43 | Periodic Review Net Worth request fan-out fixed; historical acceptance recorded 532→1 requests per domain with zero semantic mismatches. |
| DOGFOOD-02 | MERGED | `c3cd5b0` / #44 | Evaluation NAV conservation: over-100%-weight recommendation rows scale proportionally before valuation instead of clamping a negative cash residual to zero. |
| DOGFOOD-03 | MERGED | `d2df199` / #45 | Three Portfolios Gap B now uses its own canonical displayed AI return minus actual return, rather than attribution's distinct `regret_score`. |
| DOGFOOD-04 | MERGED | `29c12ad` / #46 | Resolved stale-process incident plus Scorecard / Three-Portfolios semantic reconciliation; details below. |
| DOGFOOD-05 | MERGED | `ef57951` / #47 | Native yfinance benchmark-parser crash mitigated by direct Yahoo chart JSON handling; details below. |

### DOGFOOD-04 — two separate findings, both resolved

- **Stale backend process:** the port-8000 uvicorn process had run since
  2026-09-11 without `--reload` and still served pre-DOGFOOD-03 code. The user
  restarted it; live Three Portfolios reconciled (historical portfolio 4 / 90D
  example: Ideal +5.3%, AI +5.6%, You +4.7%, Gap A −0.3%, Gap B +1.0%).
  This was an environment issue, not another Gap B formula defect; no restart
  blocker remains. The full-payload simultaneous Gap A/B regression is in
  `backend/tests/test_ideal_series.py`.
- **Scorecard semantic reconciliation:** implementation shortfall incorrectly
  recomputed a stale formula (historically −3.72% versus canonical −0.33%);
  it now reuses `compute_three_portfolios`'s Gap A. Scorecard Outcome's
  live-tracked AI shadow and full-period Ideal remain deliberately distinct
  from Three Portfolios' canonical-price/aligned-window figures. Additive
  `outcome.methodology`, labels/tooltips, a cross-reference disclaimer and
  “AI model's shadow account” verdict wording disclose those differences.
  Opportunity cost was independently found to be a decision-level sum over
  differing, often-overlapping windows, not a portfolio return or Gap B;
  it was left unchanged. Historical acceptance: 51/51 targeted tests passed;
  boundary-suite fixture fragility and nine unrelated frontend typing errors
  were documented as pre-existing, not fresh validation of this docs pass.
  The [Decision Log](engineering/DECISION_LOG.md) preserves the detailed
  investigation, price-source/window provenance and then-current dispositions.

### DOGFOOD-05 — native crash and bounded mitigation

- **Root cause:** `/operations-center` called status aggregation → regime
  detection → `_fetch_benchmark_history("^SET.BK", ...)` →
  `yfinance.Ticker(...).history()`. On the investigated dev environment,
  parsing Yahoo's degraded single-datapoint chart response caused native
  `STATUS_ACCESS_VIOLATION` (`-1073741819`), bypassing Python exception
  handling and producing no FastAPI traceback. It reproduced 5/5 directly
  and in bare yfinance calls; frontend storms/concurrency were ruled out.
  Version/dependency bisection (yfinance 1.3.0 through 1.7.0, curl_cffi
  0.15.0/0.16.3) showed dependence on the full environment: 1.3.0 and a
  minimal yfinance-only environment did not reproduce the crash. The recorded
  diagnosis was an environment-level native-library conflict in the parser,
  not a proven simple version-only regression.
- **Merged mitigation:** `backend/services/analytics/regime_detector.py`
  fetches Yahoo chart JSON directly with `requests` and parses it without
  yfinance's history parser. A valid one-row response is safely rejected as
  insufficient evidence by the existing 25-row signal minimum. Benchmark
  selection and regime/optimizer calculation semantics were unchanged.
  `backend/tests/test_regime_detector_fetch.py` contains five regression
  cases for the requests path, degraded/normal/malformed payloads and VPS
  blocking. The prior investigation recorded process crashes when these
  guards exercised the pre-fix path.
- **Historical runtime acceptance:** the page's status/trust-report/optimizer-
  history request graph succeeded against live uvicorn/dev PostgreSQL;
  repeat navigation and `/system/status` worked, with bounded observed memory
  (~198MB→213MB). The user separately confirmed the fix in their actual dev
  environment. These are preserved incident findings, not checks rerun in
  this documentation pass. PR #47 is merged; no manual PR action remains.
- **Environment caveat from that investigation:** Python dependencies were
  split across `backend/.venv`, `backend/venv-test` and conda environments.
  At that time `.venv` had Alembic/SQLAlchemy/uvicorn but lacked FastAPI/
  yfinance; `venv-test` had FastAPI/yfinance/curl_cffi and gained uvicorn;
  the conda environments lacked FastAPI/uvicorn. Verify the actual runtime
  interpreter/dependencies before launching services. The docs pass verified
  only Alembic heads/current through `.venv`, not full application readiness.

### DOGFOOD-06 — investigated / no product defect / no code fix

The separate read-only investigation supplied for this handoff found quantity
valuation, canonical price resolution and snapshot persistence succeed, with
performance unaffected. Asset Registry shadow consultation reported
`MissingBinding` for some unminted assets because registry coverage is
incomplete; consultation is intentionally shadow-only/log-only. The duplicate
`GOOGL01.BK` warning came from two different portfolios. No product code defect
was established. These are the supplied investigation findings, not a new
runtime reproduction in this documentation pass.

No symbols were minted, registry records added, warnings changed or tests
added for DOGFOOD-06. Registry rollout/backfill/data hygiene remains a separate
future concern; a shadow coverage warning must not be treated as valuation
failure. There is no fix commit or PR to invent for this investigation.

## Canonical Boundaries to Preserve

- Net Worth is tracked investments + external cash − liabilities; property
  ownership/appraisal and complete household coverage remain gaps.
- Goal designation is not contribution or transfer. Mandate is factual
  association, not funding priority or optimizer authority (ADR-007/010/011).
- ADR-008 context is `CONTEXT_ONLY`; ADR-009's explicit single-Goal horizon
  bound remains the sole documented Goal-derived behavioral exception.
- Goal Intelligence is descriptive (ADR-014); existing projection/inverse
  math is frontend-canonical in `goalWhatIf.ts` (ADR-015). No second engine,
  automatic canonical scenario, legacy Goal Wizard reinterpretation or
  per-goal shared-source shortfall attribution (ADR-016).
- Cash-side investment funding is one-sided (ADR-012); Net Worth attribution
  remains Level-1 (ADR-013). Review is editable retrospective context, not
  immutable history. Exposure is current-snapshot only; distinct evaluation
  methodologies remain disclosed rather than collapsed.
- PostgreSQL schema ownership remains Alembic-only (ADR-017). This
  documentation pass requires no schema change or migration.

## Previous Track

- Track: Cross-Portfolio Exposure Snapshot
- PR: #41
- Status: MERGED
- Delivered:
  - Current-snapshot portfolio contribution, aggregate sector exposure, and cross-portfolio symbol overlap on a new `/exposure` page
  - Descriptive only — no historical trend, severity/risk labels, target allocation, or rebalance guidance
- Final track decision: `TRACK COMPLETE`

## Earlier Track

- Track: Goal ↔ Portfolio Mandate Visibility
- PR: #40
- Status: MERGED
- Delivered:
  - Goal-first reverse lookup of mandated portfolios (`GET /wealth-goals/{id}/portfolio-mandates`)
  - Goal Detail page discloses which portfolios carry an investment mandate for that goal
- Final track decision: `TRACK COMPLETE`

## Working Rules

1. Start new product work from an up-to-date `main`.
2. Use one feature branch per track.
3. Flow: recon → implement → review → commit → push feature branch → PR → merge on GitHub → pull `main`.
4. Never push a feature branch directly to `main` with `<feature>:main`.
5. Before resuming work, read this file and confirm branch + phase + next action.
6. When switching coding agents/sessions, update `Latest active coding agent/session` immediately.
7. When a PR merges, record it under Previous Track before starting the next track.
8. Keep detailed implementation reports in PRs/docs; this file is only the handoff snapshot.
9. Do not run the full frontend Vitest suite by default on this development machine. Use targeted affected Vitest files + `npm run test:pure` + TypeScript verification. Run the full Vitest suite only when explicitly requested or when a concrete investigation requires it.

## Update Template

When handing off, update only these lines unless more context is genuinely needed:

```text
Current track:
Current branch:
Current phase:
Latest active coding agent/session:
Last completed step:
Next action:
```
