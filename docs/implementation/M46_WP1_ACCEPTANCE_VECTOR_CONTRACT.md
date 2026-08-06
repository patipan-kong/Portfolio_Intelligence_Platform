# M46-WP1 — Acceptance-Vector Contract and Coverage Matrix

**Artifact class:** Authorized WP1 documentary implementation deliverable 5 of 6

**Authoring role:** M46-WP1 Implementation Author

**Authorization:** [M46-WP1 Authorization Record](M46_WP1_AUTHORIZATION_RECORD.md)

**Contract disposition:** `COMPLETE`

**Fixture/adjudication disposition:** `FAIL-CLOSED — NO APPROVED M46 FIXTURES`

**Code and test implementation authority:** `NONE`

---

## 1. Contract purpose and limits

This document locks the generic vector catalogue required by frozen roadmap
§§17.1–17.3 and architecture §§17.1–17.5. It defines what every later approved
fixture must supply and what invariants its expected result must demonstrate.

It does not supply action facts, adjudicate an event, define canonical Asset or
Ledger vocabulary, create executable tests, or authorize WP2–WP8. Every
instance slot remains fail-closed until its named owner supplies approved
evidence and a later authorized package binds that evidence to owner contracts.

## 2. Mandatory vector record shape

Every vector instance shall contain all fields below. `N/A` is permitted only
with an owner-cited reason. Missing, ambiguous, conflicting, or inferred values
produce `BLOCKED`, never a default.

| Field ID | Required field | Exact contract |
| --- | --- | --- |
| `VF-01` | Vector identity | Immutable generic vector ID plus fixture revision |
| `VF-02` | Evidence | Immutable references, witness/source, origin, observed/received times, provenance, and conflict disposition |
| `VF-03` | Action identity | Owner-adjudicated case/co-reference identity; never inferred from symbol, price, or holding symptoms |
| `VF-04` | Participant identities | Exact permanent predecessor, successor, distributed, entitlement, and continuing asset/listing roles |
| `VF-05` | Time roles | Announcement, ex/entitlement, record, effective, election, settlement, payment, economic, and knowledge times as applicable |
| `VF-06` | Exact terms | Exact rational ratios, quantities, amounts, denominations, conditions, elections, fractions, and method versions |
| `VF-07` | Entitlement | Exact Accounting Scope, record-time holder evidence, election, and holder-specific outcome |
| `VF-08` | Confirmation path | Exact in-scope standing-policy identity/version or required-human confirmation record; absence blocks admission |
| `VF-09` | Identity consequences | Asset Foundation-owned verdict references; no WP1-authored facts |
| `VF-10` | Canonical Transactions | Ledger-owned one-stream representation, atomic group, order, idempotency, correction, and lineage references |
| `VF-11` | Total-basis instruction | Exact source basis, targets, amounts/weights, residue, fraction, cash/fee/tax treatment, denomination, and quantization |
| `VF-12` | Quote basis | Exact asset/listing, observation time, kind, unit/scale, currency, raw/source-adjusted/normalized basis, freshness, and identity |
| `VF-13` | Expected projection | Quantity, total basis, derived average cost, cash/entitlement, realized-input, cutoff, and lineage expectations |
| `VF-14` | Performance expectation | Zero return for a pure structural leg, separately classified economic legs, or explicit `UNCOMPUTABLE` |
| `VF-15` | Expected failures | Exact negative predicate, containment scope, diagnostic, and evidence required to unblock |
| `VF-16` | Immutability and determinism | Original records unchanged; repeat/cutoff result; no live provider, mutable symbol map, second stream, or host-time dependency |

## 3. Generic action-family coverage matrix

All rows require `VF-01` through `VF-16`. The “locked expectation” narrows the
family-specific invariant without supplying real terms.

| Vector ID | Required family/story | Locked positive expectation | Required negative/fail-closed counterpart | Instance state |
| --- | --- | --- | --- | --- |
| `AFV-001` | Stock split | Same identity; exact quantity rescale; retained total basis; derived average cost; structural zero return | Missing ratio, effective boundary, fraction rule, or confirmation blocks | `SLOTS ONLY` |
| `AFV-002` | ETF split | Same identity/listing unless owner says otherwise; exact rescale and basis preservation | Symbol/provider factor cannot supply identity or ratio | `SLOTS ONLY` |
| `AFV-003` | Reverse split without fractional cash | Same identity; exact rational rescale; explicit fraction eligibility and residue closure | Implicit whole-share rounding blocks | `SLOTS ONLY` |
| `AFV-004` | Reverse split with cash in lieu | Retained and disposed quantities/basis close exactly; cash leg separately classified | Missing cash price/basis allocation or holder outcome blocks | `SLOTS ONLY` |
| `AFV-005` | Symbol change | Same permanent identity; effective identifier update; zero quantity, basis, cash, and return effect | New Asset, sale/purchase, or current-symbol backfill is rejected | `SLOTS ONLY` |
| `AFV-006` | Name change | Same identity; descriptive change only | Accounting or quote substitution effect is rejected | `SLOTS ONLY` |
| `AFV-007` | Bonus shares | Exact quantity outcome and explicit total-basis instruction | Zero-basis or preserved-per-share default is rejected | `SLOTS ONLY` |
| `AFV-008` | Stock dividend | Same/distributed identity per owner verdict; exact quantity and basis | Family label cannot decide identity or basis | `SLOTS ONLY` |
| `AFV-009` | Ordinary cash dividend | Exact admitted cash movement; basis unchanged; income classification owned by Ledger | Provider dividend column alone cannot create cash truth | `SLOTS ONLY` |
| `AFV-010` | Explicit return of capital | Exact cash and explicit basis adjustment close under owner instruction | Reclassification from price/P&L symptom is rejected | `SLOTS ONLY` |
| `AFV-011` | Rights grant | Exact entitlement asset/relation and holder quantity | Missing entitlement identity, terms, or record-time holding blocks | `SLOTS ONLY` |
| `AFV-012` | Rights exercise | Existing entitlement consumed; subscription cash and received identity/quantity exact | Exercise without entitlement or election is rejected | `SLOTS ONLY` |
| `AFV-013` | Rights sale | Entitlement disposal and proceeds/basis classification exact | Inferred sale from cash receipt is rejected | `SLOTS ONLY` |
| `AFV-014` | Rights transfer | Exact transfer evidence and remaining holder state | Cross-scope or unconfirmed transfer is rejected | `SLOTS ONLY` |
| `AFV-015` | Rights lapse | Existing entitlement closes with explicit treatment | Silent expiry or guessed effective time is rejected | `SLOTS ONLY` |
| `AFV-016` | Rights cancellation | Cancellation lineage preserves original grant and creates no orphan state | Deletion or mutation of grant is rejected | `SLOTS ONLY` |
| `AFV-017` | All-stock merger/amalgamation | Exact predecessor/successor identities; one-time position and total-basis conversion | Symbol substitution, partial legs, or guessed ratio blocks | `SLOTS ONLY` |
| `AFV-018` | Cash merger/amalgamation | Predecessor disposal, cash consideration, basis, and realized inputs exact | Missing basis/cash classification or identity blocks | `SLOTS ONLY` |
| `AFV-019` | Mixed merger/amalgamation | Stock and cash legs form one complete atomic outcome; basis allocated once | Any missing leg or partial admission blocks all | `SLOTS ONLY` |
| `AFV-020` | One-child spin-off | Parent continues; child identity/relation exact; source basis allocated and closed | Market-price guess or zero child basis is rejected | `SLOTS ONLY` |
| `AFV-021` | Multi-child spin-off | Parent/children allocations and residue close exactly | Weights not summing to one or unresolved child blocks | `SLOTS ONLY` |
| `AFV-022` | Mutual-fund merger | Distinct or continuing identity only by owner verdict; quantity/basis conversion exact | Name/class similarity cannot establish continuity | `SLOTS ONLY` |
| `AFV-023` | Mutual-fund class conversion | Exact predecessor/successor class/listing identities and conversion | Related-class quote or symbol fallback is rejected | `SLOTS ONLY` |
| `AFV-024` | Corrected action | Exact reversal/compensation reference plus corrected successor; prior history retained | Mutation, over-reversal, or orphan correction is rejected | `SLOTS ONLY` |
| `AFV-025` | Postponed action | New immutable timeline revision; no effect at superseded date | Editing the original date or early admission is rejected | `SLOTS ONLY` |
| `AFV-026` | Cancelled action | Immutable cancellation/supersession; no unadmitted consequence becomes truth | Deleting announcement/adjudication history is rejected | `SLOTS ONLY` |
| `AFV-027` | Future event story | Owner-adjudicated story maps to existing governed effect algebra without replay branch | New label entering replay or ungoverned algebra extension blocks | `SLOTS ONLY` |

## 4. Cross-cutting coverage matrix

| Vector group | Required cases | Locked expectation | Coverage |
| --- | --- | --- | --- |
| `XCV-IDENTITY` | Current, historical, recycled, overlapping, and ambiguous identifier intervals; boundary instant; distinct related listing | Unique effective binding only; historical fact never re-resolved through current symbol; ambiguity inert | `COVERED BY CONTRACT — INSTANCES BLOCKED` |
| `XCV-ARITHMETIC` | Exact rational ratios, quantities, allocations, zero/positive denominators, residues, fractions, and reversals | Exact closure; declared quantization; deterministic residue; no float-derived truth | `COVERED BY CONTRACT — INSTANCES BLOCKED` |
| `XCV-TIME-SCOPE` | Same-time order permutations, economic/knowledge cutoffs, idempotent repeat, two Accounting Scopes | Canonical order only; historical-knowledge view distinct; duplicate inert; no cross-scope effect | `COVERED BY CONTRACT — INSTANCES BLOCKED` |
| `XCV-CONFIRMATION` | In-scope standing policy, absent policy, out-of-scope policy, required-human approval, missing human decision | Only exact delegation or recorded human decision admits; all other cases quarantine | `COVERED BY CONTRACT — INSTANCES BLOCKED` |
| `XCV-ONE-STREAM` | Canonical Transaction group, announcement/action object presented to replay, second effect stream, unfamiliar family label | Replay consumes only one canonical Transaction stream and no action story/classification | `COVERED BY CONTRACT — INSTANCES BLOCKED` |
| `XCV-QUOTE` | Raw, source-adjusted, normalized; unit, currency, listing, kind, freshness, related-security, predecessor/successor, DR/underlying mismatch; provider replacement | Exact compatible binding only; no double adjustment or related-security fallback; canonical result provider-neutral | `COVERED BY CONTRACT — INSTANCES BLOCKED` |
| `XCV-PERFORMANCE` | Pure structural leg, separately classified income/fee/cash leg, absent continuity composition | Structural leg yields zero return; economic leg retains owner meaning; otherwise `UNCOMPUTABLE` | `COVERED BY CONTRACT — OWNER COMPOSITION BLOCKED` |
| `XCV-MIGRATION` | Unaffected parity, affected predeclared explained difference, unresolved quarantine, interrupted shadow resume, cohort isolation, rollback read path | No production contamination; exact lineage; retry idempotent; unresolved subject not promoted | `COVERED BY CONTRACT — WP7 UNAUTHORIZED` |
| `XCV-DOWNSTREAM` | Stale snapshot/analysis/signal/evaluation and exact-lineage regeneration | Stale is visible; regeneration consumes exact admitted truth and worth only under authority | `COVERED BY CONTRACT — WP8 UNAUTHORIZED` |

## 5. Property and determinism obligations

Every applicable family vector must be paired with properties that prove:

1. quantity rescale preserves total basis except an explicitly allocated
   disposed fractional leg;
2. average cost is always derived from total basis and positive quantity;
3. allocation and conversion close exactly;
4. a pure structural leg preserves value and creates zero investment return,
   or performance is explicitly `UNCOMPUTABLE`;
5. input insertion order outside the canonical tuple is irrelevant;
6. duplicate idempotency identity cannot double-apply;
7. reversal plus corrected successor is deterministic and append-only;
8. no effect crosses Accounting Scope;
9. symbol/name change has zero accounting effect;
10. replay consults no announcement, action classification, proposal bundle,
    provider, live clock, mutable symbol map, or second stream;
11. absent/out-of-scope delegation and missing required human confirmation
    prevent admission; and
12. an unfamiliar future story cannot introduce a replay branch.

These are documentary obligations, not executed tests in WP1.

## 6. BANPU parameterized acceptance vector

BANPU is a single real-incident fixture label. No term may be copied from
portfolio symptoms, provider output, price discontinuity, or current holdings.

### 6.1 Evidence slots

| Slot | Required competent supply | WP1 value | State |
| --- | --- | --- | --- |
| Participant permanent identities/listings | Asset Foundation-approved fixture | `UNSUPPLIED` | `BLOCKED` |
| Action identity and family | Asset Foundation-approved adjudication fixture | `UNSUPPLIED` | `BLOCKED` |
| Announcement/effective/entitlement/settlement timeline | Approved evidence/adjudication fixture | `UNSUPPLIED` | `BLOCKED` |
| Conversion/distribution ratio | Approved exact-rational fixture | `UNSUPPLIED` | `BLOCKED` |
| Consideration legs | Approved fixture | `UNSUPPLIED` | `BLOCKED` |
| Fractional treatment and holder outcome | Approved fixture and portfolio evidence | `UNSUPPLIED` | `BLOCKED` |
| Total-basis instruction | Ledger-approved fixture | `UNSUPPLIED` | `BLOCKED` |
| Confirmation path | Exact standing-policy or human-decision fixture | `UNSUPPLIED` | `BLOCKED` |
| Quote identity and basis | Market Intelligence-approved fixture | `UNSUPPLIED` | `BLOCKED` |

### 6.2 Acceptance assertions once slots are competently supplied

| BANPU criterion | Required assertion | Current status |
| --- | --- | --- |
| `BANPU-01` | Every original Transaction remains byte/content unchanged and traceable | `CONTRACTED — NOT EXECUTED` |
| `BANPU-02` | Identity treatment follows Asset Foundation adjudication, never symbol substitution | `CONTRACTED — NOT EXECUTED` |
| `BANPU-03` | Quantity equals exact admitted conversion effects | `CONTRACTED — NOT EXECUTED` |
| `BANPU-04` | Predecessor total basis is allocated exactly once | `CONTRACTED — NOT EXECUTED` |
| `BANPU-05` | Successor average cost equals total basis divided by positive quantity | `CONTRACTED — NOT EXECUTED` |
| `BANPU-06` | Quote matches exact successor listing, unit, currency, time, kind, and basis | `CONTRACTED — NOT EXECUTED` |
| `BANPU-07` | Valuation/P&L has no identity, ratio, or double-adjustment artifact | `CONTRACTED — NOT EXECUTED` |
| `BANPU-08` | Structural transition yields zero return or affected performance is `UNCOMPUTABLE` | `CONTRACTED — NOT EXECUTED` |
| `BANPU-09` | Complete manifest passes ingestion and exact confirmation path | `CONTRACTED — NOT EXECUTED` |
| `BANPU-10` | Repeated replay and historical cutoffs are deterministic | `CONTRACTED — NOT EXECUTED` |
| `BANPU-11` | No code/config contains a BANPU conditional, ratio, exception, or alias | `CONTRACTED — NO CODE AUTHORIZED` |

## 7. Failure-containment contract

Every negative vector must record subject, stage, reason, immutable source
identities, conflicting/missing coordinates, observation times, smallest
truthful containment boundary, and exact resolution evidence. Expected outcomes
are limited to quarantine, unresolved identity, inadmissible bundle,
uncomputable performance, unvalued holding, blocked projection, blocked shadow
promotion, or stale downstream state as owned by later contracts. Zero,
current-symbol substitution, average-cost fallback, provider preference, and
partial admission are forbidden defaults.

## 8. Coverage verification

| Frozen obligation | Matrix location | Status |
| --- | --- | --- |
| Roadmap §17.1 generic families | §3, `AFV-001`–`AFV-027` | `COMPLETE` |
| Architecture §17.1 pure domain vectors | §3 | `COMPLETE` |
| Architecture §17.2 properties | §5 | `COMPLETE` |
| Architecture §17.3 identity/quote vectors | §4 `XCV-IDENTITY`, `XCV-QUOTE` | `COMPLETE` |
| Architecture §17.4 replay/migration vectors | §4 `XCV-TIME-SCOPE`, `XCV-ONE-STREAM`, `XCV-MIGRATION`, `XCV-DOWNSTREAM` | `COMPLETE` |
| Roadmap §17.2 cross-cutting vectors | §4 | `COMPLETE` |
| Roadmap §17.3 / Architecture §17.5 BANPU | §6 | `COMPLETE AS UNFILLED CONTRACT` |
| Evidence-to-failure field completeness | §§2 and 7 | `COMPLETE` |

The contract coverage is complete. Fixture population and execution are
blocked by absent approved owner evidence, absent later-package authority, the
open alignment residual, and the AF frozen-predecessor identity mismatches.

## 9. Terminal disposition

**Acceptance-vector contract: `COMPLETE`.**

**Acceptance fixture execution: `FAIL-CLOSED — NOT AUTHORIZED AND REQUIRED
OWNER EVIDENCE UNSUPPLIED`.**

This document does not authorize test/code implementation, action
adjudication, owner contracts, schema/runtime change, migration, replay,
accounting, quote selection, production correction, WP2–WP8, release, or
closeout.
