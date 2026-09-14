# Wealth OS — Agent Handoff

This file is the lightweight source of truth for the current Wealth OS working state.
Keep it short. Update it whenever the active track, branch, agent/session, or next action changes.

## Current Work

- Project: Wealth OS / Portfolio Intelligence Platform
- Repository: `patipan-kong/Portfolio_Intelligence_Platform`
- Current track: DOGFOOD-04 — Three Portfolios / AI Scorecard same-concept reconciliation (bugfix + presentation fix, not a product track; reviewed, committed, pushed; PR pending — no `gh`/`GITHUB_TOKEN` available on this machine to open it programmatically, same as DOGFOOD-03)
- Current branch: `fix/wealth-os-scorecard-three-portfolios-reconciliation` (pushed to origin, commit `8b85b36`). `main` is clean at `d2df199`. DOGFOOD-03 confirmed merged: PR #45.
- Current phase: PRODUCT FEATURE PAUSE
- Latest active coding agent/session: Claude Code — DOGFOOD-04 Scorecard/Three Portfolios same-concept reconciliation
- Last completed step: DOGFOOD-04 has two parts, both recorded in full in `docs/engineering/DECISION_LOG.md`:
  1. **Stale-process finding — RESOLVED environment evidence.** A live report that Gap B still didn't reconcile on Three Portfolios after DOGFOOD-03 merged (portfolio 4, 90D) traced to the port-8000 dev backend process running since 2026-09-11 (pre-dating the DOGFOOD-03 fix) with no `--reload` flag — not a code defect. The user restarted the process; live Three Portfolios now reconciles correctly (Ideal +5.3%, AI +5.6%, You +4.7%, Gap A −0.3%, Gap B +1.0%). One regression test added (`test_three_portfolios_payload_gap_a_and_gap_b_both_reconcile_simultaneously`, `tests/test_ideal_series.py`).
  2. **Scorecard/Three Portfolios same-concept reconciliation — the remaining open DOGFOOD-04 issue, fix applied, pending review.** After the restart, AI Scorecard was found showing AI Portfolio +7.1% / Ideal +3.4% for the same portfolio/90D request where Three Portfolios shows AI Portfolio +5.6% / Ideal +5.3% — same unqualified labels, different numbers. Traced: (a) `execution.implementation_shortfall`'s own code comment falsely claimed it was "the exact same figure" as `three_portfolios.gap_a` but independently recomputed a stale formula (−3.72% vs −0.33%) — a proven bug, fixed by threading `compute_three_portfolios`'s own `gap_a` value through directly; (b) `outcome.ai_model_return_pct`/`ideal_return_pct` are DISTINCT, deliberately-designed concepts from Three Portfolios' figures (per the pre-existing 2026-07-06 "Gap A Correctness Patch" — not a bug), so left numerically unchanged but now disclosed via a new additive `outcome.methodology` field, relabeled Outcome Quality card stats ("AI Model (shadow)" / "Ideal" with sub-labels + tooltips), and a Three Portfolios cross-reference disclaimer; (c) the verdict sentence's "full compliance with **the AI Portfolio**..." wording was reworded to "the AI model's shadow account" so it no longer collides with Three Portfolios' own use of that exact label. Net Opportunity Cost (−5.9%) was independently audited and found NOT defective (a sum of per-decision counterfactual deltas over different, often-overlapping windows — not comparable to a portfolio return, not related to Gap B, already honestly captioned) — left unchanged, out of scope. 3 new tests added (`tests/test_scorecard.py`; also fixed that file's own pre-existing `models.asset` fixture order-fragility). 51/51 tests passing across `test_ideal_series.py`/`test_scorecard.py`/`test_verdict_composer.py`; boundary suites re-confirmed pre-existing-only failures via `git stash`. Files touched: `backend/services/evaluation/scorecard.py`, `backend/services/evaluation/verdict_composer.py`, `backend/tests/test_scorecard.py`, `frontend/lib/api.ts`, `frontend/app/ai-analytics/(hub)/page.tsx` — all uncommitted.
- Next action: DOGFOOD-04 was approved, committed (`8b85b36`, message "fix: reconcile scorecard and three-portfolios semantics"), and pushed to `fix/wealth-os-scorecard-three-portfolios-reconciliation`. Open the PR manually against `main` (GitHub URL offered by the push: `https://github.com/patipan-kong/Portfolio_Intelligence_Platform/pull/new/fix/wealth-os-scorecard-three-portfolios-reconciliation`) — no `gh`/`GITHUB_TOKEN` on this machine to do it programmatically. Not merged. After DOGFOOD-04's PR merges, resume the prior PRODUCT FEATURE PAUSE next action — accumulate real usage on Goals, Liabilities, Mandates, Reviews/Follow-ups, and Cash before the next product-feature pass; SA35 contract alignment remains optional governance work.
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
