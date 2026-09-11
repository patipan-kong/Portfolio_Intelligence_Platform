# Wealth OS — Agent Handoff

This file is the lightweight source of truth for the current Wealth OS working state.
Keep it short. Update it whenever the active track, branch, agent/session, or next action changes.

## Current Work

- Project: Wealth OS / Portfolio Intelligence Platform
- Repository: `patipan-kong/Portfolio_Intelligence_Platform`
- Current track: DOGFOOD-01 — Periodic Review Net Worth request fan-out (bugfix, not a product track)
- Current branch: `fix/wealth-os-periodic-review-net-worth-fanout`
- Current phase: PRODUCT FEATURE PAUSE
- Latest active coding agent/session: Claude Code — DOGFOOD-01 Periodic Review Net Worth fan-out fix
- Last completed step: DOGFOOD-01 — Periodic Review Net Worth request fan-out: Fixed / final-reviewed. Root cause was two-fold: (1) `NetWorthReviewSection` called `GET /cash-accounts/{id}/as-of` and `GET /liabilities/{id}/as-of` once per (account, date) / (liability, date) pair — an accounts×dates / liabilities×dates HTTP fan-out (532 requests against this dev DB: 7 cash accounts × 76 history dates); (2) an unmemoized `investmentHistoryDates` array recomputed every render was a fetch-effect dependency, so the fan-out could re-fire on unrelated re-renders. Fix: two new bounded batch endpoints (`GET /cash-accounts/balances-as-of`, `GET /liabilities/balances-as-of`) that reuse the existing canonical `cash_balance_as_of`/`liability_balance_as_of` pure functions server-side (fetch each account's/liability's ledger once, evaluate every requested date in-process), plus `useMemo` on the date spine. Verified against the real dev DB: 532 requests → 1 request per domain, wall-clock 1772ms → 38ms, zero mismatches across all 532 compared (account, date) values. No migration; no calculation-policy change; Goals/Execution/Evaluation review sections untouched. Final review passed: backend contract, frontend request-graph, semantic-equivalence, and scope re-audited; targeted backend (164 passed) + frontend (147 passed) + `test:pure` (419 passed) + `tsc --noEmit` (no new errors) all green. Follow-up candidate: Dashboard Net Worth History (`frontend/app/page.tsx`) still uses the older per-account × per-date fan-out pattern.
- Next action: commit and open a focused bugfix PR; continue PRODUCT FEATURE PAUSE afterward — accumulate real usage on Goals, Liabilities, Mandates, Reviews/Follow-ups, and Cash before the next product-feature pass; SA35 contract alignment remains optional governance work

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
