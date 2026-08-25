# BANPU-WP4 — Retry-Order Governance Decision

**Artifact class:** Bounded canonical governance decision and amendment record
**Decision date:** 2026-08-13
**Issuing authority:** BANPU-WP4 Canonical Governance Authority
**Finding resolved at governance level:** `WP4-IIR-B1`
**Governance outcome:** `OUTCOME 2 — BOUNDED CANONICAL AMENDMENT REQUIRED`
**Selected resolution:** `ALTERNATIVE C — BOUNDED RETRY PREFLIGHT`
**Amendment lifecycle state:** `PREPARED — INDEPENDENT APPROVAL AND PLAN REAPPROVAL REQUIRED`
**Implementation reliance created by this act:** `NONE UNTIL SUCCESSOR GOVERNANCE ACTS COMPLETE`
**Implementation performed:** `NO`
**Implementation review or confirmation performed:** `NO`
**Freeze or closeout performed:** `NO`
**Release, deployment, production execution, or production-data authority:** `NONE`
**BANPU-WP5+ authority:** `NONE`
**M46 authority:** `NONE`

---

## 1. Nature and boundary of this act

This act resolves only the runtime-order conflict identified as
`WP4-IIR-B1` in
[the BANPU-WP4 Independent Implementation Review](BANPU_WP4_INDEPENDENT_IMPLEMENTATION_REVIEW.md).
It selects the smallest safe canonical amendment needed to reconcile
first-application optimistic validation with post-materialization retry
idempotency.

This record is additive. It does not silently rewrite a frozen artifact, modify
implementation or test code, correct findings `WP4-IIR-B2` through
`WP4-IIR-B6`, review a corrected candidate, confirm implementation, freeze or
close WP4, or create release, deployment, production, WP5+, or M46 authority.

The selected semantics in Section 6 are the exact bounded amendment candidate
for the successor governance chain. They are not implementation-reliable until
the independent approval, confirmation, binding, and Work Package Plan
reapproval requirements in Section 10 are complete.

## 2. Canonical authorities examined

The decision independently examined and preserved except for the proposed
bounded exception stated here:

- [the canonical implementation design](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md),
  especially Section 9;
- [the work-package roadmap](BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md),
  especially BANPU-WP4 atomicity and idempotency outcomes;
- [the mandatory implementation sequence](BANPU_IMPLEMENTATION_SEQUENCE.md),
  especially Step 4 retry, conflict, stale-expectation, and atomicity evidence;
- applicable frozen WP1, WP2, and WP3 authority and evidence;
- [the BANPU-WP4 Allocation Record](BANPU_WP4_ALLOCATION_RECORD.md);
- [the BANPU-WP4 Implementation Authorization Record](BANPU_WP4_IMPLEMENTATION_AUTHORIZATION_RECORD.md);
- [the BANPU-WP4 Work Package Plan](BANPU_WP4_WORK_PACKAGE_PLAN.md),
  especially Sections 3.2, 6, and 9;
- [the roadmap Section 1 reviewer confirmation](BANPU_WP4_ROADMAP_SECTION_1_REVIEWER_CONFIRMATION.md);
  and
- [the Independent Implementation Review](BANPU_WP4_INDEPENDENT_IMPLEMENTATION_REVIEW.md).

The existing implementation candidate was not treated as canonical authority.

## 3. Exact constitutional question

Canonical Design Section 9 states that, within one database transaction, the
service must locate the predecessor and verify optimistic quantity/basis before
it rejects a conflicting duplicate or returns `already_applied` for an
identical canonical fingerprint.

Work Package Plan Section 3.2 operationalizes that order as E5, E6, E7, E8 and
Section 9 requires the Section 3.2 runtime order to hold. At the same time:

- E10 removes or transforms the predecessor materialized holding after a
  successful first application; and
- LM-14 requires the later matching canonical retry to return
  `already_applied` as a no-op, without a duplicate transaction or repeated
  materialized-state write.

The constitutional question is whether E5/E6 must execute against current
predecessor materialized state before retry identity can be recognized even
when the first application has canonically consumed that state.

## 4. Contradiction determination

**A genuine retry-order conflict exists.**

The frozen corpus simultaneously requires:

1. E5/E6 before E8 in the stated one-transaction order, without a textual
   retry exception; and
2. a post-materialization matching retry to succeed as `already_applied` after
   E10 has removed or transformed the state E5/E6 require.

No existing sentence expressly makes the E5/E6 order first-application-only,
defines duplicate evaluation as a retry preflight, or permits an
already-materialized retry to bypass current predecessor state. Work Package
Plan Section 9 instead makes the Section 3.2 order an exit criterion. Reading an
unstated exception into that text would manufacture an interpretation to avoid
amendment and would repeat the implementation-discretion error identified by
the Independent Implementation Review.

The conflict is invocation-class-specific:

| Invocation class | Canonical need |
|---|---|
| First/new application | E5/E6 must validate current predecessor state before every write |
| Matching retry after successful materialization | Canonical transaction identity must be recognizable without recreating consumed predecessor state |
| Conflicting retry | The collision at the same canonical conversion identity must fail closed without relying on consumed predecessor state |
| Stale-state, nonduplicate attempt | No prior canonical conversion exists; E5/E6 must execute and fail closed on stale state |

Because the original text does not express that distinction, Outcome 1 is not
available.

## 5. Alternatives evaluated

### 5.1 Alternative A — unconditional original order

**Rejected.** Requiring E5/E6 on every invocation makes LM-14 unreachable after
a successful conversion removes the predecessor holding. Satisfying E5/E6
would require reconstructing, fabricating, or treating historical transaction
facts as current materialized predecessor state. That would blur replay,
repair, and live idempotency ownership and would not be a no-op retry.

### 5.2 Alternative B — unconditional E8 before E5/E6

**Rejected as overbroad.** Moving the complete idempotency decision ahead of
predecessor lookup and optimistic validation for every invocation erases the
canonical distinction between new work and retry disposition. Without a
strict prior-row predicate it could allow a new or stale conversion to bypass
the very current-state checks C-5 requires and unnecessarily changes the normal
first-application path.

### 5.3 Alternative C — bounded retry preflight

**Selected.** After the common identity, payload, registry, date, locking, and
MINOR-1 boundary, the service performs a read-only lookup for the canonical
conversion identity:

- no prior conversion: E5/E6 remain mandatory, followed by the unchanged
  first-application write order;
- prior conversion plus exact canonical fingerprint equality: complete the
  read-only transaction lifecycle and return `already_applied`, bypassing only
  current predecessor E5/E6;
- prior conversion plus a different fingerprint: complete deterministic
  rollback/cleanup and hard-fail as a conflict, bypassing only current
  predecessor E5/E6.

The bypass exists solely because the append-only canonical transaction proves
that this exact conversion identity has already crossed E9–E13. It is not a
general permission to skip optimistic validation.

### 5.4 Alternative D — reconstruct predecessor state for retry

**Rejected.** Replaying historical rows or deriving an artificial predecessor
holding solely to satisfy the original textual order would duplicate frozen WP2
replay ownership, turn idempotency into reconstruction, and increase the
surface beyond the minimum exception. It also would not validate the current
materialized state in the sense E5/E6 originally require.

## 6. Exact selected runtime-order semantics

The bounded amendment introduces one retry-disposition preflight, denoted
`E8-R`, without creating a second fingerprint or a general idempotency
framework.

### 6.1 Common validation boundary

Every invocation, including matching and conflicting retries, must complete the
following before `E8-R` can return or fail:

1. enter a service-owned, deterministic transaction lifecycle for all database
   access;
2. establish workspace/portfolio ownership and lock the portfolio so concurrent
   first applications serialize;
3. parse and validate the canonical version-1 payload;
4. establish the predecessor asset ID and successor asset ID, require them to
   be distinct, and preserve all existing registry-resolution requirements;
5. acquire locks on every relevant existing `PortfolioItem` row identified by
   the canonical asset identities and the controlled legacy fallback;
6. validate the complete E3 registry state, including successor provider
   identity, predecessor retirement and `MERGED` status, and exactly the
   required `MERGED_INTO` relationship;
7. derive and validate the canonical naive-midnight transition date solely from
   the payload calendar date;
8. complete the E7 `MINOR-1` safety gate and obtain the one canonical
   fingerprint from the canonicalizer; and
9. construct the canonical conversion identity exactly as conversion type
   `POSITION_CONVERSION` plus portfolio ID, predecessor asset ID, and canonical
   transition date, under the already-established workspace ownership.

No retry bypass may occur before this common boundary.

### 6.2 `E8-R` canonical conversion-identity lookup

Within the same owned transaction lifecycle, query the append-only transaction
store for exactly the identity in Section 6.1 item 9. The portfolio lock is the
primary serialization boundary; an existing conversion row must also be read
under the strongest row-lock behavior supported by the authorized database
path, with the existing unique constraint retained as the final concurrency
backstop.

If an existing row is found, the service must additionally prove before any
retry disposition that:

- its transaction type, workspace/portfolio ownership, predecessor asset ID,
  and transition date agree with the canonical lookup identity;
- its stored conversion payload parses as a valid canonical payload;
- its successor asset identity and every other payload semantic participate in
  the stored canonical fingerprint; and
- the incoming and stored fingerprints compare as exact strings generated by
  the one canonical fingerprint algorithm.

An invalid or internally inconsistent existing row is neither a match nor a
repair opportunity; it fails closed.

## 7. Invocation-class semantics

### 7.1 First/new application

When `E8-R` finds no prior canonical conversion:

1. perform E5 predecessor lookup by canonical asset ID with only the existing
   controlled legacy-symbol fallback;
2. perform E6 optimistic quantity and basis verification against current
   predecessor materialized state using the canonical tolerances;
3. on any missing, ambiguous, stale-quantity, or stale-basis condition, roll
   back/clean up and fail closed;
4. only after E3 and E6 succeed may E9 insert the append-only transaction;
5. retain E9 before E10–E12; and
6. retain E13 final shares, basis, cash, and identity assertions before the sole
   successful commit.

Thus E5/E6 remain mandatory for every new/nonduplicate conversion and precede
every first-application write. The amendment creates no optimistic-check bypass
for new work.

### 7.2 Matching retry

When `E8-R` finds one valid existing conversion with the same canonical
conversion identity and exact canonical fingerprint:

- classify the invocation as an already-materialized canonical retry;
- do not require current predecessor E5/E6, because E10 may have consumed that
  state during the proven first application;
- perform no insert, update, delete, cash mutation, holding mutation, registry
  mutation, repair, reconciliation, replay, or snapshot action;
- deterministically complete the read-only transaction/session lifecycle with
  no open transaction or retained lock; and
- return the canonical `already_applied` no-op disposition identifying the
  existing transaction.

Current successor materialized state is not an idempotency predicate. Later
authorized trades, accounting readers, or other legitimate changes may alter
that state. Checking or repairing it here would turn retry recognition into a
WP5-style reconciliation or repair operation. The E3 registry invariants and
the append-only canonical transaction identity remain mandatory; materialized
successor reconciliation remains outside this retry path.

### 7.3 Conflicting retry

When `E8-R` finds an existing conversion at the same canonical conversion
identity but with a different canonical fingerprint:

- classify it as a conflicting retry;
- do not require current predecessor E5/E6;
- perform no write or repair;
- deterministically roll back/clean up the transaction and release locks; and
- hard-fail with a controlled conflict disposition.

A different successor asset ID, ratio, quantity, basis, CIL fact, date semantic,
evidence value, or any other fingerprinted payload semantic therefore cannot be
accepted as `already_applied` even though the top-level conversion identity key
matches.

### 7.4 Stale-state nonduplicate attempt

When no existing conversion is found, the invocation is not a retry. It must
proceed through E5/E6. A stale quantity or basis fails closed before E9. The
existence of `E8-R` does not weaken stale-state protection.

## 8. Transaction-lifecycle rule

The bounded retry exception is inseparable from a deterministic transaction
lifecycle:

- pure parsing may occur before database access, but once any lock or query
  begins, every exit is inside the service-owned cleanup boundary;
- a successful `already_applied` no-op must finish the read-only transaction
  and release every lock before returning;
- payload, identity, registry, date, existing-row validation, and conflict
  failures must roll back/clean up before raising or returning;
- a no-prior-row first application retains exactly one transaction over its
  locks, E5/E6, E9–E13 writes, final assertions, and sole successful commit;
- no caller-visible path may leak an open transaction; and
- transaction cleanup itself performs no business mutation and cannot be used
  to disguise a retry repair.

This rule supplies the canonical precision needed to correct
`WP4-IIR-B4`; it does not implement that correction or change B4's review
classification.

## 9. Relationship to MINOR-1 and preserved prohibitions

The Independent Implementation Review's determination that `MINOR-1` is
technically satisfied at the WP4 pre-use point is preserved. `E8-R` is always
downstream of E7. This act does not reopen, widen, or modify the admitted
canonicalizer correction.

The selected amendment does not permit:

- idempotency evaluation before portfolio, payload, registry, date, or
  MINOR-1 validation;
- E5/E6 bypass when no prior canonical conversion exists;
- a second or WP4-local fingerprint;
- acceptance by partial payload comparison;
- more than one existing conversion at the canonical identity;
- materialized successor repair or reconciliation during retry;
- retry writes of any kind;
- caller-controlled identity in place of registry resolution;
- a general idempotency framework or corporate-action abstraction;
- changes to replay, validator, snapshot, CLI, API, frontend, cache, WP5+, or
  M46 behavior; or
- release, deployment, production execution, or production-data mutation.

## 10. Canonical amendment and lifecycle consequences

### 10.1 Exact canonical artifacts requiring amendment

The normative effect touches exactly:

1. `docs/implementation/BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`,
   Section 9, to distinguish the common validated retry preflight from the
   E5/E6-first new-application path and to define the matching/conflicting retry
   exception; and
2. `docs/implementation/BANPU_WP4_WORK_PACKAGE_PLAN.md`, Sections 3.2, 6, and 9,
   to operationalize `E8-R`, its cleanup evidence, the conditional E5/E6 bypass,
   and the amended exit criterion.

No roadmap, mandatory-sequence, allocation, implementation-authorization,
roadmap Section 1 confirmation, WP1/WP2/WP3 implementation, Decision Log,
Implementation INDEX, WP5+, or M46 amendment is required. Those artifacts
already authorize or require the same atomic service, canonical fingerprint,
optimistic checks for new work, matching no-op, conflicting failure, and
surface. This decision changes invocation ordering only and creates no new
capability or file surface.

### 10.2 Smallest normative change

The smallest amendment is the additive semantic supplement in Sections 6–8:
split duplicate handling into a validated read-only `E8-R` retry preflight,
retain E5/E6 for every no-prior-row application, and permit E5/E6 bypass only
after a valid prior canonical transaction proves a matching or conflicting
retry at the same canonical identity.

No existing accounting equation, payload field, canonical identity, tolerance,
write order, final invariant, file surface, or package ownership changes.

### 10.3 Required successor governance acts

Because Canonical Design Section 9 is frozen and the current Work Package Plan
expressly requires the unqualified Section 3.2 order, this decision is not
self-executing. Before implementation relies on the exception, the following
must occur in order:

1. **Independent Bounded Canonical Amendment Review** of this decision and its
   exact Design Section 9 supplement;
2. **Independent amendment approval/confirmation**, recording that the
   exception is no broader than Sections 6–9;
3. **additive amendment binding/freeze or other repository-recognized
   supersession act** making the confirmed supplement authoritative without
   rewriting the historical frozen record; and
4. **BANPU-WP4 Work Package Plan amendment and independent reapproval**,
   updating Sections 3.2, 6, and 9 before implementation resumes on B1.

Allocation and Implementation Authorization synchronization is not required
because the capabilities, production/test surfaces, residual ownership, and
implementation boundary are unchanged. If independent amendment review finds
that any of those would change, it must reject this bounded candidate and
return to governance rather than infer wider authority.

## 11. B2–B6 preservation

This governance act resolves no implementation finding other than selecting
the amendment path for B1. The Independent Implementation Review
classifications remain exactly:

| Finding | State preserved |
|---|---|
| `WP4-IIR-B2` — caller-controlled symbols | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B3` — conflicting `MERGED_INTO` preparation | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B4` — transaction cleanup | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B5` — missing final basis assertion | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B6` — incomplete verification evidence | `BLOCKING — TEST/EVIDENCE CORRECTION UNDER EXISTING WP4 AUTHORITY` |

This record gives implementation no permission to treat those findings as
closed, waived, confirmed, or governed away.

## 12. Governance disposition and resulting state

**`WP4-IIR-B1 — BOUNDED CANONICAL AMENDMENT REQUIRED; ALTERNATIVE C SELECTED`**

The constitutional conflict is resolved at the decision level by selecting the
bounded retry preflight. The amendment is prepared but not independently
approved, confirmed, bound, or reflected in a reapproved Work Package Plan.
Implementation therefore may not yet rely on the E5/E6 retry exception.

BANPU-WP4 remains:

- allocated;
- implementation-authorized within its existing bounded surface;
- implementation candidate `NOT CONFIRMED`;
- blocked on the B1 successor governance chain and unresolved B2–B6;
- not frozen or closed; and
- without release, deployment, production execution, snapshot rebuild, WP5+,
  or M46 authority.

## 13. Exact next constitutional act

The exact next constitutional act is **Independent Bounded Canonical Amendment
Review** of this retry-order decision and its exact Design Section 9 supplement.
No implementation correction may rely on the retry exception before that
review and the remaining lifecycle acts in Section 10.3 complete.
