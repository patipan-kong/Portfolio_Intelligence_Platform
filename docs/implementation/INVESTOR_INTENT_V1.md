# Investor Intent V1 — Position-Scoped Owner Restrictions

**Status:** Implemented (isolated; not read by the optimizer)
**Date:** 2026-10-07
**Branch:** `feature/investor-intent-v1`
**Migration:** `o7p8q9r0s1t2` (down: `n6o7p8q9r0s1`)

## Purpose

Investor Intent lets the owner record their real constraints and preferences
for a position so that, in a later slice, the advisory system can reason with
them *before* it recommends. It is not primarily an override mechanism. The
human remains the final decision authority at execution; overrides are
exceptions and audit signals. Declared intent is never rewritten from
observed behaviour, trades, legacy locks or previous decisions.

V1 is persistence, an owner API, a small UI, and a pure validator. **Nothing in
the recommendation, scoring, policy or execution pipeline reads it.** The UI
and every API response say so (`enforced_by_optimizer: false`).

## Owner decisions applied (2026-10-07)

| # | Decision |
|---|---|
| C1 | Existing `PortfolioItem.allow_swap=False` keeps its current legacy behaviour. It is never converted or backfilled into intent. It is shown as "legacy lock (meaning unconfirmed)". |
| C2 | An owner hard restriction constrains what the advisor may recommend. If an advisory/system rule calls for a prohibited change, the result is an explicit CONFLICT carrying both sources. Neither side is silently discarded. |
| C3 | An owner restriction is not a governance violation. A conflict with policy/risk guidance is an Intent–Policy Conflict, the underlying warning is preserved, and advisory/governance quality is not penalised for it. |

## Position identity

Intent is keyed by **(portfolio_id, position_symbol)**, not `PortfolioItem.id`:

- `portfolio_rebuilder` deletes and recreates every `PortfolioItem` row on a
  rebuild, and a full sale deletes the row. A foreign key to
  `portfolio_items.id` would destroy or orphan intent.
- `(portfolio_id, symbol)` is the existing persistent key: it is
  `uq_portfolio_symbol`, and the rebuilder already uses it to preserve
  `allow_swap` across rebuilds.
- `Watchlist.asset_id` / `PortfolioItem.asset_id` are not used (unreliable
  or unadjudicated per prior investigation).

Consequences, by design: intent and its history survive rebuilds and full sales (shown as
"not currently held"); a symbol change through a position conversion does
**not** carry intent to the successor symbol (no silent transfer).

### Holding episodes and same-symbol re-entry (R1, owner decision 2026-10-07)

A full sale followed later by a new holding of the same
`(portfolio_id, symbol)` is a new **holding episode**. An intent confirmed for
an earlier episode does not apply to the new one until the owner re-confirms
it. History is preserved and nothing is created on the owner's behalf.

**Episode start.** `PortfolioItem.created_at` is the start of the current
continuously-held `(portfolio_id, symbol)` episode:

- Live trades keep it: buys, partial sells and quantity corrections update
  the existing row in place.
- `portfolio_rebuilder._commit_rebuild` preserves it on rebuild, the same way
  it preserves `allow_swap`, keyed by the stored symbol. A legacy NULL stays
  NULL. A row that did not exist before the rebuild gets a new value.
- A full exit deletes the row (`execute_sell`, deleting a holding, the
  predecessor of a position conversion). A later re-entry creates a new row
  with a new `created_at`.

**Confirmation time.** This is the `recorded_at` of the intent's current
revision row (`position_intent_revisions`, matched on
`(position_intent_id, revision)`). It is the timestamp written when the owner
saved that revision. `PositionIntent.updated_at` is not used.

**Applicability** (`services/investor_intent.intent_status`, pure):

| Situation | `intent_status` |
|---|---|
| No intent row | `NO_CONFIRMED_INTENT` |
| Current revision's `recorded_at` ≥ episode start, or not held, or legacy NULL start | `CONFIRMED` |
| Episode start > current revision's `recorded_at` (confirmed for an earlier holding) | `RECONFIRMATION_REQUIRED` |
| Current revision row missing | `RECONFIRMATION_REQUIRED` (fails closed) |

For a future consumer, `investor_intent_store.applicable_intent_state` returns
`None` unless the status is `CONFIRMED`. An intent that needs re-confirmation
therefore behaves as "no confirmed intent" (`UNRESOLVED`), never as a
restriction or a permission. Both timestamps come from the same application
clock (`datetime.utcnow`).

**Re-confirmation.** This takes an explicit owner `PUT` with the current
`expected_revision`. With identical values it appends a revision and returns
`RECONFIRMED`; with changed values it returns `REVISED`. Either way the new
revision's `recorded_at` falls inside the current episode, so the intent is
`CONFIRMED` again. Earlier revisions are untouched. An identical write while
the intent is already `CONFIRMED` stays `UNCHANGED`, with no new revision.

**Accepted V1 limitations:**

- These are symbol-slot / holding-episode semantics, not an immutable
  economic-instrument identity.
- Position conversions and restored rows (for example, a row that the live
  state lost and a rebuild recreates) may conservatively require
  re-confirmation.
- Raw or direct ledger manipulation may not give perfect episode semantics.
  For example, ledger rows for a sale and re-entry inserted directly and then
  rebuilt, while the live row was never deleted, keep the old episode start.
  Direct SQL edits to `created_at` or `recorded_at` are not guarded.
- A canonical holding-episode identity may replace this mechanism later. V1
  adds no HoldingEpisode model, no ledger replay and no exit hooks.

## Persistence

- `position_intents` — one current row per position: `increase_prohibited`,
  `decrease_prohibited`, `soft_preference` (`NONE | PREFER_KEEP | PREFER_EXIT`),
  `revision` (from 1), `author_kind` (`OWNER` only), timestamps.
- `position_intent_revisions` — one append-only row for **every** revision,
  including the first. `(position_intent_id, revision)` identifies the intent in
  force for a later recommendation or decision. "Append-only" is a guarantee of
  the supported application write path (`services/investor_intent_store.py`
  never updates or deletes a revision row; there is no API to do so). It is
  **not** enforced by the database: direct ORM or SQL writes can still mutate
  or delete rows. No database triggers are used.
- No row ⇒ `NO_CONFIRMED_INTENT`. An explicit row with both flags false is
  `CONFIRMED` unrestricted intent. The two are never conflated.
- Authorship: the app is single-user (`_ws_id`), so the workspace owner is
  the only possible author. There is no per-request user identity to record.
- No backfill. No conversion of `allow_swap`. No delete endpoint in V1 (an
  owner can set unrestricted intent; history is preserved).
- Portfolio deletion removes intent through the ORM cascade (API path) and
  explicitly in `manage.py`'s bulk delete path, mirroring mandates.

## API

| Method | Path | Behaviour |
|---|---|---|
| GET | `/portfolios/{id}/position-intents` | Held positions plus intents for positions no longer held. Per row: `currently_held`, `holding_started_at` (current episode start), `legacy_allow_swap`, `legacy_lock_status`, `intent_status` (`CONFIRMED | NO_CONFIRMED_INTENT | RECONFIRMATION_REQUIRED`), `intent` (shown as history even when it needs re-confirmation). Includes `enforced_by_optimizer: false` and a disclosure. |
| PUT | `/portfolios/{id}/position-intents/{symbol}` | Body `{increase_prohibited, decrease_prohibited, soft_preference, expected_revision}` (strict types, extra fields rejected). `expected_revision: null` creates (201); the current revision revises (200, `REVISED`); identical values return 200 `UNCHANGED` with no new revision, unless the intent needs re-confirmation for the current holding episode: then they append a revision and return 200 `RECONFIRMED`. Stale or wrong revision → 409. Creating for a symbol not held in this portfolio → 404. |
| GET | `/portfolios/{id}/position-intents/{symbol}/revisions` | Append-only revision history (application-path guarantee, see Persistence); 404 if there is no intent. |

Ownership: every call resolves the portfolio through
`resolve_portfolio_or_404` against the caller's workspace and queries
positions/intents filtered by both workspace and portfolio. `expected_revision`
is new to this repository (no prior optimistic-concurrency convention); a
concurrent revision is also caught by `uq_position_intent_revisions_intent_revision`.

## Domain contract (`services/investor_intent.py`, pure)

Direction is judged on **share quantity only**. A weight change from price
movement is not an owner-directed increase or decrease; callers pass
quantities, never weights.

Quantity-direction boundary (`quantity_direction`):

| current → proposed | Direction |
|---|---|
| equal (including 0 → 0) | `NO_CHANGE` |
| any positive → 0 | `DECREASE` (full exit, however small the position, e.g. 0.00005 → 0) |
| 0 → any positive | `INCREASE` (entry, however small, e.g. 0 → 0.00005) |
| non-zero → non-zero, \|difference\| ≤ 0.0001 | `NO_CHANGE` (float accounting noise) |
| non-zero → non-zero, otherwise | `INCREASE` / `DECREASE` |

Zero is exact because the transaction layer removes a holding only at ≤ 0
shares (`execute_sell`, rebuilder replay), so any positive quantity is a real
holding. The 0.0001 tolerance is `execute_sell`'s oversell tolerance; it
exists to absorb float accounting noise and applies only between two non-zero
quantities. Transaction-layer quantity semantics are unchanged.

`evaluate_quantity_change(intent, current_quantity, proposed_quantity)` → `permission`:

| Situation | Permission | Reason |
|---|---|---|
| No quantity change | `ALLOWED` | `NO_QUANTITY_CHANGE` (with or without intent) |
| Position absent from referenced holdings (`current_quantity=None`) | `UNRESOLVED` | `POSITION_NOT_IN_REFERENCED_HOLDINGS` (the caller has no current quantity for it) |
| Change, no intent | `UNRESOLVED` | `NO_CONFIRMED_INTENT` |
| Increase with `increase_prohibited` | `PROHIBITED` | `INCREASE_PROHIBITED_BY_OWNER` |
| Decrease (incl. full exit) with `decrease_prohibited` | `PROHIBITED` | `DECREASE_PROHIBITED_BY_OWNER` |
| Otherwise | `ALLOWED` | `NOT_RESTRICTED_BY_CONFIRMED_INTENT` |

`evaluate_proposal(..., source, reason)` for `ADVISORY | SYSTEM_RULE | POLICY_RISK`
proposals → `outcome`: `CONSISTENT` (allowed), `CONFLICT` (prohibited),
`UNRESOLVED`. A CONFLICT returns the owner restriction, the proposal's source,
direction and reason, the intent id/revision, `conflict_kind`
(`INTENT_ADVISORY_CONFLICT | INTENT_SYSTEM_RULE_CONFLICT | INTENT_POLICY_CONFLICT`)
and `requires_owner_decision: true`. It never decides who wins.

Soft preference never changes an outcome; it is returned as context only.
Owner-entered execution decisions are not evaluated in V1.

## Isolation evidence

- `tests/test_position_intent_optimizer_inertness.py`: creating and revising
  intent leaves `/analyze/optimizer` inputs and persisted results identical;
  no module under `agents/`, `services/`, `routers/`, `models/`, `scripts/`
  other than the intent modules, ORM, API and CLI cascade references intent.
- `allow_swap` is never read or written by intent code (tested).

## Legacy `allow_swap` — characterization (unchanged behaviour)

`tests/test_allow_swap_legacy_characterization.py` pins today's behaviour:

1. The optimizer's lock resets any non-HOLD/WATCH action to HOLD, blocking both
   increases and decreases.
2. A locked holding with a SELL label keeps HOLD in allocations, while
   `swap_suggestions` still emits "Forced exit: SELL signal." for it.
3. An unlocked SELL-labelled holding is force-exited regardless of the AI.
4. Decision Workspace funding (`build_funding_sources`) has no lock input and
   uses a locked holding's SELL label as a funding source.
5. The transaction layer does not check `allow_swap`.

## Follow-up findings (recorded, not fixed in this slice)

| ID | Finding | Evidence |
|---|---|---|
| IIF-1 | Forced SELL is silently undone by `allow_swap` in allocations. | `agents/optimizer.py` forced-exit then lock loops |
| IIF-2 | Swap suggestions contradict locked allocations (forced exit still emitted). | `_derive_swap_suggestions` |
| IIF-3 | Decision Workspace funding ignores `allow_swap`. | `services/execution_plan.py`, `services/funding_source_analysis.py` |
| IIF-4 | Noise filter can suppress a forced SELL (drift < 1% or < 5,000 THB). | `services/noise_filter.py` `_SUPPRESSIBLE` includes SELL |
| IIF-5 | Min-cash and sector trims can turn a BUY into a REDUCE nobody proposed. | `_enforce_hard_policy` + `_reconcile_allocation_actions` |
| IIF-6 | Advisory Stock Analysis labels exercise deterministic authority (L1 gate, forced exits, funding, sizing, idea review). | optimizer, execution_plan, position_sizing, idea_review |
| IIF-7 | Human decisions are recorded after the recommendation and are not validated or fed back as owner constraints; `record_execution_decision` does not check `body.portfolio_id` against the snapshot's portfolio. | `main.py` `record_execution_decision` |
| IIF-8 | Lock UI copy says "won't be swapped" while code blocks every action. | `frontend/components/PortfolioTable.tsx` |

## Pre-existing test debt (unrelated, not fixed here)

| ID | Failing tests | Cause |
|---|---|---|
| TD-1 | `test_portfolio_investment_mandate_migration.py`, `test_goal_plan_amendment_history_migration.py` (one head-pin test each) | Both assert the Alembic head is `f7a9c1e3b5d7`; the head moved to `n6o7p8q9r0s1` in commit `54eacdd`, before this slice, and is now `o7p8q9r0s1t2`. Stale expectations; the chain itself is sound (`alembic heads` returns one head). |
| TD-3 | `test_position_conversion_live.py::test_lm13_no_frontend_authoring_path_for_position_conversion` | Matches the text `POSITION_CONVERSION` in `frontend/components/TransactionHistoryTable.tsx`, unchanged since commit `1f92aff` (#33). Not touched by this slice. |
| TD-2 | 4 consensus tests in `test_optimizer_pipeline.py` | Test-side `_consensus_engine()` signature mismatch (missing `l3`); already recorded in DECISION_LOG since Phase 4C.1. `optimizer.py` is unchanged by this slice. |

## Not in V1

Optimizer/prompt wiring, enforcement, Discovery integration, conversion of
legacy locks, a canonical holding-episode identity (R1 is the V1 mechanism), evaluation of
owner-entered decisions, delete/withdraw of intent, multi-user authorship.
