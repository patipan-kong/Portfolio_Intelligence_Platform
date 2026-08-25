# BANPU-WP4 — Retry-Order Bounded Canonical Amendment Confirmation

**Artifact class:** Additive Independent Amendment Confirmation Record
**Confirmation date:** 2026-08-13
**Confirmation authority:** Independent Amendment Confirmation Authority
**Candidate confirmed:** [`BANPU_WP4_RETRY_ORDER_GOVERNANCE_DECISION.md`](BANPU_WP4_RETRY_ORDER_GOVERNANCE_DECISION.md)
**Candidate identity:** raw SHA-256 `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB`; 20,350 bytes; 420 physical lines
**Independent review examined:** [`BANPU_WP4_RETRY_ORDER_AMENDMENT_INDEPENDENT_REVIEW.md`](BANPU_WP4_RETRY_ORDER_AMENDMENT_INDEPENDENT_REVIEW.md)
**Independent-review identity:** raw SHA-256 `54C3CAC4DD263CEABA1ED70211529C56839A3C27D4A054A964DD3C68135463B4`; 22,686 bytes; 417 physical lines
**Confirmation determination:** `AMENDMENT CONFIRMED`
**Binding, freeze, or supersession performed:** `NO`
**Implementation reliance created by this act:** `NONE`
**Implementation or test change performed:** `NO`
**Work Package Plan amendment or reapproval performed:** `NO`
**Release, deployment, production execution, or production-data authority:** `NONE`
**BANPU-WP5+ authority:** `NONE`
**M46 authority:** `NONE`

---

## 1. Nature and boundary of this confirmation

This is a confirmation act only. It independently confirms the unchanged,
independently reviewed retry-order amendment candidate identified above. It
does not act as the original governance decision, independent bounded amendment
review, binding/freeze/supersession act, Work Package Plan amendment or
approval, implementation correction, implementation review, implementation
confirmation, closeout, release, deployment, or production-execution act.

This record is additive. It changes no implementation file, test file, frozen
canonical artifact, Decision Log, or Implementation INDEX. A positive
confirmation does not make the amendment implementation-reliable. The
confirmed semantics remain unavailable to implementation until the successor
binding and Work Package Plan governance acts complete.

## 2. Identity continuity

The candidate was independently read from the repository before confirmation
and reproduced exactly as:

| Identity property | Confirmed value |
|---|---|
| Raw SHA-256 | `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB` |
| Raw byte length | `20,350` |
| Physical lines | `420` |

These values exactly match the candidate identity recorded by the independent
review. The review itself reproduces as raw SHA-256
`54C3CAC4DD263CEABA1ED70211529C56839A3C27D4A054A964DD3C68135463B4`,
22,686 bytes, and 417 physical lines, and expressly identifies the exact
candidate SHA-256, byte length, and physical-line count above.

The candidate identity was rechecked after creating this record and remained
unchanged. No different candidate is confirmed.

Repository status and entry-hash comparison establish that no implementation
or test change occurred between the independent review and this confirmation
act. No tracked frozen BANPU authority changed in this act. All pre-existing
working-tree changes remain outside and unabsorbed by this confirmation.

## 3. Independent-review sufficiency

The independent review's approval label was not treated as proof. Its reasoning
was inspected and independently found sufficient because it establishes all of
the following:

1. Design Section 9 and Work Package Plan Sections 3.2 and 9 require E5/E6
   before E8 without a retry exception.
2. E10 can consume the predecessor materialization that E5/E6 require, while
   LM-14 requires a later exact retry to return `already_applied` without
   repeated mutation.
3. No frozen sentence makes E5/E6 optional for retries or establishes retry
   disposition as a preflight; therefore no valid no-amendment interpretation
   exists.
4. An amendment is constitutionally necessary, and Alternative C is the
   minimum sufficient solution because it introduces one bounded read-only
   disposition point and bypasses only E5/E6 after a valid prior row is proven.
5. The common validation boundary is sufficient and retains identity, payload,
   registry, date, locking, MINOR-1, and transaction-lifecycle protections.
6. Every no-prior-row application still performs E5/E6 before any
   first-application write, retains E9 before E10–E12, and retains E13 before
   the sole successful commit.
7. Matching and conflicting retries bypass only E5/E6, perform no mutation,
   and deterministically finish transaction cleanup.
8. Existing-row validity and fingerprint equality must be established by
   parsing the stored payload and regenerating the sole canonical fingerprint.
9. MINOR-1 remains upstream of retry disposition, and no second fingerprint is
   introduced.
10. The amendment changes only runtime sequencing within the already-authorized
    capability and file surface.
11. The normative amendment surface is exactly two artifacts and the stated
    sections within them.
12. Allocation and Implementation Authorization remain valid without
    synchronization, while `WP4-IIR-B2` through `WP4-IIR-B6` remain blocking
    exactly as previously classified.

The review therefore supplies substantive support for confirmation rather than
merely a disposition or set of headings.

## 4. B1 conflict, constitutional necessity, and selected alternative

`WP4-IIR-B1` is genuine. The unqualified original order requires current
predecessor lookup and optimistic validation before duplicate disposition, but
a successful first application can remove or transform that current state
before the required matching retry. Treating historical transaction facts as a
current holding, reconstructing the predecessor, or silently reading a retry
exception into the frozen text would violate the existing boundaries.

No valid no-amendment interpretation exists. A bounded canonical amendment is
constitutionally necessary.

Alternative C is confirmed as the minimum sufficient solution. Alternative A
makes the matching-retry requirement unreachable without fabrication or
reconstruction. Alternative B moves duplicate handling too broadly and risks
weakening new-work optimistic validation. Alternative D changes a no-op retry
into replay, repair, or reconstruction. Alternative C alone introduces the
strict existing-row predicate after the common boundary, preserves E5/E6 for
all new applications, and bypasses only E5/E6 for proven retries.

## 5. Exact confirmed common boundary

Every invocation must establish all of the following before `E8-R`:

1. a service-owned transaction lifecycle;
2. workspace/portfolio ownership;
3. the portfolio lock;
4. canonical version-1 payload parsing and validation;
5. registry-resolved, distinct predecessor and successor asset IDs;
6. relevant-item locks;
7. complete registry-state validation;
8. the canonical naive-midnight transition date;
9. E7 / MINOR-1 safety;
10. the sole canonical incoming fingerprint; and
11. the canonical conversion identity.

No matching, conflict, or invalid-row disposition may bypass this boundary.
Caller-supplied identity cannot replace registry resolution.

## 6. Mandatory existing-row fingerprint recomputation

This confirmation fixes the only authorized interpretation of existing-row
fingerprint comparison:

1. parse and validate the existing row's stored canonical
   `conversion_payload`;
2. regenerate its fingerprint from that canonical payload using the sole
   canonical fingerprint algorithm;
3. require the regenerated fingerprint to represent that canonical payload
   exactly;
4. compare the regenerated fingerprint exactly with the incoming canonical
   fingerprint; and
5. fail closed if the existing row, its identity projections, or its stored
   payload is malformed, ambiguous, invalid, or internally inconsistent.

No caller-supplied digest, detached stored digest, partial payload comparison,
alternate fingerprint, or WP4-local fingerprint is authorized. The current
schema stores `conversion_payload` and not a detached fingerprint column;
recomputation applies the already-authorized payload parser and sole canonical
algorithm. It is an existing-row validation rule within `E8-R`, not a new
capability, schema, index, or file surface.

## 7. No-prior-row application

When `E8-R` finds no prior canonical conversion row:

- the invocation is not a retry;
- E5 predecessor lookup is mandatory;
- E6 quantity and basis verification is mandatory;
- missing, ambiguous, stale-quantity, or stale-basis predecessor state fails
  closed;
- E3 and E6 precede every first-application write;
- E9 remains the first conversion business write and precedes E10–E12; and
- E13 final shares, basis, cash, and identity assertions precede the sole
  successful commit.

The amendment creates no E5/E6 bypass for new or stale nonduplicate work.

## 8. Matching retry

When exactly one valid existing canonical conversion is found at the same
canonical identity and its recomputed stored-payload fingerprint exactly equals
the incoming fingerprint:

- bypass only E5/E6;
- perform no insert, update, delete, cash, holding, registry, repair,
  reconciliation, replay, or snapshot mutation;
- deterministically finish the service-owned read-only transaction and release
  every retained lock; and
- return `already_applied` identifying the existing transaction.

Current successor materialized shares, basis, cash, or other state is not an
idempotency predicate. Later legitimate activity may change current state
without changing whether this historical conversion was already applied.
Successor-state comparison or repair would improperly turn retry disposition
into reconciliation or repair.

## 9. Conflicting retry

When exactly one valid existing canonical conversion is found at the same
canonical identity but its recomputed stored-payload fingerprint differs from
the incoming canonical fingerprint:

- bypass only E5/E6;
- perform no insert, update, delete, business mutation, repair, or
  reconciliation;
- deterministically roll back or otherwise finish the transaction and release
  locks; and
- hard-fail with the controlled conflict disposition.

Fingerprint inequality covers every canonical payload semantic, including a
different successor identity. The existing conversion identity and unique
constraint make that difference a conflict, not an unrelated conversion.

## 10. Invalid or ambiguous existing row

An existing row or stored payload that is malformed, internally inconsistent,
ambiguous, noncanonical, or otherwise fails the unchanged canonical row
invariants is neither a match nor a repair opportunity. Zero or more than one
row is not a single valid match. The invocation fails closed, performs no
business mutation, and deterministically finishes cleanup.

## 11. Transaction-lifecycle semantics

Pure parsing may occur before database access. Once a query or lock begins,
every exit remains inside the service-owned cleanup boundary. Matching no-op,
conflict, invalid-row, payload, identity, registry, and date exits must finish
or roll back the transaction as appropriate and release locks before returning
or raising. Cleanup performs no business mutation.

A no-prior-row application retains one transaction across its locks, E5/E6,
E9–E13, final assertions, and sole successful commit. No caller-visible path
may retain an open transaction.

These semantics provide governance precision relevant to correcting
`WP4-IIR-B4`; they do not implement, close, waive, or reclassify B4.

## 12. MINOR-1 continuity

`E8-R` remains downstream of E7 for every invocation. The incoming fingerprint
and the fingerprint regenerated from the stored payload use the same sole
canonical algorithm; regeneration does not create a second fingerprint.
MINOR-1's admitted pre-use correction, scope, and independent disposition are
preserved and are neither reopened nor widened by this confirmation.

## 13. Exact normative amendment surface

The confirmed normative amendment surface is exactly:

1. [`BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md),
   Section 9 only; and
2. [`BANPU_WP4_WORK_PACKAGE_PLAN.md`](BANPU_WP4_WORK_PACKAGE_PLAN.md),
   Sections 3.2, 6, and 9 only.

This confirmation authorizes no amendment to the Roadmap, Mandatory Sequence,
Allocation, Implementation Authorization, roadmap Section 1 confirmation,
WP1/WP2/WP3 authority, Decision Log, Implementation INDEX, WP5+, or M46. It
does not rewrite either artifact in the confirmed surface; the successor acts
must apply and govern the exact bounded supplement.

## 14. Scope and authority preservation

The amendment changes runtime sequencing only. It creates no new production or
test file, schema, index, migration, endpoint, CLI, frontend path, replay or
repair behavior, snapshot behavior, general corporate-action framework,
release/deployment/production authority, WP5+ authority, or M46 authority.

[`BANPU_WP4_ALLOCATION_RECORD.md`](BANPU_WP4_ALLOCATION_RECORD.md) and
[`BANPU_WP4_IMPLEMENTATION_AUTHORIZATION_RECORD.md`](BANPU_WP4_IMPLEMENTATION_AUTHORIZATION_RECORD.md)
already cover the atomic conversion service, existing production/test surface,
locking, optimistic validation, canonical-fingerprint idempotency, append-only
insertion, materialization, and final assertions. Because the confirmed
amendment changes neither capability nor file surface, both records remain
valid and require no synchronization.

## 15. B2–B6 preservation

This confirmation does not resolve, waive, or reclassify any remaining
Independent Implementation Review finding:

| Finding | State preserved |
|---|---|
| `WP4-IIR-B2` — caller-controlled symbols | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B3` — conflicting `MERGED_INTO` preparation | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B4` — transaction cleanup | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B5` — missing final basis assertion | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B6` — incomplete verification evidence | `BLOCKING — TEST/EVIDENCE CORRECTION UNDER EXISTING WP4 AUTHORITY` |

The transaction-lifecycle clarification is relevant to B4's eventual
correction but does not perform or accept that correction.

## 16. Confirmation disposition and lifecycle state

The exact unchanged candidate has passed independent substantive review and
this separate identity-continuous confirmation. The confirmation disposition
is:

```text
AMENDMENT CONFIRMED
NOT YET BOUND, FROZEN, OR SUPERSEDING
NOT YET IMPLEMENTATION-RELIABLE
```

The resulting amendment lifecycle state is **independently reviewed and
confirmed; awaiting additive binding/freeze or repository-recognized
supersession**. The historical frozen Design remains unchanged and controlling
until that successor act makes the confirmed supplement authoritative.

BANPU-WP4 remains allocated and implementation-authorized only within its
existing bounded surface. Its implementation candidate remains not confirmed,
B1 remains uncorrected in implementation, B2–B6 remain blocking, WP4 is not
frozen or closed, and no release, deployment, production execution, snapshot
rebuild, WP5+, or M46 authority exists.

## 17. Required successor sequence

The remaining constitutional sequence is:

1. additive amendment binding/freeze or other repository-recognized
   supersession of the confirmed Design Section 9 supplement, preserving the
   historical frozen record;
2. WP4 Work Package Plan amendment and independent reapproval for Sections
   3.2, 6, and 9;
3. implementation corrections for B1 and still-open B2–B6;
4. renewed Independent Implementation Review; and
5. later, separate Implementation Confirmation.

No step above is performed by this record.

## 18. Exact next constitutional act

The exact next constitutional act is **additive amendment binding/freeze or
other repository-recognized supersession** of the confirmed retry-order Design
Section 9 supplement at candidate identity
`C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB`.

That act must preserve the mandatory recomputation-from-stored-payload rule and
the exact bounded semantics confirmed here. It must not infer a wider
capability, file, package, release, deployment, WP5+, or M46 authority.

## 19. Repository verification

Verification was performed after creation of this additive record. This record
is not a member of any frozen implementation corpus and does not change the
candidate or independent-review identity.

| Verification | Result |
|---|---|
| Candidate identity after record creation | `PASS` — raw SHA-256 `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB`; 20,350 bytes; 420 physical lines |
| Independent-review identity | `PASS` — raw SHA-256 `54C3CAC4DD263CEABA1ED70211529C56839A3C27D4A054A964DD3C68135463B4`; 22,686 bytes; 417 physical lines |
| Implementation/test entry-state continuity | `PASS` — all six pre-existing WP4 candidate entry hashes remain unchanged from the independent review |
| Frozen BANPU canonical artifact changed by this act | `NONE` |
| Decision Log or Implementation INDEX changed by this act | `NONE` |
| WP1/WP2/WP3 continuity | `PASS` — prior independently reproduced continuity identities and authorized pre-existing deltas remain unchanged by this act |
| Relative-link targets | `PASS` |
| Markdown fragment links | `NOT APPLICABLE` — no fragment links used |
| Trailing whitespace | `PASS` |
| `git diff --check` | `PASS` |
| `git diff --cached --check` | `PASS` |
| `graphify update .` | `PASS` |
| Staging, commit, or push | `NONE` |

Only this confirmation record is attributable to this act. All other working
tree entries pre-date it and remain preserved without absorption.
