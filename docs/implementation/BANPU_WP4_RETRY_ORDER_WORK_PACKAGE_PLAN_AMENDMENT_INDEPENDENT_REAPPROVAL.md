# BANPU-WP4 — Retry-Order Work Package Plan Amendment Independent Reapproval

**Artifact class:** Additive independent constitutional Plan-amendment reapproval record
**Reapproval date:** 2026-08-13
**Independent reviewing authority:** Independent BANPU-WP4 Work Package Plan Amendment Reapproval Authority
**Candidate amendment:** [`BANPU_WP4_RETRY_ORDER_WORK_PACKAGE_PLAN_AMENDMENT.md`](BANPU_WP4_RETRY_ORDER_WORK_PACKAGE_PLAN_AMENDMENT.md)
**Candidate amendment identity:** raw SHA-256 `52254EB873CB57A5B3C30E62897878CAC20A23DCEDC2AAF2E5EB969D5C1C4168`; 18,701 bytes; 300 physical lines
**Original Work Package Plan:** [`BANPU_WP4_WORK_PACKAGE_PLAN.md`](BANPU_WP4_WORK_PACKAGE_PLAN.md)
**Original Plan identity:** raw SHA-256 `F76DCF7867AB4D0D11774BF4343D43076DFE22A7C5CA12656959CBC137F2DCBE`; 30,266 bytes; 475 physical lines
**Authoritative governance decision:** [`BANPU_WP4_RETRY_ORDER_GOVERNANCE_DECISION.md`](BANPU_WP4_RETRY_ORDER_GOVERNANCE_DECISION.md)
**Governance-decision identity:** raw SHA-256 `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB`; 20,350 bytes; 420 physical lines
**Binding/freeze record:** [`BANPU_WP4_RETRY_ORDER_AMENDMENT_BINDING_FREEZE_RECORD.md`](BANPU_WP4_RETRY_ORDER_AMENDMENT_BINDING_FREEZE_RECORD.md)
**Binding/freeze identity:** raw SHA-256 `5E312392767737C8F0445F51182B32A87B2EDF42B4C886BFB0296164EE389669`; 17,306 bytes; 348 physical lines
**Sections independently reapproved:** Original Plan §§3.2, 6, and 9 only
**Reapproval disposition:** `PLAN AMENDMENT INDEPENDENTLY REAPPROVED`
**Composite operational Plan:** `ORIGINAL PLAN + INDEPENDENTLY REAPPROVED ADDITIVE AMENDMENT`
**Implementation reliance on authoritative E8-R:** `PERMITTED UNDER EXISTING BOUNDED WP4 IMPLEMENTATION AUTHORIZATION`
**Implementation or test change performed:** `NO`
**Implementation correction, review, or confirmation performed:** `NO`
**WP4 freeze, closeout, release, deployment, or production authority:** `NONE`

---

## 1. Nature and independence of this act

Acting only as the independent Plan-amendment reapproval authority, this act
reviews the exact candidate identity above against the live original Plan, the
exact bound governance decision, and the binding/freeze record. The amendment
author's report and embedded verification table were not accepted as proof;
all identities and semantic comparisons were independently reproduced from
live repository bytes.

This act neither authors nor modifies the candidate. It performs no canonical
Design amendment, amendment binding, implementation or test correction,
renewed Independent Implementation Review, Implementation Confirmation, WP4
freeze or closeout, release, deployment, production conversion, snapshot
rebuild, WP5+ act, or M46 act.

## 2. Identity and authority continuity

The identity gate passed without mismatch:

| Artifact | Independently reproduced live identity | Determination |
|---|---|---|
| Original Work Package Plan | `F76DCF7867AB4D0D11774BF4343D43076DFE22A7C5CA12656959CBC137F2DCBE`; 30,266 bytes; 475 lines | `EXACT` |
| Authoritative governance decision | `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB`; 20,350 bytes; 420 lines | `EXACT` |
| Binding/freeze record | `5E312392767737C8F0445F51182B32A87B2EDF42B4C886BFB0296164EE389669`; 17,306 bytes; 348 lines | `EXACT` |
| Candidate Plan amendment | `52254EB873CB57A5B3C30E62897878CAC20A23DCEDC2AAF2E5EB969D5C1C4168`; 18,701 bytes; 300 lines | `EXACT AND REVIEWED` |
| Historical Design | raw `2D2ECE4391961C85DE4076091662C66DA4586C553C6CDD57094970168BF1CE76`; 28,653 bytes; 474 lines | `UNCHANGED` |
| Allocation Record | `CEE6F01C4113697BE6485AE56BB80FE0E9E99CB8555C08BC5D3E3CD67B94BAA9`; 11,180 bytes; 214 lines | `UNCHANGED` |
| Implementation Authorization Record | `D8E89048BDC3B939731523937C8122A25E9659EDD5CE5B28F48DEAD022A6BCFA`; 17,221 bytes; 321 lines | `UNCHANGED` |

The binding/freeze record has already made the exact Design Section 9
supplement authoritative. It expressly identifies synchronization and
independent reapproval of Work Package Plan §§3.2, 6, and 9 as the remaining
governance condition before implementation reliance on `E8-R`. The candidate
is the exact additive synchronization required by that condition.

## 3. Amendment-surface determination

The candidate makes operational changes only to:

1. Plan §3.2, by replacing the unqualified E1–E13 interpretation with the
   bounded common-boundary, `E8-R`, and invocation-class order;
2. Plan §6, by refining LM-14/LM-15 and adding RTO-1 through RTO-13 evidence;
   and
3. Plan §9, by making the new semantics, evidence, B1 correction, and B2–B6
   correction/review conditions mandatory for exit.

Its other sections record identity, convention, preservation, lifecycle, and
verification effects; they create no operational Plan semantic outside the
three authorized sections. Every Plan semantic outside §§3.2, 6, and 9 is
expressly preserved. Within those sections, every unaffected dependency,
capability, evidence row, prohibition, residual, and exit criterion is also
preserved.

The amendment is the minimum sufficient synchronization. It does not amend the
Roadmap, Mandatory Sequence, roadmap §1 confirmation, frozen Design bytes,
Allocation, Implementation Authorization, Decision Log, Implementation INDEX,
WP1/WP2/WP3 authority, WP5+, or M46.

## 4. Plan §3.2 semantic conformity

### 4.1 Complete common boundary

The candidate correctly requires every invocation to establish, before any
`E8-R` disposition:

1. a deterministic service-owned transaction lifecycle;
2. workspace and portfolio ownership;
3. the portfolio lock as primary serialization boundary;
4. canonical version-1 payload parsing and validation;
5. registry-resolved distinct predecessor and successor asset IDs;
6. locks on all relevant existing portfolio items;
7. complete E3 registry-state validation;
8. the canonical naive-midnight transition date;
9. E7 / `MINOR-1` safety;
10. the sole canonical incoming fingerprint; and
11. canonical conversion identity.

No retry classification, matching return, conflict disposition, or invalid-row
failure may bypass that boundary. `E8-R` is expressly downstream of E7 and
does not reopen, weaken, or substitute the admitted `MINOR-1` pre-use gate.

### 4.2 Canonical retry preflight

After the common boundary, the candidate requires a read-only lookup by exact
canonical conversion identity. For a present row it requires the stored
canonical `conversion_payload` itself to be reparsed and validated, followed
by regeneration of the row fingerprint using the sole canonical fingerprint
algorithm.

The candidate expressly forbids a detached or stored digest, caller-supplied
digest, partial comparison, alternate fingerprint, or WP4-local fingerprint
from establishing disposition. This is exact conformity to the authoritative
stored-payload rule.

## 5. Invocation-class determination

Each authoritative invocation class is fully and correctly represented:

| Class | Independent determination |
|---|---|
| No prior row | `CONFORMING` — not a retry; E5 and E6 remain mandatory; missing, ambiguous, stale-quantity, and stale-basis state fail closed; E3 and E6 precede every business write; E9 is first and precedes E10–E12; E13 final shares, basis, cash, and identity assertions precede the sole successful commit. |
| Matching retry | `CONFORMING` — exactly one valid row at the same identity; stored payload reparsed; fingerprint regenerated; exact equality required; only E5/E6 bypassed; no mutation, repair, reconciliation, replay, or snapshot action; deterministic transaction and lock cleanup; `already_applied`; current successor state excluded as predicate. |
| Conflicting retry | `CONFORMING` — exactly one valid row at the same identity; regenerated fingerprint differs; only E5/E6 bypassed; no mutation or repair; deterministic finish/rollback and lock release; controlled conflict hard-fail. |
| Invalid or ambiguous existing state | `CONFORMING` — malformed, inconsistent, ambiguous, noncanonical, zero-or-multiple, or otherwise invalid state establishes neither match nor valid conflict authority; it is no repair opportunity; no business mutation occurs; deterministic cleanup completes; execution fails closed. |

The one-valid-row prerequisite prevents invalid or ambiguous state from being
treated as a valid conflict merely because some value differs. Current
successor materialization cannot substitute for canonical historical identity
and payload proof.

## 6. Stored-payload fingerprint determination

The candidate faithfully binds this required sequence:

1. read the stored canonical `conversion_payload` from the existing row;
2. parse and fully validate that payload;
3. regenerate its fingerprint from that payload using the sole canonical
   algorithm; and
4. compare the regenerated fingerprint exactly with the incoming canonical
   fingerprint.

No candidate wording permits trust in a detached stored fingerprint, a
caller-supplied fingerprint, partial payload comparison, an alternate
fingerprint, or a WP4-local fingerprint. Matching and conflict authority arise
from the canonical stored payload itself and the sole canonical algorithm.

## 7. Plan §6 and RTO evidence determination

RTO-1 through RTO-13 are individually sufficient for their assigned proof and
collectively cover the authoritative retry semantics:

| Row | Determination |
|---|---|
| RTO-1 | Proves all common-boundary elements and E7 precede lookup/disposition. |
| RTO-2 | Proves no-prior-row E5/E6 execution before E9 or any write. |
| RTO-3 | Proves one-row exact-equality matching, E5/E6-only bypass, no mutation, `already_applied`, and successor-state exclusion. |
| RTO-4 | Proves one-row inequality conflict, E5/E6-only bypass, no mutation/repair, and controlled failure. |
| RTO-5 | Proves reparsing and full validation of stored canonical payload. |
| RTO-6 | Proves sole-algorithm payload-derived regeneration and rejects every detached or alternate source. |
| RTO-7 | Proves exact equality classification at the same canonical identity. |
| RTO-8 | Proves inequality yields conflict rather than new work, unrelated work, or repair. |
| RTO-9 | Proves malformed, inconsistent, ambiguous, noncanonical, zero-or-multiple, or otherwise invalid state fails closed without mutation. |
| RTO-10 | Proves matching exit leaks no transaction or lock. |
| RTO-11 | Proves conflict exit leaks no transaction or lock. |
| RTO-12 | Proves invalid-state exits leak no transaction or lock. |
| RTO-13 | Proves legitimate successor-state changes do not affect retry classification. |

The candidate additionally requires no repair, reconciliation, replay,
snapshot action, or other business mutation on matching, conflict, and invalid
exits. Existing LM, NMA, M1, EQ, regression, rollback-isolation, scope,
transaction-atomicity, and final-invariant requirements remain mandatory. No
existing evidence requirement is removed, replaced, weakened, waived,
deferred, or reclassified.

## 8. Plan §9 exit-criteria determination

The amended exit criteria prevent WP4 from successful exit unless:

1. the authoritative common-boundary and `E8-R` semantics are implemented;
2. no-prior-row applications retain E5/E6 before every business write;
3. matching and conflicting retries bypass only E5/E6 and otherwise conform;
4. stored-payload reparsing and sole-algorithm fingerprint regeneration are
   proven for equality, inequality, and invalid state;
5. deterministic transaction completion and lock release are proven;
6. successor materialized state is excluded as the retry predicate;
7. B1 is corrected in implementation and independently reviewed;
8. B2–B6 are corrected and independently reviewed without waiver or
   reclassification; and
9. every unaffected original §9 criterion and applicable §6 requirement remains
   satisfied.

No blocker or prior exit criterion is silently waived. A failed criterion
returns work to WP4, and no later package may compensate for it.

## 9. B2–B6 preservation

The candidate preserves the exact Independent Implementation Review states:

| Finding | State after this reapproval |
|---|---|
| `WP4-IIR-B2` | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B3` | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B4` | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B5` | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B6` | `BLOCKING — TEST/EVIDENCE CORRECTION UNDER EXISTING WP4 AUTHORITY` |

**B4 remains open.** The authoritative transaction-lifecycle rule and RTO-10
through RTO-12 define required behavior and proof; they do not establish that
the implementation has been corrected or reviewed.

**B6 remains open.** RTO-1 through RTO-13 define the evidence the corrected
candidate must supply; their definition does not make the incomplete test
implementation complete or accepted.

## 10. Authority and scope preservation

The amendment and this reapproval create no new production-file or test-file
authority, schema, index, migration, endpoint, CLI, frontend path,
`LedgerRepair` behavior, snapshot behavior, replay or repair framework,
general corporate-action framework, release/deployment/production authority,
WP5+ authority, or M46 authority.

Allocation and Implementation Authorization remain valid and require no
synchronization. They already bind the atomic conversion service, authorized
production/test surface, optimistic validation, canonical fingerprint
idempotency, matching no-op, conflicting failure, and transaction boundary.
The amendment changes only invocation ordering within that existing authority.

## 11. Independent reapproval and composite Plan state

The candidate satisfies every positive-reapproval condition: exact identity
continuity, exact semantic conformity, minimum surface, no unauthorized
widening, preserved first-application invariants, correct four-class retry
classification, mandatory stored-payload fingerprint regeneration, sufficient
evidence, sufficient exit criteria, preserved B2–B6 blockers, and preserved
authority boundaries.

The independently reapproved composite operational Plan is now:

```text
BANPU_WP4_WORK_PACKAGE_PLAN.md
F76DCF7867AB4D0D11774BF4343D43076DFE22A7C5CA12656959CBC137F2DCBE
+
BANPU_WP4_RETRY_ORDER_WORK_PACKAGE_PLAN_AMENDMENT.md
52254EB873CB57A5B3C30E62897878CAC20A23DCEDC2AAF2E5EB969D5C1C4168
```

For Plan §§3.2, 6, and 9, the independently reapproved additive amendment
controls where the historical original Plan is inconsistent. All other
original Plan semantics continue unchanged.

Plan governance for the retry-order exception is complete. Implementation may
now rely on the authoritative `E8-R` E5/E6 retry exception under the existing
bounded WP4 Implementation Authorization.

This reliance permission does **not** mean implementation is corrected, B1 is
resolved in code, B2–B6 are resolved, the implementation candidate is
independently accepted or confirmed, WP4 is frozen or closed, or release,
deployment, production execution, snapshot rebuild, WP5+, or M46 is
authorized.

## 12. Verification

Verification was independently performed before and after creation of this
additive reapproval record. This record is not part of either identity-bearing
component of the composite Plan.

| Verification | Result |
|---|---|
| Candidate amendment identity recomputed | `PASS` — `52254EB873CB57A5B3C30E62897878CAC20A23DCEDC2AAF2E5EB969D5C1C4168`; 18,701 bytes; 300 lines |
| Original Plan identity recomputed | `PASS` — `F76DCF7867AB4D0D11774BF4343D43076DFE22A7C5CA12656959CBC137F2DCBE`; 30,266 bytes; 475 lines |
| Governance-decision identity recomputed | `PASS` — `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB`; 20,350 bytes; 420 lines |
| Binding/freeze identity recomputed | `PASS` — `5E312392767737C8F0445F51182B32A87B2EDF42B4C886BFB0296164EE389669`; 17,306 bytes; 348 lines |
| Historical Design | `UNCHANGED` — raw `2D2ECE4391961C85DE4076091662C66DA4586C553C6CDD57094970168BF1CE76`; 28,653 bytes; 474 lines |
| Allocation and Authorization | `UNCHANGED`; identities in §2 reproduce |
| Implementation/test change attributable to this act | `NONE` |
| WP1/WP2/WP3 authority changed by this act | `NONE` |
| Decision Log or Implementation INDEX changed by this act | `NONE` — repository convention does not require synchronization at additive Plan reapproval |
| Stage, commit, push, merge, release, or deployment | `NONE` |

Relative links, Markdown anchors, trailing whitespace, Git diff checks, graph
synchronization, protected-artifact continuity, and final status are verified
as completion checks for this act.

## 13. Reapproval disposition

**BANPU-WP4 RETRY-ORDER WORK PACKAGE PLAN AMENDMENT INDEPENDENTLY REAPPROVED.**

**THE COMPOSITE OPERATIONAL PLAN IS THE ORIGINAL PLAN PLUS THE EXACT ADDITIVE
AMENDMENT IDENTIFIED IN §11.**

**IMPLEMENTATION MAY NOW RELY ON AUTHORITATIVE `E8-R` UNDER THE EXISTING
BOUNDED WP4 IMPLEMENTATION AUTHORIZATION.**

## 14. Exact next constitutional act

The exact next act is **BANPU-WP4 implementation correction under the existing
bounded Implementation Authorization**, limited to correcting B1 in conformity
with the now-operative `E8-R` Plan semantics and correcting the still-blocking
B2 through B6 findings within their existing authorized surfaces.

After correction and complete evidence, a renewed Independent Implementation
Review is required as a separate later act. This reapproval performs neither
implementation correction nor that review.
