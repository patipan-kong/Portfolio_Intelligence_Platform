# M44-WP5 — Annualization Basis Ownership Determination and Requirement Specification: Architecture and Implementation Plan

**Milestone:** M44 — Portfolio Analytics Gate Closure and Normative Semantics

**Work package:** M44-WP5 only

**Artifact class:** Non-normative architecture and planning document

**Candidate:** `RC3`

**Status:** `PROPOSED — PLANNING ONLY; NOT A GOVERNANCE DETERMINATION OR CONTRACT`

**Governing authority:** Frozen [M44 Architecture and Implementation Plan](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md), especially §§3.1, 4.4, 5–6, 8.4, 10, 11 M44-WP5, 12.1.1, 12.3, 12.5, 13.1, 16.2, and 17 OQ-3; [M44 Architecture Freeze Record](M44_ARCHITECTURE_FREEZE_RECORD.md); frozen [M44-WP1 Inherited Gate Inventory and Closure Register](M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md) §4.4; frozen M43-WP2 §§8.1–8.2; and frozen M43-WP4 §§5.2 and 6.7.

**Implementation authority:** `NONE`

**Runtime authority:** `NONE`

**Source-code authority:** `NONE`

**Persistence authority:** `NONE`

**Schema/migration authority:** `NONE`

**API authority:** `NONE`

**UI authority:** `NONE`

**Provider authority:** `NONE`

**Production-method authority:** `NONE`

**Executable-validation authority:** `NONE`

**Contract-authoring, registration, extension, versioning, and serialization authority:** `NONE`

**Capability-completion authority:** `NONE`

**Frozen-artifact-amendment authority:** `NONE`

**Vocabulary-admission authority:** `NONE`

**Gate-disposition authority of this planning artifact:** `NONE`

**Planned WP5 determination scope:** G-4 only, subject to independent confirmation; authority over G-3, G-5, and the §12.1.1 checkpoint: `NONE`

---

## 0. RC2 constitutional review response

The authoritative RC2 result was `NOT APPROVED`. It found eighteen of the
nineteen RC1 findings resolved correctly and confined the remaining defects to
the ownership-proof-failure branch and its consequences. This response is
embedded because the RC2 correction is expressly limited to this planning
document. It does not reopen any resolved RC1 section.

### C-1 — `ACCEPTED`

**Constitutional rationale.** The RC2 candidate incorrectly decided a tension
among frozen authorities by asserting precedence and then supplied an owner
field value not present in the frozen terminal-state vocabulary. Frozen M44
Architecture §§3.1, 4.4, 10, 11 M44-WP5, and 16.2 require an `OPEN` record to
name the exact owner. Section 17 OQ-3(c) separately lists “No admissible owner;
G-4 `OPEN` with the ownership question itself unresolved.” WP5 has no authority
to reconcile those frozen statements, waive a required field, or amend their
meaning.

**Exact correction.** Sections 1, 2, 3, 4, 5, 7, 8, and 10 now quote and expose
the tension without selecting a governing side. The precedence assertion,
substitute owner value, and ownership-proof-failure `OPEN` row are removed. If
ownership cannot be proved, WP5 establishes no G-4 terminal state and stops.
The unestablished state is routed through frozen §12.1.1's third outcome and
the M44 Architecture Freeze Record's process for a new independently confirmed
architecture revision that names the defect before WP5 or the checkpoint may
be re-evaluated.

### C-2 — `ACCEPTED`

**Constitutional rationale.** Frozen M44 Architecture §10 states that an
ownership-proof failure makes the affected determination fail. Section 11
M44-WP5 makes proof of all four frozen M43-WP4 §6.7 propositions a conjunct of
completion. Section 12.1.1 classifies an unestablished gate state as a review
defect that must be corrected before checkpoint re-evaluation. The RC2
candidate instead routed failure to confirmation and freeze.

**Exact correction.** Sections 3, 5, 5.1, 7, and 8 now make ownership-proof
failure stop for correction: WP5.3 through WP5.6 do not begin, no
terminal determination is proposed, WP5 does not complete or freeze, and
§12.1.1 is not re-evaluated until the frozen ambiguity is corrected through a
separately authorized, independently reviewed and confirmed architecture
revision.

### J-1 — `ACCEPTED`

**Constitutional rationale.** Frozen M44 Architecture §11 M44-WP6 permits the
Component G unavailability binding only when both the missing element and
owner are named. A failed ownership proof supplies no constitutionally
formable binding and cannot be treated as a confirmed G-4 outcome.

**Exact correction.** Section 9 now limits the Component G consequence to a
conforming, independently confirmed `G-4 OPEN` record with the exact missing
element and exact owner. An unestablished G-4 state supplies no Component G
binding and cannot authorize WP6.

### J-2 — `ACCEPTED`

**Constitutional rationale.** The uppercase substitute owner token and the
state-suffix branch labels introduced vocabulary outside frozen §16.2 and
conflicted with this plan's vocabulary-admission ceiling.

**Exact correction.** Every substitute owner value and state-suffix branch
label is removed. Ownership-proof failure is described as a frozen-text
ambiguity and unestablished gate state, not as a new owner value, terminal
state, `OPEN` variant, or governed status.

### J-3 — `ACCEPTED`

**Constitutional rationale.** Frozen M44 Architecture §3.1 is a controlling
definition of G-4 and its exact-owner condition. Its omission made the §4.4
citation appear to support the opposite proposition.

**Exact correction.** The governing-authority header and §2 now include §3.1
and use the same complete M44 citation set. Section 1 quotes §§3.1, 4.4, 10, 11
M44-WP5, 16.2, 17 OQ-3(c), and §12.1.1's third outcome, with no reinterpretation
or precedence claim.

### 0.1 Preserved RC1 response record

The authoritative RC1 result was `NOT APPROVED`. All nineteen findings were
accepted. The RC1 C-1 correction is superseded by the five RC2 dispositions
above; the remaining eighteen corrections are preserved below.

#### RC1 C-1 — `ACCEPTED`

**Reason.** The RC1 plan structurally required WP5.2 to select an owner before
WP5.3 could begin and therefore omitted the fail-closed branch required by
frozen M44 Architecture §10 `Ownership proof failure`, `INV-O3`, §4.4
NON-GOALS, and §17 OQ-3(c).

**Correction.** Superseded by RC2 C-1, C-2, J-1, J-2, and J-3 above. The RC3
correction exposes the frozen tension and routes it through the existing
constitutional correction process without deciding it.

#### RC1 J-1 — `ACCEPTED`

**Reason.** The RC1 paraphrase replaced the fixed M43-WP4 §6.7 binary with an
author-defined set and dropped exact source-calendar and Market Intelligence
language.

**Correction.** §3 restores all four propositions using the frozen wording:
`VERSIONED_CALCULATION_DEPENDENCY` correct, `GOVERNED_EVIDENCE` incorrect,
caller override rejected, and no expansion of Portfolio Intelligence authority
or transfer of ownership of source calendar meaning out of Market
Intelligence.

#### RC1 J-2 — `ACCEPTED`

**Reason.** RC1 conflated M43-WP2 §8.1's five-field declaration record with
M43-WP4 §6.7's separately required owner-published dependency information.

**Correction.** §§2, 4, 5, 7, and 8 now keep the lists separate: M43-WP2 §8.1
supplies Dependency key, Owning domain, Dependency contract kind, Dependency
identifier, and Dependency version; M43-WP2 §8.2 supplies closure; M43-WP4
§6.7 separately requires exact owner, existing governed contract kind,
identifier, immutable version, and canonical value bytes.

#### RC1 J-3 — `ACCEPTED`

**Reason.** RC1 omitted the mandatory post-WP5 §12.1.1 checkpoint and its
independent confirmation.

**Correction.** §§5 and 9 now place the checkpoint after WP5 confirmation and
freeze but outside WP5's stages, cite frozen M44 Architecture §§12.1.1, 12.3,
and 12.5 point 5 plus WP1 §4.4, and state that WP5 cannot disposition the
checkpoint. With frozen `G-3 OPEN — PARTIAL`, the checkpoint outcome is stop or
formally re-scope; WP6 and WP7 remain unauthorized.

#### RC1 J-4 — `ACCEPTED`

**Reason.** The RC1 authority block was incomplete against frozen `INV-A1` and
sibling M44 governance records.

**Correction.** The header now separately declares persistence,
schema/migration, API, UI, provider, production-method, executable-validation,
capability-completion, frozen-artifact-amendment, vocabulary-admission, and
scoped gate-disposition authority.

#### RC1 J-5 — `ACCEPTED`

**Reason.** The RC1 plan incorrectly called the WP5 deliverable normative.

**Correction.** §6 now uses the frozen M44 Architecture §11 term
`architectural deliverable` and expressly preserves its determination and
requirement-specification class without converting the requirement statement
into an owner-domain instrument.

#### RC1 J-6 — `ACCEPTED`

**Reason.** The controlling frozen WP1 §4.4 gate record and multiple governing
M44 sections were missing.

**Correction.** The header and §2 now cite WP1 §4.4 and frozen M44 Architecture
§§6, 8.4, 10, 12.1.1, 12.3, 12.5, 13.1, and 17 OQ-3. §7 maps all seven WP1
§4.4 disposition-evidence items.

#### RC1 J-7 — `ACCEPTED`

**Reason.** RC1 treated Market Intelligence ownership as settled before the
ownership proof.

**Correction.** §2 now states the OQ-3 hypothesis precisely: Market
Intelligence is tested first but must be proved or rejected; M39/M40–M41 form
the search corpus only if that proof succeeds.

#### RC1 J-8 — `ACCEPTED`

**Reason.** RC1 required positive examples without carrying the frozen
artificiality rule.

**Correction.** §§4 and 7 require every illustrative positive example lacking
an existing owner-published contract to be marked `ARTIFICIAL`,
`NON-EFFECTIVE`, and `INCAPABLE OF PASSING THE FUTURE GATE`; no artificial
label may satisfy M43-WP2 §8.2 closure.

#### RC1 N-1 — `ACCEPTED`

**Reason.** RC1 phrased WP5 plus D-7 as sufficient for D-2b and omitted D-1.

**Correction.** §9 now states that D-2b remains behind D-1 and all of its own
separate prerequisites.

#### RC1 N-2 — `ACCEPTED`

**Reason.** RC1 omitted D-7 and conditional D-3 consequences.

**Correction.** §9 now names D-7 and D-3 where attribution requires
annualization.

#### RC1 N-3 — `ACCEPTED`

**Reason.** RC1 paraphrased the frozen G-2 status vocabulary.

**Correction.** §2 now uses exactly
`RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE`.

#### RC1 N-4 — `ACCEPTED`

**Reason.** RC1 could imply that the WP4 closeout closed the M44 epic.

**Correction.** §2 now names the artifact `M44-WP4 Epic Closeout` and states
that it is work-package-scoped and does not close M44.

#### RC1 N-5 — `ACCEPTED`

**Reason.** RC1 used `admitted`, but WP5 has no admission authority.

**Correction.** §7 now uses `assessed as admissible` and denies admission
effect.

#### RC1 N-6 — `ACCEPTED`

**Reason.** Internal working labels could be mistaken for governed vocabulary.

**Correction.** §5 declares all stage-output labels non-governed internal
planning labels with no identity, registration, or vocabulary effect.

#### RC1 N-7 — `ACCEPTED`

**Reason.** WP5.1 candidate framing could be mistaken for proof.

**Correction.** §5 limits WP5.1 to recording hypotheses; only WP5.2 may prove
or reject an authority class or owner.

#### RC1 E-1 — `ACCEPTED`

**Reason.** The section describes a determination method, not a new ownership
model.

**Correction.** §3 is retitled `Ownership determination method`.

#### RC1 E-2 — `ACCEPTED`

**Reason.** The `CLOSED` outcome's pronoun had an ambiguous antecedent.

**Correction.** §1 now identifies the exact existing governed contract kind as
the object that may later be cited.

#### RC1 E-3 — `ACCEPTED`

**Reason.** The plan lacked a review candidate label.

**Correction.** The header identifies this revision as candidate `RC3`.

---

## 1. Purpose and constitutional effect

This document proposes the architecture, bounded work decomposition, and
evidence sequence for M44-WP5. It does not itself determine the owner of an
annualization basis, identify an admissible contract, close or disposition
`G-4`, or create a requirement specification with normative effect.

The architectural objective of M44-WP5 is narrow:

> Determine, by constitutional proof, the owner of the annualization-basis
> dependency required by annualization-dependent Portfolio Analytics methods;
> then determine whether an exact, existing governed contract kind is already
> published in that owner's frozen corpus. If it is absent, record the exact
> missing element, exact owner, and the requirements that a future owner-domain
> governance instrument must meet—without authoring that instrument.

The work package has only two permitted terminal outcomes:

| Outcome | Meaning | Effect |
| --- | --- | --- |
| `G-4 CLOSED` | The proved owner already publishes an exact existing governed contract kind and all required information. | That exact existing governed contract kind may be cited by a later annualization-dependent specification, subject to its own authority and gates. |
| `G-4 OPEN` | No exact existing governed contract kind is found in the proved owner's frozen corpus. | The requirement specification, exact missing element, exact owner, and downstream consequences are recorded. This is not closure. |

### 1.1 Frozen ownership-proof-failure tension

The frozen corpus speaks in terms WP5 cannot reconcile:

- Frozen M44 Architecture §3.1 states: “G-4 accordingly admits exactly two
  terminal states in M44: `CLOSED`, only if an owner-domain governance
  instrument satisfying frozen M43-WP2 §8.1 already exists and is identified,
  or `OPEN`, with the exact missing element and the exact owner it must come
  from recorded by name.”
- Section 4.4 NON-GOALS states: “If ownership cannot be proved, or if the
  owner-domain instrument does not already exist, the correct M44 outcome is a
  recorded, named, open gate stating the exact missing element and its exact
  owner.”
- Section 10 `Ownership proof failure` states: “The affected determination
  fails and no contract is authored — by M44 or on any domain's behalf. A
  failed ownership proof produces a recorded named blockage with the exact
  missing element and the exact owner it must come from, never an implicit
  owner (INV-O3).”
- Section 11 M44-WP5 states that the purpose is to “record G-4 `OPEN` with the
  exact missing element and its exact owner” when an exact existing governed
  contract kind is absent. Its completion criteria state: “The ownership
  determination is proved with all four frozen M43-WP4 §6.7 proofs,” and its
  `OPEN` row requires that “the exact missing element and exact owner are
  named.”
- Section 16.2 defines `OPEN`: “The obligation is not discharged; the exact
  missing element and its exact owner are named,” and requires each gate state
  to be drawn “from this closed vocabulary and from no other.”
- Section 17 OQ-3(c), however, lists: “No admissible owner; G-4 `OPEN` with the
  ownership question itself unresolved.”

This planning document does not decide whether OQ-3(c) can form an `OPEN`
record while the exact-owner requirements remain unsatisfied. It establishes
no precedence between these frozen statements, supplies no substitute owner,
and creates no additional terminal state or `OPEN` variant.

If WP5 cannot prove an admissible owner, the ownership determination fails
under §10, the §11 completion criteria are not met, and no G-4 terminal state
is established. Frozen §12.1.1 then supplies the existing route: “Stop. An
unestablished gate state is a review defect in the producing work package and
is corrected before the checkpoint is re-evaluated.” WP5 has no authority to
perform that constitutional correction. Under the frozen M44 Architecture
Freeze Record, the defect can be corrected only by a new architecture revision
that names the defect and is independently reviewed and confirmed. Until that
process completes, WP5 remains incomplete and the checkpoint, WP6, and WP7
remain unauthorized.

No intermediate finding, candidate, analogy, market convention, or apparent
implementation practice may be treated as a terminal outcome.

## 2. Frozen baseline and dependency statement

M44-WP5 depends on the following immutable decisions and artifacts. It consumes
them by citation only and does not reconcile, restate, or edit them.

| Prior authority | Dependency for WP5 |
| --- | --- |
| Platform Architecture Laws 1–15; §§6–8 and 11–12 | Ownership, layer, vocabulary, precedence, and fail-closed rules. |
| ADR-001 through ADR-005 | Ledger source-of-truth, no compensation, two-timeline, one-rule, and replay-correctness boundaries. |
| M34-D-0005 and M34-D-0010 | Existing producing-domain grammar and Provenance ownership; neither is an annualization authority. |
| M39 and M40–M41 frozen Market Intelligence corpus | OQ-3 hypothesis only: Market Intelligence ownership is tested first and must be proved or rejected. These artifacts become the owner-domain search corpus if and only if WP5.2 proves Market Intelligence is the owner. They are not ownership evidence by their mere existence. |
| M42, including WP2, WP5, and WP7 | Portfolio coordinate, Benchmark Declaration, and Composition boundaries; WP5 may not change or default any of them. |
| M43 Architecture and M43-WP1 through WP8 | Frozen Portfolio Analytics ownership, dependency, gate, and downstream sequencing baseline. |
| M43-WP2 §8.1 | The declaration record: Dependency key, Owning domain, Dependency contract kind, Dependency identifier, and Dependency version. |
| M43-WP2 §8.2 | Transitive dependency-closure test and fail-closed rejection rules. |
| M43-WP4 §5.2 and §6.7 | Exact-existing-kind rule; the four exact ownership/authority proofs; and the separately required exact owner, existing governed contract kind, identifier, immutable version, and canonical value bytes. |
| M44 Architecture §§3.1, 4.4, 5–6, 8.4, 10, 11 M44-WP5, 12.1.1, 12.3, 12.5, 13.1, 16.2, and 17 OQ-3 | G-4 definition, exact-owner requirements, authority invariants, C4 allocation, fail-closed ownership behavior, WP5 completion criteria, checkpoint, prerequisites, confirmation, artifact path, closed terminal-state vocabulary, and OQ-3 alternatives. |
| M44-WP1 Freeze Record and M44-WP1 Inherited Gate Inventory and Closure Register §4.4 | Work-package start condition; `G-4` purpose, authority split, permitted terminal states, and seven required evidence items. |
| M44-WP2 and M44-WP3 closeouts; M44-WP4 Freeze Record and M44-WP4 Epic Closeout | Current M44 state: WP1–WP4 are frozen; `G-2` is `RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE`; `G-3` remains `OPEN — PARTIAL`. The M44-WP4 Epic Closeout is work-package-scoped and does not close M44. None of these states is reinterpreted by WP5. |

M44-WP5 is independently startable after the frozen M44-WP1 predecessor
condition. It is not dependent on a `G-3 CLOSED` result. A constitutionally
formable, independently confirmed WP5 outcome is a strict input to M44-WP6's
Component G binding and to the annualization-dependent portion of the deferred
M43-WP7 work (`D-2b`), subject to §12.3 and the §12.1.1 checkpoint.

## 3. Ownership determination method

The annualization basis is not presumed to be Portfolio Intelligence-owned.
WP5 has determination authority only; it does not acquire the subject merely
because Portfolio Analytics consumes it.

The determination must prove or fail closed against all four frozen M43-WP4
§6.7 propositions, without substitution or generalization:

1. why `VERSIONED_CALCULATION_DEPENDENCY` is constitutionally correct;
2. why `GOVERNED_EVIDENCE` is constitutionally incorrect for the
   annualization basis;
3. why caller override is constitutionally rejected; and
4. why the proposed owner and placement do not expand Portfolio Intelligence
   authority or transfer ownership of source calendar meaning out of Market
   Intelligence.

If all four proofs succeed, the proved owner-domain corpus is the only corpus
searched for an admissible dependency contract. A similar object, calendar,
provider field, module, configuration value, or convention elsewhere is not a
substitute.

If the proof cannot establish an admissible owner, frozen M44 Architecture §10
and `INV-O3` require the determination to fail closed. The frozen tension
quoted in §1.1 prevents WP5 from forming a terminal G-4 record without
resolving constitutional meaning outside its authority. WP5 therefore authors
no contract or owner-domain requirement, establishes no G-4 state, does not
enter the corpus-search stage, and stops under §12.1.1's third outcome pending
the M44 Architecture Freeze Record's required new independently confirmed
architecture revision that names the defect.

## 4. Scope boundary

### 4.1 Included

- documentary constitutional ownership analysis for the annualization basis;
- an exhaustive, cited inventory of the proved owner's relevant frozen corpus;
- exact declaration-shape assessment under frozen M43-WP2 §8.1, including
  Dependency key, Owning domain, Dependency contract kind, Dependency
  identifier, and Dependency version;
- closure assessment under frozen M43-WP2 §8.2;
- separate assessment of the M43-WP4 §6.7 information: exact owner, existing
  governed contract kind, identifier, immutable version, and canonical value
  bytes;
- caller-override rejection and version non-substitutability analysis;
- a terminal `G-4` determination record, subject to independent review and
  confirmation;
- if `G-4 OPEN` with a proved owner, a non-normative requirement specification
  for the future owner-domain instrument, naming only what that owner must
  supply;
- if ownership proof fails, an explicit stop that exposes the frozen §1.1
  ambiguity without a substitute owner, terminal-state proposal, or
  owner-domain instrument requirement; and
- documentary positive, boundary, and negative vectors plus a coverage ledger.
  Any illustrative positive example not backed by an exact existing
  owner-published contract must be marked `ARTIFICIAL`, `NON-EFFECTIVE`, and
  `INCAPABLE OF PASSING THE FUTURE GATE`; no artificial label can satisfy
  M43-WP2 §8.2 closure.

### 4.2 Excluded

- authoring, drafting, registering, extending, naming, versioning, or
  serializing any contract kind or dependency in any corpus;
- selecting an annualization factor, calendar, market, session count, provider,
  or default; `252`, `365`, and `365.25` are inadmissible when ambient or
  unversioned;
- defining annualization arithmetic or any Portfolio Analytics method formula;
- making a calculation dependency declaration, Method Version, applicability
  requirement, manifest entry, or result contract;
- changing M44-WP4's frozen `G-3 OPEN — PARTIAL` outcome or using it as evidence
  that an annualization basis is available;
- implementation artifacts, source code, test harnesses, runnable fixtures,
  serializers, validators, APIs, schemas, migrations, persistence, UI,
  provider access, or runtime behavior;
- modification of any frozen M1–M44-WP4 artifact, Decision Log entry,
  Implementation INDEX entry, ROADMAP capability status, or Graphify output;
- authorizing M44-WP6, M44-WP7, M43-WP6/WP7/WP8 method work, or M44 epic
  closeout.

## 5. Proposed work decomposition and sequencing

The following are internal planning stages, not newly authorized formal work
packages and not independently closable milestones.

`Authority intake`, `hypothesis record`, `corpus inventory`, `candidate
record`, `absence record`, and similar stage-output descriptions below are
non-governed internal planning labels only. They create no vocabulary,
identity, registry, contract, or artifact class.

| Sequence | Planning stage | Responsibility | Entry condition | Output / exit condition |
| --- | --- | --- | --- | --- |
| WP5.1 | Authority intake and boundary lock | Establish the exact frozen citations, authority boundaries, no-authoring ceiling, and OQ-3 ownership hypotheses. WP5.1 records hypotheses only; it cannot prove or reject an owner or authority class. | M44-WP1 is frozen; current frozen-state records verified. | Non-governed citation and hypothesis record plus explicit exclusions; ownership proof is reserved entirely to WP5.2. |
| WP5.2 | Ownership proof | Apply the four exact M43-WP4 §6.7 proofs to prove one owner or establish that no admissible owner can be proved. | WP5.1 complete. | Success: reviewable proof with no transferred meaning or new noun. Failure: no G-4 state is established; stop under §12.1.1's third outcome and route the frozen ambiguity through the M44 Architecture Freeze Record's process for a new independently confirmed architecture revision that names the defect. WP5.3 through WP5.6 do not begin. |
| WP5.3 | Existing-contract corpus inventory | Search only the proved owner's frozen corpus exhaustively. Record M43-WP2 §8.1 declaration fields separately from M43-WP4 §6.7 owner-published information. | WP5.2 proves an owner. No entry is permitted after ownership-proof failure. | Non-governed cited candidate record or absence record; no invented contract. |
| WP5.4 | Admissibility and terminal-state analysis | Apply M43-WP2 §8.2 closure; test the distinct M43-WP4 §6.7 information, caller-override rejection, and version non-substitutability. | WP5.3 complete. | One proposed terminal state: `CLOSED` or `OPEN`. |
| WP5.5 | Requirement and consequence record | If `OPEN`, specify the missing owner-domain instrument requirements. If `CLOSED`, cite the existing owner-domain publication exactly. State all downstream consequences. | WP5.4 complete after WP5.2 proves an owner. | One bounded determination artifact and documentary vectors; no owner-domain artifact is created. |
| WP5.6 | Independent governance lifecycle | Conduct author-independent constitutional review, correction if required, renewed review, independent confirmation, and freeze only under the frozen M44 lifecycle. | WP5.5 is complete. | Confirmed and frozen WP5, with unresolved findings `NONE`; or work remains open. |

The path through WP5.2–WP5.5 is strictly sequential and requires a proved
owner. Ownership-proof failure stops at WP5.2; WP5.3 through WP5.6 do not
begin, WP5 does not complete or freeze, and no candidate terminal
determination becomes eligible for confirmation. The governance lifecycle may
begin only after a candidate determination artifact exists and must not
substitute for ownership proof or corpus inventory.

### 5.1 Post-WP5 checkpoint boundary

WP5 confirmation and freeze trigger, but do not disposition, the frozen M44
Architecture §12.1.1 gate-state checkpoint. The checkpoint is not a WP5 stage.
It requires the independent confirmation at frozen §12.5 point 5 and consumes
the established terminal states of both G-3 and G-4. Under §12.3, WP5 has no
authority to release WP6 or WP7.

The checkpoint has a third frozen outcome in addition to its two G-3 rows:
“Either gate's state not established” requires “Stop. An unestablished gate
state is a review defect in the producing work package and is corrected before
the checkpoint is re-evaluated.” Ownership-proof failure implicates that
outcome because, as §1.1 records, the unresolved frozen tension prevents WP5
from establishing a G-4 state. WP5 cannot disposition the defect or the
checkpoint; a new independently confirmed architecture revision that names the
defect must first correct the ambiguity, after which WP5 and then the
checkpoint may be re-evaluated.

Because frozen M44-WP4 currently establishes `G-3 OPEN — PARTIAL`, the frozen
checkpoint outcome is **Stop, or formally re-scope**. M44-WP6 and M44-WP7 do
not begin. WP5 neither changes G-3 nor declares the checkpoint satisfied.

## 6. Planned documentary deliverables

The frozen M44 Architecture §11 assigns exactly one architectural deliverable
path to WP5:

- `docs/implementation/M44_WP5_ANNUALIZATION_BASIS_OWNERSHIP_DETERMINATION_AND_REQUIREMENT_SPECIFICATION.md`

The deliverable is a determination and requirement-specification artifact. It
is not a normative Portfolio Analytics semantics specification, not a governed
dependency contract, and not the owner-domain instrument it may describe.

The planning lifecycle may additionally require separately named review,
response, confirmation, freeze, and closeout records. Those records are
governance evidence only; their exact names and creation remain subject to the
frozen M44 lifecycle. No document in this plan authorizes an implementation
artifact or an owner-domain contract artifact.

## 7. Acceptance and evidence plan

A proposed WP5 determination is eligible for constitutional review only when
it supplies all seven disposition-evidence items frozen by M44-WP1 §4.4:

1. **Four proofs.** It states exactly why
   `VERSIONED_CALCULATION_DEPENDENCY` is constitutionally correct, why
   `GOVERNED_EVIDENCE` is constitutionally incorrect for the annualization
   basis, why caller override is constitutionally rejected, and why the owner
   and placement do not expand Portfolio Intelligence authority or transfer
   ownership of source calendar meaning out of Market Intelligence. If these
   cannot all be proved, no terminal determination is proposed and the stop
   for correction in §§1.1 and 5.1 applies.
2. **Corpus search.** When an owner is proved, the search of that owner's
   frozen corpus is exhaustive and cited, and distinguishes an absence result
   from an unsearched surface. When no owner is proved, the non-entry of the
   corpus-search stage is explicit.
3. **`CLOSED` evidence.** The exact citation, identifier, immutable version,
   and canonical value bytes are recorded as the owner already publishes them.
   Separately, any concrete dependency declaration is checked against all five
   M43-WP2 §8.1 fields—including Dependency key—and passes §8.2 closure.
4. **`OPEN` evidence.** The requirement specification states exactly what the
   owner-domain instrument must supply, the named missing element, named owner,
   and consequences for `D-2b` and `D-7`. Ownership-proof failure cannot
   satisfy this evidence item and produces no proposed `OPEN` record.
5. **Ambient-value rejection.** Negative vectors reject an unversioned or
   ambient `252`, `365`, or `365.25`; a separate vector distinguishes a
   governed version-bound derived session count of `252` from an ambient one.
   The governed example may be assessed as admissible only when already
   owner-published and fully bound; WP5 performs no admission.
6. **M44-authored-kind rejection.** A negative vector rejects any contract
   kind authored by M44 and any requirement specification presented as a
   contract kind.
7. **Independent confirmation.** Author-independent constitutional review and
   independent confirmation complete with unresolved findings `NONE` before a
   terminal result is effective.

Positive and boundary examples that are not backed by an exact existing
owner-published contract must be marked `ARTIFICIAL`, `NON-EFFECTIVE`, and
`INCAPABLE OF PASSING THE FUTURE GATE`. No artificial label, fixture, or
example satisfies M43-WP2 §8.2 closure. Version substitution, wrong-owner,
caller-override, and transitive-closure rejection remain directly covered.

The final terminal state must be recorded only after independent constitutional
review and confirmation. A review result does not itself make an unconfirmed
candidate available to any later work.

## 8. Risks, dependencies, and prerequisite assumptions

| Risk or assumption | Consequence | Required control |
| --- | --- | --- |
| A calendar-like term is mistaken for proof of owner or contract kind. | Unauthorized ownership transfer or false `G-4 CLOSED`. | Separate the M43-WP4 §6.7 ownership proof from the M43-WP2 §8.1 declaration fields and §8.2 closure. |
| A common `252`/`365`/`365.25` value is treated as canonical. | Ambient default admitted as governed dependency. | Negative vectors reject ambient values; accept only owner-published, version-bound canonical bytes. |
| A future requirement specification is treated as a present contract. | M44 creates the very dependency it lacks authority to create. | Label it non-normative; prohibit registration and require `G-4 OPEN` until the owner acts. |
| A WP5 finding is used to authorize annualized method work. | Downstream scope bypass. | State that `D-2b` remains separately gated and that WP5 grants no method or runtime authority. |
| The owner corpus is incomplete, moved, or not frozen. | A negative finding is not evidentially complete. | Record corpus boundary and evidence completeness; if exact frozen corpus cannot be established, fail closed and do not claim `CLOSED`. |
| Vocabulary drift turns implementation syntax into a new business noun. | Unreviewed vocabulary admission. | Reuse existing terms; any genuinely new governed noun follows the frozen five-part vocabulary gate before use. |
| Frozen M44-WP4 status is reinterpreted. | G-3 result or §12.1.1 checkpoint is altered by implication. | Cite WP4 only as immutable context; make no G-3 or §12.1.1 disposition. |
| Ownership proof fails but the frozen corpus also requires an exact owner in an `OPEN` record. | WP5 cannot form a terminal state without resolving the frozen §1.1 ambiguity outside its authority. | Stop at WP5.2; establish no G-4 state, do not search a presumptive corpus, and route the defect through §12.1.1 and the M44 Architecture Freeze Record's process for a new independently confirmed architecture revision that names the defect. |

The key prerequisite assumption is evidentiary, not operational: the proved
owner's frozen corpus must be accessible enough to establish either a complete
exact-existing-kind match or a complete absence finding. No runtime service,
provider, database, source module, or live data is a prerequisite.

## 9. Downstream boundaries

WP5's confirmed outcome reaches downstream work only through the frozen
§12.1.1 checkpoint:

- M44-WP6 Component G would bind an exact existing governed dependency when
  `G-4 CLOSED`, or *annualization unavailable — named missing element and named
  owner* when a conforming `G-4 OPEN` record is independently confirmed, only
  if the §12.1.1 checkpoint permits WP6 to begin. An ownership-proof failure
  establishes no G-4 state, supplies no Component G binding, and cannot
  authorize WP6.
- With current frozen `G-3 OPEN — PARTIAL`, frozen M44 Architecture §12.1.1
  requires **Stop, or formally re-scope**. The checkpoint is
  `NOT DISPOSITIONED`; WP5 cannot disposition it, release WP6, or release WP7.
- Deferred annualization-dependent risk and benchmark-relative work (`D-2b`)
  remains behind `D-1`, the WP5 determination, the owner-domain instrument
  (`D-7`) when no exact existing kind is available, and all of D-2b's other
  separately governed prerequisites. WP5 and D-7 are necessary in the open
  case, never sufficient by themselves.
- `D-3` consumes the WP5 outcome only where an attribution method requires
  annualization; otherwise it has no WP5 dependency.
- No WP5 outcome changes or dispositions G-3, G-5, or any frozen artifact.

## 10. Final planning statement

M44-WP5 is a documentary ownership-and-availability determination, not a
calendar or annualization implementation effort. Its success condition is an
honest, independently reviewed terminal result—`G-4 CLOSED` only upon proof of
an exact owner-published existing contract, otherwise `G-4 OPEN` with the
missing element and exact owner recorded. If ownership cannot be proved, WP5
establishes no terminal state and stops through the existing frozen
constitutional correction process. This plan creates no contract, governed
vocabulary, runtime behavior, implementation authority, checkpoint
disposition, or downstream authorization beyond that frozen scope.
