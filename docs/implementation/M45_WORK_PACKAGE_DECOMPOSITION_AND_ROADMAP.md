# M45 — Work-Package Decomposition and Roadmap

**Milestone label:** M45 — prospective; allocation not yet evidenced
**Artifact class:** Work-package roadmap planning candidate
**Status:** `PLANNING CANDIDATE — NOT RATIFIED`
**Review state:** `CORRECTIONS REQUIRED`; N-1 through N-3 independently resolved; N-4 correction prepared for third focused re-review
**Normative specification authority:** `NONE`
**Implementation authority:** `NONE`
**Runtime authority:** `NONE`
**Source-code authority:** `NONE`
**Persistence/schema/migration authority:** `NONE`
**API/transport/UI authority:** `NONE`
**Provider-selection authority:** `NONE`
**Frozen-artifact amendment authority:** `NONE`
**Cross-domain authority:** `NONE`
**Gate-disposition authority:** `NONE`
**Ownership-determination authority:** `NONE`
**Vocabulary-admission authority:** `NONE`
**Contract authoring/registration/extension/versioning authority:** `NONE`
**Executable-validation authority:** `NONE`
**Production-method authority:** `NONE`

This file and
[M45_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md](M45_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
form one candidate planning corpus. Both require the same review,
confirmation, ratification, identity validation, and freeze acts. Presently
neither is ratified and no M45 work package is authorized.

---

## 0. Interpretation and universal lifecycle

- **`[NORMATIVE IF RATIFIED]`** is proposed future governance.
- **`[INFORMATIVE]`** is guidance only.
- “Implementation sequence” below means documentary work, never code or
  runtime implementation.

**`[NORMATIVE IF RATIFIED]`** Every M45-owned substantive artifact shall follow:

`DRAFT` → `REVIEW CANDIDATE` → independent review → correction by additive
candidate revision if required → focused re-review → `CONFIRMED` → exact
content-identity validation → `FROZEN`.

No freeze may precede independent confirmation. A post-freeze defect requires
an additive successor `RCn`, its own focused review, confirmation, identity,
and freeze. A downstream WP consumes the latest applicable frozen revision and
re-verifies cited identities.

The architecture lifecycle before WP1 is defined in the paired architecture
§4.2. Review approval does not ratify the planning corpus, ratification does
not authorize WP1, and no actor may determine or grant its own authority.

---

## 1. External predecessor conditions — not M45 work packages

The following receive no M45 identifiers:

| Condition | Acceptance evidence | M45 action if present | M45 action if absent or defective |
| --- | --- | --- | --- |
| Milestone allocation, lifecycle actors, ratification, joint architecture freeze, WP1 authorization | Exact competent records | Verify and cite | Remain blocked |
| Ledger & Accounting canonical forms | Competent owner; independent authority; immutable identity; reviewed, confirmed, frozen lifecycle; exact forms; sufficient G-3 coverage | Receive, verify, cite, preserve | Record absence and stop |
| Asset Foundation canonical forms | Same, including `asset_id` and Base Currency denomination dimension | Receive, verify, cite, preserve | Record absence and stop |
| Connectivity & Ingestion Provenance form | Same, including content, boundary, sequence, completeness | Receive, verify, cite, preserve | Record absence and stop |
| Separately authorized Portfolio Intelligence nested-form artifact | Exact governed artifact class and authority; M42 non-conflict; independent review, confirmation, freeze | Receive, verify, cite, preserve | Preserve `WP4-NR-032`; stop |
| Competent G-2 recording vehicle, if one exists | Authority that settles `OQ-5` and expressly authorizes the Decision Log act | WP7 may synchronize confirmed truth | Leave G-2 outstanding |
| Substantive M45-WP5 authorization stage | Separately competent authority not identified by this candidate; frozen WP3 intended-branch evidence; content-identified `M45-WP5 substantive-work authorization record` | WP4 verifies exactly `WP5 SUBSTANTIVE WORK AUTHORIZED`; it does not treat the result as checkpoint or entry verification | WP4 verifies `WP5 SUBSTANTIVE WORK NOT AUTHORIZED` or confirmed absence in bounded mode, produces and freezes the WP5-entry blocked determination through its own lifecycle, leaves WP5 unstarted, and routes canonical TB-4 to WP7 |

M45 cannot request, commission, schedule, govern, review, confirm, correct, or
freeze these external acts. Routing is a record, not a request.

The substantive-authorization stage is the external lifecycle stage defined in
the paired architecture §4.4. It is distinct from architecture ratification,
architecture freeze, WP1 authorization, G-3 closure, the WP4 checkpoint, and
WP4 entry verification. WP4 cannot issue it. Its exact terminal dispositions
are `WP5 SUBSTANTIVE WORK AUTHORIZED` and
`WP5 SUBSTANTIVE WORK NOT AUTHORIZED`.
The external stage produces only that authorization record. It does not
produce TB-4 and cannot bypass WP4. WP4 executes authorization-result
verification on either outcome and is the sole producer of the bounded,
frozen TB-4 determination.

For the Portfolio Intelligence nested forms, frozen
[M42-WP3 Stage B](M42_WP3_STAGE_B_INVESTMENT_UNIVERSE_DECLARATION_CONTRACT_SPECIFICATION.md)
§9.2, [M44-WP1](M44_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md)
§6.6, [M44-WP4](M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md)
`WP4-NR-032`, and [M44 G-3 Roadmap](M44_G3_CLOSURE_AND_WP6_ENTRY_ROADMAP.md)
§4 all control. The external artifact must state whether it is representation
completion, clarification, amendment, successor contract, or another governed
class. M45 authors none of those forms.

---

## 2. M45-WP1 — Authority and frozen-baseline verification

### Purpose

**`[NORMATIVE IF RATIFIED]`** Verify that M45 may act and establish its exact
read-only predecessor baseline.

### Scope

- verify allocation, architecture ratification/freeze, and separate WP1
  authorization;
- reconcile M44 terminal states and authority exhaustion;
- identify the outstanding G-2 fact and any externally supplied competent
  authority record; and
- publish prohibitions for later M45 packages.

WP1 does not settle `OQ-5`, determine its own competence, write the Decision
Log, or close G-2.

### Deliverables

1. Authority-chain verification register.
2. Frozen-baseline and content-identity register.
3. Gate/checkpoint entry-state table with a distinct historic-`STOP`
   preservation record.
4. G-2 outstanding-fact and external-authority observation.
5. Prohibition and non-authority register.
6. WP1 independent review, correction, confirmation, and freeze records.

### Exit criteria

- every authority record is independently verified;
- the M44 `STOP` and all gate states match frozen closeout;
- G-2 remains outstanding unless an external competent record already exists,
  and no Decision Log write occurs;
- unresolved review findings are `NONE`;
- content identity is validated before WP1 freeze.

If allocation, planning freeze, or WP1 authority is missing, WP1 does not
start and no M45 WP—including WP7—may run. The competent external governance
process records the pre-M45 blocked state; it is not M45 milestone completion.

### Dependencies

The complete external governance chain in architecture §4.2, including
separate WP1 authorization.

### Risks

- self-authorization;
- stale navigation treated as authority;
- historic `STOP` treated as provisional;
- G-2 observation mistaken for recording.

### Expected implementation sequence

1. Verify authorization before opening WP1.
2. Verify frozen artifact identities.
3. Reconcile states without changing them.
4. Record G-2 observation only.
5. Run the universal lifecycle.

### Independent freeze boundary

WP1 freezes only its verification register. It supplies no external evidence,
gate disposition, or Decision Log authority.

---

## 3. M45-WP2 — External frozen-artifact intake and competence verification

### Purpose

**`[NORMATIVE IF RATIFIED]`** Determine whether already-existing external
artifacts qualify for use as G-3 evidence.

### Scope

For each artifact, verify:

1. competent owner;
2. independently established authority;
3. immutable artifact identity;
4. completed authoring, review, confirmation, and freeze lifecycle;
5. exact canonical representation or deterministic byte definition;
6. complete field/facet coverage for its G-3 element; and
7. non-conflict with frozen M42–M44.

For Base Currency, verify one G-3 element with the Ledger & Accounting
coordinate dimension and Asset Foundation denomination-identifier dimension.
For the nested-form artifact, verify the exact artifact class and authority
required by §1.

### Deliverables

1. External-artifact intake register.
2. Competence and authority matrix.
3. Immutable identity and lifecycle manifest.
4. Eight-element G-3 coverage matrix.
5. Joint Base Currency compatibility record.
6. Nested-form constitutional-basis record.
7. Accepted/rejected/deferred evidence disposition.
8. WP2 lifecycle records.

### Exit criteria

- every accepted artifact passes all seven checks;
- routing, examples, implementation forms, labels, and specimens are rejected
  as supply;
- no owner artifact is corrected or normalized by M45;
- Base Currency is counted once;
- the nested-form artifact expressly reconciles M42-WP3 §9.2, M44-WP1 §6.6,
  `WP4-NR-032`, and M44 G-3 Roadmap §4;
- unresolved review findings are `NONE`;
- the WP2 register is confirmed and frozen.

An incomplete evidence set may produce a frozen intake register with
`DEPENDENT BRANCH BLOCKED`; it may not release WP3.

### Dependencies

Frozen WP1 and the independent existence of external artifacts.

### Risks

- intake becomes solicitation;
- custody is mistaken for ownership;
- M45 repairs an owner gap as “clarification”;
- joint Base Currency is double-counted;
- a Portfolio Intelligence ownership label is mistaken for nested amendment
  authority.

### Expected implementation sequence

1. Receive, never solicit.
2. Verify owner, authority, and lifecycle.
3. Verify identities and exact coverage.
4. Reconcile the nested-form constitutional basis.
5. Record accept/reject/defer.
6. Run the universal lifecycle.

### Independent freeze boundary

WP2 freezes an intake determination, not external artifacts. A later external
revision requires a new additive WP2 `RCn` intake revision.

---

## 4. M45-WP3 — G-3 evidence manifest and complete formability determination

### Purpose

**`[NORMATIVE IF RATIFIED]`** Determine whether accepted source evidence makes
complete Composition, `PMS1`, and `PAIM1` bytes formable.

### Scope

- assemble a source-owner evidence manifest;
- preserve owner bytes opaquely;
- apply frozen container order and framing;
- test every field and nested facet;
- derive concrete Composition, `PMS1`, and `PAIM1` instances; and
- obtain independent constitutional and serialization review.

WP3 is not a source of owner semantics and does not itself close G-3.

### Deliverables

1. Source-owner evidence manifest.
2. Field/facet and identity coverage matrix.
3. Complete Composition construction record.
4. Concrete `PMS1` and `PAIM1` formability records.
5. Two-independent-reader byte-identity record.
6. Constitutional and serialization review record.
7. Corrections and focused re-review records, if needed.
8. Independent confirmation and WP3 freeze record.

### Exit criteria

- all eight G-3 elements trace to qualifying frozen sources;
- no gap is closed by assembly-time “clarification,” inference, default,
  normalization, substitution, or synthetic bytes;
- two independent readers derive byte-identical outputs;
- every review finding is discharged by a defined additive candidate revision;
- unresolved findings are `NONE`;
- independent confirmation and identity validation precede freeze.

If an external defect is found, M45 records it and stops. It cannot initiate
owner correction. If an M45-owned candidate defect is found, WP3 issues an
additive revision and focused re-review before confirmation.

### Dependencies

Frozen WP2 with all required evidence accepted.

### Risks

- assembly invents missing semantics;
- opaque bytes are parsed or normalized;
- affirmative absence collapses into missing;
- WP3 candidate freezes before review;
- a downstream citation points to a superseded revision.

### Expected implementation sequence

1. Lock accepted source identities.
2. Assemble the manifest.
3. Construct complete bytes without repair.
4. Run two-reader derivation.
5. Conduct independent dual-boundary review.
6. Correct additively and re-review as required.
7. Confirm, validate identity, freeze.

### Independent freeze boundary

WP3 freezes only after its own independent review and confirmation. It does
not freeze or amend owner artifacts and does not issue a gate disposition.

---

## 5. M45-WP4 — Prospective checkpoint and bounded entry verification

### Purpose

**`[NORMATIVE IF RATIFIED]`** Apply the evidence neutrally and decide whether
WP5 contract authoring may begin.

### Scope

- verify the exact terminal record from the separate substantive M45-WP5
  authorization stage before any G-3 or checkpoint act;
- if and only if that record is `WP5 SUBSTANTIVE WORK AUTHORIZED`, apply all
  objective G-3 criteria from
  [M44 G-3 Roadmap](M44_G3_CLOSURE_AND_WP6_ENTRY_ROADMAP.md) §12 and issue a
  distinct G-3 determination;
- preserve the historic M44 `STOP`;
- after the separate G-3 determination, issue a distinct prospective `STOP`
  or, only when `G-3 CLOSED` is supported, an authorizing checkpoint
  disposition; and
- after independent confirmation of the checkpoint, apply the frozen WP6-0
  five-condition boundary to M45-WP5 in a separate entry-verification act.

WP4 does not authorize substantive WP5 work. It verifies a separately issued
authorization record and executes on both authorization outcomes. An absent
or negative record confines WP4 to bounded verification, prevents the G-3 and
checkpoint phases, and causes WP4 to produce
`WP5 ENTRY BLOCKED — SUBSTANTIVE AUTHORIZATION ABSENT OR NOT AUTHORIZED`, and
after the WP4 lifecycle routes the frozen determination to WP7 without
changing G-3 or checkpoint truth.

The exact five-condition mapping from frozen
[M44 G-3 Roadmap](M44_G3_CLOSURE_AND_WP6_ENTRY_ROADMAP.md) §9 is:

| Frozen WP6-0 condition | Prospective M45 satisfier | Required artifact or record | Verifier | Fail-closed outcome |
| --- | --- | --- | --- | --- |
| 1. A separately authorized future governance act explicitly authorizes substantive work | External substantive M45-WP5 authorization stage | Content-identified record with `WP5 SUBSTANTIVE WORK AUTHORIZED` | WP4 entry-verification act | `WP5 ENTRY BLOCKED — SUBSTANTIVE AUTHORIZATION ABSENT OR NOT AUTHORIZED`; WP5 unstarted; TB-4 to WP7 |
| 2. `G-3 CLOSED` evidence is valid, complete, independently confirmed, and traceable to frozen owner-domain forms | WP3 evidence/formability package plus WP4's separate G-3 determination | Frozen WP3 manifest, formability and two-reader records; independently confirmed WP4 G-3 determination | WP4 entry-verification act | Prospective `STOP`, `G-3 OPEN — PARTIAL`, or `WP5 ENTRY BLOCKED — FIVE-CONDITION VERIFICATION FAILED`, as the exact failed fact requires; TB-2, TB-3, or TB-6 |
| 3. A distinct independently confirmed authorizing checkpoint disposition exists | WP4 prospective-checkpoint phase, distinct from its G-3 determination and entry verification | Independently confirmed prospective authorizing checkpoint disposition | WP4 entry-verification act | `STOP` or `WP5 ENTRY BLOCKED — FIVE-CONDITION VERIFICATION FAILED`; TB-3 or TB-6 |
| 4. M44-WP4 and M44-WP5 remain frozen and their cited outputs resolve at exact canonical paths | WP1 exact predecessor-path and identity verification | Frozen WP1 baseline/content-identity register | WP4 entry-verification act | `WP5 ENTRY BLOCKED — FIVE-CONDITION VERIFICATION FAILED`; TB-6 |
| 5. The historic `STOP` is not bypassed by implication | WP1 historic-`STOP` preservation determination, distinct from exact-path verification and the prospective checkpoint | Frozen WP1 gate/checkpoint entry-state and historic-`STOP` preservation record | WP4 entry-verification act | `WP5 ENTRY BLOCKED — FIVE-CONDITION VERIFICATION FAILED`; TB-6 |

Each condition has a distinct satisfier and record. The WP4 entry-verification
act only verifies those five pre-existing facts; it satisfies none of them and
cannot create a missing authorization, gate closure, checkpoint, frozen path,
or non-bypass fact.

`G-4 OPEN — EFFECTIVE AND FROZEN` does not block WP5 entry once all G-3,
substantive-authorization, checkpoint, and entry-verification conditions are
satisfied. WP4 does not close, cure, replace, reinterpret, or weaken `G-4`;
Component G later binds only the named annualization unavailability.

### Deliverables

1. Objective G-3 criterion matrix.
2. Distinct G-3 determination record.
3. Prospective checkpoint candidate and independent confirmation.
4. M45-WP5 five-condition entry-verification record.
5. M45-WP5 entry-status record with exactly one applicable disposition:
   `WP5 ENTRY VERIFIED`, `WP5 ENTRY BLOCKED — SUBSTANTIVE AUTHORIZATION ABSENT
   OR NOT AUTHORIZED`, or
   `WP5 ENTRY BLOCKED — FIVE-CONDITION VERIFICATION FAILED`.
6. Independent review, correction, confirmation, identity, and freeze records.

### Exit criteria

- whenever the prospective-checkpoint phase executes, its disposition is
  evidence-derived and exactly one of `STOP` or the explicitly defined
  authorizing disposition;
- the G-3 determination, checkpoint disposition, and entry-verification record
  are separate content-identified acts;
- `G-3 CLOSED` is recorded only if every objective criterion passes;
- any missing criterion forces `STOP` and retains `G-3 OPEN — PARTIAL`;
- the historic M44 `STOP` is not reversed, corrected, bypassed, or amended;
- WP5 is released only when the separate authorization record is
  `WP5 SUBSTANTIVE WORK AUTHORIZED`, the checkpoint is authorizing and
  independently confirmed, and all five mapped conditions verify;
- independent confirmation and identity validation precede freeze.

A confirmed `STOP` is a successful procedural WP4 result. It routes directly
to WP7 and does not authorize WP5.

An absent or refused substantive authorization is also a valid procedural
result. WP4 verifies that result in bounded mode, leaves WP5 unstarted,
preserves G-3 and checkpoint truth exactly, and issues only the WP5-entry
blocked determination. That WP4 determination completes independent review,
confirmation, content-identity validation, and freeze before canonical TB-4
routes to WP7. It is not an architecture failure and does not convert an
otherwise valid checkpoint into substantive authority.

### Dependencies

Frozen WP3; independently established checkpoint authority; and a
content-identified terminal determination from the separate substantive
M45-WP5 authorization stage. A negative or absent-authorization determination
always releases WP4 authorization-result verification, but only in bounded
mode: it releases the WP5-entry block lifecycle and eventual WP7 route, not
the G-3 or checkpoint phases.

### Risks

- intended-path pressure predetermines authorization;
- historic and prospective checkpoints are conflated;
- review approval is mistaken for checkpoint confirmation;
- checkpoint authorization is mistaken for substantive WP5 authority;
- WP6-0 conditions are weakened.

### Expected implementation sequence

1. Verify the external substantive-authorization terminal record.
2. If absent or negative, produce the bounded WP5-entry blocked determination
   candidate and skip the G-3 and checkpoint phases.
3. If authorized, verify checkpoint authority and apply G-3 criteria in a
   separate determination.
4. Draft and independently confirm the neutral prospective checkpoint.
5. Verify the five entry conditions in a separate bounded act.
6. Run the universal lifecycle for the applicable WP4 result, including
   independent review, confirmation, content-identity validation, and freeze.
7. Route only a frozen `STOP` or entry block to WP7; release WP5 only from
   `WP5 ENTRY VERIFIED`.

### Independent freeze boundary

WP4 alone owns the prospective checkpoint, its bounded entry verification,
and the WP5-entry status record. WP4 is the sole producer, reviewer,
confirmer, content-identity validator, and freezer of TB-4. It neither issues
substantive WP5 authority, alters M44, nor makes WP5 output exist.

---

## 6. M45-WP5 — Atomic Components A–K normative semantic contract

### Purpose

**`[NORMATIVE IF RATIFIED]`** Produce one documentary specification that fully
discharges `I-7`.

### Scope

The allocation originates in frozen
[M43-WP4](M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md)
§§6.1–6.11. The frozen
[M44-WP6 Plan](M44_WP6_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
carries forward its entry, atomicity, and no-result-leakage discipline.

The one atomic scope is:

| Component | Frozen subject |
| --- | --- |
| A | Portfolio Measurement Window |
| B | Economic time, record time, and stable ordering |
| C | Portfolio Base Currency and FX |
| D | Calendar and observation alignment |
| E | Benchmark alignment |
| F | Risk-free evidence and authority-class proof |
| G | Named annualization-basis unavailability only |
| H | Missing data, density, and partial windows |
| I | Numeric model and arithmetic |
| J | Dependency arithmetic |
| K | Canonical serialization |

No Result classification, method formula, runtime behavior, or provider
selection is in scope.

### Deliverables

1. One atomic A–K normative documentary candidate.
2. Ownership and dependency matrix.
3. Risk-free-evidence authority-class proof.
4. G-4 named-unavailability binding.
5. No-default and no-result-leakage registers.
6. Canonical serialization and documentary vector corpus.
7. Independent review, correction, confirmation, identity, and freeze records.

### Exit criteria

- all A–K components are complete in one revision;
- no partial A–J or component-level freeze is effective;
- Component F proves the required authority-class disposition;
- Component G introduces no factor, value, alias, placeholder, or synthetic
  dependency;
- no Portfolio Measure Result classification leaks into WP5;
- before authoring began, frozen WP3 intended-branch evidence, the separate
  `WP5 SUBSTANTIVE WORK AUTHORIZED` record, the frozen independently confirmed
  WP4 authorizing checkpoint, and `WP5 ENTRY VERIFIED` were all cited by exact
  identity;
- `I-7` is discharged by content, including its risk-free proof;
- unresolved findings are `NONE`;
- confirmation and identity validation precede atomic freeze.

`I-7` is recorded in frozen
[M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §4.1 and is
grounded in frozen M43-WP4 and the
[M43-WP7](M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) dependency
model at §3.1, §3.2 items 5–6, and §3.3. Discharge is by content, not
predecessor path.

### Dependencies

All of the following, without substitution:

1. frozen WP3 evidence and formability determination supporting the intended
   branch;
2. a separate content-identified
   `WP5 SUBSTANTIVE WORK AUTHORIZED` record from the external stage;
3. a frozen, independently confirmed WP4 authorizing checkpoint disposition;
4. a completed, frozen WP4 `WP5 ENTRY VERIFIED` record covering all five
   frozen WP6-0 conditions; and
5. the existing frozen WP1 predecessor-path and historic-`STOP` preservation
   records cited by that entry verification.

WP4's disposition alone cannot release WP5.

### Risks

- partial A–K publication;
- annualization placeholder laundering;
- result semantics leak upstream;
- planning text is treated as executable behavior.

### Expected implementation sequence

1. Lock frozen sources and authority.
2. Verify all five dependency classes above by exact identity.
3. Draft all A–K rows atomically.
4. Complete proofs, serialization, and vectors.
5. Conduct independent constitutional and semantic review.
6. Correct additively and re-review as required.
7. Confirm, validate identity, freeze atomically.

### Independent freeze boundary

Only a complete A–K revision freezes. WP5 does not authorize runtime use or
WP6 by implication; WP6 still verifies the frozen dependency.

---

## 7. M45-WP6 — Portfolio Measure Result normative contract

### Purpose

**`[NORMATIVE IF RATIFIED]`** Produce the universal documentary Result contract
that fully discharges `I-8`.

### Scope

- Portfolio Measure Result identity and value-presence rules;
- Portfolio Input Sufficiency;
- Portfolio Computation Outcome;
- Degraded State relationship;
- lineage, Provenance, and canonical serialization;
- deterministic classification of frozen WP5 semantic facts.

WP6 does not redefine A–K, add formulas, or convert absence into a numeric
value.

### Deliverables

1. Portfolio Measure Result normative candidate.
2. Sufficiency/outcome/degraded-state matrix.
3. Value-presence and `UNAVAILABLE` state rules.
4. Lineage and Provenance contract.
5. Canonical identity and serialization rules.
6. Documentary positive, boundary, and negative vectors.
7. Independent review, correction, confirmation, identity, and freeze records.

### Exit criteria

- the complete atomic WP5 revision is frozen and cited by exact identity;
- result classification consumes rather than redefines WP5 predicates;
- `UNAVAILABLE` is a state, never a zero, null substitute, or invented value;
- a hash does not substitute for canonical content or Provenance;
- `I-8` is discharged by content against frozen M43-WP5 planning obligations;
- unresolved findings are `NONE`;
- confirmation and identity validation precede freeze.

`I-8` is recorded in frozen
[M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §4.1 and is
grounded in frozen
[M43-WP5](M43_WP5_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md)
and the [M43-WP7](M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md)
dependency model at §3.1, §3.2 items 5–6, and §3.3. Discharge is by content,
not predecessor path.

### Dependencies

Frozen complete WP5.

### Risks

- Result rules redefine upstream arithmetic;
- unavailable becomes a numeric fallback;
- serialization loses lineage or affirmative absence;
- runtime adoption is inferred.

### Expected implementation sequence

1. Verify frozen WP5 identity.
2. Draft classification and value-presence rules.
3. Close lineage, Provenance, identity, and serialization.
4. Complete documentary vectors.
5. Run the universal lifecycle.

### Independent freeze boundary

WP6 freezes only its Result contract. It grants no runtime, method, registry,
API, or persistence authority.

---

## 8. M45-WP7 — Truthful reconciliation and milestone closeout

### Purpose

**`[NORMATIVE IF RATIFIED]`** Record the exact terminal truth of M45 without
turning unavailable work into closure.

### Scope

- reconcile every WP and external prerequisite;
- record final gate and checkpoint states;
- distinguish intended-path and fail-closed outcomes;
- synchronize Decision Log and INDEX only if explicit competent authority
  exists and the facts are independently confirmed; and
- create closeout, independent confirmation, and freeze records.

### Deliverables

1. WP and external-prerequisite terminal matrix.
2. Gate/checkpoint terminal matrix.
3. Intended-path or fail-closed outcome statement.
4. Outstanding blocker and successor-obligation register.
5. Authorized Decision Log/INDEX synchronization, if authority exists.
6. Independent closeout review and confirmation.
7. M45 closeout freeze record.

### Exit criteria

- every started WP has an exact terminal lifecycle state;
- unavailable external work is not marked incomplete M45 work;
- the historic M44 `STOP` remains unchanged;
- `G-3`, `G-4`, and `G-5` reflect evidence exactly;
- G-2 is recorded only if a competent external vehicle expressly authorizes
  the Decision Log write; otherwise it remains outstanding;
- a WP4 `STOP` is reported as a valid procedural outcome;
- no unperformed WP is reported complete or frozen;
- no code, runtime, schema, API, provider, migration, or production file
  changed;
- independent confirmation and identity validation precede closeout freeze.

### Dependencies

Frozen WP1 plus exactly one canonical post-WP1 terminal branch from §12.1:

1. **TB-1 — frozen WP2 blocked or deferred intake determination** because
   owner evidence is unavailable, incomplete, or defective;
2. **TB-2 — frozen WP3 blocked formability or external-defect determination**
   because complete Composition, `PMS1`, or `PAIM1` bytes are not formable;
3. **TB-3 — frozen WP4 `STOP` disposition** with the exact supported G-3
   state;
4. **TB-4 — frozen WP5-entry blocked/not-authorized determination** caused
   only by absence or refusal of the separate substantive authorization act;
5. **TB-5 — frozen WP6 intended-path completion**; or
6. **TB-6 — another frozen lawful downstream block**: WP4 five-condition
   entry-verification failure other than TB-4, or a WP5/WP6
   blocked/not-confirmed determination after lawful start.

No WP3 failure is routed through WP4. TB-4 is not a WP4 `STOP`, does not alter
an existing checkpoint disposition, and does not authorize WP5. For TB-4,
WP7 consumes the frozen WP4 entry-status record; WP7 never produces, confirms,
or freezes it.

### Risks

- closeout pressure converts blockage to closure;
- navigation files become an unauthorized G-2 vehicle;
- planned work is reported as performed;
- branch cleanliness is confused with constitutional completeness.

### Expected implementation sequence

1. Inventory exact terminal evidence.
2. Select the truthful terminal branch.
3. Reconcile gates without predetermined closure.
4. Perform only explicitly authorized synchronization.
5. Independently review and confirm closeout.
6. Validate identities and freeze.

### Independent freeze boundary

WP7 freezes the truthful closeout only. It cannot retroactively authorize,
complete, or freeze another WP or external artifact.

---

## 9. Recommended implementation order

| Stage | Action | Release condition |
| --- | --- | --- |
| 0 | Complete allocation and planning lifecycle | Both planning files ratified and frozen |
| 1 | Authorize and execute WP1 | Separate competent WP1 authorization |
| 2 | Await external evidence; execute WP2 | Qualifying external artifacts exist |
| 2A | Emit fail-closed branch TB-1 | WP2 has reviewed, confirmed, content-identified, and frozen its blocked or deferred intake determination |
| 3 | Execute WP3 | WP2 accepts complete evidence |
| 3A | Emit fail-closed branch TB-2 | WP3 has reviewed, confirmed, content-identified, and frozen its blocked formability or external-defect determination |
| 4 | Obtain external substantive WP5 authorization determination | Frozen WP3 intended-branch evidence exists; competent actor acts independently of WP4 |
| 5 | Execute WP4 authorization-result verification on either outcome | Content-identified external terminal determination exists |
| 5A | Complete bounded WP4 lifecycle and emit TB-4 | Authorization is absent or `NOT AUTHORIZED`; WP4 reviews, confirms, content-identifies, and freezes its WP5-entry blocked determination; frozen TB-4 then releases WP7 |
| 5B | Continue WP4 G-3 determination, checkpoint, and five-condition entry verification | `WP5 SUBSTANTIVE WORK AUTHORIZED`; frozen WP3; checkpoint authority |
| 6A | Fail-closed closeout | TB-3 or TB-6 |
| 6B | Execute WP5 | Frozen WP3 intended evidence; separate substantive authorization; frozen independently confirmed WP4 authorizing checkpoint; frozen `WP5 ENTRY VERIFIED` |
| 7 | Execute WP6 | Complete atomic WP5 frozen |
| 8 | Execute WP7 | Exactly one of TB-1 through TB-6 is available |

No stage is calendar-promised. External conditions can block indefinitely.

---

## 10. Risk assessment

### Technical risk

- byte divergence: require exact framing and two-reader identity;
- loss of opaque owner bytes: prohibit parsing and normalization;
- incomplete Provenance: require owner-supplied completeness basis.

### Architectural risk

- cross-domain overreach: external conditions are not WPs;
- silent M42 amendment: require separate act class and authority;
- checkpoint disposition mistaken for substantive WP5 authority: require the
  distinct external authorization stage and five-condition mapping;
- premature freeze: attach the full lifecycle to every substantive WP;
- partial A–K: atomic WP5 freeze only.

### Migration risk

- documentary contracts treated as cutover authority: all implementation
  authority remains `NONE`;
- external revisions invalidate citations: downstream packages re-verify the
  latest frozen identity.

### Operational risk

- unavailable owner evidence: stop and close out truthfully;
- predetermined checkpoint: preserve binary neutral review;
- refused substantive WP5 authority: WP4 verifies the result in bounded mode,
  freezes its entry-block determination, leaves WP5 unstarted, and closes
  through TB-4 without changing G-3 or checkpoint truth;
- G-2 self-recording: WP1 only observes; WP7 writes only with explicit
  competent authority.

---

## 11. Independent implementability and reviewability

Each M45 WP:

- has one owner: Portfolio Intelligence;
- produces a bounded documentary artifact set;
- has explicit predecessor evidence;
- completes its own independent review and confirmation;
- has a distinct content-identity and freeze boundary; and
- may terminate blocked without changing predecessor truth.

External owner artifacts remain independently governed outside this matrix.
M45's inability to correct them is a deliberate constitutional boundary.

---

## 12. Roadmap completion model

### 12.1 Canonical post-WP1 terminal-branch inventory

This inventory is exhaustive and is reused by WP7 Dependencies and the
consolidated stage table:

1. **TB-1 — frozen WP2 blocked or deferred intake determination** because
   owner evidence is unavailable, incomplete, or defective;
2. **TB-2 — frozen WP3 blocked formability or external-defect determination**
   because complete Composition, `PMS1`, or `PAIM1` bytes are not formable;
3. **TB-3 — frozen WP4 `STOP` disposition** with the exact supported G-3
   state;
4. **TB-4 — frozen WP5-entry blocked/not-authorized determination** caused
   only by absence or refusal of the separate substantive authorization act;
5. **TB-5 — frozen WP6 intended-path completion**; or
6. **TB-6 — another frozen lawful downstream block**: WP4 five-condition
   entry-verification failure other than TB-4, or a WP5/WP6
   blocked/not-confirmed determination after lawful start.

WP7 closes truthfully from every branch. No branch may be relabelled as
another: in particular, TB-2 does not pass through WP4, and TB-4 is not a
checkpoint `STOP`. WP4 is the sole producer of TB-4; WP7 consumes only its
frozen determination.

### Intended path

`WP1 → WP2 complete intake → WP3 formable → separate WP5 substantive authorization → WP4 authorization-result verification (AUTHORIZED) → WP4 G-3 determination → WP4 authorizing checkpoint → WP4 five-condition entry verification → WP5 → WP6 → WP7 (TB-5)`

### Pre-M45 blocked states

Unavailable allocation, planning ratification/freeze, or WP1 authority leaves
the candidate or commissioned milestone blocked before WP execution. No WP7
closeout and no M45 completion claim is available.

### Valid fail-closed M45 paths after WP1

- TB-1 — frozen WP2 blocked or deferred intake determination;
- TB-2 — frozen WP3 blocked formability or external-defect determination;
- TB-3 — frozen WP4 `STOP` disposition;
- TB-4 — external authorization absent or `NOT AUTHORIZED` → bounded WP4
  authorization-result verification → WP4 entry-block candidate → WP4 review
  → WP4 confirmation → WP4 content-identity validation → WP4 freeze → frozen
  WP5-entry blocked/not-authorized determination → WP7;
- TB-6 — another frozen lawful downstream block.

TB-5 is the intended-path completion branch. TB-1 through TB-4 and TB-6 may
reach truthful procedural closeout with exact blockers. Only TB-5 may claim
both `I-7`/`I-8` discharge and `G-5 CLOSED`.

---

## 13. Present boundary

This roadmap is a corrected planning candidate only. It changes no gate,
allocates no competent authority, and authorizes no work package. M45 remains
not ratified, M45-WP1 remains not authorized, and the historic M44 checkpoint
remains `STOP`.
