# Wealth OS — Agent Handoff

This file is the lightweight source of truth for the current Wealth OS working state.
Keep it short. Update it whenever the active track, branch, agent/session, or next action changes.

## Current Work

- Project: Wealth OS / Portfolio Intelligence Platform
- Repository: `patipan-kong/Portfolio_Intelligence_Platform`
- Current track: DOGFOOD-05 — Operations Center backend process crash (native segfault in regime detector's live market-data fetch; root-caused and fixed, uncommitted)
- Current branch: `main` at `29c12ad`. DOGFOOD-04 confirmed merged: PR #46 (this handoff file's prior text was stale — it still said "PR pending" for DOGFOOD-04; git confirms it merged).
- Current phase: PRODUCT FEATURE PAUSE
- Latest active coding agent/session: Claude Code — DOGFOOD-05 Operations Center crash investigation
- Last completed step: DOGFOOD-05 — real-user report: backend process (`uvicorn main:app`) exits with no FastAPI traceback when navigating to `/operations-center`. Root-caused and fixed; not yet committed. Full account:
  1. **Root cause.** `GET /operations-center/status` → `services/operations_center.py::build_operations_status` → `services/analytics/regime_detector.py::detect_regime` → `_fetch_benchmark_history("^SET.BK", ...)`, which called `yfinance.Ticker(symbol).history()`. On this dev machine, `yfinance` (>=1.4, confirmed through 1.7.0; 1.3.0 does not reproduce) segfaults — `STATUS_ACCESS_VIOLATION` (exit code `-1073741819`), a genuine OS-level crash, not a Python exception — while parsing a degraded, single-datapoint chart response that Yahoo Finance returns for the `^SET.BK` index symbol (confirmed via raw HTTP inspection: Yahoo returns only 1 data point despite a 6-month range request, for this specific synthetic ticker, seemingly permanently). This is why no FastAPI traceback ever appeared: a native access violation bypasses Python's exception machinery entirely — no `try/except` in application code could ever have caught it. Reproduced deterministically (5/5) by calling `regime_detector.detect_regime(db)` directly, and independently by calling bare `yfinance.Ticker("^SET.BK").history()` with zero application code involved — ruling out frontend request storms, concurrency, and Operations Center's own code as the cause. Bisected across `yfinance` 1.3.0/1.4.0/1.5.1/1.5.2-equivalent/1.7.0 and `curl_cffi` 0.15.0/0.16.3; crash persisted across nearly all combinations and was shown to depend on this machine's full backend dependency set, not yfinance/curl_cffi versions alone (a minimal venv with only yfinance's own dependencies did not reproduce it) — i.e. an environment-level native-library conflict inside `yfinance`'s own history parser, not a simple upstream version regression.
  2. **Fix.** `_fetch_benchmark_history` no longer uses `yfinance.Ticker(...).history()`. It now calls Yahoo's chart API directly via `requests` (already a direct dependency) and parses the JSON response manually — the same external endpoint yfinance itself calls, but never touching yfinance's internal parser. Verified this alternate path handles the exact degraded `^SET.BK` payload cleanly (returns a valid 1-row DataFrame, which the existing `_compute_signals` 25-row minimum already filters out via `bundle.ok = False` — so live-computed regime output is byte-identical to before for all currently-working benchmarks; only the previously-fatal failure mode changed). No calculation semantics, benchmark list, or regime/optimizer business logic changed. File: `backend/services/analytics/regime_detector.py` (`_fetch_benchmark_history`, ~30 lines). Regression test added: `backend/tests/test_regime_detector_fetch.py` (5 tests) — asserts the fetch goes through `requests` not `yfinance`, handles the real captured degraded-response payload, handles a normal multi-row response, degrades gracefully on a malformed response, and stays VPS-blocked correctly. Confirmed these tests **crash the actual test process** (a live segfault, not a clean failure) when run against the pre-fix code via `git stash` — the strongest possible proof this is a genuine regression guard for a real native crash, not a speculative test.
  3. **Runtime acceptance.** Full real request graph the `/operations-center` page issues on mount (`GET /operations-center/status`, `GET /analytics/evaluation/trust-report`, `GET /optimizer/history`) exercised against a live `uvicorn` instance with the real dev Postgres DB — all succeeded, server stayed alive, memory stayed bounded (~198MB → ~213MB), repeat navigation and an unrelated endpoint (`/system/status`) still worked afterward.
  4. **Environment note for future sessions:** this machine has no single Python environment with the full backend dependency set already installed — `backend/.venv` (has alembic/sqlalchemy/uvicorn but not fastapi/yfinance), `backend/venv-test` (has fastapi/yfinance/curl_cffi but was missing uvicorn until this session installed it), and two conda envs (`base`, `tradingagents`, neither has fastapi/uvicorn) were all found incomplete. `backend/venv-test` + a `pip install uvicorn[standard]` is the closest thing to a working dev environment discovered so far; confirm with the user which environment they actually use before assuming.
  5. **User runtime verification — CONFIRMED.** The user manually verified the fix on their actual local development environment (the real dev backend process, not the agent's reproduction venv): navigating to `/operations-center` no longer terminates the backend process. Approved for commit/PR on this basis.
- Next action: DOGFOOD-05 committed on `fix/wealth-os-operations-center-yfinance-crash` and pushed to origin. Open the PR manually against `main` if not opened programmatically. After it merges, resume the prior PRODUCT FEATURE PAUSE next action (below).
- Prior step (DOGFOOD-04, merged): Three Portfolios / AI Scorecard same-concept reconciliation. Merged via PR #46. Full detail:
  1. **Stale-process finding — RESOLVED environment evidence.** A live report that Gap B still didn't reconcile on Three Portfolios after DOGFOOD-03 merged (portfolio 4, 90D) traced to the port-8000 dev backend process running since 2026-09-11 (pre-dating the DOGFOOD-03 fix) with no `--reload` flag — not a code defect. The user restarted the process; live Three Portfolios now reconciles correctly (Ideal +5.3%, AI +5.6%, You +4.7%, Gap A −0.3%, Gap B +1.0%). One regression test added (`test_three_portfolios_payload_gap_a_and_gap_b_both_reconcile_simultaneously`, `tests/test_ideal_series.py`).
  2. **Scorecard/Three Portfolios same-concept reconciliation — the remaining open DOGFOOD-04 issue, fix applied, pending review.** After the restart, AI Scorecard was found showing AI Portfolio +7.1% / Ideal +3.4% for the same portfolio/90D request where Three Portfolios shows AI Portfolio +5.6% / Ideal +5.3% — same unqualified labels, different numbers. Traced: (a) `execution.implementation_shortfall`'s own code comment falsely claimed it was "the exact same figure" as `three_portfolios.gap_a` but independently recomputed a stale formula (−3.72% vs −0.33%) — a proven bug, fixed by threading `compute_three_portfolios`'s own `gap_a` value through directly; (b) `outcome.ai_model_return_pct`/`ideal_return_pct` are DISTINCT, deliberately-designed concepts from Three Portfolios' figures (per the pre-existing 2026-07-06 "Gap A Correctness Patch" — not a bug), so left numerically unchanged but now disclosed via a new additive `outcome.methodology` field, relabeled Outcome Quality card stats ("AI Model (shadow)" / "Ideal" with sub-labels + tooltips), and a Three Portfolios cross-reference disclaimer; (c) the verdict sentence's "full compliance with **the AI Portfolio**..." wording was reworded to "the AI model's shadow account" so it no longer collides with Three Portfolios' own use of that exact label. Net Opportunity Cost (−5.9%) was independently audited and found NOT defective (a sum of per-decision counterfactual deltas over different, often-overlapping windows — not comparable to a portfolio return, not related to Gap B, already honestly captioned) — left unchanged, out of scope. 3 new tests added (`tests/test_scorecard.py`; also fixed that file's own pre-existing `models.asset` fixture order-fragility). 51/51 tests passing across `test_ideal_series.py`/`test_scorecard.py`/`test_verdict_composer.py`; boundary suites re-confirmed pre-existing-only failures via `git stash`. Files touched: `backend/services/evaluation/scorecard.py`, `backend/services/evaluation/verdict_composer.py`, `backend/tests/test_scorecard.py`, `frontend/lib/api.ts`, `frontend/app/ai-analytics/(hub)/page.tsx` — all uncommitted.
- PRODUCT FEATURE PAUSE next action (once DOGFOOD-05 merges, resume this): accumulate real usage on Goals, Liabilities, Mandates, Reviews/Follow-ups, and Cash before the next product-feature pass; SA35 contract alignment remains optional governance work.
- Prior step (DOGFOOD-03, merged): Three Portfolios GAP B semantic/calculation mismatch fixed — `gap_b` now sourced from `compute_three_portfolios`'s own `ai_return - actual_return` instead of `attribution_engine`'s `regret_score`. Merged via PR #45.
- Prior step (DOGFOOD-02, merged): Evaluation Scorecard NAV invariant failure fixed — over-100%-weight `RecommendationSnapshot` rows now scale proportionally before market-value computation instead of clamping a negative cash residual to 0. Merged via PR #44.
- Prior step (DOGFOOD-01, merged): Periodic Review Net Worth request fan-out fixed (532→1 requests per domain, zero semantic mismatches). Merged via PR #43.

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
