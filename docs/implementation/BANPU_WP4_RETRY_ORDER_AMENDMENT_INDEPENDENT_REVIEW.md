# BANPU-WP4 — Retry-Order Amendment Independent Review

**Artifact class:** Additive Independent Bounded Canonical Amendment Review
**Review date:** 2026-08-13
**Review authority:** Independent Bounded Canonical Amendment Reviewer
**Candidate reviewed:** [`BANPU_WP4_RETRY_ORDER_GOVERNANCE_DECISION.md`](BANPU_WP4_RETRY_ORDER_GOVERNANCE_DECISION.md)
**Candidate identity:** raw SHA-256 `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB`; 20,350 bytes; 420 physical lines
**Independent review disposition:** `APPROVED — SUITABLE TO PROCEED TO SEPARATE INDEPENDENT AMENDMENT CONFIRMATION`
**Amendment confirmation performed:** `NO`
**Binding, freeze, or supersession performed:** `NO`
**Implementation reliance created:** `NONE`
**Implementation or test change performed:** `NO`
**Release, deployment, production execution, or production-data authority:** `NONE`
**BANPU-WP5+ authority:** `NONE`
**M46 authority:** `NONE`

---

## 1. Review boundary and independence

This act independently reviews the bounded canonical amendment candidate in
the governance decision. The issuing governance authority's reasoning was
treated as a claim to verify, not as proof.

This reviewer does not act as the issuing governance authority, implementer,
Work Package Plan amendment authority, implementation reviewer,
implementation-confirmation authority, freeze or binding authority, closeout
authority, or release/deployment authority. This act changes no candidate,
frozen authority, implementation file, or test file.

A positive independent review is not amendment confirmation. It does not make
the E5/E6 retry exception implementation-reliable.

## 2. Exact corpus reviewed and authority hierarchy

The review inspected the following live repository authorities:

1. [`BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md),
   especially §§6.1–6.3, 7, 8, 9, 16, and 17;
2. [`BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`](BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md),
   especially universal package rules, the WP4 scope, acceptance criteria, and
   strict dependency graph;
3. [`BANPU_IMPLEMENTATION_SEQUENCE.md`](BANPU_IMPLEMENTATION_SEQUENCE.md),
   especially the sequence invariants and Step 4;
4. the applicable frozen WP1 authority and continuity records:
   [`BANPU_WP1_CONFIRMATION.md`](BANPU_WP1_CONFIRMATION.md),
   [`BANPU_WP1_FREEZE_RECORD.md`](BANPU_WP1_FREEZE_RECORD.md),
   [`BANPU_WP1_FREEZE_IDENTITY_CORRECTION_RECORD.md`](BANPU_WP1_FREEZE_IDENTITY_CORRECTION_RECORD.md),
   and [`BANPU_WP1_RESIDUAL_IDENTITY_RECORD.md`](BANPU_WP1_RESIDUAL_IDENTITY_RECORD.md);
5. the applicable frozen WP2 authority:
   [`BANPU_WP2_WORK_PACKAGE_PLAN.md`](BANPU_WP2_WORK_PACKAGE_PLAN.md),
   [`BANPU_WP2_IMPLEMENTATION_CONFIRMATION.md`](BANPU_WP2_IMPLEMENTATION_CONFIRMATION.md),
   [`BANPU_WP2_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP2_IMPLEMENTATION_FREEZE_RECORD.md),
   and [`BANPU_WP2_EPIC_CLOSEOUT.md`](BANPU_WP2_EPIC_CLOSEOUT.md);
6. the applicable amended and frozen WP3 authority:
   [`BANPU_WP3_BOUNDED_PLANNING_AMENDMENT_RECORD.md`](BANPU_WP3_BOUNDED_PLANNING_AMENDMENT_RECORD.md),
   [`BANPU_WP3_PLANNING_AMENDMENT_CONFIRMATION.md`](BANPU_WP3_PLANNING_AMENDMENT_CONFIRMATION.md),
   [`BANPU_WP3_AMENDED_PLANNING_FREEZE_RECORD.md`](BANPU_WP3_AMENDED_PLANNING_FREEZE_RECORD.md),
   [`BANPU_WP3_IMPLEMENTATION_CONFIRMATION.md`](BANPU_WP3_IMPLEMENTATION_CONFIRMATION.md),
   [`BANPU_WP3_IMPLEMENTATION_FREEZE_RECORD.md`](BANPU_WP3_IMPLEMENTATION_FREEZE_RECORD.md),
   and [`BANPU_WP3_EPIC_CLOSEOUT.md`](BANPU_WP3_EPIC_CLOSEOUT.md);
7. [`BANPU_WP4_ALLOCATION_RECORD.md`](BANPU_WP4_ALLOCATION_RECORD.md);
8. [`BANPU_WP4_IMPLEMENTATION_AUTHORIZATION_RECORD.md`](BANPU_WP4_IMPLEMENTATION_AUTHORIZATION_RECORD.md);
9. [`BANPU_WP4_WORK_PACKAGE_PLAN.md`](BANPU_WP4_WORK_PACKAGE_PLAN.md),
   especially §§3.2, 4, 6, and 9;
10. [`BANPU_WP4_ROADMAP_SECTION_1_REVIEWER_CONFIRMATION.md`](BANPU_WP4_ROADMAP_SECTION_1_REVIEWER_CONFIRMATION.md);
11. [`BANPU_WP4_INDEPENDENT_IMPLEMENTATION_REVIEW.md`](BANPU_WP4_INDEPENDENT_IMPLEMENTATION_REVIEW.md); and
12. the candidate governance decision identified above.

The repository establishes this controlling order: the approved canonical
Design governs semantics; the Roadmap allocates those semantics to packages;
the Mandatory Sequence fixes predecessor order; frozen WP1/WP2/WP3 records
bind accepted predecessor state; WP4 Allocation and Implementation
Authorization bind the existing capability and file surface; and the WP4 Work
Package Plan operationalizes that authority. A later implementation candidate
cannot amend any of those authorities. Frozen text remains historical evidence
unless an independently reviewed and confirmed additive supplement is bound or
recognized as its successor under the repository's amendment convention.

## 3. Independently reproduced B1 conflict

The conflict is real:

1. Design §9 requires, within one transaction, predecessor lookup and
   optimistic quantity/basis verification before duplicate evaluation.
2. The WP4 Plan makes that sequence explicit as E5, E6, E7, E8 and makes the
   §3.2 order an exit criterion.
3. A successful first application performs E10, which removes or transforms
   the current predecessor materialization.
4. LM-14 nevertheless requires a later exact retry to return
   `already_applied` without another transaction row or another materialized
   conversion.

After E10, a matching retry cannot satisfy E5 using canonical current-state
semantics when the predecessor holding was removed. It therefore cannot reach
E6 or E8 in the unqualified original order. Historical transaction facts are
not a current holding, and neither replay nor reconstruction is authorized in
the live retry path.

No frozen sentence makes E5/E6 optional for retries, defines duplicate lookup
as a preflight, or limits the stated ordering to first applications. The
cross-step rules in Plan §3.2 do not erase the complete ordered table, and Plan
§9 expressly requires that order. There is no valid no-amendment
interpretation.

**Determination:** `WP4-IIR-B1 INDEPENDENTLY REPRODUCED`.

## 4. Necessity and alternatives

| Alternative | Independent result | Reason |
|---|---|---|
| A — unconditional original order | `REJECTED` | Makes LM-14 unreachable after canonical predecessor consumption unless current state is fabricated or reconstructed |
| B — unconditional E8 before E5/E6 | `REJECTED AS OVERBROAD` | Does not express the strict prior-row predicate and could obscure mandatory new-work optimistic validation |
| C — bounded retry preflight | `APPROVED` | Separates retry disposition only after a common validated boundary and retains E5/E6 for every no-prior-row application |
| D — reconstruct predecessor state | `REJECTED` | Converts a no-op retry into replay, repair, or reconstruction and duplicates frozen WP2 ownership |

An amendment is constitutionally necessary. Alternative C is the minimum
sufficient amendment because it introduces one read-only disposition point and
bypasses only the two checks whose required current state may have been
canonically consumed.

## 5. Common-boundary review

The candidate requires every invocation to enter the service-owned lifecycle,
establish workspace/portfolio ownership, lock the portfolio, parse the version-1
payload, resolve distinct canonical predecessor and successor IDs, lock
relevant existing holdings, validate the complete E3 registry state, derive
the canonical transition date, pass E7/MINOR-1, generate the sole canonical
fingerprint, and construct the exact canonical conversion identity before
`E8-R` can decide or fail.

That boundary prevents retry classification from bypassing:

- workspace and portfolio ownership;
- canonical asset identity and registry resolution;
- payload schema, decimal, date, projection, and fingerprint semantics;
- predecessor/successor distinctness and registry-transition invariants;
- transition-date construction and naive-midnight identity;
- the MINOR-1 precision gate;
- the authorized portfolio serialization boundary; and
- deterministic transaction cleanup.

Caller-supplied symbols or provider identifiers cannot substitute for registry
identity under these semantics. The boundary creates no new caller or operator
authority.

**Determination:** `COMMON BOUNDARY SUFFICIENT`.

## 6. First/new application

When the exact identity lookup finds no prior conversion row, the candidate
does not classify the invocation as a retry. E5 predecessor lookup remains
mandatory, including only the existing controlled legacy-symbol fallback. E6
must verify current quantity and basis within the canonical tolerances. Missing,
ambiguous, stale-quantity, and stale-basis conditions fail closed before E9.

E3 and E6 precede every first-application write. E9 remains the first
conversion business write and remains before E10–E12. E13 still asserts final
shares, basis, cash, and identity before the sole successful commit. All steps
remain within one owned transaction.

**Determination:** `FIRST-APPLICATION ACCOUNTING, OPTIMISTIC VALIDATION, WRITE
ORDER, AND ATOMICITY PRESERVED`.

## 7. Matching retry and successor-state determination

An existing valid conversion at the exact canonical identity with the exact
regenerated canonical fingerprint proves that the same append-only conversion
request was previously recorded. Requiring current predecessor E5/E6 would be
invalid because the proven first application may have consumed that state.
Bypassing only E5/E6 is therefore safe after the complete common boundary and
existing-row validation.

The matching path still proves portfolio ownership, both registry-resolved
asset identities, registry state, payload validity, transition date, canonical
identity, MINOR-1-safe fingerprint equality, and validity of the existing
conversion row. It performs no business write and finishes its read-only
transaction before returning `already_applied`.

Current successor shares, basis, or cash are **not** idempotency predicates.
Later legitimate purchases, sales, distributions, conversions, accounting
reads, or other authorized activity may change materialized state without
changing whether this historical conversion was already applied. Requiring
current successor state to equal the post-conversion E13 state would reject a
valid historical retry and turn retry recognition into reconciliation or
repair. That work remains outside WP4 and outside this amendment.

**Determination:** `MATCHING RETRY SAFE; CURRENT SUCCESSOR STATE CORRECTLY
EXCLUDED`.

## 8. Conflicting retry

An existing valid row at the same canonical identity but with a different
canonical fingerprint establishes a collision after the predecessor may have
been consumed. E5/E6 bypass is justified by the same current-state reason as
for a match, but the result must be a hard failure.

Exact fingerprint inequality covers a different successor identity, ratio,
quantity, basis, CIL fact, date semantic, evidence field, or any other
fingerprinted payload semantic. The path permits no insert, update, delete,
materialized-state action, repair, or reconciliation and must clean up before
raising or returning the controlled conflict.

The identity key is conversion type plus portfolio, canonical predecessor asset
ID, and canonical transition date under established workspace ownership. The
existing partial unique constraint uses the same database identity. A row with
a different successor or payload is therefore a conflict at that identity, not
an unrelated conversion aliased by a weaker lookup.

**Determination:** `CONFLICTING RETRY FAILS CLOSED WITHOUT MUTATION OR ALIAS`.

## 9. Existing-row validation and fingerprint determination

The amendment must not trust a digest as detached historical authority. The
current schema stores `conversion_payload` but has no separate stored
fingerprint column. The canonicalizer derives `PositionConversion.fingerprint`
from the parsed payload. Consequently the only corpus-compatible meaning of
the decision's “stored canonical fingerprint” is:

1. parse and validate the existing row's stored canonical payload;
2. regenerate its fingerprint from that payload using the one canonical
   fingerprint algorithm;
3. require the regenerated value to be a valid exact canonical digest; and
4. compare that regenerated string exactly with the incoming canonical
   fingerprint.

This is option **B** in substance. Option A is neither safe nor representable
by the authorized schema. If a future implementation introduces a detached
stored digest, trusts a caller digest, performs a partial payload comparison,
or does not regenerate from the stored payload, it will violate this reviewed
candidate and require correction; no repair behavior is authorized.

The existing row must also satisfy the unchanged canonical row invariants in
Design §§6.1–6.3: type, portfolio ownership, top-level predecessor identity,
naive-midnight transition date, payload validity and projections, and
successor/payload semantics. The decision's express rule that an invalid or
internally inconsistent row fails closed preserves those already-binding
invariants; this review does not add a new one. Zero or more than one row is not
a match.

**Determination:** `SUFFICIENT, WITH MANDATORY RECOMPUTATION FROM STORED
CANONICAL PAYLOAD; NO STORED DIGEST IS TRUSTED`.

## 10. Concurrency and locking

The portfolio lock remains the primary serialization boundary for competing
applications. Relevant existing holding locks remain within the already
authorized model. Locking an existing conversion row with the strongest
behavior supported by the authorized database path narrows the read race and
does not create a new schema or index. The existing conversion-only unique
constraint remains the final insert-race backstop.

The amendment does not claim that SQLite proves production-dialect row-lock
semantics. PD-WP4-4 remains the accepted evidence limitation, and the amendment
introduces no new unbounded concurrency mechanism beyond the already-authorized
atomic service.

**Determination:** `CONCURRENCY AND ATOMICITY MODEL PRESERVED; PD-WP4-4
UNCHANGED`.

## 11. Transaction lifecycle

Once database access or locking starts, every exit is within the service-owned
cleanup boundary. A matching no-op must finish the read-only transaction and
release locks. Parse, identity, registry, date, existing-row, and conflict
failures after database access must roll back or otherwise deterministically
finish the transaction. A no-prior-row application retains one transaction
over locks, E5/E6, E9–E13, final assertions, and the sole commit. Cleanup may
not perform a business mutation.

These semantics are sufficient governance precision for correcting
`WP4-IIR-B4`. They do not change B4's current implementation-review state and
do not perform its correction.

**Determination:** `TRANSACTION-LIFECYCLE SEMANTICS SUFFICIENT`.

## 12. MINOR-1 relationship

`E8-R` is downstream of E7 on every invocation. The sole incoming fingerprint
and the fingerprint regenerated from stored payload use the same canonical
algorithm; they are not competing fingerprints. Equality is exact, not partial.
The independently reviewed MINOR-1 correction is neither reopened nor widened.

**Determination:** `MINOR-1 GATE AND PRIOR REVIEW PRESERVED`.

## 13. Exact amendment surface

The normative amendment surface is exactly:

1. Canonical Design §9, to state the validated `E8-R` disposition boundary and
   conditional E5/E6 retry exception; and
2. WP4 Work Package Plan §§3.2, 6, and 9, to operationalize the order, add the
   corresponding retry/cleanup evidence, and amend the exit criterion.

No Roadmap or Mandatory Sequence amendment is required: each already requires
the same atomic service, optimistic validation, canonical-fingerprint matching
no-op, conflicting failure, and verification outcomes without specifying the
now-disputed invocation-class exception. Design §§6–8 and 16 remain consistent;
their payload, schema, replay, row-invariant, and test semantics do not change.

No amendment is required to Allocation, Implementation Authorization, the
roadmap Section 1 reviewer confirmation, WP1/WP2/WP3 authority, Decision Log,
Implementation INDEX, WP5+, or M46. The candidate changes runtime sequencing
within an already-authorized capability and file surface; it does not change
package ownership or repository navigation state.

**Determination:** `EXACT TWO-ARTIFACT NORMATIVE SURFACE CONFIRMED`.

## 14. Capability and authority continuity

The amendment creates no production or test-file surface, schema, migration,
endpoint, CLI, frontend behavior, snapshot behavior, replay/repair capability,
general corporate-action framework, release/deployment authority, WP5+
authority, or M46 authority.

Allocation and Implementation Authorization already bind the atomic live
conversion service, locking, optimistic checks, canonical-fingerprint
idempotency, append-only insertion, materialization, and final assertions. The
amendment changes no capability or authorized file. Their synchronization is
therefore unnecessary and their bounded authority remains valid. The Work
Package Plan does require amendment because it alone operationalizes the
unqualified E5/E6-before-E8 order.

## 15. B2–B6 preservation

| Finding | State after this review |
|---|---|
| `WP4-IIR-B2` — caller-controlled symbols | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B3` — conflicting `MERGED_INTO` preparation | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B4` — transaction cleanup | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B5` — missing final basis assertion | `BLOCKING — CORRECTABLE UNDER EXISTING WP4 AUTHORITY` |
| `WP4-IIR-B6` — incomplete verification evidence | `BLOCKING — TEST/EVIDENCE CORRECTION UNDER EXISTING WP4 AUTHORITY` |

The amendment clarifies the lifecycle semantics needed for B4 but implements
nothing and closes, waives, or reclassifies none of B2–B6.

## 16. Amendment lifecycle determination

The candidate's successor sequence is consistent with repository convention:

1. this Independent Bounded Canonical Amendment Review;
2. separate Independent Amendment Confirmation;
3. additive binding/freeze or repository-recognized supersession of the
   confirmed Design §9 supplement, preserving the historical frozen text;
4. WP4 Work Package Plan amendment and separate independent reapproval;
5. implementation correction for B1 and the still-open B2–B6 work;
6. renewed Independent Implementation Review; and
7. later, separate Implementation Confirmation.

Repository precedent separates amendment review, confirmation, amended freeze
or supersession, authority synchronization where scope changed, Work Package
Plan reapproval, implementation review, and implementation confirmation. Here
Allocation and Authorization synchronization can be omitted because scope and
surface do not change. The plan amendment and its independent reapproval may be
recorded in one approval act if that act independently verifies the exact
amended plan identity; neither may be combined with this review or the prior
governance decision merely for convenience.

## 17. Independent review disposition

The proposed amendment is:

- constitutionally necessary;
- technically sound;
- the minimum sufficient amendment;
- correctly bounded to retry disposition after the common boundary;
- compatible with all preserved BANPU authorities; and
- suitable to proceed to independent amendment confirmation.

**Disposition:**

```text
BANPU-WP4 RETRY-ORDER BOUNDED CANONICAL AMENDMENT — INDEPENDENT REVIEW APPROVED
READY FOR SEPARATE INDEPENDENT AMENDMENT CONFIRMATION
NOT YET IMPLEMENTATION-RELIABLE
```

## 18. Exact next constitutional act

The exact next act is **Independent Amendment Confirmation** of the reviewed
retry-order supplement at governance-decision identity
`C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB`.

That confirmation must independently verify this review and the unchanged
candidate identity. It must not perform binding/freeze, Work Package Plan
amendment, implementation correction, implementation review, implementation
confirmation, release, deployment, production execution, snapshot rebuilding,
WP5+, or M46 work.

## 19. Repository verification

Verification was performed after creation of this additive review. The review
artifact is not a member of any frozen implementation corpus and did not alter
the candidate identity above.

| Verification | Result |
|---|---|
| Only additive artifact created by this act | `SATISFIED` — this review artifact only |
| Implementation/test entry-state continuity | `PASS` — all 6 pre-existing WP4 candidate raw SHA-256 values rechecked unchanged |
| Frozen Design/Roadmap/Sequence or other frozen governance artifact changed by this act | `NONE` |
| Decision Log or Implementation INDEX changed | `NONE` |
| Governance-decision identity | `PASS` — `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB`, unchanged |
| WP1 canonical-LF member identities | `PASS/EXPECTED DELTA` — 10 of 12 reproduce exactly; the only two deltas are the pre-existing, authorized WP4 `MINOR-1` candidate files `transaction_canonicalizer.py` and `test_transaction_canonicalizer.py`, and both entry hashes are unchanged by this act |
| WP2 identity continuity | `PASS` — current canonical-LF/committed-blob aggregate `6E50F5B5E2AAA008EA1C3DA25D1FC34C41F9CBAE81A293A463FB3F6BF5DA4159`; raw checkout differences remain line-ending evidence, not a change by this act |
| WP3 frozen implementation identity | `PASS` — aggregate `E2C44B920D533D386FE3C470C48A8701806D14BA4C1866A7F9058C700FB0E7B8` independently reproduced from freeze commit `f09e958`; five later pre-existing tracked revisions are outside this act and unchanged |
| Relative-link targets | `PASS` — 23 of 23 exist |
| Markdown fragments/anchors | `NOT APPLICABLE` — no fragment links used |
| Trailing whitespace | `PASS` — zero findings |
| `git diff --check` | `PASS` |
| `git diff --cached --check` | `PASS` |
| Untracked review-artifact whitespace check | `PASS` |
| `graphify update .` | `PASS` — 21,470 nodes, 41,572 edges, 1,746 communities |
| Final Git status | `PASS` — this review is the only new path attributable to this act; all other listed changes pre-date it and remain unabsorbed |
| Staging, commit, or push | `NONE` |

The Git checks emitted only the environment's pre-existing inaccessible global
ignore warning. It does not affect diff or whitespace results.
