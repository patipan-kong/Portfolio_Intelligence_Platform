# BANPU-WP4 — Retry-Order Amendment Binding and Freeze Record

**Artifact class:** Additive constitutional amendment binding/freeze and supersession record
**Binding/freeze date:** 2026-08-13
**Issuing authority:** BANPU Canonical Amendment Binding/Freeze Authority
**Confirmed amendment candidate:** [`BANPU_WP4_RETRY_ORDER_GOVERNANCE_DECISION.md`](BANPU_WP4_RETRY_ORDER_GOVERNANCE_DECISION.md)
**Candidate identity:** raw SHA-256 `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB`; 20,350 bytes; 420 physical lines
**Independent review:** [`BANPU_WP4_RETRY_ORDER_AMENDMENT_INDEPENDENT_REVIEW.md`](BANPU_WP4_RETRY_ORDER_AMENDMENT_INDEPENDENT_REVIEW.md)
**Independent-review identity:** raw SHA-256 `54C3CAC4DD263CEABA1ED70211529C56839A3C27D4A054A964DD3C68135463B4`; 22,686 bytes; 417 physical lines
**Independent confirmation:** [`BANPU_WP4_RETRY_ORDER_AMENDMENT_CONFIRMATION.md`](BANPU_WP4_RETRY_ORDER_AMENDMENT_CONFIRMATION.md)
**Amendment-confirmation identity:** raw SHA-256 `41E1A23C5C09D095686E5675A37CF5DC191802060DC9BB104A99D2EEC2574BC8`; 17,832 bytes; 363 physical lines
**Binding/freeze disposition:** `AMENDMENT BOUND / FROZEN / AUTHORITATIVE`
**Work Package Plan state:** `NOT YET AMENDED OR REAPPROVED`
**Implementation reliance:** `PROHIBITED UNTIL WORK PACKAGE PLAN GOVERNANCE COMPLETES`
**Implementation or test change performed:** `NO`
**BANPU-WP4 implementation freeze or closeout performed:** `NO`
**Release, deployment, production execution, or production-data authority:** `NONE`
**BANPU-WP5+ authority:** `NONE`
**M46 authority:** `NONE`

---

## 1. Constitutional authority and repository convention

Acting only as the competent BANPU Canonical Amendment Binding/Freeze
Authority, this act binds and freezes the exact confirmed retry-order amendment
identified above. It performs no amendment authorship, independent review,
confirmation, Work Package Plan amendment or reapproval, implementation,
implementation review, implementation confirmation, WP4 freeze or closeout,
release, deployment, or production act.

Repository convention permits this additive mechanism. The controlling BANPU
precedent is the
[`BANPU_WP3_AMENDED_PLANNING_FREEZE_RECORD.md`](BANPU_WP3_AMENDED_PLANNING_FREEZE_RECORD.md),
which uses an additive constitutional freeze record to:

1. bind an exact independently reviewed and confirmed amendment identity;
2. make the amended rule authoritative as the current target;
3. preserve the earlier frozen record and content as historical evidence; and
4. leave successor allocation, authorization, plan, implementation, and review
   acts separate unless their synchronization is constitutionally required.

That convention fits this bounded amendment without rewriting the historical
frozen Design. This record therefore binds the confirmed decision as an
additive Design Section 9 supplement and freezes its exact candidate identity.
It invents no alternate supersession mechanism.

## 2. Confirmation continuity and identity chain

The complete predecessor chain was independently verified before this act:

| Lifecycle artifact | Required disposition or identity | Binding verification |
|---|---|---|
| Governance decision | `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB` | `EXACT` — 20,350 bytes; 420 physical lines |
| Independent amendment review | `54C3CAC4DD263CEABA1ED70211529C56839A3C27D4A054A964DD3C68135463B4` | `EXACT` — 22,686 bytes; 417 physical lines |
| Independent amendment confirmation | `41E1A23C5C09D095686E5675A37CF5DC191802060DC9BB104A99D2EEC2574BC8` | `EXACT` — 17,832 bytes; 363 physical lines |
| Confirmation disposition | `AMENDMENT CONFIRMED` | `SATISFIED` |

The independent review refers to the exact decision candidate identity. The
independent confirmation refers to both that exact decision identity and the
exact independent-review identity, confirms the mandatory stored-payload
fingerprint recomputation interpretation, and names additive binding/freeze or
repository-recognized supersession as the next constitutional act.

The chain is continuous and internally consistent. No candidate substitution,
identity drift, missing approval, or unresolved amendment-review condition
prevents binding.

## 3. Exact frozen authoritative supplement identity

The authoritative supplement bound by this act is the confirmed bounded
normative content of the governance decision at this immutable identity:

```text
docs/implementation/BANPU_WP4_RETRY_ORDER_GOVERNANCE_DECISION.md
C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB
20,350 raw bytes
420 physical lines
```

The candidate's Sections 6 through 9 state the bounded Design Section 9
supplement. The entire decision remains the identity-bearing governance record,
while only those confirmed retry-order semantics have normative effect. This
binding record is a lifecycle artifact and is not a member of the frozen
supplement identity.

The supplement must not be represented by copied or paraphrased text detached
from the candidate identity above. Any substantive change requires a new
amendment lifecycle; it is not covered by this freeze.

## 4. Exact semantics made authoritative

The following bounded retry-order semantics are now authoritative as an
additive supplement to Canonical Design Section 9.

### 4.1 Common boundary before `E8-R`

Every invocation must establish all of the following before `E8-R` can return
or fail:

1. service-owned deterministic transaction lifecycle;
2. workspace and portfolio ownership;
3. portfolio lock as the primary serialization boundary;
4. canonical version-1 payload parsing and validation;
5. registry-resolved, distinct predecessor and successor asset IDs;
6. locks on all relevant existing portfolio items;
7. complete E3 registry-state validation;
8. canonical naive-midnight transition date;
9. E7 / MINOR-1 safety;
10. the sole canonical incoming fingerprint; and
11. canonical conversion identity.

No retry classification, return, or conflict failure may bypass this common
boundary.

### 4.2 No-prior-row or new application

If the canonical identity lookup finds no prior canonical conversion row:

- the invocation is not a retry;
- E5 predecessor lookup remains mandatory;
- E6 optimistic quantity and basis verification remains mandatory;
- missing, ambiguous, stale-quantity, or stale-basis predecessor state fails
  closed;
- E3 and E6 precede every first-application write;
- E9 remains the first conversion business write and precedes E10–E12; and
- E13 final shares, basis, cash, and identity assertions precede the sole
  successful commit.

The supplement creates no E5/E6 bypass for new, nonduplicate, or stale-state
work.

### 4.3 Matching retry

If exactly one valid existing canonical conversion exists at the same exact
canonical identity and the fingerprint regenerated from its stored canonical
payload exactly equals the incoming canonical fingerprint:

- bypass only E5/E6;
- perform no insert, update, delete, cash mutation, holding mutation, registry
  mutation, repair, reconciliation, replay, or snapshot action;
- deterministically finish the read-only transaction and release all locks;
  and
- return `already_applied` identifying the existing transaction.

Current successor materialized shares, basis, cash, or other current state is
not a retry-idempotency predicate. Later legitimate activity cannot change the
historical fact established by the valid canonical conversion row. Successor
state comparison or repair remains outside this retry path.

### 4.4 Conflicting retry

If exactly one valid existing canonical conversion exists at the same exact
canonical identity but the fingerprint regenerated from its stored canonical
payload differs from the incoming canonical fingerprint:

- bypass only E5/E6;
- perform no insert, update, delete, business mutation, repair, reconciliation,
  replay, or snapshot action;
- deterministically roll back or otherwise finish the transaction and release
  all locks; and
- hard-fail with the controlled conflict disposition.

A different successor or any other fingerprinted payload semantic is a
conflict at the canonical identity, not an unrelated conversion.

### 4.5 Invalid existing row

An existing row or stored payload that is malformed, internally inconsistent,
ambiguous, noncanonical, or otherwise fails unchanged canonical row validation
is neither a match nor a repair opportunity. Zero or more than one row is not
one valid match. The invocation fails closed, performs no business mutation,
and deterministically finishes cleanup.

### 4.6 Transaction lifecycle

Once any query or lock begins, every exit remains inside the service-owned
cleanup boundary. Matching no-op, conflict, invalid-row, payload, identity,
registry, and date exits must finish or roll back the transaction as
appropriate and release locks before returning or raising. Cleanup performs no
business mutation.

A no-prior-row first application retains one transaction across its locks,
E5/E6, E9–E13, final assertions, and sole successful commit. No caller-visible
path may leak an open transaction.

## 5. Mandatory stored-payload fingerprint recomputation

An existing conversion row is never trusted through a detached digest. Before
any matching or conflicting retry disposition, the service must:

1. parse and validate the existing row's stored canonical
   `conversion_payload`;
2. regenerate its fingerprint from that payload using the sole canonical
   fingerprint algorithm;
3. require the regenerated fingerprint to represent the canonical payload
   exactly;
4. compare the regenerated fingerprint exactly with the incoming canonical
   fingerprint; and
5. fail closed if the existing row, identity projections, payload, or
   regenerated result is invalid or internally inconsistent.

No caller-supplied digest, detached stored digest, partial payload comparison,
alternate fingerprint, or WP4-local fingerprint is authorized. Regeneration
uses the already-authorized canonical payload and fingerprint semantics; it
creates no new capability, schema, index, migration, or file surface.

E7 / MINOR-1 remains upstream of `E8-R`. The incoming fingerprint and the
fingerprint regenerated from the stored payload use one algorithm and do not
constitute competing fingerprints.

## 6. Historical Design preservation and supersession relationship

The historical frozen
[`BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md)
is not rewritten by this act. Its identity still independently reproduces the
WP1 Freeze Record's canonical-LF identity:

| Historical Design property | Preserved value |
|---|---|
| Canonical-LF SHA-256 | `7EE5300D1251A845FB9FD626076ED03FC77307117F7CFB7731B152D68500DE60` |
| Canonical-LF bytes | `28,179` |
| Physical lines | `474` |
| Current raw SHA-256 | `2D2ECE4391961C85DE4076091662C66DA4586C553C6CDD57094970168BF1CE76` |
| Current raw bytes | `28,653` — the 474-byte difference is the existing CRLF representation |

The original Design and its freeze identity remain historical evidence and
continue to govern every semantic not expressly supplemented here.

For the retry-order conflict only, the exact confirmed supplement at the
identity in Section 3 is the current authoritative interpretation of Design
Section 9. Where the original unqualified E5/E6-before-E8 ordering conflicts
with the invocation-class distinction, this supplement controls by introducing
`E8-R` after the common boundary, retaining E5/E6 for no-prior-row applications,
and permitting E5/E6 bypass only for proven matching or conflicting retries.

No other Design section, accounting equation, payload field, canonical
identity, tolerance, write order, final invariant, replay rule, schema rule,
test authority, capability, or file surface is superseded or reinterpreted.

## 7. Exact normative scope

The complete confirmed amendment lifecycle identifies exactly two normative
surfaces:

1. Canonical Design Section 9; and
2. BANPU-WP4 Work Package Plan Sections 3.2, 6, and 9.

This act binds and freezes only the Design Section 9 supplement. It does not
amend, rewrite, or reapprove the Work Package Plan. That plan still expresses
the unqualified pre-amendment order and must complete its own separate
amendment and independent reapproval before implementation may rely on the
retry exception.

No Roadmap, Mandatory Sequence, Allocation, Implementation Authorization,
roadmap Section 1 confirmation, WP1/WP2/WP3 artifact, Decision Log,
Implementation INDEX, WP5+ artifact, or M46 artifact is amended or superseded.

The amendment changes runtime sequencing only. It creates no production file,
test file, endpoint, CLI, frontend path, schema, index, migration, replay or
repair behavior, snapshot behavior, general corporate-action framework,
release/deployment authority, WP5+ authority, or M46 authority.

Allocation and Implementation Authorization remain valid and require no
synchronization because capability, ownership, and file surfaces are unchanged.

## 8. B2–B6 preservation

This binding/freeze act does not resolve, waive, reclassify, implement, review,
or confirm any remaining Independent Implementation Review finding:

| Finding | State preserved |
|---|---|
| `WP4-IIR-B2` — caller-controlled symbols | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B3` — conflicting `MERGED_INTO` preparation | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B4` — transaction cleanup | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B5` — missing final basis assertion | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B6` — incomplete verification evidence | `BLOCKING — TEST/EVIDENCE CORRECTION UNDER EXISTING WP4 AUTHORITY` |

The authoritative transaction-lifecycle clarification is relevant to the
future B4 correction but does not perform or accept that correction.

## 9. Resulting constitutional state and reliance boundary

The amendment lifecycle state after this act is:

```text
AMENDMENT BOUND / FROZEN / AUTHORITATIVE
WORK PACKAGE PLAN NOT YET AMENDED OR REAPPROVED
IMPLEMENTATION MAY NOT YET RELY ON THE RETRY EXCEPTION
```

The Design Section 9 supplement is now authoritative and immutable at the
identity in Section 3. The Work Package Plan remains constitutionally
inconsistent with that supplement until its Sections 3.2, 6, and 9 are amended
and independently reapproved. Implementation reliance therefore remains
prohibited until plan governance completes.

BANPU-WP4 remains allocated and implementation-authorized only within its
existing bounded surface. Its implementation candidate remains not confirmed;
B1 has not been corrected in implementation; B2–B6 remain blocking; and WP4 is
not frozen or closed.

No commit, push, merge, release, deployment, production execution,
production-data mutation, snapshot rebuild, WP5+, or M46 authority is created.

## 10. Verification

Verification was performed before and after creation of this additive record.
This record is not a member of the frozen supplement identity.

| Verification | Result |
|---|---|
| Governance-decision identity | `PASS` — `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB`; 20,350 bytes; 420 physical lines |
| Independent-review identity | `PASS` — `54C3CAC4DD263CEABA1ED70211529C56839A3C27D4A054A964DD3C68135463B4`; 22,686 bytes; 417 physical lines |
| Independent-confirmation identity | `PASS` — `41E1A23C5C09D095686E5675A37CF5DC191802060DC9BB104A99D2EEC2574BC8`; 17,832 bytes; 363 physical lines |
| Historical Design canonical-LF identity | `PASS` — `7EE5300D1251A845FB9FD626076ED03FC77307117F7CFB7731B152D68500DE60`; 28,179 bytes; 474 physical lines |
| Implementation/test entry-state continuity | `PASS` — all six pre-existing WP4 candidate entry hashes remain unchanged |
| WP1/WP2/WP3 continuity | `PASS` — frozen identities and previously authorized deltas remain unchanged by this act |
| Frozen Design, Roadmap, Mandatory Sequence, Allocation, Authorization, WP1/WP2/WP3, Decision Log, INDEX, WP5+, or M46 artifact changed by this act | `NONE` |
| Relative-link targets | `PASS` |
| Markdown fragment links | `NOT APPLICABLE` — no fragment links used |
| Trailing whitespace | `PASS` |
| `git diff --check` | `PASS` |
| `git diff --cached --check` | `PASS` |
| `graphify update .` | `PASS` |
| Staging, commit, push, merge, release, or deployment | `NONE` |

Only this binding/freeze record is attributable to this act. All other working
tree entries pre-date it and remain preserved without absorption.

## 11. Binding/freeze disposition

**BANPU-WP4 RETRY-ORDER AMENDMENT BOUND / FROZEN / AUTHORITATIVE** at candidate
identity `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB`.

**BANPU-WP4 WORK PACKAGE PLAN NOT YET AMENDED OR REAPPROVED.**

**IMPLEMENTATION MAY NOT YET RELY ON THE RETRY EXCEPTION UNTIL PLAN GOVERNANCE
COMPLETES.**

## 12. Exact next constitutional act

The exact next constitutional act is **BANPU-WP4 Work Package Plan amendment
and independent reapproval**, limited to Sections 3.2, 6, and 9 and conforming
exactly to the authoritative Design Section 9 supplement bound here.

This record performs no part of that next act.
