# M44-WP1 — Inherited Gate Inventory and Closure Register

**Milestone:** M44 — Portfolio Analytics Gate Closure and Normative Semantics Foundation

**Work package:** M44-WP1 only

**Artifact class:** Constitutional evidence and navigation register

**Status:** `RC2 — CORRECTED AFTER INDEPENDENT CONSTITUTIONAL REVIEW; REQUIRES
INDEPENDENT CONSTITUTIONAL CONFIRMATION`

**Register date:** 2026-07-29 (RC1)

**Revision:** RC2, 2026-07-29 — citation-integrity correction only, applied under
[M44-WP1 Formal Constitutional Response](M44_WP1_FORMAL_CONSTITUTIONAL_RESPONSE.md).
No constitutional meaning, authority, gate, disposition, or repository fact is
changed. See §15.

**Governing frozen authority:** [M44 Architecture and Implementation Plan](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
(RC2), `COMPLETE AND FROZEN` per [M44 Architecture Freeze Record](M44_ARCHITECTURE_FREEZE_RECORD.md) §9

**Runtime authority:** `NONE`
**Source-code authority:** `NONE`
**Persistence/schema/migration authority:** `NONE`
**API/transport authority:** `NONE`
**UI/presentation authority:** `NONE`
**Implementation authority:** `NONE`
**Provider authority:** `NONE`
**Production-method authority:** `NONE`
**Executable-validation authority:** `NONE`
**Capability-completion authority:** `NONE`
**Frozen-artifact-amendment authority:** `NONE`
**Gate-disposition authority:** `NONE`
**Ownership-determination authority:** `NONE`
**Vocabulary-admission authority:** `NONE`

---

## 0. Executive determination

This register is the canonical, cited enumeration of every constitutional
obligation that M44 inherits. It is evidence and navigation only, exactly as
frozen [M44 RC2](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §8.7 C0 allocates:
*"Authority. Evidence and navigation only. It closes nothing."*

It records five inherited gates, `G-1` through `G-5`, each traced to the exact
frozen sentence that created it and to the exact repository state that leaves it
undischarged. It reconciles those five against the complete inherited-gate
enumerations of frozen M43-WP7 §3.2, frozen M43-WP6 §3.2, and frozen M43-WP8 §4,
so that no inherited obligation is silently dropped and none is counted twice. It
allocates each gate to exactly one M44 work package or to exactly one deferred
successor obligation, and it fixes, per gate, the admissible terminal states that
frozen RC2 §16.2 permits.

**It dispositions nothing.** At the date of this register every inherited gate
carries the terminal state `NOT YET DISPOSITIONED`, because no M44 work package
that holds disposition authority has run (frozen
[Freeze Record](M44_ARCHITECTURE_FREEZE_RECORD.md) §6.2).

---

## 1. Purpose and normative boundary

### 1.1 What this register does

1. Enumerates every inherited constitutional obligation entering M44 (§4, §5).
2. Records, per gate, the ten register fields required for it to be actionable
   by its owning work package: identifier, constitutional purpose, governing
   frozen authority, current repository evidence, why it remains open, exact
   closure authority, responsible work package, downstream dependencies,
   permitted terminal states, and evidence required for disposition (§4).
3. Reconciles the M44 five-gate framing against the frozen M43 gate
   enumerations, proving completeness and non-duplication (§5).
4. Fixes the gate and work-package dependency graph (§6).
5. Fixes the closure matrix — owner, artifact, confirmation requirement, and
   downstream work packages released (§7).
6. Inventories every frozen artifact consumed as evidence, including the three
   paths whose *absence* is itself constitutional evidence (§9).
7. States objective completion criteria for M44-WP1 (§10).

### 1.2 What this register does not do

Per frozen RC2 §8.7 and §11 M44-WP1 excluded scope, this register does not:

- close, release, defer, or otherwise disposition any gate;
- admit, rename, reject, or rely upon any new constitutional noun;
- determine any owner of any semantic concern;
- select, propose, or constrain any encoding, formula, method, or method
  version;
- modify, amend, restate, or reinterpret any frozen M1–M43 artifact, or the
  frozen M44 architecture;
- author, register, extend, version, or serialize any contract kind in any
  domain's corpus (frozen RC2 INV-C4);
- authorize any downstream work package to begin.

### 1.3 Interpretation rule for the disposition vocabulary

Frozen RC2 §11 M44-WP1 states the completion criterion that every gate carries
"exactly one disposition of `CLOSED BY M44-WPn` or `DEFERRED TO D-n`." Frozen
RC2 §16.2 separately fixes a closed five-state *terminal-state* vocabulary in
which only `CLOSED` counts as closure, and frozen RC2 §11 preamble states that
"no work package promises a closure it may lack the authority or the upstream
inputs to reach."

These are reconciled here, and the reconciliation is a reading of frozen text,
not an amendment of it:

- **Disposition** names the *allocation of closure responsibility*. It answers
  "which instrument is responsible for discharging this obligation." It is
  recorded now, by this register.
- **Terminal state** names the *outcome actually reached*, drawn from the frozen
  §16.2 five-state vocabulary. It is recorded later, by the responsible work
  package, and never by this register.

`CLOSED BY M44-WPn` therefore reads as *"closure responsibility is allocated to
M44-WPn"*. It is not a prediction, a promise, or a claim that closure will be or
has been achieved. Every gate below carries both fields, and every terminal-state
field currently reads `NOT YET DISPOSITIONED`.

---

## 2. Governing authority

Authority order for this register, highest first, restating frozen RC2 §1.2
without extension:

1. [Platform Architecture](../architecture/platform_architecture.md) Laws 1–15,
   §6 domain allocations, §7 relationships and gates, §8 cross-cutting
   principles, §11 governance precedence, §12 canonical vocabulary;
2. Domain Constitutions —
   [Portfolio Calculation Rules](../investment/PORTFOLIO_CALCULATION_RULES.md)
   and [Optimizer Philosophy](../investment/OPTIMIZER_PHILOSOPHY.md);
3. [ADR-001](../decisions/ADR-001_TRANSACTION_LEDGER_SINGLE_SOURCE_OF_TRUTH.md)
   through [ADR-005](../decisions/ADR-005_REPLAY_CORRECTNESS_BASELINE.md), and
   the [Decision Log](../engineering/DECISION_LOG.md);
4. frozen M34 ownership allocations;
5. frozen M36, M39, M40–M41, and M42 contracts;
6. the frozen [M43 Architecture](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) and
   frozen M43-WP1 through M43-WP8 artifacts;
7. the frozen [M44 Architecture (RC2)](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
   and the [M44 Architecture Freeze Record](M44_ARCHITECTURE_FREEZE_RECORD.md);
8. this register, after independent confirmation, within the authority classes
   declared above — all of which are `NONE` except documentary evidence and
   navigation.

A lower authority cannot amend, weaken, reinterpret, or bypass a higher one.
Legacy source code, deployed formulas, provider behavior, API contracts, and UI
behavior are evidence of current state only and carry no constitutional
authority.

---

## 3. Authorization precondition — recorded, and subsequently remediated

Frozen RC2 §1.1 conditions the start of every M44 work package on the
independent confirmation being "recorded as a repository-local artifact at
`docs/implementation/M44_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md`." Frozen
[Freeze Record](M44_ARCHITECTURE_FREEZE_RECORD.md) §2.1 records that the four
review-chain artifacts are filed under different names, states that the
architecture may not be edited to match the filings, and concludes:

> **Until that rename is performed, no M44 work package is authorized to begin
> under frozen RC2 §1.1.**

### 3.1 Verified repository state

**As verified at original register authoring (RC1, 2026-07-29).** This table is
retained unchanged as the historical record of the divergence frozen Freeze
Record §2.1 names:

| Path required by frozen RC2 §1.1 / §13.1 | Resolves | Path as filed | Resolves |
| --- | --- | --- | --- |
| `M44_ARCHITECTURE_INDEPENDENT_REVIEW.md` | `NO` | `M44_INDEPENDENT_CONSTITUTIONAL_REVIEW.md` | `YES` |
| `M44_ARCHITECTURE_FORMAL_CONSTITUTIONAL_RESPONSE.md` | `NO` | `M44_FORMAL_CONSTITUTIONAL_RESPONSE.md` | `YES` |
| `M44_ARCHITECTURE_CONSTITUTIONAL_ADJUDICATION.md` | `NO` | `M44_CONSTITUTIONAL_ADJUDICATION.md` | `YES` |
| `M44_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md` | `NO` | `M44_INDEPENDENT_CONFIRMATION.md` | `YES` |

At that point the filing remediation required by frozen Freeze Record §2.1 had
**not** been performed.

**As verified after the filing remediation, by directory enumeration of
`docs/implementation/` (RC2, 2026-07-29):**

| Path required by frozen RC2 §1.1 / §13.1 | Resolves | Former non-conforming filing | Resolves |
| --- | --- | --- | --- |
| [M44_ARCHITECTURE_INDEPENDENT_REVIEW.md](M44_ARCHITECTURE_INDEPENDENT_REVIEW.md) | `YES` | `M44_INDEPENDENT_CONSTITUTIONAL_REVIEW.md` | `NO` — renamed |
| [M44_ARCHITECTURE_FORMAL_CONSTITUTIONAL_RESPONSE.md](M44_ARCHITECTURE_FORMAL_CONSTITUTIONAL_RESPONSE.md) | `YES` | `M44_FORMAL_CONSTITUTIONAL_RESPONSE.md` | `NO` — renamed |
| [M44_ARCHITECTURE_CONSTITUTIONAL_ADJUDICATION.md](M44_ARCHITECTURE_CONSTITUTIONAL_ADJUDICATION.md) | `YES` | `M44_CONSTITUTIONAL_ADJUDICATION.md` | `NO` — renamed |
| [M44_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md](M44_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md) | `YES` | `M44_INDEPENDENT_CONFIRMATION.md` | `NO` — renamed |

The filing remediation required by frozen Freeze Record §2.1 has been performed,
by rename, after this register was originally authored. `P-1` is therefore
**satisfied**, and the confirmation resolves at the path frozen RC2 §1.1
declares.

The rename was performed outside M44-WP1, under separate authority. M44-WP1
neither authorized nor performed it; this section records the verified fact and
claims no part in the act. The remediation took the form frozen Freeze Record
§2.1 requires — renaming the filings to the declared paths — and not the form it
forbids: no frozen artifact was edited to match the filings.

### 3.2 Consequence for this register

This register is authored as a candidate artifact. Its effectiveness is
conditioned on both of the following, and it performs neither:

- **P-1** — the frozen Freeze Record §2.1 filing remediation is performed, so
  that the confirmation resolves at the path frozen RC2 §1.1 declares.
  **`SATISFIED`** — performed by rename outside M44-WP1 after this register was
  originally authored; verified at §3.1.
- **P-2** — this register receives independent constitutional review and
  confirmation with unresolved findings `NONE` (frozen RC2 §12.5 point 2).
  **`OUTSTANDING`** — independent constitutional review has been received and
  returned `APPROVED WITH MINOR CORRECTIONS`; independent confirmation has not
  been recorded.

Until `P-1` and `P-2` are both satisfied, this register is `NON-EFFECTIVE`, no
downstream M44 work package may cite it as a discharged predecessor, and no gate
disposition may be attempted. `P-1` is satisfied and `P-2` is not, so this
register **remains `NON-EFFECTIVE`**. Recording `P-1` here is a register
obligation under frozen RC2 INV-B2 ("every open gate is named, cited by exact
path and section, and reported in every artifact that inherits it"); performing
the remediation was not within M44-WP1's scope and was not attempted by this
register at RC1 or at RC2.

---

## 4. Repository Gate Inventory

Five inherited gates enter M44. The framing, the identifiers, and the gate
statements are consumed verbatim in substance from frozen RC2 §3.1 and frozen
Freeze Record §1. This register adds no gate, removes no gate, and renumbers no
gate.

### 4.0 Gate summary

| Gate | Obligation | Source authority | Disposition | Terminal state at register date |
| --- | --- | --- | --- | --- |
| `G-1` | Repository-local M43 Architecture confirmation record absent | frozen M43-WP1 Register §1 | `CLOSED BY M44-WP2` | `NOT YET DISPOSITIONED` |
| `G-2` | M43 §8 canonical period-return ownership governance correction outstanding | frozen M43-WP1 Register §7.4 | `CLOSED BY M44-WP3` | `NOT YET DISPOSITIONED` |
| `G-3` | Portfolio Composition canonical-byte obligation undischarged | frozen M42-WP7 §5; frozen M43-WP3 Subject §7.1 | `CLOSED BY M44-WP4` | `NOT YET DISPOSITIONED` |
| `G-4` | Annualization-basis governed dependency absent | frozen M43-WP4 Plan §6.7 | `CLOSED BY M44-WP5` | `NOT YET DISPOSITIONED` |
| `G-5` | The two universal normative specifications do not exist | frozen M43-WP7 Plan §3.1; frozen M43-WP8 Plan §4 | `CLOSED BY M44-WP6` (first half) and `CLOSED BY M44-WP7` (second half) | `NOT YET DISPOSITIONED` |

---

### 4.1 `G-1` — M43 Architecture confirmation record absent

| Field | Content |
| --- | --- |
| **Gate identifier** | `G-1` |
| **Constitutional purpose** | To ensure that a milestone whose commissioning authority holds it confirmed carries a **repository-local** record of that confirmation, so that a downstream reader can resolve the status by repository path rather than by external assertion. The defect class is precisely "a confirmed status whose repository-local record does not resolve at the declared path" (frozen Freeze Record §2.1). |
| **Governing frozen authority** | [M43-WP1 Register](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md) §1: the commissioning authority "records the governing M43 Architecture as `COMPLETE AND FROZEN` after Independent Constitutional Confirmation `APPROVED`"; "The repository-local M43 plan header has not yet been synchronized to that confirmed state"; "a separately authorized governance change must synchronize the plan's status line or provide its repository-local confirmation artifact; WP1 cannot self-authorize that external edit." Carried into M44 by frozen RC2 §3.1 `G-1`. |
| **Current repository evidence** | (a) [M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) line 3 reads `Proposed status: READY FOR INDEPENDENT ARCHITECTURE CONFIRMATION` — verified 2026-07-29. (b) No file matching `M43_ARCHITECTURE_INDEPENDENT_*` exists in `docs/implementation/` — verified by directory enumeration 2026-07-29. (c) [M43_EPIC_CLOSEOUT.md](M43_EPIC_CLOSEOUT.md) §1 states "This closeout does not close an inherited gate and grants no additional authority," and §2 states that "Historical workflow-stage labels inside frozen artifacts remain unchanged." |
| **Why the gate remains `OPEN`** | The obligation named by frozen M43-WP1 §1 is discharged by exactly one of two acts — synchronizing the frozen plan's status line, or providing a repository-local confirmation artifact. Neither has occurred. The first is unavailable to M44 in any case (frozen RC2 §1.6 rule 3 and §4.2 forbid modifying any frozen M1–M43 artifact, including the M43 header). The second has not been authored. The M43 epic closeout expressly disclaims closing it. |
| **Exact closure authority** | Frozen RC2 §5.1 row 1 read with §8.1 C1 and §11 M44-WP2: a documentary governance record, authored under M44 authority, exercising extension basis **E-3** of frozen RC2 §5.3 (supplying a repository-local record where a frozen governance chain required one and none was written). It states status; it grants nothing. |
| **Responsible work package** | `M44-WP2 — M43 Architecture Confirmation Record and Status Reconciliation`. Sole deliverable `M44_WP2_M43_ARCHITECTURE_CONFIRMATION_RECORD.md` (frozen RC2 §11, §13.1). |
| **Downstream dependencies** | `M44-WP3` strictly — frozen RC2 §12.3 requires WP2 before WP3 because "the corrected artifact's own status must be settled first." Also: every M44 artifact that cites M43 Architecture status (frozen RC2 §11 M44-WP2 downstream consumers). `G-1` gates no other gate and blocks no other work package. |
| **Permitted terminal states** | `CLOSED` — the only state frozen RC2 §11 M44-WP2 contemplates ("G-1 recorded `CLOSED`"). Residually, if the record cannot be produced, frozen RC2 §16.2 admits `OPEN` with the exact missing element and its exact owner named (INV-B2, INV-F1). `RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE`, `OPEN — PARTIAL`, and `DEFERRED` are not available to this gate: no frozen authority names a partial form, a separate recording vehicle, or a successor obligation for it. |
| **Evidence required for disposition** | (1) The confirmation record exists at `docs/implementation/M44_WP2_M43_ARCHITECTURE_CONFIRMATION_RECORD.md`. (2) It states the confirmed M43 status, the exact divergence from the in-file header line, and the reconciliation basis drawn from the M43 Epic Closeout, the Decision Log M43 entries, and the Implementation INDEX. (3) Its claimed status matches those sources verbatim in substance. (4) `git diff` contains no frozen M43 path. (5) The record asserts no authority. (6) Independent confirmation, unresolved findings `NONE`. |

---

### 4.2 `G-2` — M43 period-return ownership governance correction outstanding

| Field | Content |
| --- | --- |
| **Gate identifier** | `G-2` |
| **Constitutional purpose** | To reconcile the governing M43 §8 ownership row to the confirmed frozen M43-WP1 §7.3 two-part allocation — Portfolio-performance *meaning* to Portfolio Intelligence, accounting semantics determining what enters the return to Ledger & Accounting — and thereby to dispose of the standing block `M43-WP6 BLOCKED — GOVERNANCE CORRECTION REQUIRED BEFORE WP6`, without creating a second period-return rule (Law 9) and without amending the level-2 Portfolio Calculation Rules. |
| **Governing frozen authority** | [M43 Architecture](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §8, line 174: "Canonical period-return rule — Candidate: Ledger & Accounting — OWNER TO PROVE AT WP1 … WP6 is blocked until disposition; no second rule is permitted." [M43-WP1 Register](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md) §7.3 (the split) and §7.4 (the block, the four-step correction path, and the release condition "Until steps 1–3 are complete, WP6 may not begin"). Carried into M44 by frozen RC2 §3.1 `G-2`, which keeps **block release** (steps 1–3) and **final recording** (step 4) constitutionally separate. |
| **Current repository evidence** | (a) Frozen M43 §8 line 174 is unchanged and still presents the composite candidate row. (b) Frozen M43-WP1 §7.4 step 3 — "the governing M43 ownership row must be reconciled by an independently reviewed constitutional correction before WP6 begins" — has no corresponding repository artifact. (c) Step 4's named vehicle, "the consolidated Decision Log entry authorized at M43 epic closeout by frozen M43 §§13 and 17," has passed: [M43_EPIC_CLOSEOUT.md](M43_EPIC_CLOSEOUT.md) §1 records that the closeout "does not close an inherited gate." (d) Frozen [M43-WP7 Plan](M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §3.2 item 2 records the block as live and states "Closure belongs to the M43 governance sequence, not WP6 or WP7." |
| **Why the gate remains `OPEN`** | Steps 3 and 4 of the frozen four-step correction path were never performed. Step 3 is the release condition and is unperformed; step 4's named recording vehicle has lapsed. M43 cannot perform either: it is frozen and unamendable. |
| **Exact closure authority** | Frozen RC2 §5.1 row 1 and §8.2 C2: the **M43 governance sequence**, exercised by M44 under frozen M43-WP1 §7.4 **step 3**. Step 3 plus its independent confirmation discharges the frozen release condition. No M44 instrument holds authority to discharge step 4, and none asserts it (frozen RC2 §8.2, §11 M44-WP3, §12.6). |
| **Responsible work package** | `M44-WP3 — Period-Return Ownership Governance Correction`. Sole deliverable `M44_WP3_PERIOD_RETURN_OWNERSHIP_GOVERNANCE_CORRECTION.md`. Strict predecessors: `M44-WP1`, `M44-WP2`. |
| **Downstream dependencies** | `D-1` (normative core performance and rolling method specification) — `M44-WP3` is its entry gate. Transitively `D-2a`, `D-2b`, `D-3`, `D-4`. `G-2` has **no** downstream M44 work-package consumer (frozen RC2 §11.1: "M44-WP3 has no downstream M44 consumer; it gates D-1 only"). It does not gate `M44-WP6` or `M44-WP7`. |
| **Permitted terminal states** | `RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE` — the state frozen RC2 §11 M44-WP3 requires ("G-2 is reported `RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE`, **never** `CLOSED`"). `CLOSED` is **prohibited** at M44-WP3 while no authorized step 4 recording vehicle exists (frozen RC2 §12.6, §17 OQ-5). Residually, if step 3 is not performed or fails confirmation, `OPEN` under §16.2 with the missing element named. `OPEN — PARTIAL` and `DEFERRED` are not available: the frozen authority states the release condition exactly and allocates no successor. |
| **Evidence required for disposition** | (1) A constitutional proof restating the confirmed §7.3 split against Platform Architecture §§6.3 and 6.5, Portfolio Calculation Rules §§1–9 and §10, M40-WP1 §8.3, ADR-001, and ADR-004 — that is, every governing authority listed in frozen M43-WP1 §7.2. (2) A superseding record naming the M43 §8 row, without editing it. (3) An explicit release statement discharging the frozen steps 1–3 condition and disposing of the standing `M43-WP6 BLOCKED` item, with the exact preconditions under which `D-1` may begin. (4) An explicit outstanding-recording statement naming step 4, its lapsed vehicle, and the fact that final G-2 recording is not claimed. (5) Exactly one allocation per concern; no formula; no second period-return rule; no amendment to Portfolio Calculation Rules or any ADR. (6) Independent confirmation, unresolved findings `NONE`. |

---

### 4.3 `G-3` — Portfolio Composition canonical-byte obligation undischarged

| Field | Content |
| --- | --- |
| **Gate identifier** | `G-3` |
| **Constitutional purpose** | To discharge the **delegated** canonical-byte obligation that frozen M42-WP7 §5 expressly conditioned, declined to supply, and preserved — supplying the Composition's own **container-level** framing over owner-supplied coordinate canonical references — so that a concrete Portfolio Measure Subject (`PMS1`) and Portfolio Analytics Input Manifest (`PAIM1`) become formable. Until it is discharged, every subject, manifest, result identity, hash, and canonical-byte claim in the Portfolio Analytics corpus is artificial. |
| **Governing frozen authority** | [M42-WP7](M42_WP7_PORTFOLIO_COMPOSITION_CONTRACT_SPECIFICATION.md) §5: the tag `M42-WP7-PORTFOLIO-COMPOSITION-1`; the ten-element canonical semantic field order; "A representation may claim canonical bytes only if it preserves this tag, this order, exact citations, owner attributions, Provenance associations, and the explicit-absence distinction"; "This documentation-only contract defines no byte or character encoding, delimiter, escaping, container syntax, transport, serialization library, or persistence form"; "Their exclusion does not remove or defer the frozen canonical-byte obligation"; and the container-level limit "This does not define nested field order inside any source-owned coordinate or alter an upstream coordinate." [M43-WP3 Subject](M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md) §7.1: "until a separately authorized contract supplies the exact Composition canonical bytes, no concrete Portfolio Measure Subject—and consequently no concrete Portfolio Analytics Input Manifest—can be formed," and "If an owning contract cannot supply one exact immutable canonical reference or canonical representation required here, a conforming subject cannot be formed." [M43-WP3 Manifest](M43_WP3_PORTFOLIO_ANALYTICS_INPUT_MANIFEST_CONTRACT_SPECIFICATION.md) §6.3 and §10.3. Carried into M44 by frozen RC2 §3.1 `G-3`. |
| **Current repository evidence** | (a) Frozen M42-WP7 §5 supplies tag and field order and no byte representation — verified 2026-07-29. (b) Frozen M43-WP3 Subject §7.1 records the failure and states "Every WP3 example remains an artificial documentary placeholder. Conformance MUST fail closed, and no reader, implementation, provider, or WP3 artifact may invent an encoding." (c) Frozen M43-WP3 Manifest §6.3 records under `PORTFOLIO_COMPOSITION` that "this mandatory entry—and therefore a concrete manifest—cannot yet be formed." (d) No separately authorized Composition byte contract exists in `docs/implementation/`. (e) Frozen M42-WP7 §3 allocates the coordinate classes: Portfolio Identity, Accounting Scope, Portfolio Membership, and Portfolio Base Currency to **Ledger & Accounting**; Investment Universe Declaration and Portfolio Benchmark Declaration to **Portfolio Intelligence**; Portfolio Lifecycle State to **Ledger & Accounting**; and Provenance meaning and capture to **Connectivity & Ingestion**. |
| **Why the gate remains `OPEN`** | The instrument frozen M43-WP3 §7.1 names — "a separately authorized contract" supplying the exact Composition canonical bytes — has never been authored. The obligation is not extinguished by M42-WP7's silence on mechanism; frozen M42-WP7 §5 expressly preserves it. |
| **Exact closure authority** | Frozen RC2 §5.1 row 2 and §8.3 C3: **Portfolio Intelligence**, as sole owner of the Portfolio Composition noun under frozen M42-WP7 §9 checklist item 1, exercising extension bases **E-1** (the §5 conditional permission and preserved obligation) and **E-2** (the remedy frozen M43-WP3 §7.1 names but does not supply). Expressly **not** declared silence / E-3 (frozen RC2 §5.3, Appendix A item 5). |
| **Responsible work package** | `M44-WP4 — Portfolio Composition Canonical Byte Representation Contract`. Deliverables `M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md` plus positive and negative documentary vector files under `docs/implementation/m44/fixtures/`. |
| **Downstream dependencies** | `M44-WP6` and `M44-WP7`, **strictly and only in the `CLOSED` terminal state** (frozen RC2 §12.3). The mandatory §12.1.1 gate-state checkpoint sits between `M44-WP4` and `M44-WP6`. Transitively `G-5`, and `D-1` through `D-4`. `G-3` `OPEN — PARTIAL` is a prerequisite failure for `M44-WP6` and `M44-WP7` "without exception" (frozen RC2 §12.3). |
| **Permitted terminal states** | Exactly two, and never a blend (frozen RC2 §3.1 `G-3`, §11 M44-WP4): `CLOSED` — every one of the ten frozen coordinates has an owner-supplied exact immutable canonical reference and the container framing is confirmed; or `OPEN — PARTIAL` — at least one required coordinate reference is unsupplied. "There is no third state, and `OPEN — PARTIAL` is not a closure." `CLOSED` and `OPEN — PARTIAL` are never asserted together. `RELEASED — …` and `DEFERRED` are unavailable. |
| **Evidence required for disposition** | (1) The nested-coordinate canonical-reference obligation inventory across all ten frozen M42-WP7 fields, with per-coordinate closure or fail-closed routing to the owning domain naming the exact missing element. (2) The container-level tagged, length-delimited, injective, round-trippable, order-stable, locale-independent byte representation preserving the frozen tag and field order over opaque owner-supplied coordinate canonical references. (3) Explicit-absence, owner-attribution, and Provenance-association representation. (4) Rejection rules for unknown fields, alternate forms, duplicate keys, non-canonical numbers, trailing bytes, and Unicode ambiguity. (5) A **non-triggering conformance proof** addressing `PC-NGV-11`, `PC-NGV-12`, `PC-NGV-13`, and `PC-NGV-14` individually and by name, plus frozen M42-WP7 §9 checklist items 10, 11, and 12, each with a direct conformance statement and at least one negative vector. (6) A coverage ledger mapping each of the ten frozen fields to at least one positive and one negative vector. (7) A preservation check proving tag and field order are byte-order-identical to frozen M42-WP7 §5. (8) For `CLOSED` only: two independent readers derive byte-identical Composition bytes for the same logical Composition. (9) Independent constitutional review **and** an independent serialization review distinct from the author; unresolved findings `NONE`. |

---

### 4.4 `G-4` — Annualization-basis governed dependency absent

| Field | Content |
| --- | --- |
| **Gate identifier** | `G-4` |
| **Constitutional purpose** | To determine the constitutional owner of the annualization basis and to establish, by search of that owner's frozen corpus, whether an exact **existing** governed contract kind is already present — so that annualized methods either acquire a lawful dependency or remain explicitly blocked, and never acquire an implicit `252`, `365`, or `365.25`. |
| **Governing frozen authority** | [M43-WP4 Plan](M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §6.7: the four required proofs; "Frozen WP2 §8.1 requires an exact existing governed contract kind"; "The frozen corpus presently supplies no such annualization contract kind"; "WP4 MUST NOT author, name, imply, or serialize a new governed dependency contract"; methods "remain blocked until a separately authorized governance instrument supplies an exact owner, existing governed contract kind, identifier, immutable version, and canonical value bytes"; and "No unstated, ambient, implicit, or hidden `252`, `365`, `365.25`, or other constant is permitted." [M43-WP2](M43_WP2_PORTFOLIO_MEASURE_DEFINITION_METHOD_VERSION_AND_APPLICABILITY_CONTRACT_SPECIFICATION.md) §8.1–8.2. [M43-WP4 Plan](M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §5.2 (no "artificial contract kind, or WP4-authored dependency kind"). Carried into M44 by frozen RC2 §3.1 `G-4`. |
| **Current repository evidence** | (a) Frozen M43-WP4 §6.7 states on its own authority that the frozen corpus supplies no such contract kind. (b) Frozen [M43-WP7 Plan](M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §3.2 item 8 records the annualization-dependency gate as live and blocking annualized volatility, tracking error, downside deviation, Sharpe, Sortino, information ratio, and alpha. (c) Frozen [M43-WP6 Plan](M43_WP6_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §3.2 records the same gate for annualized return: "WP6 cannot manufacture any missing coordinate." (d) No annualization-basis governance instrument exists at any path in the repository. |
| **Why the gate remains `OPEN`** | The required instrument must satisfy two frozen predicates M44 cannot satisfy on its own: the **existing** predicate (frozen M43-WP2 §8.1 requires an exact *existing* governed contract type; a kind registered for the purpose cannot be "existing" at the moment of declaration) and the **owner-domain** predicate (frozen M43-WP4 §6.7 requires the owner be proved "without expanding Portfolio Intelligence authority," and frozen RC2 §5.1 records the owner as presumptively **not** Portfolio Intelligence). M44 therefore has no authority to author, register, extend, version, or serialize the instrument (frozen RC2 INV-C4). |
| **Exact closure authority** | Split, and the split is constitutive: the **ownership determination and requirement specification** are M44's, under frozen RC2 §5.1 row 5 and §8.4 C4. The **governance instrument itself** is owned exclusively by the domain M44-WP5 proves, produced under that domain's own authority, and is recorded as deferred obligation `D-7`. `G-4` closes at M44 **only if** an exact existing governed contract kind is already present in the determined owner's frozen corpus and is identified by exact citation. |
| **Responsible work package** | `M44-WP5 — Annualization Basis Ownership Determination and Requirement Specification`. Sole deliverable `M44_WP5_ANNUALIZATION_BASIS_OWNERSHIP_DETERMINATION_AND_REQUIREMENT_SPECIFICATION.md`. **No** contract-kind registration is produced in any domain's corpus under either outcome (frozen RC2 §13.1). |
| **Downstream dependencies** | `M44-WP6` Component G, which binds M44-WP5's outcome **in either state** — `G-4` `OPEN` is expressly *not* a prerequisite failure for `M44-WP6` or `M44-WP7` (frozen RC2 §12.3). `D-2b` (annualization-dependent risk and benchmark-relative methods). `D-7` (the owner-domain instrument). `D-3` only where an attribution method would require annualization. `D-2a` is deliberately **not** dependent on `G-4`. |
| **Permitted terminal states** | Exactly two (frozen RC2 §3.1 `G-4`, §11 M44-WP5): `CLOSED` — an exact existing governed contract kind is identified by citation in the determined owner's frozen corpus, with all five required fields already published by that owner, and it passes frozen M43-WP2 §8.2 closure unchanged; or `OPEN` — no such existing kind is identified; the requirement specification is delivered and the exact missing element and exact owner are named. `OPEN` is "a valid and honest terminal state for the work package, and it is **not** a gate closure." `OPEN — PARTIAL`, `RELEASED — …`, and `DEFERRED` are unavailable. |
| **Evidence required for disposition** | (1) All four frozen M43-WP4 §6.7 proofs: `VERSIONED_CALCULATION_DEPENDENCY` correct; `GOVERNED_EVIDENCE` incorrect; caller override rejected; owner and placement expand no domain's authority and transfer no source calendar meaning out of Market Intelligence. (2) An exhaustive, cited search of the determined owner's frozen corpus. (3) For `CLOSED`: the exact citation, identifier, immutable version, and canonical value bytes **as the owner already publishes them**. (4) For `OPEN`: the requirement specification stating exactly what the owner-domain instrument must supply, the named missing element, the named owner, and the consequences for `D-2b` and `D-7`. (5) Negative vectors rejecting an unversioned or ambient `252`/`365`/`365.25`, and a vector distinguishing a governed version-bound derived session count of `252` from an ambient one. (6) A negative vector rejecting any contract kind, or requirement specification presented as a contract kind, authored by M44. (7) Independent confirmation, unresolved findings `NONE`. |

---

### 4.5 `G-5` — The two universal normative specifications do not exist

| Field | Content |
| --- | --- |
| **Gate identifier** | `G-5` |
| **Constitutional purpose** | To supply the two method-family-independent normative specifications on which every blocked Portfolio Analytics method family depends: the temporal/currency/calendar/benchmark/arithmetic semantics contract (frozen M43-WP4 Components A–K) and the Portfolio Measure Result contract (frozen M43-WP5's twelve closures). Without them, no method family can bind a calendar, currency, alignment, missing-data, precision, rounding, or result-classification rule. |
| **Governing frozen authority** | [M43-WP7 Plan](M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §3.1, naming the two required binding-source paths and stating "A plan, expected filename, or unchanged prerequisite is not a substitute for an existing independently confirmed normative specification." [M43-WP6 Plan](M43_WP6_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §3.2 items 4–5 and its statement "Neither specification is present in the current repository corpus." [M43-WP8 Plan](M43_WP8_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §4: "The required WP4 and WP5 normative specifications and WP6 normative method specification are not currently present. Consequently, future WP8 normative method work remains blocked." Content allocations: frozen M43-WP4 §§6.1–6.11 Components A–K and §7 no-default matrix; frozen M43-WP5 §§0, 3, 5–10, 13. Carried into M44 by frozen RC2 §3.1 `G-5`. |
| **Current repository evidence** | Neither required path exists in `docs/implementation/` — verified by directory enumeration 2026-07-29: `M43_WP4_TEMPORAL_CURRENCY_CALENDAR_BENCHMARK_AND_ARITHMETIC_SEMANTICS_CONTRACT_SPECIFICATION.md` `ABSENT`; `M43_WP5_PORTFOLIO_MEASURE_RESULT_CONTRACT_SPECIFICATION.md` `ABSENT`. Only the frozen *plans* `M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md` and `M43_WP5_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md` exist, and frozen M43-WP7 §3.1 expressly denies that a plan substitutes for a confirmed specification. |
| **Why the gate remains `OPEN`** | M43 froze the plans for both specifications and closed without authorization to author either. The normative work was never begun, and M43 cannot begin it now. |
| **Exact closure authority** | Frozen RC2 §5.1 rows 3 and 4: **Portfolio Intelligence** normative semantics and normative result-contract authority, non-production, under frozen M43-WP4 §§4, 6 and frozen M43-WP5 §§0, 5. Exercised through frozen RC2 §8.5 C5 and §8.6 C6. |
| **Responsible work package** | Two, each owning one half: `M44-WP6 — Portfolio Analytics Normative Semantics Specification` (first half; deliverable at the frozen M43-named path `M43_WP4_TEMPORAL_CURRENCY_CALENDAR_BENCHMARK_AND_ARITHMETIC_SEMANTICS_CONTRACT_SPECIFICATION.md`, per frozen RC2 §17 OQ-2 resolved in favour of the M43-named paths) and `M44-WP7 — Portfolio Measure Result Normative Contract Specification` (second half; deliverable at `M43_WP5_PORTFOLIO_MEASURE_RESULT_CONTRACT_SPECIFICATION.md`). Each must state in its header that it is authorized by M44 and discharges a frozen M43 allocation (frozen RC2 §13.1, R-6). |
| **Downstream dependencies** | `D-1`, `D-2a`, `D-2b`, `D-3`, `D-4`. Internally: `M44-WP7` is strictly downstream of `M44-WP6`; both are strictly downstream of `M44-WP4` with `G-3` `CLOSED`, and of the §12.1.1 checkpoint. |
| **Permitted terminal states** | `CLOSED` — both specifications exist at their declared paths, are independently confirmed and frozen, and every allocated component and closure is discharged with vector coverage; or `OPEN` — the specifications are not authored, with the cause named. Frozen RC2 §13.1 fixes the `OPEN` case explicitly: if the §12.1.1 checkpoint does not permit `M44-WP6` and `M44-WP7` to begin, "they are not authored, and the closeout records G-5 as open with the checkpoint outcome as its cause." See `RQ-1` in §8.2 for the asymmetric half-discharge case, which frozen RC2 does not name and which this register does not decide. |
| **Evidence required for disposition** | **First half (`M44-WP6`):** every one of frozen M43-WP4 Components A–K carries at least one normative row with at least one positive and one negative vector; every row of the frozen M43-WP4 §7 no-default matrix has a direct negative vector; the risk-free-evidence authority-class proof of §6.6 is discharged; Component G binds M44-WP5's outcome, including the named-unavailability binding where `G-4` is `OPEN`; Component K's canonical serialization rests on confirmed formable Composition bytes; determinism, timezone, market-closure, sparse-history, FX-gap, benchmark-gap, zero-denominator, negative-value, leap-year, rounding-boundary, and caller-override-rejection vectors exist; a coverage ledger with no uncovered row. **Second half (`M44-WP7`):** the twelve frozen M43-WP5 §0 closures are each discharged and each mapped to at least one positive and one negative vector; identical inputs and Portfolio Method Version yield byte-identical results; every unavailable or degraded result carries a named reason; `UNAVAILABLE` is never promoted to a Portfolio Computation Outcome; Canonical Temporal Claim compatibility is complete. **Both:** independent constitutional review plus an independent serialization/numerical review distinct from the author; unresolved findings `NONE`. |

---

## 5. Inherited-obligation reconciliation — completeness and non-duplication

Frozen RC2 §11 M44-WP1 requires a "completeness check against the frozen
M43-WP7 §3.2 enumeration." This section performs that check and extends it to
the other two frozen enumerations, so that every inherited obligation appears
exactly once and carries exactly one disposition.

### 5.1 Frozen M43-WP7 §3.2 — inherited external gates 1–10

| # | Frozen M43-WP7 §3.2 gate | Maps to | Disposition |
| --- | --- | --- | --- |
| 1 | WP7 identity gate — retain the frozen title and allocation "Risk and Benchmark-Relative Method Specifications" | Not an M44 gate; a standing allocation constraint on the successor obligation | `DEFERRED TO D-2` (constraint carried, never relaxed) |
| 2 | M43 governance-correction gate — frozen WP1 §§7.3–7.4 | `G-2` | `CLOSED BY M44-WP3` |
| 3 | WP6 normative completion gate — the required independently confirmed core-performance method specification | Not an M44 gate; the specification is `D-1` | `DEFERRED TO D-1` |
| 4 | WP3 / M42-WP7 representability gate | `G-3` | `CLOSED BY M44-WP4` |
| 5 | WP4 normative-specification gate | `G-5`, first half | `CLOSED BY M44-WP6` |
| 6 | WP5 normative-result gate | `G-5`, second half | `CLOSED BY M44-WP7` |
| 7 | Risk-free-evidence gate — frozen WP4 §6.6 | Constituent of `G-5` first half (frozen RC2 §4.1 I-7: "including the risk-free-evidence authority-class proof") | `CLOSED BY M44-WP6` |
| 8 | Annualization-dependency gate — frozen WP4 §6.7 | `G-4` | `CLOSED BY M44-WP5` for the determination; the instrument is `DEFERRED TO D-7` |
| 9 | Benchmark-form evidence gate — `Composite` and `Category` unavailable | Not an M44 gate; requires separate governed Market Intelligence evidence | `DEFERRED TO D-6` |
| 10 | Vocabulary gate — frozen WP1 downstream vocabulary rule | Standing procedural gate binding every M44 artifact under frozen RC2 §9.7 | Addressed by §11 of this register; no admission required, so no gate is opened |

All ten are accounted for. None is duplicated. None is unassigned.

### 5.2 Frozen M43-WP6 §3.2 — entry gates 1–7 and the two additional gates

| # | Frozen M43-WP6 §3.2 entry gate | Maps to | Disposition |
| --- | --- | --- | --- |
| 1 | The WP1 §7.4 standing block closed by the separately authorized governance-correction workflow | `G-2` | `CLOSED BY M44-WP3` |
| 2 | The correction records the exact singular ownership and semantic boundary | `G-2` (content requirement) | `CLOSED BY M44-WP3` |
| 3 | The correction leaves one and only one canonical period-return rule and preserves Ledger & Accounting accounting semantics | `G-2` (content requirement) | `CLOSED BY M44-WP3` |
| 4 | The WP4 normative semantics specification exists, is confirmed, and is cited by exact path | `G-5`, first half | `CLOSED BY M44-WP6` |
| 5 | The WP5 normative result contract exists, is confirmed, and is cited by exact path | `G-5`, second half | `CLOSED BY M44-WP7` |
| 6 | All frozen WP2–WP5 prerequisites remain effective and unchanged | Standing invariant, not a gate | Preserved by frozen RC2 INV-C1; verified at closeout (frozen RC2 §12.7 step 4) |
| 7 | The proposed corpus passes the downstream vocabulary gate | Same as M43-WP7 §3.2 item 10 | See §11 |
| + | Composition canonical-byte representability gate (prose, §3.2) | `G-3` | `CLOSED BY M44-WP4` |
| + | Annualization representability gate (prose, §3.2) | `G-4` | `CLOSED BY M44-WP5` / `DEFERRED TO D-7` |

### 5.3 Frozen M43-WP8 §4 — validation-recorded blockage

| Frozen M43-WP8 §4 statement | Maps to | Disposition |
| --- | --- | --- |
| "The required WP4 and WP5 normative specifications … are not currently present" | `G-5` | `CLOSED BY M44-WP6` and `CLOSED BY M44-WP7` |
| "… and WP6 normative method specification [is] not currently present" | `D-1` | `DEFERRED TO D-1` |
| "Normative WP8 method work: `BLOCKED PENDING INHERITED GATE CLOSURE`" | `D-3` | `DEFERRED TO D-3` |

### 5.4 The frozen M43-WP9 allocation — `OQ-4` recorded

Frozen [M43 Architecture](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §9 line
385 allocates "M43-WP9 — Runtime Realization, Compatibility, and Cutover
Design." No WP9 artifact exists, and [M43_EPIC_CLOSEOUT.md](M43_EPIC_CLOSEOUT.md)
declares M43 complete with WP1–WP8. Frozen M43-WP6, WP7, and WP8 each still
cite WP9 as a live future authority.

Frozen RC2 §17 `OQ-4` sets the decision deadline for this item at "M44-WP1
confirmation, so the register records the allocation as
deferred-with-owner-unassigned rather than silently dropped," and adopts
alternative (a).

**Recorded here accordingly:**

| Item | Record |
| --- | --- |
| Frozen M43-WP9 allocation | `LIVE IN FROZEN TEXT — NO OWNING MILESTONE` |
| Disposition | `DEFERRED TO D-4` — deferred-with-owner-unassigned |
| Prerequisite | `D-1` through `D-3` frozen (frozen RC2 §4.5) |
| Milestone number assigned | `NONE`. M44 holds no future-milestone allocation authority (frozen RC2 §4.5, §16.9, Freeze Record §3.3) |
| Absorbed into M44 | `NO` (frozen RC2 §4.4, §2.4) |
| Declared discharged by the M43 closeout | `NO` — the closeout closed no gate and discharged no allocation |

### 5.5 Deferred obligation inventory

Consumed verbatim in substance from frozen RC2 §4.3 and Freeze Record §6.3. No
obligation below is a gate M44 may close, and none is assigned a milestone
number.

| # | Deferred obligation | Blocked on |
| --- | --- | --- |
| `D-1` | Normative core performance and rolling method specification | `M44-WP3` (`G-2`); `M44-WP6` and `M44-WP7` confirmed and frozen |
| `D-2a` | Non-annualized normative risk methods | `D-1` |
| `D-2b` | Annualization-dependent normative risk and benchmark-relative methods | `D-1`, plus `G-4` and `D-7` |
| `D-3` | Normative position and sector attribution method specification | `D-1` |
| `D-4` | Runtime realization, compatibility, and cutover design — the live frozen M43-WP9 allocation | `D-1` through `D-3` frozen |
| `D-5` | Executable Portfolio Analytics implementation, registry, kernel, adapters, shadow parity, API cutover | `D-4` frozen, under a separately authorized implementation milestone |
| `D-6` | Benchmark `Composite` and `Category` evidence construction and matching | separate governed Market Intelligence evidence |
| `D-7` | The owner-domain annualization-basis governance instrument | the determined owner domain, acting under its own authority |

---

## 6. Gate Dependency Graph

### 6.1 Gate-to-work-package allocation

```text
G-1 ──────────────► M44-WP2
G-2 ──────────────► M44-WP3
G-3 ──────────────► M44-WP4
G-4 ──────────────► M44-WP5
G-5 ──────────────► M44-WP6  (first half)
      └──────────► M44-WP7  (second half)
```

Exactly one work package owns each gate half. No gate is owned by two work
packages, and no work package owns a gate this register did not allocate to it
(frozen RC2 INV-A3).

### 6.2 Work-package order with gate conditions

```text
                        M44-WP1
                 (this register; closes nothing)
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
     M44-WP2             M44-WP4             M44-WP5
      (G-1)               (G-3)               (G-4)
        │                   │                   │
        ▼                   │                   │
     M44-WP3                │                   │
      (G-2)                 │                   │
        │                   └────────┬──────────┘
        │                            ▼
        │              §12.1.1 GATE-STATE CHECKPOINT
        │              G-3 CLOSED ──────► proceed
        │              G-3 OPEN — PARTIAL ► STOP or formally re-scope
        │              state unestablished ► STOP
        │                            │
        │                            ▼
        │                        M44-WP6
        │                       (G-5 first half)
        │                            │
        │                            ▼
        │                        M44-WP7
        │                       (G-5 second half)
        │                            │
        ▼                            ▼
       D-1 ◄─────────────────────────┘
        │
        ├──► D-2a
        ├──► D-2b ◄──── G-4 outcome + D-7 (owner-domain instrument)
        ├──► D-3
        └──► D-4 ──► D-5
```

### 6.3 Inter-gate dependencies

| From | To | Nature | Frozen basis |
| --- | --- | --- | --- |
| `G-1` | `G-2` | Strict sequencing. `M44-WP3` corrects a row inside an artifact whose own confirmed status must first be settled by `M44-WP2`. | frozen RC2 §12.3; §8.2 C2 "Dependencies. C1 for the confirmed status of the artifact whose row is corrected" |
| `G-3` | `G-5` | Strict blocking. `M44-WP6` Component K and `M44-WP7` result identity both resolve through Composition bytes; `G-3` `OPEN — PARTIAL` is a prerequisite failure "without exception." | frozen RC2 §12.3; §11 M44-WP6 and M44-WP7 predecessor requirements; frozen M43-WP3 §7.1 |
| `G-4` | `G-5` | Content-constraining, **not** blocking. `M44-WP6` Component G binds the outcome in either state; where `G-4` is `OPEN`, Component G binds exactly one value: *annualization unavailable — named missing element and named owner*. | frozen RC2 §11 M44-WP6 Component G binding rule; §12.3; frozen M43-WP4 §6.7 |
| `G-2` | — | No inter-gate dependency. `G-2` gates `D-1` only and has no downstream M44 work-package consumer. | frozen RC2 §11.1 |
| `G-1`, `G-2`, `G-3`, `G-4`, `G-5` | — | No cycle exists. | frozen RC2 §11.1, §18 "Circular dependencies: `NONE FOUND`" |

### 6.4 Non-dependencies recorded explicitly

To prevent a later artifact from inventing a blocking relation the frozen
architecture does not create:

- `G-4` `OPEN` does **not** block `M44-WP6` or `M44-WP7` (frozen RC2 §12.3).
- `G-2` does **not** block `M44-WP4`, `M44-WP5`, `M44-WP6`, or `M44-WP7`.
- `G-1` does **not** block `M44-WP4` or `M44-WP5`.
- `D-2a` does **not** depend on `G-4` or `D-7`; only `D-2b` does (frozen RC2
  §4.3).
- `D-3` does **not** depend on `M44-WP5` unless an attribution method requires
  annualization (frozen RC2 §7.2).

---

## 7. Closure Matrix

| Gate | Closure owner | Closure artifact | Confirmation requirement | Downstream released on the closing terminal state |
| --- | --- | --- | --- | --- |
| `G-1` | M44, exercising extension basis E-3 as a documentary governance record; frozen RC2 §8.1 C1 | `docs/implementation/M44_WP2_M43_ARCHITECTURE_CONFIRMATION_RECORD.md` | Independent constitutional review → corrections response if findings exist → independent confirmation, unresolved findings `NONE` (frozen RC2 §12.4, §12.5 point 3) | `M44-WP3` may begin |
| `G-2` | The M43 governance sequence, exercised by M44 under frozen M43-WP1 §7.4 **step 3**; frozen RC2 §8.2 C2 | `docs/implementation/M44_WP3_PERIOD_RETURN_OWNERSHIP_GOVERNANCE_CORRECTION.md` | Independent constitutional review → independent confirmation, unresolved findings `NONE`. Confirmation of step 3 **is** the discharge of the frozen steps 1–3 release condition. Step 4 is **not** confirmed by this chain and is not claimed | The standing `M43-WP6 BLOCKED` item is disposed; `D-1` acquires its entry gate. No M44 work package is released |
| `G-3` | Portfolio Intelligence as sole owner of the Portfolio Composition noun, under E-1 and E-2; frozen RC2 §8.3 C3 | `docs/implementation/M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md`; `docs/implementation/m44/fixtures/M44_WP4_POSITIVE_DOCUMENTARY_VECTORS.md`; `docs/implementation/m44/fixtures/M44_WP4_NEGATIVE_DOCUMENTARY_VECTORS.md` | Independent constitutional review **and** an independent serialization review distinct from the constitutional reviewer (frozen RC2 §12.4); then the §12.1.1 gate-state checkpoint confirmation (frozen RC2 §12.5 point 5), which no work package may declare satisfied on its own authority | On `CLOSED` **and** a passing checkpoint: `M44-WP6`, then `M44-WP7`. On `OPEN — PARTIAL`: nothing is released; the milestone stops or is formally re-scoped through a new independently confirmed architecture revision |
| `G-4` | Determination: M44-WP5, determination and requirement-specification authority only. Instrument: the determined owner domain, under its own authority (`D-7`) | `docs/implementation/M44_WP5_ANNUALIZATION_BASIS_OWNERSHIP_DETERMINATION_AND_REQUIREMENT_SPECIFICATION.md`. **No** contract file is produced at any path under any outcome | Independent constitutional review → independent confirmation, unresolved findings `NONE`; then the §12.1.1 checkpoint confirmation that the terminal state is established | On `CLOSED`: `D-2b` becomes reachable behind `D-1`. On `OPEN`: `M44-WP6` still proceeds under the Component G named-unavailability binding; `D-2b` remains deferred behind `D-7` |
| `G-5` first half | Portfolio Intelligence normative semantics authority; frozen RC2 §8.5 C5 | `docs/implementation/M43_WP4_TEMPORAL_CURRENCY_CALENDAR_BENCHMARK_AND_ARITHMETIC_SEMANTICS_CONTRACT_SPECIFICATION.md`; `m44/fixtures/M44_WP6_POSITIVE_DOCUMENTARY_VECTORS.md`; `m44/fixtures/M44_WP6_NEGATIVE_DOCUMENTARY_VECTORS.md` | Independent constitutional review **and** an independent serialization/numerical review; independent confirmation, unresolved findings `NONE` (frozen RC2 §12.4, §12.5 point 6) | `M44-WP7` may begin |
| `G-5` second half | Portfolio Intelligence normative result-contract authority; frozen RC2 §8.6 C6 | `docs/implementation/M43_WP5_PORTFOLIO_MEASURE_RESULT_CONTRACT_SPECIFICATION.md`; `m44/fixtures/M44_WP7_POSITIVE_DOCUMENTARY_VECTORS.md`; `m44/fixtures/M44_WP7_NEGATIVE_DOCUMENTARY_VECTORS.md` | Independent constitutional review **and** an independent serialization/numerical review; independent confirmation, unresolved findings `NONE` (frozen RC2 §12.5 point 7) | `D-1` becomes reachable, and transitively `D-2a`, `D-2b`, `D-3`, `D-4` under their own prerequisites |

**Closure-matrix rules.**

1. No gate is released by an artifact other than the closure artifact named in
   its row.
2. No confirmation requirement may be satisfied by the artifact's own author
   acting as sole reviewer (frozen RC2 §12.4, §16.4).
3. A release column entry is contingent on the **closing** terminal state named
   in §4 for that gate. A non-closure terminal state releases nothing, and no
   artifact may report a release on the strength of a recorded blockage, a
   routing, a requirement specification, or a successor obligation (frozen RC2
   §16.2).

---

## 8. Admissible terminal states

### 8.1 The closed vocabulary

Consumed verbatim from frozen RC2 §16.2. This register neither extends nor
narrows it.

| Terminal state | Meaning | Counts as closure |
| --- | --- | --- |
| `CLOSED` | The obligation is fully discharged; every element the frozen authority requires is present | Yes |
| `RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE` | The frozen release condition is discharged; a separate recording obligation remains outstanding with its vehicle named | No |
| `OPEN` | The obligation is not discharged; the exact missing element and its exact owner are named | No |
| `OPEN — PARTIAL` | Some constituents are discharged and at least one is not; the frozen authority admits no partial form | No |
| `DEFERRED` | Allocated to a named successor obligation with a stated prerequisite | No |

Per-gate admissibility, restated from §4 for checking:

| Gate | Admissible | Expressly prohibited | Basis |
| --- | --- | --- | --- |
| `G-1` | `CLOSED`; residually `OPEN` | `RELEASED — …`, `OPEN — PARTIAL`, `DEFERRED` | frozen RC2 §11 M44-WP2 |
| `G-2` | `RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE`; residually `OPEN` | `CLOSED` — expressly, while no authorized step 4 vehicle exists | frozen RC2 §11 M44-WP3, §12.6, §17 OQ-5 |
| `G-3` | `CLOSED` **or** `OPEN — PARTIAL`, never both | any third state; any blend | frozen RC2 §3.1 G-3, §11 M44-WP4 |
| `G-4` | `CLOSED` **or** `OPEN` | any third state | frozen RC2 §3.1 G-4, §11 M44-WP5 |
| `G-5` | `CLOSED` **or** `OPEN` | — | frozen RC2 §13.1, §11 M44-WP6/WP7 |

### 8.2 Referred question — not decided by this register

**`RQ-1` — the asymmetric `G-5` case.** Frozen RC2 names the `G-5` `OPEN` case
only for the situation in which the §12.1.1 checkpoint withholds both `M44-WP6`
and `M44-WP7` (§13.1). It does not name the state of `G-5` where exactly one of
its two halves is confirmed and frozen and the other is not. Because `G-5` is a
two-constituent gate, §16.2's definition of `OPEN — PARTIAL` is textually
available, while §13.1's instruction names `OPEN`.

This register **does not decide** `RQ-1`. Deciding it would be a gate
disposition, which frozen RC2 §8.7 withholds from `M44-WP1`. It is recorded here
under frozen RC2 INV-B2 so that it cannot be resolved silently, and it is
referred to the §12.1.1 checkpoint confirmation and the M44 epic closeout, which
hold the authority to record terminal states. `RQ-1` gates no work package: the
strict `M44-WP6` → `M44-WP7` ordering in frozen RC2 §12.3 makes the asymmetric
case reachable only through a withheld or failed `M44-WP7`, which is itself a
recorded event.

### 8.3 Prohibited reporting patterns

Restated from frozen RC2 §16.2, §12.7 step 2, §19, and R-14, and binding on
every M44 artifact that inherits this register:

- A recorded blockage is **never** a gate closure.
- An `OPEN` or `OPEN — PARTIAL` gate is **never** reported as a closure.
- A routing of an obligation to its owner **records** the obligation; it never
  discharges it.
- A requirement specification is **never** the instrument it specifies.
- A successor obligation is **never** a discharge.
- A partial discharge is **never** continued past (frozen RC2 §12.1.1).

---

## 9. Repository Evidence Inventory

Every artifact consumed by this register, with the exact material consumed and
its verified resolution as of 2026-07-29. No interpretation beyond frozen
evidence is applied, and no artifact below is modified.

### 9.1 Frozen governing architecture (M44)

| Path | Material consumed | Resolves |
| --- | --- | --- |
| [M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) | §1.1–1.7 authority and revision provenance; §3.1 gates `G-1`–`G-5`; §4.1 included capabilities; §4.3 deferred set; §4.5 successor obligations; §5.1 owned surfaces; §5.3 extension bases E-1/E-2/E-3; §6 invariants (INV-A3, INV-B2, INV-C1, INV-C4, INV-F1, INV-O3); §7.2 downstream consumers; §8.1–8.7 components C0–C6; §9.2–9.3 contracts; §10 failure behavior; §11 work packages and §11.1 graph; §12.1–12.7 roadmap and checkpoint; §13.1 file forecast; §16.2 terminal-state vocabulary; §17 OQ-1 to OQ-5; §19 | `YES` |
| [M44_ARCHITECTURE_FREEZE_RECORD.md](M44_ARCHITECTURE_FREEZE_RECORD.md) | §1 gate table; §2 lifecycle; §2.1 filing divergence and the authorization precondition; §3.3 authority ceilings; §6.1 work-package states; §6.2 undispositioned gates; §6.3 deferred obligations; §6.4 open questions; §9 freeze declaration; §10 exclusions | `YES` |
| [M44_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md](M44_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md) | Findings 1–6 `PASS`; Constitutional, Repository, and Authority Compatibility `PASS`; `APPROVED FOR FREEZE` | `YES` (cited at RC1 as `M44_INDEPENDENT_CONFIRMATION.md`, a non-conforming path since remediated — see §3.1) |
| [M44_ARCHITECTURE_CONSTITUTIONAL_ADJUDICATION.md](M44_ARCHITECTURE_CONSTITUTIONAL_ADJUDICATION.md) | Binding dispositions of Findings 1–6, as summarized in frozen RC2 §1.7 | `YES` (cited at RC1 as `M44_CONSTITUTIONAL_ADJUDICATION.md`) |
| [M44_ARCHITECTURE_FORMAL_CONSTITUTIONAL_RESPONSE.md](M44_ARCHITECTURE_FORMAL_CONSTITUTIONAL_RESPONSE.md) | Review-history provenance only | `YES` (cited at RC1 as `M44_FORMAL_CONSTITUTIONAL_RESPONSE.md`) |
| [M44_ARCHITECTURE_INDEPENDENT_REVIEW.md](M44_ARCHITECTURE_INDEPENDENT_REVIEW.md) | Review-history provenance only | `YES` (cited at RC1 as `M44_INDEPENDENT_CONSTITUTIONAL_REVIEW.md`) |

### 9.2 Frozen M43 corpus

| Path | Material consumed | Resolves |
| --- | --- | --- |
| [M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md](M43_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) | Header line 3 status; §8 subsystem-ownership table line 174 (canonical period-return row); §9 WP1–WP9 allocation, including the M43-WP9 row | `YES` |
| [M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md) | §1 confirmation-record obligation; §7.1 candidate tested; §7.2 governing evidence; §7.3 the ownership split; §7.4 the standing block, the four-step correction path, and the release condition; §8 duplication controls; downstream vocabulary rule | `YES` |
| [M43_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md](M43_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md) | §2 roadmap non-marking convention; §4 legacy dispositions; §5 negative corpus (23 prohibited statements) — consumed as the controlling precedent for the M44 reconciliation deliverable | `YES` |
| [M43_WP2_PORTFOLIO_MEASURE_DEFINITION_METHOD_VERSION_AND_APPLICABILITY_CONTRACT_SPECIFICATION.md](M43_WP2_PORTFOLIO_MEASURE_DEFINITION_METHOD_VERSION_AND_APPLICABILITY_CONTRACT_SPECIFICATION.md) | §8.1 the "exact *existing* governed contract kind" predicate; §8.2 dependency closure | `YES` |
| [M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md](M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md) | §7.1 the representability failure and the "separately authorized contract" remedy; §7.2 `PMS1` framing (`ASCII`, `u32`, `lp(x)`, embedded `lp(portfolio_composition_canonical_bytes)`); §7.3 identity and order | `YES` |
| [M43_WP3_PORTFOLIO_ANALYTICS_INPUT_MANIFEST_CONTRACT_SPECIFICATION.md](M43_WP3_PORTFOLIO_ANALYTICS_INPUT_MANIFEST_CONTRACT_SPECIFICATION.md) | §6.3 `PORTFOLIO_COMPOSITION` entry rules and the unformable-manifest statement; §10.3 canonical serialization | `YES` |
| [M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md](M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) | §5.2 prohibition on an authored dependency kind; §6.6 Component F risk-free evidence; §6.7 Component G annualization; §6.8–6.11 Components H–K; §7 no-default matrix | `YES` |
| [M43_WP5_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md](M43_WP5_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) | §0 the twelve required result closures; §§3, 5–10, 13 acceptance criteria | `YES` |
| [M43_WP6_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md](M43_WP6_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) | §3.1 hard dependencies; §3.2 entry gates 1–7, the two binding-source paths, the "Neither specification is present" statement, and the Composition and annualization representability gates | `YES` |
| [M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md](M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) | §3.1 the two required binding-source paths and the "not a substitute" rule; §3.2 inherited external gates 1–10; §5.1 closed inherited vocabulary; §11.3 vector authority | `YES` |
| [M43_WP8_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md](M43_WP8_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) | §2 dependency and ownership model; §4 validation summary and the `BLOCKED PENDING INHERITED GATE CLOSURE` record | `YES` |
| [M43_EPIC_CLOSEOUT.md](M43_EPIC_CLOSEOUT.md) | §1 "This closeout does not close an inherited gate and grants no additional authority"; §2 repository synchronization and the preserved-labels statement | `YES` |

### 9.3 Frozen M42 corpus

| Path | Material consumed | Resolves |
| --- | --- | --- |
| [M42_WP7_PORTFOLIO_COMPOSITION_CONTRACT_SPECIFICATION.md](M42_WP7_PORTFOLIO_COMPOSITION_CONTRACT_SPECIFICATION.md) | §3 admissible coordinates and their owners; §5 tag, ten-element canonical semantic field order, conditional canonical-byte permission, exclusion of encoding, preserved obligation, and the nested-coordinate limit; §8 vectors `PC-NGV-11`–`PC-NGV-14`; §9 conformance checklist items 1, 10, 11, 12 | `YES` |
| [M42_WP2_PORTFOLIO_IDENTITY_ACCOUNTING_SCOPE_MEMBERSHIP_AND_BASE_CURRENCY_CONTRACT_SPECIFICATION.md](M42_WP2_PORTFOLIO_IDENTITY_ACCOUNTING_SCOPE_MEMBERSHIP_AND_BASE_CURRENCY_CONTRACT_SPECIFICATION.md) | Coordinate identity — cited as a `G-3` coordinate-owner reference only | `YES` |
| [M42_WP3_STAGE_B_INVESTMENT_UNIVERSE_DECLARATION_CONTRACT_SPECIFICATION.md](M42_WP3_STAGE_B_INVESTMENT_UNIVERSE_DECLARATION_CONTRACT_SPECIFICATION.md) | Investment Universe Declaration — coordinate-owner reference only | `YES` |
| [M42_WP5_PORTFOLIO_BENCHMARK_DECLARATION_CONTRACT_SPECIFICATION.md](M42_WP5_PORTFOLIO_BENCHMARK_DECLARATION_CONTRACT_SPECIFICATION.md) | Portfolio Benchmark Declaration including `Explicitly None`; `Composite`/`Category` unavailability feeding `D-6` | `YES` |
| [M42_WP6_PORTFOLIO_LIFECYCLE_STATE_REUSE_AND_PROVENANCE_CONTRACT_SPECIFICATION.md](M42_WP6_PORTFOLIO_LIFECYCLE_STATE_REUSE_AND_PROVENANCE_CONTRACT_SPECIFICATION.md) | Portfolio Lifecycle State; Provenance carriage — coordinate-owner reference only | `YES` |

### 9.4 Constitutional and domain authorities

| Path | Material consumed | Resolves |
| --- | --- | --- |
| [platform_architecture.md](../architecture/platform_architecture.md) | §5 platform layers; §6.1–6.9 domain allocations, in particular §6.2 Market Intelligence, §6.3 Ledger & Accounting, §6.5 Portfolio Intelligence; §7 relationships and the three gates; §8 cross-cutting principles; §11 governance precedence; §12 canonical vocabulary | `YES` |
| [PORTFOLIO_CALCULATION_RULES.md](../investment/PORTFOLIO_CALCULATION_RULES.md) | §§1–9 accounting semantics; §10 consumption rule; §12 open questions, recorded as expressly outside M44 | `YES` |
| [OPTIMIZER_PHILOSOPHY.md](../investment/OPTIMIZER_PHILOSOPHY.md) | Consulted as a level-2 Domain Constitution; no M44-WP1 material derives from it | `YES` |
| [ENGINEERING_PRINCIPLES.md](../engineering/ENGINEERING_PRINCIPLES.md) | Consulted; no gate derives from it | `YES` |
| [DECISION_LOG.md](../engineering/DECISION_LOG.md) | The M43 epic closeout entry, consumed as the reconciliation source for `G-1` and as the lapsed step 4 vehicle for `G-2` | `YES` |

### 9.5 Absence evidence

The following paths are asserted **absent**, and their absence is itself the
constitutional evidence for `G-1` and `G-5`. Verified by directory enumeration
of `docs/implementation/` on 2026-07-29.

| Path | State | Gate it evidences |
| --- | --- | --- |
| `docs/implementation/M43_ARCHITECTURE_INDEPENDENT_*` (any) | `ABSENT` | `G-1` |
| `docs/implementation/M43_WP4_TEMPORAL_CURRENCY_CALENDAR_BENCHMARK_AND_ARITHMETIC_SEMANTICS_CONTRACT_SPECIFICATION.md` | `ABSENT` | `G-5`, first half |
| `docs/implementation/M43_WP5_PORTFOLIO_MEASURE_RESULT_CONTRACT_SPECIFICATION.md` | `ABSENT` | `G-5`, second half |
| Any separately authorized Portfolio Composition canonical-byte contract | `ABSENT` | `G-3` |
| Any annualization-basis governed dependency instrument, at any path | `ABSENT` | `G-4` |
| Any M43-WP9 artifact | `ABSENT` | §5.4, `D-4` |

**Superseded absence row (RC1 → RC2).** RC1 of this table carried one further
row: `docs/implementation/M44_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md` —
`ABSENT` (content exists at a different path) — evidencing the §3 authorization
precondition `P-1`. That path now **resolves** (§3.1), so the row is no longer
absence evidence and is withdrawn from the table. The RC1 entry is restated here
verbatim so the withdrawal is visible rather than silent. The absences
evidencing `G-1`, `G-3`, `G-4`, and `G-5` are unaffected and unchanged.

### 9.6 Evidence not consulted, and why

- `docs/FUTURE_EXPERIMENTS.md`, `docs/archive/`, `docs/debug-notes/` — not
  authoritative project knowledge for a constitutional register.
- `backend/`, `frontend/`, `scripts/`, and all configuration — current-state
  evidence under constitution G6 only, carrying no constitutional authority. No
  gate in §4 rests on any of them, and none is modified.
- `docs/architecture/ROADMAP.md` — read for position only; not modified, and no
  capability-completion mark is made or implied (frozen RC2 §3.3, §4.2).

---

## 10. Completion Criteria for M44-WP1

M44-WP1 completes when, and only when, every criterion below is objectively
satisfied. Each is stated so a reviewer can falsify it against repository
evidence.

### 10.1 Deliverable completeness

| # | Criterion | State at register date |
| --- | --- | --- |
| `C-01` | `docs/implementation/M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md` exists at the path frozen RC2 §11 and §13.1 declare | `MET` by this artifact |
| `C-02` | `docs/implementation/M44_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md` exists at the path frozen RC2 §11 and §13.1 declare | `NOT MET` — see §10.5 |
| `C-03` | The nested-coordinate encoding-obligation pre-inventory feeding `M44-WP4` exists, is cited, and is the deciding evidence for frozen RC2 §17 `OQ-1` | `NOT MET` — see §10.5 |

### 10.2 Register completeness and traceability

| # | Criterion | State |
| --- | --- | --- |
| `C-04` | Every gate named in any frozen M43 artifact appears in this register exactly once | `MET` — §5.1 (10 of 10), §5.2 (7 entry gates + 2 prose gates), §5.3 (3 statements) |
| `C-05` | Every gate carries exactly one disposition, `CLOSED BY M44-WPn` or `DEFERRED TO D-n` | `MET` — §4.0, §5.1–5.3 |
| `C-06` | No gate is unassigned, and no gate is assigned to two work packages | `MET` — §6.1 |
| `C-07` | Every gate carries all ten required register fields | `MET` — §4.1–4.5 |
| `C-08` | Every cited path and section resolves, and says what the citation claims (citation-existence check) | `MET` for every citation in §9; re-verification is a review obligation |
| `C-09` | Every asserted absence in §9.5 is verified by enumeration, not by inference | `MET` — verified 2026-07-29 |
| `C-10` | Every gate's permitted terminal states are drawn only from the frozen RC2 §16.2 closed vocabulary, and each restriction is cited to frozen text | `MET` — §4, §8.1 |
| `C-11` | The frozen M43-WP9 allocation is recorded as deferred-with-owner-unassigned, with no milestone number assigned (frozen RC2 §17 `OQ-4`) | `MET` — §5.4 |
| `C-12` | The §12.1.1 checkpoint is recorded as the register's own carrying obligation, so its outcome can be recorded here and carried into the epic closeout (frozen RC2 §12.1.1) | `MET` — §6.2, §12 |
| `C-13` | Collision and overlap scan: no gate identifier, disposition, or deferred-obligation identifier collides with, or silently redefines, one used by a frozen artifact | `MET` — identifiers `G-1`–`G-5` and `D-1`–`D-7` are consumed from frozen RC2, not minted here |

### 10.3 Constitutional consistency

| # | Criterion | State |
| --- | --- | --- |
| `C-14` | No gate is dispositioned; every terminal-state field reads `NOT YET DISPOSITIONED` | `MET` — §4.0 |
| `C-15` | No owner of any semantic concern is determined, proposed, or implied | `MET` — §1.2 |
| `C-16` | No encoding, formula, method, or method version is selected or constrained | `MET` — §1.2 |
| `C-17` | No new constitutional noun is required, or each required noun has entered the frozen M43-WP1 downstream vocabulary gate | `MET` — §11 records that none is required |
| `C-18` | Every authority class in the header is declared `NONE` (frozen RC2 INV-A1) | `MET` |
| `C-19` | No authority is asserted that frozen RC2 withheld (INV-A2), and every statement traces to an exact citation | `MET` — §1.3 is the only interpretive statement, and it is grounded in frozen RC2 §11 and §16.2 |
| `C-20` | No frozen M1–M43 artifact and no frozen M44 artifact is modified; `git diff` contains no frozen path (INV-C1) | `MET` — this register creates one new file |
| `C-21` | No contract kind is authored, registered, extended, versioned, or serialized in any domain's corpus (INV-C4) | `MET` |
| `C-22` | No milestone number is assigned to any successor obligation (frozen RC2 §4.5) | `MET` — §5.4, §5.5 |
| `C-23` | Every open gate is named and cited by exact path and section (INV-B2), including the §3 authorization precondition and `RQ-1` | `MET` — §3, §4, §8.2 |
| `C-24` | No blockage, routing, requirement specification, or successor obligation is reported as a closure (frozen RC2 §16.2, R-14) | `MET` — §8.3 |

### 10.4 Governance completeness

| # | Criterion | State |
| --- | --- | --- |
| `C-25` | The frozen Freeze Record §2.1 filing remediation (`P-1`) is performed, so the M44 confirmation resolves at the path frozen RC2 §1.1 declares | `MET` — performed by rename outside M44-WP1 after RC1; verified by directory enumeration at §3.1. `NOT MET` at RC1 |
| `C-26` | This register receives an independent constitutional review by a reviewer who did not author it (frozen RC2 §12.4, §16.4) | `MET` — review received, determination `APPROVED WITH MINOR CORRECTIONS`, one finding. `NOT MET` at RC1 |
| `C-27` | Every finding from that review is answered by a corrections response, and every correction is re-reviewed | `NOT MET` — the single finding is answered by the [Formal Constitutional Response](M44_WP1_FORMAL_CONSTITUTIONAL_RESPONSE.md) and applied at RC2 (§15); **re-review of the correction is outstanding** |
| `C-28` | Independent confirmation is recorded with unresolved findings `NONE` (frozen RC2 §12.5 point 2) — `P-2` | `NOT MET` |
| `C-29` | No repository governance record — Decision Log, Implementation INDEX, GLOSSARY, ROADMAP — is synchronized by this work package; synchronization is a single act at epic closeout under separate authorization (frozen RC2 §12.6) | `MET` — none is modified |

### 10.5 Explicitly outstanding at this register's date

M44-WP1 is **not complete**. Two frozen scope items remain undelivered, and both
are named here rather than absorbed, deferred, or silently dropped:

| Outstanding item | Frozen allocation | Consequence if not delivered |
| --- | --- | --- |
| `M44_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md` | frozen RC2 §11 M44-WP1 architectural deliverables; §13.1 | `C-02` cannot be met; M44-WP1 cannot be confirmed; no downstream M44 work package may begin |
| Nested-coordinate encoding-obligation pre-inventory feeding `M44-WP4` | frozen RC2 §11 M44-WP1 included scope; §15 R-2 mitigation; §17 `OQ-1` "The WP1 pre-inventory is the deciding evidence" | `C-03` cannot be met; `M44-WP4` would begin without the evidence frozen RC2 designates as deciding for `OQ-1`, and the §12.1.1 checkpoint would lack its basis |

Neither item is attempted in this artifact, which is scoped to the gate register.
Recording them as outstanding is required by frozen RC2 INV-B2 and §16.2; it is
not a deferral, and neither may be treated as discharged.

---

## 11. Vocabulary-sufficiency finding

Frozen RC2 §9.7 requires that if any M44 work package proves an unavoidable new
noun, it must run the frozen M43-WP1 downstream vocabulary rule before any
reliance.

**Finding:** this register requires **no** new constitutional noun.

Every term it relies on is already disposed by a frozen artifact: the Portfolio
Analytics nouns admitted by frozen M43-WP1 §§4–5 and restated in frozen M43-WP7
§5.1; the M42 coordinate nouns; `Degraded State` and `Canonical Temporal Claim`
under `M34-D-0005`; the gate identifiers `G-1`–`G-5`, the deferred-obligation
identifiers `D-1`–`D-7`, the component identifiers `C0`–`C6`, the extension
bases `E-1`–`E-3`, and the five terminal states, all consumed from frozen RC2.

The identifiers `P-1`, `P-2`, `RQ-1`, and `C-01`–`C-29` introduced in this
register are **document-local labels for register mechanics**, not
constitutional nouns: they name no semantic concern, allocate no ownership,
carry no authority, and are scoped to this artifact. They do not enter
`docs/GLOSSARY.md`, and `docs/GLOSSARY.md` is not modified.

---

## 12. Checkpoint-outcome carrier

Frozen RC2 §12.1.1 states that the gate-state checkpoint outcome "is recorded in
the M44-WP1 closure register and carried into the epic closeout," and that "no
work package may declare the checkpoint satisfied on its own authority."

This section is that carrier. It is reserved and currently unpopulated.

| Field | Value at register date |
| --- | --- |
| Observed `G-3` terminal state | `OPEN — PARTIAL` |
| Observed `G-4` terminal state | `OPEN` |
| Checkpoint outcome | `STOP` |
| Independent checkpoint confirmation | `CONFIRMED` — unresolved findings `NONE` |
| Recorded by | Independent §12.1.1 gate-state checkpoint confirmation under frozen RC2 §12.5 point 5, 2026-07-30 |

Populating this table requires the independent confirmation named at frozen RC2
§12.5 point 5. It is not populated by `M44-WP4`, `M44-WP5`, or this register
acting alone.

**Carrier population — additive record, 2026-07-30.** The five values above were
written by the independent §12.1.1 gate-state checkpoint confirmation required by
frozen RC2 §12.5 point 5, performed by a confirmer distinct from the author of the
checkpoint disposition. They are the confirmed terminal states and outcome as of
that confirmation date. The column heading "Value at register date" and the
sentence "It is reserved and currently unpopulated." above describe this carrier's
pre-population state at the register's own date; as to this carrier only, both are
superseded by this additive record, and neither is edited — in keeping with the
repository convention that a superseded in-file statement in a frozen artifact is
corrected by an additive record and never by amendment (frozen
[M44_WP1_FREEZE_RECORD.md](M44_WP1_FREEZE_RECORD.md) §7.3; frozen RC2 §1.6 rule 3).
No other statement, section, or table in this register is altered, superseded, or
reinterpreted.

Exact evidence basis:

- `G-3` `OPEN — PARTIAL` — frozen
  [M44_WP4_FREEZE_RECORD.md](M44_WP4_FREEZE_RECORD.md) §5 "Final Freeze Status" and
  §6, blob `8623bbdabbb4fd35318e125173cd99c48ffd9c2e`; underlying determination
  frozen
  [M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md](M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md)
  §10 `WP4-NR-030`; the eight unsupplied elements and their exact frozen owning
  domains are recorded at that contract's §3.3, which states "This map is a record,
  not a request." They are recorded open elements, not requests to those owners and
  not obligations imposed on them (frozen RC2 `INV-C4`, §4.5).
- `G-4` `OPEN` — frozen [M44_WP5_FREEZE_RECORD.md](M44_WP5_FREEZE_RECORD.md) §5
  "Effective frozen determination" and §10, blob
  `1dc63389227cfb323820fe774554fb810eb389ef`; owning domain `MARKET INTELLIGENCE`,
  effective and frozen; missing element named there.
- Checkpoint outcome `STOP` — frozen RC2 §12.1.1 second row, applied to the two
  established states above; frozen RC2 §12.3, under which `G-3 OPEN — PARTIAL` is a
  prerequisite failure for M44-WP6 and M44-WP7 "without exception" while `G-4 OPEN`
  is expressly not a prerequisite failure. The outcome turns on `G-3` alone.
- Confirmed disposition —
  [M44_GATE_STATE_CHECKPOINT_DISPOSITION.md](M44_GATE_STATE_CHECKPOINT_DISPOSITION.md).
  Per the repository convention above, that record's own header and §11 continue to
  read as authored, before confirmation; this carrier is the record of the
  confirmation act, exactly as frozen RC2 §12.1.1 directs.

Downstream consequence, recorded under frozen RC2 §16.5 with this checkpoint
outcome cited as cause:

| Downstream item | State |
| --- | --- |
| `M44-WP6` | `NOT REACHED — WITHHELD BY CHECKPOINT` |
| `M44-WP7` | `NOT REACHED — WITHHELD BY CHECKPOINT` |

`G-5` remains `OPEN` with the checkpoint outcome as its cause (frozen RC2 §13.1).
The referred question `RQ-1` (§8.2) is not decided here; it remains referred to the
M44 epic closeout.

Neither `G-3` nor `G-4` is closed, released, deferred, or reinterpreted by this
population. `OPEN — PARTIAL` and `OPEN` are non-closure states under frozen RC2
§16.2 and §8.1 of this register. This population authorizes no work package to
begin, authors no architecture re-scope, and does not author or perform the M44
Epic Closeout.

---

## 13. Validation performed on this register

| Check | Result | Evidence |
| --- | --- | --- |
| Gate closed, released, deferred, or otherwise dispositioned by this artifact | `NONE` | §4.0 terminal-state column; §1.2 |
| Gate omitted from the inventory | `NONE FOUND` | §5.1 covers 10 of 10 frozen M43-WP7 §3.2 gates; §5.2 covers 7 entry gates plus 2 prose gates; §5.3 covers 3 M43-WP8 §4 statements; §5.4 covers the M43-WP9 allocation |
| Gate duplicated or double-allocated | `NONE FOUND` | §6.1; each gate maps to exactly one work package, `G-5`'s two halves to two distinct work packages |
| Disposition without a frozen basis | `NONE FOUND` | Every disposition in §4 and §5 cites the frozen sentence that creates the obligation |
| Terminal state invented outside frozen RC2 §16.2 | `NONE FOUND` | §8.1 reproduces the closed vocabulary; §8.2 refers rather than decides the one unnamed case |
| Authority asserted beyond frozen RC2 §8.7 C0 | `NONE FOUND` | Header declarations; §1.2; §1.3 |
| Ownership determined or implied | `NONE FOUND` | §1.2; coordinate owners in §4.3 are quoted from frozen M42-WP7 §3, not determined here |
| Frozen artifact modified | `NONE` | One new file created; no frozen path written |
| New constitutional noun introduced | `NONE` | §11 |
| Milestone number assigned to a successor | `NONE` | §5.4, §5.5 |
| Contract kind authored or registered in any domain's corpus | `NONE` | §1.2, `C-21` |
| Repository governance record synchronized prematurely | `NONE` | `C-29`; frozen RC2 §12.6 |
| Blockage reported as closure | `NONE FOUND` | §8.3; §10.5 reports outstanding items as outstanding |
| Circular dependency among gates or work packages | `NONE FOUND` | §6.2, §6.3; consistent with frozen RC2 §11.1 |
| Citation that does not resolve | `NONE FOUND` | §9.1–9.4 verified at RC1 and re-verified at RC2 after the filing remediation, 2026-07-29; §9.5 records verified absences |
| Open obligation left unnamed | `NONE FOUND` | §3 (`P-1`, since satisfied; `P-2` outstanding), §8.2 (`RQ-1`), §10.5 (two outstanding WP1 items at RC1) |

---

## 14. Final constitutional boundary

This register is the authoritative inherited-gate inventory for M44. It records
five gates, their exact frozen provenance, the repository evidence that leaves
each undischarged, the single instrument responsible for each, the dependencies
among them, and the terminal states each may lawfully reach.

It closes nothing. It releases nothing. It determines no owner, selects no
encoding, admits no noun, and authorizes no work package to begin. Every gate it
names remains `NOT YET DISPOSITIONED`, and every obligation it cannot discharge —
the frozen Freeze Record §2.1 filing remediation (named at RC1, performed
afterwards outside M44-WP1, recorded at §3.1), the two undelivered M44-WP1 scope
items, and the referred question `RQ-1` — is named in place rather than absorbed
or assumed.

M44-WP1 completes when the criteria in §10 are all met. They are not all met at
this register's date, and this artifact says so rather than claiming otherwise.

---

## 15. Correction record — RC1 → RC2

This section exists so that the difference between RC1 and RC2 is auditable
without recourse to version control, and so that no corrected statement can be
mistaken for an original one.

### 15.1 Occasion

Independent constitutional review of M44-WP1 returned `APPROVED WITH MINOR
CORRECTIONS`, with exactly one finding: several review-chain citations in this
register still referenced the superseded `M44_*` filings after the repository
filing remediation had been completed. The finding is answered by the
[M44-WP1 Formal Constitutional Response](M44_WP1_FORMAL_CONSTITUTIONAL_RESPONSE.md),
which authorizes this revision and no other change.

### 15.2 Corrections applied

| # | Location | Correction | Class |
| --- | --- | --- | --- |
| 1 | Header | `RC1` → `RC2`; revision line added, citing the authorizing response | Status label |
| 2 | §3 heading | "recorded, not resolved" → "recorded, and subsequently remediated" | Current state |
| 3 | §3.1 | RC1 divergence table retained verbatim as the historical record; post-remediation verification table added; the four required paths re-pointed and confirmed to resolve | Citation integrity |
| 4 | §3.2 | `P-1` marked `SATISFIED`, `P-2` marked `OUTSTANDING`; the `NON-EFFECTIVE` conclusion restated and **unchanged** | Current state |
| 5 | §9.1, four rows | `M44_INDEPENDENT_CONFIRMATION.md`, `M44_CONSTITUTIONAL_ADJUDICATION.md`, `M44_FORMAL_CONSTITUTIONAL_RESPONSE.md`, `M44_INDEPENDENT_CONSTITUTIONAL_REVIEW.md` re-pointed to their `M44_ARCHITECTURE_*` paths; each row records the RC1 citation it replaces | Citation integrity |
| 6 | §9.5 | The `M44_ARCHITECTURE_INDEPENDENT_CONFIRMATION.md` `ABSENT` row withdrawn, the path now resolving; the withdrawn row restated verbatim beneath the table | Current state |
| 7 | §10.4 `C-25` | `NOT MET` → `MET`, with the RC1 state preserved in the cell | Current state |
| 8 | §13 | Citation-resolution and open-obligation rows updated to record RC2 re-verification and the satisfied `P-1` | Current state |
| 9 | §14 | The filing-remediation clause updated to record that the obligation named at RC1 was performed afterwards, outside M44-WP1 | Current state |
| 10 | §10.4 `C-26`, `C-27` | Updated to record that the independent review occurred and that its single finding is answered; `C-27` held `NOT MET` because re-review of the correction is outstanding. Consequential to the review's own occurrence, not a new finding | Current state |
| 11 | §15 | This correction record added | Additive record |

### 15.3 What RC2 does not change

| Preserved | Verification |
| --- | --- |
| Constitutional meaning | No sentence of §§1–2, §4–§8, §11, §12, §14 reasoning is rewritten |
| Authority | Every header authority class remains `NONE`; no class is added, widened, or narrowed |
| Gate inventory | `G-1`–`G-5` unchanged in identity, statement, provenance, evidence, closure authority, owning work package, dependency, and permitted terminal states |
| Dispositions | Every disposition in §4.0, §5.1–5.5, and §7 is byte-identical to RC1 |
| Terminal states | Every terminal-state field still reads `NOT YET DISPOSITIONED`; §8.1 vocabulary untouched |
| Repository evidence | No evidence claim is added or withdrawn except the one absence that ceased to exist by remediation, recorded at §9.5 |
| Deferred obligations | `D-1`–`D-7` unchanged; no milestone number assigned |
| Referred question | `RQ-1` unchanged and still undecided |
| Effectiveness | The register remains `NON-EFFECTIVE` pending `P-2` |
| Frozen artifacts | None modified; `git diff` contains no frozen path |

### 15.4 Boundary of this revision

RC2 repairs citation integrity and the `P-1` / `C-25` current-state records. It
dispositions no gate, performs no confirmation, and authorizes no work package
to begin. `C-26` is met by the review that occasioned it. `C-27` remains
`NOT MET`: the finding is answered and the correction applied, but the
correction has not been re-reviewed. `C-28` remains `NOT MET`. M44-WP1 is
therefore `RC2 — CORRECTED, NOT CONFIRMED`.
