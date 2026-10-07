# Advisory Integration V1 — Slice 1: Held-Position Intent Context + Deterministic Review

**Status:** Implemented behind a default-OFF flag; not committed.
**Date:** 2026-10-07
**Branch:** `feature/advisory-intent-integration-v1` (from `origin/main` `bedf5b9`, which contains #54 Investor Intent and #55 Shadow Candidate Discovery)
**Flag:** `FEATURE_ADVISORY_INTENT_REVIEW_V1` (only `"true"` enables, any case)
**Contracts:** `wealth.advisory-intent-review.v1`, projection `wealth.held-quantity-projection.v1`, Intent `investor-intent.v1`
**Migration:** none. The Alembic head stays `o7p8q9r0s1t2`.

## Specification source

This slice implements the owner's Slice-1 instruction (2026-10-07), which
restates the Slice-0 contract-closure verdict. The Slice-0 report itself was
not available in the repository or in this session's context. Where the
instruction left room, the engineering choices are listed under
**Engineering choices** below. None of them is a new product semantic.

## Scope

- **In scope:** `/analyze/optimizer`, for existing positive held positions only.
- **Not Intent-aware yet:**
  - position sizing, risk budget, idea review, Decision Workspace funding/execution plan;
  - Candidate Discovery;
  - new-position and Cash Intent;
  - Stock Analysis;
  - legacy `allow_swap` migration;
  - the decision workflow.

The UI says the other tools are not Intent-aware.

## One flag, one unit

`services/advisory_intent_flag.py` holds the only switch. It covers, as one unit:
- the frozen Intent context;
- the common-NAV basis;
- prompt context;
- provenance;
- the review;
- the envelope;
- the response fields.

No narrower switch exists, so AI Intent context can never run without the deterministic review.

**Flag off:**
- `run_layered_optimizer` receives no `advisory` argument, and every hook in `agents/optimizer.py` is a no-op.
- Prompts are byte-identical, and allocations, persistence and the response are unchanged.
- The Intent API keeps its "not yet read" disclosure.
- History and snapshot reads gain no fields.

The response-view refactor (`apply_response_views`) runs the same three stages in the same order for the legacy path.

## Flow of an enabled run

1. **Before any AI call,** `build_advisory_run` loads the frozen run context once, in bulk:
   - one query for intents and one for revisions, using `investor_intent_store.held_intent_applicability`;
   - it reads the holdings the run already references, the run's quotes, and Registry currency facts.
2. **L1/L2/L3, the L1 retry and the single-shot fallback** receive only that object:
   - hard restrictions go to every layer;
   - soft preference goes to L2 and the fallback only, because the fallback substitutes for L2 allocation reasoning.
3. **Mutation sites record proposal transitions** in a bounded, run-scoped ledger, as they happen.
4. **After stabilization,** the economic allocation stays exactly as stabilization left it. A deep copy, the *response projection*, runs the noise filter, action summary and execution optimization once.
5. **The review** reads the economic rows, the response rows and the ledger, then builds and freezes the envelope (sha256 digest).
6. **The envelope is persisted** in `OptimizerHistory.result_json["advisory_intent_review"]`. The stored rows stay the unfiltered economic rows, as before.
7. **The already-computed response projection is returned,** with the envelope.

## Canonical NAV and quantity contract

- `N = E + C`: frozen held quotes times referenced shares, plus referenced cash.
- When that basis resolves, held current weights for the AI prompts and for `pc_map` (and therefore `current_weight` on allocation rows) are `100·V0/N`. Otherwise legacy (equity-only) weights stand.
- Quantities use `Decimal` and are serialized as exact decimal strings. Proposed shares are quantized to `0.000001` with `ROUND_HALF_UP`. Rounded display values are never fed back into the projection.

| Proposal | Proposed shares |
|---|---|
| HOLD / WATCH (unchanged control) | `q0` |
| SELL to 0 (full exit) | `0`, delta `−V0` |
| BUY / ACCUMULATE / REDUCE / partial SELL | `N·t/100 / p` |

If the action's direction and the quantity's direction disagree, the result is `UNRESOLVED` (`ACTION_QUANTITY_DIRECTION_MISMATCH`). Direction is never inferred from whichever field makes Intent look satisfied.

### Temporary mixed-basis boundary (`SLICE1_TEMPORARY_MIXED_BASIS`)

Slice 1 deliberately does not convert the policy engines to the common NAV. The boundary is explicit and is recorded in every envelope under `valuation.basis_boundary`.

| Uses the frozen common NAV (when the basis resolves) | Keeps its legacy basis / rule semantics |
|---|---|
| Held current weights in the L1/L2/L3/fallback prompts | Policy envelope inputs |
| `pc_map`, and therefore every allocation row's `current_weight` | Tier-1 breach detection and current sector weights (equity-only `weight_pct`) |
| Canonical quantity projection | Hard-policy rules: emergency freeze, position cap, cash floor, regime rules, sector trim |
| Intent review | DR/illiquid execution cap, forced SELL, legacy lock, action reconciliation, neutral snap, stabilization, noise filter, execution scheduling |

**Known mixing point.** Rules that compute `allocation_change_percent = target_weight − current_weight` (hard policy, reconciliation, noise drift) read the row's `current_weight`. In an enabled run with a resolved basis, that is the common-NAV value. The thresholds and rule definitions themselves are unchanged and are not re-based.

**Evidence representation:**
- Every transition carries `rule_semantics` (`ADVISORY_MODEL_OUTPUT`, `LEGACY_POLICY_RULE` or `LEGACY_SYSTEM_RULE`) and `row_current_weight_basis` (`COMMON_NAV_FROZEN_QUOTES` or `LEGACY_EQUITY_ONLY`).
- Each proposal records `target_origin_stage` and `target_origin_semantics`. A policy cap that scales an advisory proposal without reversing it keeps `source = ADVISORY` but moves the target origin to `HARD_POLICY` / `LEGACY_POLICY_RULE`.
- The final and retained projections carry `basis_evidence`: `projection_basis` (the frozen common NAV the target is projected onto) and the target origin. A legacy rule's target projected onto the NAV is therefore never presented as if the rule had computed on the NAV.

Converting policy, breach and sector logic to the common NAV is a later slice.

**Unresolved basis.** The basis is `UNRESOLVED`, legacy advice is kept, and nothing is fabricated when any of these hold:
- a missing, zero, negative, stale, cache-miss or quarantined quote;
- unknown Registry currency;
- mixed units (including THB cash with non-THB holdings);
- a duplicate or negative holding row;
- an invalid cash balance;
- a non-positive NAV.

There is no average-cost substitution and no FX conversion.

**Tolerance ambiguity.** When the exact six-decimal direction and the kernel's 0.0001-tolerance direction disagree, the review is `UNRESOLVED` with `QUANTITY_DIRECTION_TOLERANCE_AMBIGUITY`.

## Provenance (bounded, not event sourcing)

**Vocabulary:**
- **Sources:** `ADVISORY`, `SYSTEM_RULE`, `POLICY_RISK`.
- **Effects:** `ORIGINATE`, `REPLACE`, `SUPPRESS`, `RELABEL`, `DEFER`, `SCALE`.
- **Dispositions:** `ACTIVE`, `REPLACED`, `SUPPRESSED`, `ABANDONED`.

Each transition records:
- sequence, attempt, proposal id and replaced proposal id;
- source, stage and effect;
- reason code and reason text;
- before/after action, target weight and current weight;
- the resulting disposition.

Unbounded values are rejected. A capture failure never breaks the run: it marks every final review `UNRESOLVED` (`PROVENANCE_CAPTURE_FAILED`).

**Stages captured:**

| Stage | Effect / reason |
|---|---|
| Accepted L1 swap legs | ORIGINATE; legs dropped by the legacy lock are SUPPRESSED (both `INTERMEDIATE_REASONING`, see below) |
| L2 allocation | ORIGINATE |
| Fallback allocation | ORIGINATE |
| Forced SELL | — |
| Legacy `allow_swap` | — |
| Hard policy | Emergency freeze, position cap, cash floor, regime cap / cash floor, sector trim |
| DR/illiquid execution cap | — |
| Action reconciliation | — |
| Neutral snap | — |
| Stabilization drift deferral | — |
| Noise filter | — |
| Execution scheduling | DEFERRED / SCALED |

A `SCALE` that reverses direction (for example a cash-floor trim that turns BUY into a decrease) becomes a `REPLACE`, so the original advisory proposal is retained.

**Abandoned attempts.** When the primary pipeline falls back, every primary-attempt proposal becomes `ABANDONED`, and the prompt path marks primary successes `ABANDONED`. Abandoned proposals are never active and never a conflict.

## Final versus retained review

- **Final review:** the quantity the plan proposes today. It mirrors the execution-plan derivation: noise-suppressed and drift-tolerant rows are unchanged today. Scheduling is excluded; its SCALE/DEFER quantities are kept separately under `proposal.scheduled` and never overwrite the economic proposal.
- **Retained reviews:** every non-abandoned **material** proposal other than the one that *is* the final plan whose direction differs from the final direction (or cannot be resolved). This includes the deferred economic proposal of a drift-tolerant row.
- **Materiality (owner decision, 2026-10-07):** L1 strategist legs are intermediate advisory reasoning. The material recommendation path is the accepted L2/fallback allocation plus the deterministic system/policy mutations downstream of it (forced SELL, policy trims and reversals, legacy-lock suppression of a material proposal, noise suppression, scheduling).
  - An L1 leg is `INTERMEDIATE_REASONING`, and so is the HOLD placeholder the legacy lock leaves when it drops an L1 leg.
  - Once superseded, these are listed under `review.non_material_provenance` (`excluded_from_review: SUPERSEDED_INTERMEDIATE_REASONING`) and stay in the transition log.
  - They are never reviewed, never counted in conflict coverage, never set `requires_owner_decision` and never mark the position as a material change.
- **Applicability:** an intent that is not `CONFIRMED` (`NO_CONFIRMED_INTENT`, `RECONFIRMATION_REQUIRED`, `CONTEXT_UNAVAILABLE`) gives `UNRESOLVED` even for an unchanged quantity. A re-confirmation-required intent appears only as `historical_intent` evidence.
- **Owner decision:** `requires_owner_decision` is true when any final or retained proposal conflicts.

A conflict is not:
- a governance violation;
- a policy penalty;
- a HOLD/SELL decision;
- a redistribution.

Tests prove that allocations, consensus, policy, action summary and execution optimization are identical with and without a conflicting intent.

## Envelope sections

**Top level:** `identity`, `reference`, `valuation`, `prompt_use`, `positions`, `provenance`, `display`, `coverage`, `review`, `integrity`.

**Each position carries:**
- referenced shares and episode start;
- legacy lock;
- applicability;
- applicable intent (id, revision, confirmation time) or `null`;
- historical intent evidence;
- hard restrictions;
- soft preference;
- economic candidate, final effective and scheduled quantities;
- its transitions;
- final and retained reviews;
- display disposition.

**Coverage** counts:
- referenced positive held positions;
- checked positions;
- resolved positions;
- unresolved positions;
- conflict positions (the union);
- final-conflict positions;
- retained-conflict positions.

These are symbol sets, so overlapping conflict categories are never double-counted.

## Historical reads

With the flag on, `GET /optimizer/history/{id}` and `GET /optimizer/snapshots/{id}` (through the existing `optimizer_history_id` link) return the frozen envelope with `advisory_intent_review_status`:
- `CAPTURED`;
- `NOT_CAPTURED` (no envelope);
- `EVIDENCE_INVALID` (unsupported version, missing section, or digest mismatch).

They never recompute from current intent, thresholds or policy. Current intent is used only for `advisory_intent_changes_since_run`, which lists positions whose stored revision moved since the run. RecommendationSnapshot has no new column and no copy of the envelope.

## UI

`components/optimizer/AdvisoryIntentReviewCard.tsx`, under the Execution Plan card, shows:
- the conflict or coverage summary;
- per-position detail only for conflicts, unresolved positions, and material replacement/suppression/deferral;
- the not-a-block note;
- the not-yet-Intent-aware tools.

"Recommendation respects your intent" appears only when coverage is fully resolved and consistent. The Investor Intent panel's disclosure follows the flag, and `enforced_by_optimizer` stays `false`.

## Engineering choices (made without the Slice-0 report)

1. **Cash unit.** `Portfolio.cash_balance` has no currency column, and every platform cash, goal and liability amount is THB-constrained, so cash counts as THB. Holdings with any other Registry currency make the basis `CURRENCY_MIXED` (all-USD holdings with zero cash resolve in USD).
2. **Stale quotes fail closed** (`QUOTE_STALE`). On a VPS node serving expired cache this leaves reviews UNRESOLVED; see operational note O-1.
3. **Canonical weights** replace the held current weights given to the AI and in `pc_map` only. Policy envelope inputs, Tier-1 breach detection and sector projections keep their existing equity-only basis, because changing policy inputs is out of scope. See the temporary mixed-basis boundary above.
4. **L1 swap legs** carry a direction but no target. The original choice reviewed them by direction only; the owner overrode it on 2026-10-07, so superseded L1 legs are now non-material provenance and are not reviewed (see Materiality).
5. **Same direction as final.** A retained proposal whose direction equals the final direction is not listed, because its review equals the final review.
6. **Run-level stabilization status** (COOLDOWN / NO_REBALANCE) is recorded in `display`, not applied per row. The execution plan derivation does not remove rows for it either.
7. **Context-load failure** produces a run with no prompt context in which every held position is `CONTEXT_UNAVAILABLE`. Legacy advice continues, and the error is logged.

## Tests

| File | Coverage |
|---|---|
| `tests/test_advisory_intent_projection.py` | 29 pure tests: NAV basis, projections, precision, quotes, currency, duplicates, tolerance ambiguity, ledger semantics, materiality, target-origin semantics |
| `tests/test_advisory_intent_integration.py` | 28 end-to-end tests through the real endpoint and optimizer, with `call_ai` mocked and no live calls |
| `tests/test_position_intent_optimizer_inertness.py` | Updated allow-list: only the two advisory modules may read Intent besides its own modules; the flag-off behavioural inertness test pins the flag off |
| `frontend/tests/AdvisoryIntentReviewCard.test.tsx` | 7 tests |

## Known test debt (pre-existing, not introduced here)

- **TD-2:** 4 consensus tests in `test_optimizer_pipeline.py` fail with `_consensus_engine() missing 1 required positional argument: 'l3'`. This is a test-side signature mismatch.
- **TD-4:** `test_optimizer_history_snapshot_injection.py` fails in isolation (5 tests) because the file does not import `models.asset` before `create_all`. Run after a module that does, it passes (verified on clean `bedf5b9` as well as this branch).
- **Frontend `tsc`:** 9 pre-existing errors in `tests/ReportCardPage.test.tsx` and `tests/GoalAwareOptimizerBridge.test.tsx`.

## Operational note

**O-1.** With the flag on, any held quote served from expired cache (`_stale_data`) makes the valuation basis UNRESOLVED for the whole run. That keeps legacy weights and gives UNRESOLVED reviews. This is correct fail-closed behaviour, but it may be frequent on a VPS node whose quote cache is not refreshed. Check quote freshness before enabling in production.
