# M46 — Architecture and Implementation Plan — Corrections Response

**Artifact class:** Author corrections response
**Lifecycle stage:** Correction after independent architecture review
**Author role:** M46 Planning Candidate Correction Author
**Corrected subject:** [M46 Architecture and Implementation Plan](M46_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
**Governing allocation:** [M46 Planning Allocation / Commissioning Record](../governance/M46_CORPORATE_ACTION_PORTFOLIO_ACCOUNTING_PLANNING_ALLOCATION_RECORD.md)
**Independent review:** Commissioning input dated 2026-08-05
**Review disposition:** `REQUIRES CORRECTION`
**Response status:** `AUTHOR CORRECTION COMPLETE — PENDING FOCUSED INDEPENDENT RE-REVIEW`
**Implementation authority:** `NONE`
**Work-package allocation or authorization:** `NONE`

## 1. Authority and non-effects

This response performs the correction act authorized for the M46 Planning
Candidate Correction Author by allocation §8. It updates the reviewed candidate
in place and answers findings `M46-R-F1` through `M46-R-F10`.

This response is not the review, focused re-review, confirmation, ratification,
freeze, work-package allocation, implementation authorization, migration,
production correction, cutover, release, or runtime act. A finding marked
`Corrected` below is the correction author's response, not a declaration that
the finding is independently resolved. Only a later competent focused
re-review may determine that.

Exactly one additional artifact is created by this correction act: this
response. The separately intended
`M46_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md` candidate remains absent and is
recorded as a confirmation blocker rather than silently manufactured or
waived.

## 2. Review disposition

The independent review disposition was `REQUIRES CORRECTION`. It reported one
Critical finding, five Major findings, three Minor findings, and one Editorial
finding. This response accepts and corrects all ten. No finding is rejected or
partially corrected.

The correction preserves the reviewed architecture's permanent identity,
effective-dated identifier, total-cost-basis, derived-average-cost, exact quote
binding, deterministic migration, and fail-closed foundations. Changes are
limited to the review's admission-gate, performance, replay, ownership,
authority-anchor, corpus-completeness, cash, time-attribution, Ledger-authority,
and wording findings.

## 3. Finding-by-finding response

| Finding | Severity | Response | Exact corrected locations | Rationale |
| --- | --- | --- | --- | --- |
| `M46-R-F1` — ingestion gate and human confirmation absent | Critical | **Corrected** | Candidate header and opening boundary; §1.1 items 11–12; §2.3; P3–P4; §5.1 rows for admission and accounting truth; §5.2A and §5.2C; §5.3; §8.2–§8.4; §12.1; §13.1 and §13.3; §14.3; §15 WP2; §16.3 G2; §17.1–§17.2 and §17.5; §18.2; §19; §22 | Externally derived consequences are now proposals until Connectivity & Ingestion completes normalization, provenance, identity resolution, attribution, validation, conflict handling, and review. Routine actions require an explicit, specific, versioned, auditable, revocable standing policy; ambiguous, unusual, first-of-kind, high-impact, or non-delegated actions require human confirmation. Atomic release occurs only after confirmation and owner-domain verdicts. |
| `M46-R-F2` — structural-event performance transparency omitted | Major | **Corrected** | §1.1 item 11; §1.2; P13; §7.3–§7.4; §11.5; §12.1; §13.4; §14.4; §15 WP4; §16.3 G4; §17.1–§17.2 and §17.5; §18.2; §19; §20.16; §22 | The candidate now makes value continuity and zero structural-event return explicit. It also records that the frozen return formula has no corporate-action continuity term and prohibits reusing unrelated strip terms or creating a second formula. Affected performance is `UNCOMPUTABLE` until Portfolio Intelligence and Ledger & Accounting provide a governed composition. |
| `M46-R-F3` — two-stream replay contradicts frozen replay contract and Open Question 6 | Major | **Corrected** | §2.3; §5.2C; §8.1 and §8.3–§8.4; §9.1–§9.4; §14.3–§14.4; §15 WP4–WP5; §16.3 G4; §17.2 and §17.4; §18.2; §19; §20.6; §22 | Replay now consumes one canonical Transaction stream. Admitted structural consequences are indistinguishable from other Transactions at the replay boundary. Effect-bundle identity is lineage and atomic-group metadata, not a second stream. Open Question 6 is narrowed to the Ledger-owned canonical Transaction representation and cannot expose Corporate Action classification to replay. |
| `M46-R-F4` — conflict over structural-event adjudication ownership silently resolved | Major | **Corrected** | §2.1.1; §2.3; P4; §5.1 ownership matrix; §5.2A; §5.3; §8.3–§8.4; §12.1; §15 WP1–WP2; §16.3 G1; §19; §22 | The candidate now names the conflict between Asset Foundation §§3.4/4.4 and Corporate Action Domain §§1–4. It treats Platform Architecture §11 G4 as the controlling conflict rule, selects neither lower-source answer, makes Corporate Action Case process-neutral, and blocks WP2–WP4 and every M46 admission until a competent reconciliation is recorded. |
| `M46-R-F5` — Accounting Scope anchored to a source that does not define it | Major | **Corrected** | §2.1 governing-source list | The Portfolio Domain Model citation now states only the accounting-boundary and Base Currency facts it establishes. The candidate directly links the canonical Glossary `Accounting Scope` entry and the governing M42-WP2 contract for scope membership and Base Currency. |
| `M46-R-F6` — intended planning candidate pair is incomplete | Major | **Corrected** | §16.0; §16.3 G0; §18.1 item 9; §20.17; §21.3; §22 | The candidate explicitly states that inline §§15–16 do not discharge the separately named output, that the artifact remains absent, and that the planning corpus is `INCOMPLETE FOR INDEPENDENT CONFIRMATION`. Creation or disposition remains a later competent act. |
| `M46-R-F7` — multi-denomination cash asserted while Base Currency boundary deferred | Minor | **Corrected** | §5.2D; §7.1 Cash row; §20.12 | The projection retains the frozen single cash scalar. Event denomination remains evidence, while multi-denomination cash is conditional on a future governed Ledger/Portfolio contract; actions that cannot be represented under the current contract fail closed. |
| `M46-R-F8` — replay time attribution omitted ADR-003 and frozen rule citation | Minor | **Corrected** | §2.1 ADR list; §20.13 | ADR-003 is now a governing source, and Open Question 13 links both Portfolio Calculation Rules §2 and ADR-003 while preserving the distinction between replay order and incremental window membership. |
| `M46-R-F9` — WP4 presumed a Ledger authoring path that does not exist | Minor | **Corrected** | §15 WP4 row and the paragraph immediately after the work-package table | WP4 now depends on a new competent governance act establishing successor Ledger ownership, role, scope, and documentary authority. Without that act, WP4 is explicitly blocked. |
| `M46-R-F10` — non-existent roadmap candidate described as unmodified | Editorial | **Corrected** | §21.2–§21.3 | The absent file was removed from the unmodified-file list and is now accurately described as an intended artifact not created, tied to the Section 16.0 confirmation block. |

## 4. Remaining disagreements and unresolved conditions

### 4.1 Disagreements with review findings

`NONE`.

No finding is rejected. No constitutional justification for rejection is
therefore required.

### 4.2 Unresolved architecture or supply conditions preserved by correction

These are not disagreements with the review and are not silently treated as
resolved:

1. structural-event adjudication ownership and ownership of the
   both-or-neither guarantee remain blocked pending a competent G4
   reconciliation;
2. the structural-event performance-continuity composition remains owner-domain
   work, and affected authoritative performance fails closed meanwhile;
3. the exact canonical Transaction vocabulary for normalized structural
   consequences remains a Ledger & Accounting determination within the fixed
   one-stream replay boundary;
4. M46-WP4 has no present authoring path until a competent successor governance
   act supplies one; and
5. the intended second planning candidate remains absent, leaving the M46
   planning corpus incomplete for independent confirmation.

## 5. Scope control

The correction does not redesign the architecture beyond the findings. It does
not alter permanent identity, identifier interval semantics, cost-basis
allocation mathematics, quote-binding dimensions, migration phases, BANPU's
acceptance-only status, or the proposed eight-package decomposition except
where the review required a gate, authority dependency, or replay wording
change.

All proposed work packages remain `UNALLOCATED` and `UNAUTHORIZED`.
Implementation, migration, runtime, production correction, cutover, release,
confirmation, ratification, and freeze authority remain `NONE`.

## 6. Verification

Verification is bounded to the corrected architecture candidate and this
response:

- all ten review finding identifiers have exactly one response and each is
  marked `Corrected`;
- the corrected candidate contains 39 repository-local links; after this
  response was created, all 39 resolve, including five section anchors;
- the correction response contains two repository-local links and both resolve;
- corrected candidate structure: 105 headings, no heading-level jump, 14 code
  fences and balanced;
- both corrected artifacts are strict UTF-8;
- both corrected artifacts contain zero trailing-whitespace lines, zero tab
  lines, and no placeholder or patch artifacts;
- the corrected candidate contains eight proposed work-package rows and an
  explicit declaration that all are unallocated and unauthorized;
- `git diff --check` and `git diff --cached --check` report no error;
- no tracked or frozen file is modified; and
- no production test was run because this is architecture/documentary
  correction only and the repository exposes no dedicated Markdown validator.

Corrected candidate identity at this correction boundary:

- lines: `1651`;
- SHA-256: `8C48A812EE374ABC41CAE31FADDF8496B17691488649EA98D7DE125AA8227139`.

## 7. Git status

```text
?? docs/governance/M46_CORPORATE_ACTION_PORTFOLIO_ACCOUNTING_PLANNING_ALLOCATION_RECORD.md
?? docs/implementation/M46_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md
?? docs/implementation/M46_ARCHITECTURE_CORRECTIONS_RESPONSE.md
```

The allocation record was already present and remains unchanged. No file is
staged or committed.

## 8. Current disposition and next act

**Current disposition:** `CORRECTED REVIEW CANDIDATE — PENDING FOCUSED INDEPENDENT RE-REVIEW`; M46 planning corpus `INCOMPLETE FOR INDEPENDENT CONFIRMATION`.

The next competent act is focused independent re-review of findings
`M46-R-F1` through `M46-R-F10` against the corrected locations in §3. This
response does not perform or pre-approve that re-review and does not perform
confirmation.
