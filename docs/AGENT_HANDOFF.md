# Wealth OS — Agent Handoff

This file is the lightweight source of truth for the current Wealth OS working state.
Keep it short. Update it whenever the active track, branch, agent/session, or next action changes.

## Current Work

- Project: Wealth OS / Portfolio Intelligence Platform
- Repository: `patipan-kong/Portfolio_Intelligence_Platform`
- Current track: DOGFOOD-02 — Evaluation Scorecard NAV invariant failure (bugfix, not a product track)
- Current branch: `fix/wealth-os-scorecard-nav-invariant`, stacked on the still-unmerged DOGFOOD-01 branch `fix/wealth-os-periodic-review-net-worth-fanout` (tip `cd7044f`, PR pending) — stacked by explicit instruction rather than branched independently from `main`. DOGFOOD-02's eventual PR should target the DOGFOOD-01 branch as its base (or be rebased onto `main` once DOGFOOD-01 merges), not `main` directly, until DOGFOOD-01 lands.
- Current phase: PRODUCT FEATURE PAUSE
- Latest active coding agent/session: Claude Code — DOGFOOD-02 Evaluation Scorecard NAV invariant fix
- Last completed step: DOGFOOD-02 — Evaluation Scorecard NAV invariant failure: Fixed / awaiting review. `GET /analytics/evaluation/scorecard?portfolio_id=2&period_days=90` 500'd via `NavInvariantError` inside `compute_ideal_series`'s 2026-07-15 rebalance. Root cause: the real, persisted `RecommendationSnapshot` for that rebalance (portfolio 2, snapshot_id=78 — the only such row out of 140 in this dev DB) has `target_weight` values summing to 101.1% instead of ≤100%. The canonical shared rebalance-sizing helper `_resolve_shares_from_weights` (services/decision_memory/shadow_tracker.py, used by both `compute_ideal_series` and the ACTIVE_MODEL shadow — not a duplicated/drifted copy) computed each holding's market_value from those raw over-100% weights, then clamped the resulting negative cash residual to 0 via `max(0.0, ...)` — silently letting equity exceed NAV by exactly `1.1% × NAV`. Fix: when target weights sum above 100%, scale every weight down proportionally before computing market_value, so deployed equity can never exceed NAV and cash lands at exactly 0 by construction rather than by a clamp; under-100% weights (the intentional cash floor) are unaffected. `assert_nav_conserved` itself was left strict/unweakened — it correctly detected a real defect. No migration; no historical data mutated (isolated to this one anomalous snapshot, confirmed not systemic). Verified against real dev DB: portfolios 2/3/4 × period_days 30/60/90/180/365 all now return 200 (previously portfolio 2 at period_days ≥ 60 500'd). Follow-up candidate: an identical inline clamp pattern (`cash = max(0.0, (100 - deployed_weight)/100 * inception_value)`) exists at `regenerate_static_shadow` (shadow_tracker.py ~line 1774) but is not on this failure's call path — left unfixed, flagged for a separate pass.
- Next action: review and commit the DOGFOOD-02 fix (working tree intentionally left uncommitted pending review); after both DOGFOOD-01 and DOGFOOD-02 merge, resume the prior PRODUCT FEATURE PAUSE next action — accumulate real usage on Goals, Liabilities, Mandates, Reviews/Follow-ups, and Cash before the next product-feature pass; SA35 contract alignment remains optional governance work
- Prior step (DOGFOOD-01, still pending merge — PR not yet confirmed open): Periodic Review Net Worth request fan-out fixed and final-reviewed (532→1 requests per domain, zero semantic mismatches, tests green); pushed to `origin/fix/wealth-os-periodic-review-net-worth-fanout` at `cd7044f`; PR creation was handed to the user manually (no `gh` CLI / API token available in this environment). Follow-up candidate from that pass: Dashboard Net Worth History (`frontend/app/page.tsx`) still uses the older per-account × per-date fan-out pattern.

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
