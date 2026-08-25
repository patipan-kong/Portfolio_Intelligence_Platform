# BANPU-WP4 — Retry-Order Work Package Plan Amendment

**Artifact class:** Additive constitutional Work Package Plan amendment supplement
**Amendment date:** 2026-08-13
**Issuing authority:** BANPU-WP4 Work Package Plan Amendment Authority
**Original Work Package Plan:** [`BANPU_WP4_WORK_PACKAGE_PLAN.md`](BANPU_WP4_WORK_PACKAGE_PLAN.md)
**Original Plan identity:** raw SHA-256 `F76DCF7867AB4D0D11774BF4343D43076DFE22A7C5CA12656959CBC137F2DCBE`; 30,266 bytes; 475 physical lines
**Authoritative retry-order amendment:** [`BANPU_WP4_RETRY_ORDER_GOVERNANCE_DECISION.md`](BANPU_WP4_RETRY_ORDER_GOVERNANCE_DECISION.md)
**Authoritative amendment identity:** raw SHA-256 `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB`; 20,350 bytes; 420 physical lines
**Binding/freeze artifact:** [`BANPU_WP4_RETRY_ORDER_AMENDMENT_BINDING_FREEZE_RECORD.md`](BANPU_WP4_RETRY_ORDER_AMENDMENT_BINDING_FREEZE_RECORD.md)
**Binding/freeze identity:** raw SHA-256 `5E312392767737C8F0445F51182B32A87B2EDF42B4C886BFB0296164EE389669`; 17,306 bytes; 348 physical lines
**Sections amended:** Work Package Plan §§3.2, 6, and 9 only
**Disposition:** `PLAN AMENDMENT PREPARED — NOT YET INDEPENDENTLY REAPPROVED`
**Implementation reliance:** `PROHIBITED — IMPLEMENTATION MUST NOT YET RELY ON THE RETRY EXCEPTION`
**Implementation or test change performed:** `NO`
**Independent reapproval performed by this act:** `NO`

---

## 1. Nature and authority of this act

This record prepares the minimum bounded amendment required to synchronize the
BANPU-WP4 Work Package Plan with the already bound, frozen, and authoritative
Design Section 9 retry-order supplement. It amends only the operational
semantics of Plan §§3.2, 6, and 9. It performs no implementation, test repair,
independent review, independent reapproval, implementation review,
implementation confirmation, WP4 freeze or closeout, release, deployment, or
production act.

The authoritative semantic source is the exact governance-decision identity
recorded above, as bound by the exact binding/freeze identity recorded above.
This Plan amendment may operationalize that source but may not reinterpret,
widen, or replace it.

## 2. Repository amendment convention

Repository governance permits additive amendment and supersession of an
identity-bearing historical artifact:

1. the BANPU-WP3 planning lifecycle preserves predecessor identities while
   using additive amendment, confirmation, freeze, and reapproval records;
2. the authoritative WP4 binding/freeze record itself applies the same
   preservation rule to the historical Design and leaves Plan amendment and
   independent reapproval as separate successor acts; and
3. the independent retry-order review states that historical text remains
   evidence unless an independently reviewed and confirmed additive supplement
   is bound or recognized as successor.

The original WP4 Plan is already relied upon throughout the WP4 lifecycle and
is therefore preserved at the identity above. Direct byte rewriting is neither
necessary nor constitutionally preferable for this bounded synchronization.
This additive record is the sole Plan-amendment artifact created by this act.
It becomes operative only after separate independent Plan amendment
reapproval. Until then, the original Plan remains historical operational
evidence, the authoritative Design supplement governs the canonical target,
and implementation reliance on the retry exception remains prohibited.

## 3. Amendment to Plan §3.2 — runtime order

This section supplements and, only where inconsistent, supersedes the original
Plan §3.2 statement that E1 through E13 form one unqualified linear order. E0,
E1 through E4, E9 through E13, all unaffected dependencies, the first-
application write order, and the sole successful commit boundary remain
preserved. Original step E8 is refined as `E8-R`, a bounded retry-disposition
point.

### 3.1 Common boundary before `E8-R`

Every invocation must establish all of the following before any retry
classification, matching return, conflict failure, or invalid-row failure at
`E8-R`:

1. a service-owned deterministic transaction lifecycle;
2. workspace and portfolio ownership;
3. the portfolio lock as the primary serialization boundary;
4. canonical version-1 payload parsing and validation;
5. registry-resolved, distinct predecessor and successor asset IDs;
6. locks on all relevant existing portfolio items;
7. complete E3 registry-state validation;
8. the canonical naive-midnight transition date;
9. E7 / `MINOR-1` safety;
10. the sole canonical incoming fingerprint; and
11. canonical conversion identity.

No retry classification or conflict disposition may bypass this common
boundary. `E8-R` is downstream of E7 / `MINOR-1`; it does not weaken, move, or
substitute the canonical pre-use gate.

### 3.2 `E8-R` — canonical retry preflight

After the common boundary, the service performs a read-only lookup by exact
canonical conversion identity. If a row is present, the service must validate
the row from its stored canonical `conversion_payload`, reparse that payload,
and regenerate its fingerprint from that payload with the sole canonical
fingerprint algorithm.

No detached or stored digest, caller-supplied digest, partial comparison,
alternate fingerprint, or WP4-local fingerprint may establish a retry
disposition. The incoming fingerprint and the stored-payload-regenerated
fingerprint are products of the same sole canonical algorithm.

### 3.3 Invocation-class disposition

| Invocation class | Required runtime order and result |
|---|---|
| **No prior canonical conversion row** | This is not a retry. E5 predecessor lookup and E6 optimistic quantity/basis validation are mandatory. Missing, ambiguous, stale-quantity, or stale-basis predecessor state fails closed. E3 and E6 precede every first-application write. E9 remains the first conversion business write, E9 precedes E10–E12, and E13 final shares, basis, cash, and identity assertions precede the sole successful commit. |
| **Exactly one valid matching row** | Exact equality between the fingerprint regenerated from the stored canonical payload and the incoming canonical fingerprint proves a matching retry. Bypass only E5/E6. Perform no business mutation, repair, reconciliation, replay, or snapshot action. Deterministically finish the transaction and release all locks, then return `already_applied`. |
| **Exactly one valid conflicting row** | Inequality between the fingerprint regenerated from the stored canonical payload and the incoming canonical fingerprint proves a conflict. Bypass only E5/E6. Perform no business mutation or repair. Deterministically finish or roll back the transaction as appropriate, release all locks, and hard-fail with the controlled conflict disposition. |
| **Invalid or ambiguous existing state** | A malformed, inconsistent, ambiguous, noncanonical, or otherwise invalid row or stored payload establishes neither matching nor conflict authority. It is not a repair opportunity. Fail closed, perform no business mutation, and deterministically finish cleanup. |

Current successor materialized shares, basis, cash, identity, or other current
state is not an idempotency predicate. Later legitimate successor activity
cannot change the historical retry fact established by one valid canonical
conversion row.

### 3.4 Preserved ordering rules

The original §3.2 ordering rules are read as follows after reapproval:

1. E7 precedes `E8-R` on every invocation.
2. E5 and E6 remain mandatory for every no-prior-row first application.
3. E5 and E6 may be bypassed only after one valid prior canonical conversion
   row, validated from its stored canonical payload, establishes a matching or
   conflicting retry classification.
4. E3 precedes every first-application write, and E6 precedes every first-
   application write.
5. E9 remains the first conversion business write and precedes E10–E12.
6. A first application retains one service-owned transaction across its locks,
   E5/E6, E9–E13, final assertions, and sole successful commit.
7. E13 remains the only successful commit boundary. Every return or failure
   after a query or lock begins deterministically finishes the transaction and
   releases locks without cleanup-time business mutation.

## 4. Amendment to Plan §6 — mandatory verification and evidence

All existing LM, NMA, M1, EQ, regression, rollback-isolation, and scope
requirements remain mandatory and may not be weakened, waived, substituted, or
reclassified by this amendment. LM-14 and LM-15 are refined by the
authoritative semantics below, and the following evidence is additionally
required. These are Plan requirements, not claims that the current tests
satisfy them.

| ID | Mandatory evidence | Required observation |
|---|---|---|
| RTO-1 | Common-boundary ordering | Retry identity lookup and disposition cannot occur before E7 / `MINOR-1`, and every common-boundary element in §3.1 is established first. |
| RTO-2 | No-prior-row path | E5 predecessor lookup and E6 optimistic quantity/basis validation both execute before E9 or any other first-application business write. |
| RTO-3 | Matching retry branch | Exactly one valid row with equal regenerated fingerprint bypasses only E5/E6, performs no mutation, returns `already_applied`, and does not use current successor materialized state as a predicate. |
| RTO-4 | Conflicting retry branch | Exactly one valid row with unequal regenerated fingerprint bypasses only E5/E6, performs no mutation or repair, and raises the controlled conflict disposition. |
| RTO-5 | Stored-payload parsing | The existing row's stored canonical `conversion_payload` is reparsed and fully validated before it can establish retry disposition. |
| RTO-6 | Fingerprint regeneration | The existing-row fingerprint is regenerated from the stored canonical payload with the sole canonical algorithm; detached, caller-provided, partial, alternate, and WP4-local fingerprints cannot establish disposition. |
| RTO-7 | Equality classification | Exact equality of the incoming canonical fingerprint and valid stored-payload-regenerated fingerprint is necessary and sufficient for the matching classification at the same canonical identity. |
| RTO-8 | Inequality classification | Inequality of those fingerprints at the same canonical identity yields controlled conflict, not a new application, unrelated conversion, or repair. |
| RTO-9 | Invalid-row fail-closed behavior | Malformed, inconsistent, ambiguous, noncanonical, zero-or-multiple, or otherwise invalid existing state establishes neither match nor conflict authority, performs no mutation, and fails closed. |
| RTO-10 | Matching cleanup | Matching-return evidence proves no open transaction and no retained portfolio or item lock. |
| RTO-11 | Conflict cleanup | Controlled-conflict evidence proves no open transaction and no retained portfolio or item lock. |
| RTO-12 | Invalid-state cleanup | Every invalid-existing-state exit proves no open transaction and no retained portfolio or item lock. |
| RTO-13 | Predicate exclusion | Perturbation by legitimate later successor activity proves current successor shares, basis, cash, identity, or other current materialized state is not used to decide idempotency. |

The eventual evidence must also prove that matching, conflict, and invalid-row
cleanup performs no repair, reconciliation, replay, snapshot action, or other
business mutation. Existing transaction-atomicity and final-invariant evidence
continues to apply to the no-prior-row path.

This amendment does not repair or accept the incomplete `WP4-IIR-B6` test
implementation. It specifies the evidence the corrected candidate must later
provide under existing WP4 test authority.

## 5. Amendment to Plan §9 — acceptance and exit criteria

All unaffected original §9 criteria remain mandatory. The original references
to the unqualified E7-before-E8 order, LM-14/LM-15, and the full §6 matrix are
construed after reapproval to include §§3 and 4 of this amendment. WP4 cannot
enter a successful exit, confirmation, freeze, or closeout state unless all of
the following additional conditions hold:

1. the authoritative `E8-R` common-boundary and invocation-class semantics are
   implemented exactly;
2. the no-prior-row path executes mandatory E5/E6 before any first-application
   business write;
3. matching and conflicting retries bypass only E5/E6 and otherwise conform to
   §3.3 without business mutation or repair;
4. existing-row canonical payload reparsing and sole-algorithm fingerprint
   regeneration are proven, including equality, inequality, and invalid-state
   dispositions;
5. deterministic transaction completion and lock release are proven for
   matching, conflicting, and invalid-row exits;
6. current successor materialized state is proven not to be the retry
   predicate;
7. `WP4-IIR-B1` is corrected in implementation and independently reviewed;
8. `WP4-IIR-B2` through `WP4-IIR-B6` are corrected and independently reviewed
   as required, with no finding waived, reclassified, or treated as resolved by
   this Plan amendment; and
9. every original §9 criterion and every applicable original §6 LM, NMA, M1,
   EQ, regression, isolation, and scope requirement remains satisfied.

A failed criterion returns work to WP4. No later package may compensate for
it. This amendment grants no implementation confirmation, freeze, closeout,
release, deployment, or production execution authority.

## 6. Blocking findings preserved

This act does not resolve, waive, implement, reclassify, review, or confirm any
remaining Independent Implementation Review finding:

| Finding | Preserved state |
|---|---|
| `WP4-IIR-B2` | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B3` | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B4` | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B5` | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B6` | `BLOCKING — TEST/EVIDENCE CORRECTION UNDER EXISTING WP4 AUTHORITY` |

The Section 4 evidence requirements describe the future proof required for
correction; they do not establish that any correction exists.

## 7. Preservation and excluded effects

Every Plan semantic outside §§3.2, 6, and 9 is preserved. Within those sections,
every semantic not expressly supplemented or superseded here is preserved.
In particular, this amendment does not change:

- E0 registry preparation or the first-application E9–E13 write order;
- the authorized capability or file surface;
- `MINOR-1`, `NEW-MINOR-A`, LM, NMA, M1, EQ, regression, transaction-isolation,
  or final-invariant obligations except to add the retry evidence above;
- WP1, WP2, or WP3 authority or continuity;
- the Roadmap, Mandatory Sequence, roadmap §1 confirmation, historical Design,
  Allocation, Implementation Authorization, Decision Log, Implementation
  INDEX, WP5+, or M46; or
- any carried residual or prohibition.

This amendment creates no production file, new test-file authority, schema,
index, migration, endpoint, CLI, frontend path, `LedgerRepair` behavior,
snapshot behavior, replay or repair framework, general corporate-action
framework, release/deployment/production authority, WP5+ authority, or M46
authority.

The existing [`BANPU_WP4_ALLOCATION_RECORD.md`](BANPU_WP4_ALLOCATION_RECORD.md)
and
[`BANPU_WP4_IMPLEMENTATION_AUTHORIZATION_RECORD.md`](BANPU_WP4_IMPLEMENTATION_AUTHORIZATION_RECORD.md)
remain valid and unchanged. The amendment changes runtime sequencing only and
therefore requires no Allocation or Authorization synchronization.

## 8. Reliance boundary and lifecycle state

This amendment is authored but has not been independently reapproved. Its
current lifecycle state is therefore:

```text
DESIGN SECTION 9 SUPPLEMENT BOUND / FROZEN / AUTHORITATIVE
PLAN AMENDMENT PREPARED — NOT YET INDEPENDENTLY REAPPROVED
IMPLEMENTATION MAY NOT YET RELY ON THE RETRY EXCEPTION
```

The author of this record cannot supply its independent reapproval. Until that
separate act completes, no implementer or implementation reviewer may treat
the E5/E6 retry bypass as operational Plan authority.

## 9. Verification performed

All identities below were recomputed from live repository bytes before this
artifact was created.

| Verification | Result |
|---|---|
| Original Work Package Plan identity | `PASS` — `F76DCF7867AB4D0D11774BF4343D43076DFE22A7C5CA12656959CBC137F2DCBE`; 30,266 bytes; 475 physical lines |
| Authoritative amendment identity | `PASS` — `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB`; 20,350 bytes; 420 physical lines |
| Binding/freeze identity | `PASS` — `5E312392767737C8F0445F51182B32A87B2EDF42B4C886BFB0296164EE389669`; 17,306 bytes; 348 physical lines |
| Historical Design preserved | `PASS` — raw SHA-256 `2D2ECE4391961C85DE4076091662C66DA4586C553C6CDD57094970168BF1CE76`; 28,653 bytes; 474 physical lines |
| Allocation continuity | `PASS` — unchanged raw SHA-256 `CEE6F01C4113697BE6485AE56BB80FE0E9E99CB8555C08BC5D3E3CD67B94BAA9` |
| Implementation Authorization continuity | `PASS` — unchanged raw SHA-256 `D8E89048BDC3B939731523937C8122A25E9659EDD5CE5B28F48DEAD022A6BCFA` |
| Implementation or test change attributable to this act | `NONE` |
| WP1/WP2/WP3 authority changed by this act | `NONE` |
| Decision Log or Implementation INDEX changed by this act | `NONE` — repository convention does not require either during amendment authorship |
| Staging, commit, push, release, or deployment | `NONE` |

Relative links, Markdown anchors, trailing whitespace, Git diff checks,
graph synchronization, protected-artifact continuity, and final working-tree
status are verified as part of this act's completion and reported by the
issuing authority. This artifact does not convert those checks into independent
reapproval.

## 10. Plan-amendment disposition

**BANPU-WP4 RETRY-ORDER WORK PACKAGE PLAN AMENDMENT PREPARED — NOT YET
INDEPENDENTLY REAPPROVED.**

**IMPLEMENTATION MAY NOT YET RELY ON THE RETRY EXCEPTION.**

## 11. Exact next constitutional act

The exact next constitutional act is **Independent BANPU-WP4 Work Package Plan
Amendment Reapproval**, limited to this additive amendment's synchronization of
original Plan §§3.2, 6, and 9 with the authoritative Design Section 9
supplement.

That reviewer must independently verify the original Plan identity, the
authoritative amendment and binding identities, exact semantic conformity,
scope preservation, B2–B6 preservation, and the continuing implementation-
reliance prohibition. This act performs no part of that independent reapproval.
