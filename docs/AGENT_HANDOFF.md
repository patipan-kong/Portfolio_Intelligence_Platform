# Wealth OS — Agent Handoff

This file is the lightweight source of truth for the current Wealth OS working state.
Keep it short. Update it whenever the active track, branch, agent/session, or next action changes.

## Current Work

- Project: Wealth OS / Portfolio Intelligence Platform
- Repository: `patipan-kong/Portfolio_Intelligence_Platform`
- Current track: DOGFOOD-03 — Three Portfolios GAP B semantic/calculation mismatch (bugfix, not a product track)
- Current branch: `fix/wealth-os-gap-b-semantics`, branched fresh from up-to-date `main` (DOGFOOD-01/DOGFOOD-02 confirmed merged: PRs #43/#44) — not stacked on any prior dogfood branch.
- Current phase: PRODUCT FEATURE PAUSE
- Latest active coding agent/session: Claude Code — DOGFOOD-03 Three Portfolios GAP B semantic/calculation fix
- Last completed step: DOGFOOD-03 — Three Portfolios GAP B semantic/calculation mismatch: Fixed, reviewed, approved, committed, and pushed to `origin/fix/wealth-os-gap-b-semantics`; PR opened (not merged). Root cause and fix recorded in full in `docs/engineering/DECISION_LOG.md`, "GAP B Semantic/Calculation Fix (DOGFOOD-03)": `compute_three_portfolios`'s `gap_b` read `attribution_engine`'s `regret_score`, which sources "AI" from a different, undisplayed, live-priced/full-window `ai_model_shadow.return_pct` rather than the canonical-priced, overlap-truncated `ai_return` already computed in the same function and rendered as the "AI Portfolio" headline on the same screen — so Gap B could (and on live portfolio 4 did) disagree in sign with the two displayed numbers it is captioned to explain. Fixed by sourcing `gap_b` from the function's own `ai_return - actual_return`; `regret_score` itself and its other consumers (Scorecard, Trust Report) are untouched. No migration, no schema change, no frontend change (existing copy was already accurate once the number matches). 6 new tests in `tests/test_ideal_series.py` (24 total, all passing); boundary tests (`test_attribution_waterfall`, `test_verdict_composer`, `test_scorecard`, `test_human_vs_ai_scoreboard`, `test_trust_report`) re-run, zero regressions (pre-existing order-fragile failures reproduce identically with/without this change).
- Next action: merge the DOGFOOD-03 PR on GitHub once approved there (not done by this agent — merge was explicitly out of scope for this pass); after it merges, resume the prior PRODUCT FEATURE PAUSE next action — accumulate real usage on Goals, Liabilities, Mandates, Reviews/Follow-ups, and Cash before the next product-feature pass; SA35 contract alignment remains optional governance work
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
