# M45 Architecture — Focused Independent Constitutional and Architecture Re-Review

**Reviewed milestone:** M45 (corrected planning candidate)

**Artifact class:** Focused independent re-review record

**Re-review date:** 2026-07-31

**Predecessor review:** [M45_ARCHITECTURE_INDEPENDENT_REVIEW.md](M45_ARCHITECTURE_INDEPENDENT_REVIEW.md) — `NOT APPROVED`

**Candidate status at re-review time:** `PLANNING CANDIDATE — NOT RATIFIED`

**Final disposition:** `CORRECTIONS REQUIRED`

**F-1 … F-10:** `RESOLVED` = 10; `PARTIALLY RESOLVED` = 0; `NOT RESOLVED` = 0;
`SUPERSEDED BY NEW FINDING` = 0

**New findings:** `BLOCKING` = 0; `MAJOR` = 2; `MINOR` = 1; `ADVISORY` = 2

**Ratification performed by this record:** `NO`

**Confirmation performed by this record:** `NO`

**Freeze performed by this record:** `NO`

**M45-WP1 authorized by this record:** `NO`

**Implementation authority:** `NONE`

**Runtime authority:** `NONE`

**Gate-disposition authority:** `NONE`

**Cross-domain authority:** `NONE`

**Frozen-artifact amendment authority:** `NONE`

---

## 1. Review scope

This is a focused re-review of the corrected M45 planning corpus against the
ten non-advisory findings and five advisory observations issued in the original
independent review, plus a cross-cutting regression review of the restructuring
those corrections produced.

In scope:

- each original finding `F-1` … `F-10`, tested at its root rather than by
  textual comparison;
- each advisory `A-1` … `A-5` disposition, tested for accuracy;
- regressions, omissions, and inconsistencies introduced or exposed by the
  reduction from eleven work packages to seven;
- the authority and ratification lifecycle, the dependency graph, the
  work-package decomposition, gate states, and procedural neutrality.

Out of scope and not performed: ratification, adoption, independent
confirmation, architecture freeze, WP1 authorization, gate disposition, and any
change to a candidate, frozen, navigation, or non-documentary file.

This record does not modify either corrected candidate artifact, the
corrections response, the original review, or any frozen artifact.

---

## 2. Evidence examined

### 2.1 Candidate and review corpus

| Artifact | Path | Read |
| --- | --- | --- |
| Original independent review | [M45_ARCHITECTURE_INDEPENDENT_REVIEW.md](M45_ARCHITECTURE_INDEPENDENT_REVIEW.md) | Full |
| Corrections response | [M45_ARCHITECTURE_REVIEW_CORRECTIONS_RESPONSE.md](M45_ARCHITECTURE_REVIEW_CORRECTIONS_RESPONSE.md) | Full |
| Corrected architecture plan | [M45_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md](M45_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) | Full |
| Corrected work-package roadmap | [M45_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md](M45_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md) | Full |

### 2.2 Frozen and constitutional sources verified directly

| Source | Verified for |
| --- | --- |
| [Platform Architecture](../architecture/platform_architecture.md) | Exact titles of Laws 1–15, governance rules G1–G6, vocabulary rules V1–V4 |
| [M44 G-3 Closure and WP6-Entry Roadmap](M44_G3_CLOSURE_AND_WP6_ENTRY_ROADMAP.md) | §4 owner-domain evidence inventory and the "separately authorized owner-domain act"; §5 source-owner lifecycle; §7 dual-boundary review; §8 distinct checkpoint; §9 WP6-0 five conditions; §12 seven objective closure criteria; §13 four ordered permission conditions; §14 authority limitations |
| [M44-WP4 Composition Byte Contract](M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md) | `WP4-NR-001` exact text; `WP4-NR-032` exact text and its scoping to M44-WP4; §8 own-domain scoping row |
| [M44-WP1 Reconciliation](M44_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md) | §6.6 own-domain question and silent-amendment risk |
| [M42-WP3 Stage B Declaration Specification](M42_WP3_STAGE_B_INVESTMENT_UNIVERSE_DECLARATION_CONTRACT_SPECIFICATION.md) | §9.2 WP7 permissions, exact text |
| [M44 Architecture and Implementation Plan](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) | §4.1 obligation register — `I-7` and `I-8` exact rows; risk `R-2`; risks `R-10` and `R-15` on restatement-instead-of-citation; `INV-C4` |
| [M44 Architecture Constitutional Adjudication](M44_ARCHITECTURE_CONSTITUTIONAL_ADJUDICATION.md), [M44 Architecture Freeze Record](M44_ARCHITECTURE_FREEZE_RECORD.md) | Upheld finding on successor milestone numbering |
| [M44 Epic Closeout](M44_EPIC_CLOSEOUT.md), [Freeze Record](M44_EPIC_CLOSEOUT_FREEZE_RECORD.md), [Independent Confirmation](M44_EPIC_CLOSEOUT_INDEPENDENT_CONSTITUTIONAL_CONFIRMATION.md) | Terminal gate matrix; §5 G-2 non-substitute-vehicle statement; the `OQ-5` qualifier |
| [M43-WP1 Vocabulary and Ownership Register](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md) | §7.4 step-4 recording obligation |
| [M43-WP4 Plan](M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) | §§6.1–6.11 Components A–K titles, including §6.8 Component H exact title |
| [M43-WP5 Plan](M43_WP5_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) | Result-contract planning baseline |
| [M43-WP7 Plan](M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) | `G-5` definition and dependency model |
| [M44-WP6 Plan](M44_WP6_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) | Atomicity, no-result-leakage, WP6-0 entry discipline |

### 2.3 Method

Every claim in the corrections response was tested against the corrected
artifact text, and every claim in the corrected artifacts was tested against
the frozen source it cites — not against the correction author's summary. A
correction was treated as resolved only where the constitutional, authority,
lifecycle, dependency, or state-model defect is absent at its root, not merely
where the offending sentence has been removed. Repository-wide searches were
used to establish whether restated rule titles correspond to any frozen
corpus convention.

---

## 3. Reviewer independence statement

This re-review is performed by the same independent reviewer who issued
[M45_ARCHITECTURE_INDEPENDENT_REVIEW.md](M45_ARCHITECTURE_INDEPENDENT_REVIEW.md),
as the review brief prefers. That reviewer did not author, co-author, edit,
advise on, or contribute material to either candidate artifact, to the
corrections response, or to any M44 or prospective M45 work package, and
performed none of the corrections now under review. Independence from the
correction author is preserved.

Reviewer continuity carries one obligation, discharged in §12.2 below: where
the original review's own analysis is found to have been insufficiently
granular, that is recorded here rather than relied upon.

This record originates no gate disposition, ratifies nothing, confirms nothing,
freezes nothing, and authorizes no work package.

---

## 4. Original finding register

| Finding | Severity | Subject |
| --- | --- | --- |
| `F-1` | `BLOCKING` | Cross-domain work packages constituted without cross-domain authority |
| `F-2` | `BLOCKING` | Former WP4 contradicted frozen `WP4-NR-032` / M44-WP1 §6.6 without engaging it |
| `F-3` | `MAJOR` | WP1's G-2 recording was self-authorizing and contradicted the candidate's own synchronization rule |
| `F-4` | `MAJOR` | No allocation authority for the M45 identifier; no specified ratification lifecycle |
| `F-5` | `MAJOR` | No correction path for a frozen M45 output found defective downstream |
| `F-6` | `MAJOR` | §1.1/§2.2/§2.3 presupposed `G-3 CLOSED` and framed the frozen `STOP` as a problem |
| `F-7` | `MINOR` | Components A–K attributed to M44-WP6 rather than frozen M43-WP4 |
| `F-8` | `MINOR` | WP9/WP10 did not cite `I-7`/`I-8` |
| `F-9` | `MINOR` | Headers omitted seven authority classes, most consequentially cross-domain |
| `F-10` | `MINOR` | Ratification scope of the roadmap artifact was ambiguous |
| `A-1` … `A-5` | `ADVISORY` | Component H title; branch name; `G-4` label; WP6 clarification risk; WP6-0 correspondence |

---

## 5. Finding-by-finding determination — F-1 through F-10

### F-1 — Cross-domain authority — `RESOLVED`

The correction is structural, not cosmetic, and resolves the defect at its root.

Verified:

- **No external-domain work carries an M45 identifier.** The former M45-WP2
  (Ledger & Accounting), M45-WP3 (Asset Foundation), and M45-WP5 (Connectivity
  & Ingestion) no longer exist. Roadmap §1 is titled "External predecessor
  conditions — not M45 work packages" and opens "The following receive no M45
  identifiers." Architecture §5.2 carries the same table under "External
  predecessor conditions … not M45 work packages and receive no M45
  identifiers." The seven surviving packages are all Portfolio
  Intelligence-owned (roadmap §11).
- **M45 cannot commission, schedule, govern, review, confirm, freeze, or
  compel.** Roadmap §1: "M45 cannot request, commission, schedule, govern,
  review, confirm, correct, or freeze these external acts." Architecture §5.2:
  "M45 cannot request, commission, schedule, govern, review, confirm, or freeze
  any item in this table." Architecture §2.4 repeats the prohibition as an
  explicit non-goal naming the three domains.
- **Routing is never described as a request.** Roadmap §1 states "Routing is a
  record, not a request," matching frozen `WP4-NR-005` and the frozen
  [M44-WP4 Contract](M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md)
  §3.3 formulation. Architecture §3.4 states "A routed gap is a record, not a
  request."
- **External artifacts exist only through owner-domain authority.** Every row
  of roadmap §1 and architecture §5.2 requires an independently established
  owner, independent authority, immutable identity, and a completed
  authoring/review/confirmation/freeze lifecycle — the exact lifecycle of frozen
  [M44 G-3 Roadmap](M44_G3_CLOSURE_AND_WP6_ENTRY_ROADMAP.md) §5.
- **WP2 performs intake and competence verification only.** Roadmap §3 scope is
  seven verification checks; its exit criteria forbid M45 correcting or
  normalizing an owner artifact; its freeze boundary states "WP2 freezes an
  intake determination, not external artifacts."
- **Absence blocks rather than escalates.** Roadmap §1 column 4 is "Record
  absence and stop" for each owner-domain row; architecture §5.2 closes
  "Absence blocks the dependent branch"; roadmap §3 permits a frozen intake
  register carrying `DEPENDENT BRANCH BLOCKED`.
- **No completion criterion restores cross-domain authority.** Architecture
  §12.1 criterion 3 conditions citation on M45's *verification* of received
  evidence, and criterion 4 requires unavailable or defective external evidence
  to be "recorded without M45 correction or owner solicitation." The former
  criterion making M45 completion contingent on other domains' freezes is gone.

This is option (b) of the original required correction, which was the
reviewer's recommendation. The acceptance-test language retained in roadmap §1
and §3 (what M45 will require *on intake*) is within the permitted scope of
that option and imposes no obligation, identifier, deliverable, exit criterion,
or schedule on another domain.

### F-2 — Portfolio Intelligence nested forms — `RESOLVED`

Verified against the frozen text directly, including the exact wording of
`WP4-NR-032` and of M42-WP3 Stage B §9.2.

- **`WP4-NR-032` remains controlling.** Architecture §5.3 states it expressly:
  "Therefore `WP4-NR-032` remains controlling. M45 performs no form authoring."
  Roadmap §1 lists `WP4-NR-032` among the four controlling sources and directs
  "Preserve `WP4-NR-032`; stop" where the external artifact is absent.
- **The candidate does not authorize nested-form authoring.** The former
  M45-WP4 that proposed to supply the Investment Universe nested form and the
  Benchmark facets is removed entirely. Architecture §2.4 makes "author the
  missing Investment Universe or Benchmark forms inside the M45 work-package
  chain" an explicit non-goal.
- **A future representation artifact requires separately established
  authority, reviewed, confirmed, and frozen before intake.** Architecture §5.3
  requires the external act to classify itself as representation completion,
  clarification, amendment, successor contract, or another governed class; name
  its authority source; prove M42 non-conflict; complete independent review and
  confirmation; and freeze — "If any element is absent, M45 stops." Roadmap §1
  row 5 and §3 (deliverable 6, exit criterion 5) carry the same requirement into
  intake.
- **The four sources are accurately reconciled.** Architecture §5.3's summary of
  each was checked against the source. M42-WP3 Stage B §9.2 does permit WP7 to
  "define Portfolio Composition and portfolio-wide serialization only under
  WP7's own separately confirmed authority"; the candidate reproduces the
  "separately confirmed authority" qualifier rather than the permission alone.
  `WP4-NR-032` is correctly characterized as scoped to M44-WP4's container
  authority, and the candidate nonetheless treats it as controlling for M45 —
  the conservative direction, and the one frozen M44-WP1 §6.6 requires while the
  question is unsettled.
- **No permissive sentence is elevated over the controlling resolution.** §9.2
  appears in architecture §5.1 and §5.3 as a *conditional* permission and is
  never used to license an M45 act.
- **No silent amendment of frozen M42 is implied**, because M45 authors no form
  at all. Roadmap §3's risk list names "a Portfolio Intelligence ownership label
  is mistaken for nested amendment authority," which is precisely the
  `WP4-NR-032` failure mode.

One construction deserves affirmative note: the candidate treats a separately
authorized Portfolio Intelligence act as *external to M45*, not as internal by
virtue of shared domain. That distinction — domain ownership is not milestone
authority — is correct and is what makes the resolution sound.

### F-3 — G-2 recording authority — `RESOLVED`

- **WP1 cannot determine its own competence or settle `OQ-5`.** Roadmap §2
  states flatly: "WP1 does not settle `OQ-5`, determine its own competence,
  write the Decision Log, or close G-2." Its risk list names
  "self-authorization" and "G-2 observation mistaken for recording."
- **WP1 cannot write or synchronize the Decision Log.** Deliverable 4 is
  reduced to a "G-2 outstanding-fact and external-authority observation"; the
  exit criterion requires that "no Decision Log write occurs"; the freeze
  boundary states WP1 "supplies no external evidence, gate disposition, or
  Decision Log authority."
- **G-2 may remain outstanding without dishonesty.** Architecture §3.3
  assumption 6: "G-2 may remain outstanding without falsifying M45 completion."
  Architecture §2.2 treats it as a condition observed, not solved.
- **Any future recording requires a separately competent explicit vehicle.**
  Roadmap §1 row 6 requires "authority that settles `OQ-5` and expressly
  authorizes the Decision Log act"; architecture §5.2 row 6 the same.
- **WP7 does not bypass unresolved authority through closeout language.**
  Roadmap §8 exit criterion: "G-2 is recorded only if a competent external
  vehicle expressly authorizes the Decision Log write; otherwise it remains
  outstanding." Its risk list names "navigation files become an unauthorized
  G-2 vehicle." Architecture §12.1 criterion 8 conditions any Decision Log or
  INDEX change on "explicit competent synchronization authority after confirmed
  truth."

The two acts the original review required to be split — determining whether a
vehicle exists, and performing the recording — are now split, and neither is
placed where the actor could supply its own authority.

### F-4 — Allocation and architecture lifecycle — `RESOLVED`

Both halves of the finding are addressed.

- **The identifier is no longer presupposed.** Both headers read "Milestone
  label: M45 — prospective; allocation not yet evidenced." Architecture §4.1
  states that no frozen record reviewed establishes who may allocate the
  identifier, ratify the corpus, or authorize WP1, and that "Those authorities
  are not invented here." Architecture §3.3 assumption 4 records the same as a
  standing assumption. The former §1.1 assertion that M45 *is* the successor
  milestone is gone; §1.2 now says only that M45 "is a possible successor
  governance vehicle."
- **The nine-stage lifecycle is specified with the required columns.**
  Architecture §4.2 gives, for each of allocation, planning candidate,
  independent review, correction, focused re-review, independent confirmation,
  ratification, architecture freeze, and WP1 authorization: the competent actor
  or role, inputs, permitted action, prohibited action, output artifact,
  terminal disposition, and the release condition for the next stage.
- **The four required separations are stated explicitly.** Architecture §4.2
  closes: "Review approval is not confirmation. Confirmation is not
  ratification. Ratification is not WP1 authorization." Stage 8 (freeze) and
  stage 9 (WP1 authorization) are distinct rows with distinct actors, and stage
  9's prohibited action is "Infer authorization from ratification." Roadmap §0
  repeats the chain.
- **Absent authority yields a blocked state, not an invented one.** Stages 1, 7,
  8, and 9 each carry an explicit negative disposition (`BLOCKED`,
  `NOT RATIFIED`, `FREEZE REFUSED`, `NOT AUTHORIZED`), and roadmap §2 states
  that if allocation, planning freeze, or WP1 authority is missing, "WP1 does
  not start and no M45 WP—including WP7—may run," with the pre-M45 blocked state
  recorded by external governance rather than as M45 completion. That last
  clause forecloses the obvious evasion of using WP7 to close out a milestone
  that was never authorized.
- **The unknown actors remain named as unknown.** Stages 1, 7, and 9 read "not
  identified by this candidate" / "not identified here" rather than naming a
  plausible-sounding authority. This is the correct discharge: the finding
  required the lifecycle to be specified and the gap to be honest, not filled.

### F-5 — Correction and freeze lifecycle — `RESOLVED`

- **One universal lifecycle now binds every substantive artifact.**
  Architecture §8.1 and roadmap §0 both state
  `DRAFT` → `REVIEW CANDIDATE` → `APPROVED`/`CORRECTIONS REQUIRED` → additive
  `RCn` correction and focused re-review → `CONFIRMED` → content-identity
  validation → `FROZEN`.
- **No freeze precedes independent review and confirmation.** Roadmap §0: "No
  freeze may precede independent confirmation." Architecture §8.1: "No candidate
  freezes before independent review and confirmation. The primary author cannot
  independently review or confirm their own artifact." Every one of the seven
  packages carries "independent confirmation and identity validation precede
  freeze" (or equivalent) in its exit criteria, and each carries its own review,
  correction, confirmation, and freeze records as deliverables.
- **Frozen artifacts are never edited; corrections are additive with distinct
  identity.** Architecture §8.2: after freeze, "a defect can be discharged only
  by an additive successor `RCn` artifact with its own review, confirmation,
  identity validation, and freeze record; the frozen revision is never edited,
  reopened, or re-frozen." Architecture §3.4 carries the same as a constraint.
  This adopts the M44 revision-candidate precedent the original finding cited.
- **Downstream re-verification is required.** Architecture §8.2 and roadmap §0:
  a downstream WP "consumes the latest applicable frozen revision and
  re-verifies cited identities." Roadmap §3's freeze boundary requires a new
  additive WP2 `RCn` intake revision when an external artifact is revised, and
  roadmap §4's risk list names "a downstream citation points to a superseded
  revision."
- **The specific WP6-before-WP7 defect is eliminated, with no hidden
  successor.** The former defect was that the assembly package froze before the
  independent review package existed. In the corrected decomposition the
  assembly package is WP3, and it carries its own independent constitutional and
  serialization review (scope bullet 6, deliverables 6–8) *before* its own
  freeze: "WP3 freezes only after its own independent review and confirmation."
  Its risk list names "WP3 candidate freezes before review." Each remaining
  freeze-then-consume edge (WP3→WP4, WP4→WP5, WP5→WP6) is now backed by the
  §8.2 `RCn` path.
- **External-artifact defects are correctly excluded from M45's reach.**
  Architecture §8.2 and roadmap §4: "If an external defect is found, M45 records
  it and stops. It cannot initiate owner correction."
- **Independent review is not represented as author work.** Architecture §8.1
  and §3.4, plus §4.2 stages 3, 5, and 6, all separate the roles.

### F-6 — Procedural neutrality — `RESOLVED`

- **Closure is no longer a definitional feature.** Architecture §1.1 now states
  the purpose as determining "whether the evidence can satisfy frozen `G-3`
  criteria," and adds explicitly: "M45 does not define success as `G-3 CLOSED`.
  Its duty is to determine whether closure is warranted. A correctly evidenced
  `STOP`, retained `G-3 OPEN — PARTIAL`, unavailable owner evidence, or
  non-approved review is a valid and successful procedural outcome when recorded
  exactly."
- **The "Problems solved" table is gone.** §2.2 is retitled "Conditions
  examined, not predetermined outcomes," and the historic `STOP` row now reads
  "Preserve as valid historic truth and predecessor boundary" — context, not a
  defect awaiting remedy. This matches frozen
  [M44 G-3 Roadmap](M44_G3_CLOSURE_AND_WP6_ENTRY_ROADMAP.md) §8 and frozen
  [M44 Epic Closeout](M44_EPIC_CLOSEOUT.md) §3.
- **Success criteria no longer pressure WP4.** §2.3 requires that "every gate
  and checkpoint disposition follows the evidence, including `STOP`" and that
  "closeout reports unresolved blockers without converting them into closure."
  No criterion requires closure or authorization.
- **All lawful outcomes are enumerated.** Architecture §12.3 and roadmap §12
  list unavailable evidence, invalid competence or lifecycle, non-approved
  review, retained `G-3 OPEN — PARTIAL`, prospective `STOP`, WP5 not authorized,
  and a later candidate not confirmable — each reaching truthful procedural
  closeout. Roadmap §5: "A confirmed `STOP` is a successful procedural WP4
  result."
- **Procedural completion is separated from the intended outcome.**
  Architecture §12.1 (procedural completion) and §12.2 (intended
  contract-completion outcome) are distinct sections with distinct criteria, and
  roadmap §12 mirrors the split: "Only the intended path may claim `I-7`/`I-8`
  discharge or `G-5 CLOSED`."
- **No indirect success bias remains.** §1.2, §1.3, §5.6, §10, §11.1, and §11.2
  were each read for reintroduced bias. §5.6 and §11.2 deliberately state the
  value of *both* branches; §11.1 states M45 "is not inevitable." The residual
  bias the original finding identified is absent.

### F-7 — Components A–K attribution — `RESOLVED`

Roadmap §6 now opens: "The allocation originates in frozen
[M43-WP4](M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) §§6.1–6.11.
The frozen [M44-WP6 Plan](M44_WP6_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
carries forward its entry, atomicity, and no-result-leakage discipline."
Architecture §5.1 states the same relationship in its dependency table —
M43-WP4 as "Original Components A–K allocation and risk-free proof," M44-WP6 as
"Carried-forward entry and atomicity discipline." The architecture no longer
contains a competing A–K table, so no second location can drift. The eleven
component titles in roadmap §6 were compared row by row against frozen M43-WP4
§§6.1–6.11 and match, including Component H (see `A-1`) and Component G's
restriction to named unavailability.

### F-8 — `I-7` and `I-8` discharge — `RESOLVED`

Roadmap §6 purpose: WP5 shall "produce one documentary specification that fully
discharges `I-7`," with exit criterion "`I-7` is discharged by content,
including its risk-free proof." Roadmap §7 purpose and exit criteria do the same
for `I-8`. Architecture §12.2 items 4 and 5 repeat both, item 4 naming "the
risk-free-evidence authority-class proof" explicitly.

The citation was verified at source: frozen
[M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §4.1 does record
`I-7` as "Normative Portfolio Analytics semantics specification discharging
frozen M43-WP4 Components A–K, including the risk-free-evidence authority-class
proof → G-5" and `I-8` as "Normative Portfolio Measure Result contract
specification discharging frozen M43-WP5 → G-5." The candidate's attribution is
exact. Both roadmap sections and architecture §12.2 add "Discharge is by
content, not predecessor path," which is the statement the original finding
required and which the original review confirmed to be correct.

### F-9 — Authority headers — `RESOLVED`

Both headers now declare an identical sixteen-class block, including the seven
classes previously omitted: cross-domain, gate-disposition,
ownership-determination, vocabulary-admission, contract
authoring/registration/extension/versioning, executable-validation, and
production-method authority. Every class is `NONE`. The consequential one —
cross-domain authority — is now declared `NONE` and is consistent with the
structural resolution of `F-1`: the corpus both disclaims the authority and no
longer presupposes it.

### F-10 — Planning-corpus ratification scope — `RESOLVED`

Architecture §4.3: "The ratified corpus shall consist of this file and
[M45_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md](M45_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md).
The same ratification and freeze acts shall name and content-identify both."
The roadmap's opening states the reciprocal: "Both require the same review,
confirmation, ratification, identity validation, and freeze acts." Architecture
§4.2 stage 7 permits adopting "both planning artifacts as one corpus" and stage
8 freezing "both exact identities in one act"; roadmap §9 stage 0's release
condition is "Both planning files ratified and frozen." Architecture §7 now
states that the per-package detail "are normative only if the paired roadmap is
ratified and frozen with this file." The ambiguity is removed from every
location the finding named.

---

## 6. Advisory determination — A-1 through A-5

| Advisory | Claimed | Verified | Determination |
| --- | --- | --- | --- |
| `A-1` Component H title | `ADOPTED` | Roadmap §6 row H reads "Missing data, density, and partial windows", matching frozen M43-WP4 §6.8 exactly; the "asynchronous series" insertion is gone | `ADOPTED` — accurate |
| `A-2` Branch name | `NOT ADOPTED` | Branch remains `feature/m44-governance` | `NOT ADOPTED` — accurate; see below |
| `A-3` `G-4` label reconciliation | `ADOPTED` | Architecture §6.3 bullet 2 reconciles the WP5 freeze record's `OPEN — EFFECTIVE AND FROZEN` with epic closeout's `OPEN` as "the same non-closed condition" | `ADOPTED` — accurate |
| `A-4` Assembly-time "clarification" risk | `ADOPTED` | Roadmap §4 exit criterion forbids closing a gap by "assembly-time 'clarification,' inference, default, normalization, substitution, or synthetic bytes"; risk list names "assembly invents missing semantics" | `ADOPTED` — accurate |
| `A-5` WP6-0 correspondence | `ADOPTED` | Roadmap §5 states "M45-WP4's entry verification discharges the frozen WP6-0 boundary's five conditions, applied prospectively to M45-WP5 rather than M44-WP6" | `ADOPTED` — accurate as a statement; but see `N-1`, which the adoption exposes |

**On `A-2`.** Non-adoption is reasonable. Branch selection is a repository
publication act outside the authorized correction brief, and the concern was
recorded as presentational with no constitutional effect. It creates **no
ratification blocker**. It is noted only that if the corpus is ever frozen on
this branch, the freeze record should state the branch fact plainly so that no
future reader infers M44 continuation from repository topology — architecture
§1.2 and §1.3 already carry the substantive disclaimer.

No advisory non-adoption is upgraded into a defect. `A-5` is recorded as
accurately adopted; the finding at `N-1` below arises from the *content* of the
five conditions the adoption incorporates, not from the adoption itself.

---

## 7. Cross-cutting regression review

### 7.1 Function inventory across the restructuring

Every function formerly held by WP7–WP11 was traced into the seven-package
decomposition:

| Former function | New home | Assessment |
| --- | --- | --- |
| Independent constitutional and serialization review of the evidence package | WP3 scope bullet 6, deliverables 6–8, exit criteria | Present, and now *precedes* the WP3 freeze — an improvement on the reviewed original |
| Corrections and confirmation | Universal lifecycle (architecture §8.1–8.2, roadmap §0) plus per-WP deliverables | Present in all seven packages |
| Prospective checkpoint | WP4 | Present; distinct from the historic checkpoint |
| Bounded WP6-0-equivalent entry verification | WP4 scope bullet 4 | Present; but see `N-1` |
| Atomic A–K authoring and review | WP5 | Present, atomicity preserved |
| Result contract authoring and review | WP6 | Present, downstream position preserved |
| Gate reconciliation | WP7 scope, deliverable 2, exit criteria | Present |
| Decision Log and INDEX synchronization under explicit authority | WP7 scope bullet 4, deliverable 5, exit criterion on G-2 | Present, correctly conditioned |
| Epic closeout and freeze | WP7 deliverables 6–7 | Present |

No function was lost in the reduction from eleven packages to seven. The
reduction is a genuine simplification: the four packages removed were the three
cross-domain packages that `F-1` found unconstitutional and the nested-form
package that `F-2` found unsupported, and their legitimate residue is the
intake verification now performed by WP2.

### 7.2 Work-package quality

All seven packages carry purpose, bounded scope, deliverables, objective exit
criteria, exact dependencies, meaningful risks, an expected sequence, and an
explicit independent freeze boundary. Spot-checks:

- Exit criteria are objective and testable throughout; no criterion turns on
  judgment words alone.
- Every risk list names a failure mode specific to that package rather than
  generic caution — WP2's "custody is mistaken for ownership," WP3's "affirmative
  absence collapses into missing," WP4's "review approval is mistaken for
  checkpoint confirmation," and WP5's "annualization placeholder laundering" are
  each precise and each traceable to a frozen concern.
- Freeze boundaries are correctly narrow: WP2 freezes an intake determination
  and not the external artifacts; WP4 "neither alters M44 nor makes WP5 output
  exist"; WP7 "cannot retroactively authorize, complete, or freeze another WP or
  external artifact."

### 7.3 Dependency graph

| Property | Result |
| --- | --- |
| Circular dependency | `NONE` |
| Missing entry gate | `NONE` on the declared chain |
| Authority implied by artifact intake | `NONE` — roadmap §3 freeze boundary and §11 both foreclose it |
| Downstream use of an unconfirmed candidate | `NONE` — every dependency names a *frozen* predecessor |
| External receipt → G-3 closure without determination | `NONE` — WP2 intake and WP3 formability both expressly decline to close G-3; only WP4 may record `G-3 CLOSED` |
| G-3 evidence → WP5 without confirmed WP4 disposition | `NONE` — WP5 dependencies require a frozen WP4 authorizing disposition |
| WP6 start before complete frozen WP5 | `NONE` — WP6 dependency is "Frozen complete WP5"; exit criterion 1 requires the complete atomic revision cited by exact identity |
| WP7 synchronization before confirmed terminal truth | `NONE` — WP7 scope bullet 4 and exit criteria both require confirmation first |
| Terminal-branch coverage into WP7 | **Incomplete** — see `N-3` |

Architecture §5.5's diagram, architecture §9's order, and roadmap §9's stage
table agree with one another and with each package's stated dependencies. The
`STOP`-routes-to-WP7 edge appears in all three.

### 7.4 External artifact intake

WP2 verifies, without owning: competent owner; independently established
authority; immutable artifact identity; completed authoring/review/confirmation/
freeze lifecycle; exact canonical representation or deterministic byte
definition; complete field-and-facet coverage for its G-3 element; and
non-conflict with frozen M42–M44. All eight checks required by the re-review
brief are present, distributed across roadmap §3's seven scope checks and §1's
acceptance-evidence column.

Rejection without amendment is explicitly possible: exit criteria require that
"routing, examples, implementation forms, labels, and specimens are rejected as
supply" and that "no owner artifact is corrected or normalized by M45"; the
disposition deliverable is "Accepted/rejected/deferred." This tracks frozen
`WP4-NR-030` and frozen
[M44 G-3 Roadmap](M44_G3_CLOSURE_AND_WP6_ENTRY_ROADMAP.md) §4's exclusion of
"labels, examples, display values, database keys, provider values, inferred
forms, artificial specimens, or roadmap-authored substitutes."

### 7.5 G-3 evidence and formability

WP3 consumes only accepted frozen inputs (dependency: "Frozen WP2 with all
required evidence accepted"); preserves owner bytes opaquely and applies frozen
container order and framing without redefinition; derives concrete Composition,
`PMS1`, and `PAIM1` instances; requires two-independent-reader byte identity;
and states expressly that it "is not a source of owner semantics and does not
itself close G-3." Neutrality between closure and continued open state is
preserved — WP3 produces a formability determination, not a disposition.

The joint Base Currency element is treated once and only once: roadmap §1 row 3
attaches the denomination dimension to Asset Foundation and row 2 the coordinate
to Ledger & Accounting; roadmap §3 scope requires verifying "one G-3 element
with the Ledger & Accounting coordinate dimension and Asset Foundation
denomination-identifier dimension"; the exit criterion "Base Currency is counted
once" and the risk "joint Base Currency is double-counted" both survive the
restructuring. This matches frozen
[M44 G-3 Roadmap](M44_G3_CLOSURE_AND_WP6_ENTRY_ROADMAP.md) §4 exactly and
remains the best-engineered seam in the package.

### 7.6 WP4 prospective checkpoint

Distinctly prospective (§5 scope bullet 3, "distinct prospective"); preserves
the historic `STOP` (scope bullet 2 and exit criterion 4: "not reversed,
corrected, bypassed, or amended"); independently confirmed before freeze; sole
release authority for WP5; binary permitted dispositions with `G-3 CLOSED`
recorded "only if every objective criterion passes" and any missing criterion
forcing `STOP` with `G-3 OPEN — PARTIAL` retained; and able to freeze validly
carrying `STOP`. Against frozen
[M44 G-3 Roadmap](M44_G3_CLOSURE_AND_WP6_ENTRY_ROADMAP.md) §8's five checkpoint
requirements and §12's seven objective criteria, the mapping is faithful.

`G-4` is neither cured nor treated as a universal blocker: architecture §2.2
binds it "only as named annualization unavailability," §6.3 reconciles its two
frozen labels, and WP5 deliverable 4 is the "G-4 named-unavailability binding."
WP4 itself is silent on `G-4`; see advisory `A-6`.

The defect at `N-1` concerns the entry-condition set WP4 applies, not its
disposition neutrality.

### 7.7 WP5 and WP6 seams

The seams the original review approved are intact and, in two places, improved:

- Components A–K remain one atomic scope; "no partial A–J or component-level
  freeze is effective"; the freeze boundary states "Only a complete A–K revision
  freezes."
- Component G binds only named annualization unavailability and "introduces no
  factor, value, alias, placeholder, or synthetic dependency."
- No concrete method formula is introduced: roadmap §6 scope closes "No Result
  classification, method formula, runtime behavior, or provider selection is in
  scope."
- WP5 owns predicates and universal semantics; WP6 owns Result classification
  and enclosure. "No Portfolio Measure Result classification leaks into WP5"
  (§6) and "WP6 does not redefine A–K, add formulas, or convert absence into a
  numeric value" (§7); WP6 exit criterion 2 requires that classification
  "consumes rather than redefines WP5 predicates."
- `UNAVAILABLE` remains a state, "never a zero, null substitute, or invented
  value"; a hash "does not substitute for canonical content or Provenance."
- Upstream canonical bytes remain opaque (roadmap §4 scope and risks;
  architecture §6.1 Law-9 row).
- No runtime, schema, API, provider, UI, or production authority is introduced:
  both headers, architecture §2.4, §3.2, §5.4 ("No runtime capability is
  introduced"), §12.1 criterion 9, and both WP freeze boundaries.

Additionally, WP5's freeze boundary now states that WP5 "does not authorize
runtime use or WP6 by implication; WP6 still verifies the frozen dependency" —
an anti-implication guard that did not exist in the reviewed original.

### 7.8 WP7 reconciliation and closeout

WP7 reports exact terminal states for every started WP and for every gate;
requires that "unavailable external work is not marked incomplete M45 work" and
that "no unperformed WP is reported complete or frozen"; preserves the historic
`STOP` unchanged; conditions Decision Log and INDEX synchronization on explicit
competent authority over independently confirmed facts; treats a WP4 `STOP` as a
valid procedural outcome; claims no production capability and requires that no
code, runtime, schema, API, provider, migration, or production file changed; and
freezes only after independent confirmation and identity validation. Its risk
list correctly names "branch cleanliness is confused with constitutional
completeness."

The one gap is the terminal-branch enumeration in its dependencies — `N-3`.

### 7.9 Corrections-response accuracy

Each row of the corrections-response §2 matrix was checked against the corrected
text at the sections it names. All ten rows describe changes that were in fact
made, at the sections cited, with source authorities that exist and say what the
row claims. No row overstates a correction, and every row correctly carries
`READY FOR FOCUSED RE-REVIEW` rather than a self-declared resolution — the
response's §1 statement that "Text changes do not resolve findings" and §5's
"findings independently resolved: `NONE`" are the constitutionally correct
posture and are affirmed. The advisory table in §4 is accurate in all five rows.

---

## 8. Authority and lifecycle review

| Required property | Result | Evidence |
| --- | --- | --- |
| Milestone allocation authority named or honestly recorded as absent | `PASS` | Architecture §4.1, §3.3 assumption 4; both headers |
| Nine lifecycle stages present with actor, inputs, permitted, prohibited, output, disposition, release | `PASS` | Architecture §4.2 |
| Review approval ≠ ratification | `PASS` | Architecture §4.2 closing; roadmap §0 |
| Confirmation ≠ ratification | `PASS` | Architecture §4.2 stage 6 prohibited action; closing statement |
| Ratification ≠ WP1 authorization | `PASS` | Architecture §4.2 stages 7 and 9; stage 9 prohibited action |
| Architecture freeze distinct from WP1 authorization | `PASS` | Architecture §4.2 stages 8 and 9 |
| No invented authority | `PASS` | Architecture §4.1; stages 1, 7, 9 all read "not identified" |
| Missing allocation ⇒ blocked | `PASS` | Architecture §4.2 stage 1 `BLOCKED`; roadmap §2 and §12 |
| No actor determines or grants its own authority | `PASS` | Roadmap §0 closing sentence; roadmap §2 |
| Substantive-package authorization | **`FAIL`** | WP5 has no authorization act distinct from WP4's disposition — `N-1` |

---

## 9. Work-package and dependency review

Summarized from §§7.2–7.8:

| WP | Scope vs. authority | Exit criteria | Dependencies | Freeze safety | Findings |
| --- | --- | --- | --- | --- | --- |
| WP1 | Correct — verification only | Objective; no Decision Log write | Complete | Safe | none |
| WP2 | Correct — intake only, no ownership | Objective | Complete | Safe | none |
| WP3 | Correct — assembly and formability, no closure | Objective | Complete | Safe — reviews before freeze | none |
| WP4 | Correct on disposition neutrality | Objective | Complete on artifacts | Safe | `N-1` (entry-condition set) |
| WP5 | Correct — atomic A–K only | Objective | Complete on artifacts; **incomplete on authorization** | Safe | `N-1` |
| WP6 | Correct — Result contract only | Objective | Complete | Safe | none |
| WP7 | Correct — truthful closeout only | Objective | **Incomplete branch enumeration** | Safe | `N-3` |

WP1, WP2, WP3, and WP6 require no correction. WP4 and WP5 require the
authorization correction at `N-1`; WP7 requires the branch-enumeration
correction at `N-3`.

---

## 10. Gate-state and procedural-neutrality review

| Gate / checkpoint | Frozen entry state | Candidate treatment | Assessment |
| --- | --- | --- | --- |
| `G-2` | `RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE`; step-4 recording outstanding | Observed by WP1; recorded by WP7 only under an express external vehicle settling `OQ-5`; may remain outstanding without falsifying completion | Correct — `F-3` resolved |
| `G-3` | `OPEN — PARTIAL` | Preserved on entry; `CLOSED` only on WP4's evidence-derived disposition against the seven frozen objective criteria | Correct — `F-6` resolved |
| Historic M44 checkpoint | `STOP`, independently confirmed | Preserved as valid historic truth in architecture §1.3, §2.2, §12.1 criterion 5; roadmap §5, §8, §13 | Correct |
| `G-4` | `OPEN` (`OPEN — EFFECTIVE AND FROZEN` at the WP5 freeze record) | Remains open; bindable only as named unavailability; both labels reconciled | Correct — `A-3` adopted |
| `G-5` | `OPEN` | `CLOSED` only on independently confirmed and frozen `I-7` and `I-8` discharge | Correct — `F-8` resolved |
| Prospective checkpoint | Not yet issued | Distinct, neutral, binary, `STOP` freezable | Correct |

Procedural neutrality is established. No statement in either artifact makes
`G-3 CLOSED`, `AUTHORIZE CONTRACT AUTHORING`, WP5 or WP6 completion, `G-5`
closure, or the intended contract-completion outcome a definitional feature of
M45 or a condition of its success. All eight lawful alternative outcomes named
in the re-review brief are expressly permitted at architecture §12.3 and roadmap
§12. The historic `STOP` is treated as preserved truth in every location it
appears.

---

## 11. Validation findings

| Validation | Result |
| --- | --- |
| Both corrected candidates read in full | `PASS` |
| Corrections response read in full | `PASS` |
| Original review read in full | `PASS` |
| Every frozen source cited by a finding or by the response verified at source | `PASS` |
| Candidate artifacts modified by this re-review | `NO` |
| Corrections response modified by this re-review | `NO` |
| Original review modified by this re-review | `NO` |
| Frozen M1–M44 artifact modified | `NO` |
| Decision Log or Implementation INDEX modified | `NO` |
| Ratification, confirmation, freeze, or WP1 authorization record created | `NO` |
| Source, schema, migration, API, UI, provider, runtime, or configuration file modified | `NO` |
| Repository-relative links in this record resolve | `PASS` — see final report |
| `git diff --check` | `PASS` — see final report |

---

## 12. New findings

### N-1 — `MAJOR` — WP5 has no authorization act distinct from WP4's checkpoint disposition, collapsing two frozen-distinct entry conditions

**Affected artifact and section.**
[M45_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md](M45_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md)
§5 (WP4 scope bullet 4 and the sentence beginning "M45-WP4's entry
verification discharges…"), §6 (WP5 Dependencies), §9 stage 5B; and
[M45_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md](M45_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
§7 (WP5 release condition), §9 step 7, §4.2 stage 9.

**Violated or endangered controlling rule.** Frozen
[M44 G-3 Roadmap](M44_G3_CLOSURE_AND_WP6_ENTRY_ROADMAP.md) §9, condition 1: WP6-0
may pass only when it verifies that "a separately authorized future governance
act explicitly authorizes substantive … work" — a condition frozen §9 states
*in addition to* condition 3, "a distinct independently confirmed authorizing
checkpoint disposition exists." Frozen §13 repeats the separation as an ordered
permission boundary: item 1 (separately authorized governance has authorized
substantive work) is distinct from item 3 (a distinct checkpoint has issued an
authorizing disposition and been independently confirmed) and item 4 (WP6-0 has
verified the entry conditions). Governance rule G2 — a lower artifact "may never
relax a law, reinterpret a boundary, or carve an exception."

**Explanation.** Roadmap §5 expressly binds M45 to the frozen WP6-0 boundary:
"M45-WP4's entry verification discharges the frozen WP6-0 boundary's five
conditions, applied prospectively to M45-WP5 rather than M44-WP6." Having
adopted that boundary, the candidate must satisfy all five conditions —
including condition 1's *separately authorized* act.

It does not. WP5's stated dependencies are "Frozen WP4 authorizing disposition
and frozen WP3 evidence package"; architecture §7 gives WP5's release condition
as "WP4 authorizes contract authoring"; roadmap §9 stage 5B's release condition
is "WP4 authorizes." No M45 artifact requires, or provides a place for, a
governance act authorizing substantive WP5 work that is distinct from WP4's own
checkpoint disposition. Only two readings are available, and both are defective:

- WP4 verifies condition 1 and finds nothing to verify, in which case WP5 is
  unreachable on the intended path and the candidate's own intended path
  (roadmap §12) is internally unsatisfiable; or
- WP4's authorizing disposition is treated as satisfying both condition 1 and
  condition 3, in which case one M45-internal act discharges two conditions that
  the frozen boundary deliberately separates — the boundary is weakened, and the
  candidate does so while its own WP4 risk list names "WP6-0 conditions are
  weakened" as the risk to avoid.

The defect is sharpened by an internal asymmetry the candidate has otherwise
been careful about. Architecture §4.2 stage 9 requires a *separate* competent
authorization for WP1 — the least consequential package, which only verifies —
and expressly prohibits inferring it from ratification. The most consequential
package, WP5, which authors normative universal semantics discharging `I-7`,
carries no equivalent requirement. That is the inverse of the fail-closed
posture the corrected candidate adopts everywhere else.

This is not a residue of `F-1` or `F-2`; it is a consequence of the
restructuring, exposed by the candidate's own adoption of advisory `A-5`.

**Required correction.** Either:

- **(a)** add an explicit external authorization stage for substantive WP5 work,
  parallel to architecture §4.2 stage 9 — naming the competent actor as
  unidentified if it is, its record class, its terminal dispositions, and the
  prohibition on inferring it from WP4's disposition or from ratification — and
  add it to WP5's dependencies, architecture §7's WP5 release condition, and
  roadmap §9 stage 5B; or
- **(b)** state expressly, with reasoning, why frozen §9 condition 1 and frozen
  §13 item 1 are discharged by an act other than a separate authorization in the
  M45 setting, identify that act, and record that a competent authority
  independent of WP4 confirms the equivalence.

Option (a) is the reviewer's recommendation: it is the smaller change, it
matches the candidate's own WP1 treatment, and it preserves the frozen
separation rather than arguing around it. Under either option, roadmap §5 must
enumerate the five WP6-0 conditions individually with their prospective M45
mapping, so that a reviewer can test each one rather than the aggregate claim.

**Required focused re-review scope.** Roadmap §5 (scope bullet 4 and the WP6-0
mapping sentence), §6 Dependencies, §9 stages 5B and 6; architecture §4.2, §7
WP5 row, §9 step 7. Re-review must confirm that all five frozen WP6-0 conditions
have a distinct, named satisfier and that no single M45-internal act discharges
more than one of them.

---

### N-2 — `MAJOR` — Architecture §6 misstates the Platform Laws and governance rules it claims compliance with

**Affected artifact and section.**
[M45_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md](M45_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
§6.1 ("Platform Laws 1–15" table, rows 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12) and
§6.2 ("Governance and vocabulary rules" table, rows `G2`, `G3`, `G4`, `G6`).

**Violated or endangered controlling rule.**
[Platform Architecture](../architecture/platform_architecture.md), which fixes
the Laws as: 1 the ledger is the single source of truth; 2 recorded history is
immutable; 3 holdings are derived; 4 replay is deterministic and reproducible; 5
asset identity is permanent; 6 identity is resolved decisively or not at all; 7
AI never performs accounting; 8 evaluation observes, it never touches; 9 every
business rule has exactly one implementation; 10 the core never knows the edge;
11 everything enters through the hallway; 12 the human owns the ledger and the
decision point; 13 failure is loud; 14 explainability is a fiduciary duty; 15
correctness outranks everything — and the governance rules as: `G1` higher
states intent, lower states reality; `G2` lower may refine, never weaken; `G3`
silence delegates; `G4` conflict is a defect, resolved upward; `G5` each level
amends by its own mechanism; `G6` code is never precedent. Vocabulary rule `V1`
(one term, one meaning, one home). Law 14 (explainability). Frozen
[M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) risk `R-10`,
which names "New authors restate rather than cite" as a `V1` violation by which
"a private dialect forms," and risk `R-15`, which warns against a shorter
restated framing displacing the frozen text.

**Explanation.** §6 is titled "Constitutional compliance." It is the section in
which the candidate demonstrates that it is constitutionally valid, and it is
the section a ratifying authority would rely on. Eleven of its fifteen law
titles do not correspond to the Laws they are numbered as — §6.1 row 1 reads
"Correct dependency direction" where Law 1 is the ledger as single source of
truth; row 3 "One authority per meaning" where Law 3 is that holdings are
derived; row 8 "Ownership is semantic" where Law 8 is that evaluation observes;
row 10 "Failure is modeled" where Law 10 is that the core never knows the edge;
and so on. Only rows 2, 13, 14, and 15 match. In §6.2, `G2` is given as "domains
own their terms" (actually: lower may refine, never weaken), `G4` as
"implementation is not architecture" (actually: conflict is a defect, resolved
upward — the given text is closer to `G6`), and `G6` as "downstream cannot
redefine upstream" (actually: code is never precedent). `G3` is rendered
"silence is not authority," which is the frozen `WP4-NR-001` rule, not `G3`.

A repository-wide search confirms these labels appear nowhere in the frozen
corpus and correspond to no established convention: every one of them is unique
to this candidate. Frozen M44, by contrast, cites `G5`, `G3`, `V1`, and `V2`
accurately and by number, and does not attempt a laws-compliance table at all.

Two consequences follow, and the second is the serious one. First, ratifying and
freezing this corpus would freeze an inaccurate constitutional record — the
precise `V1` "private dialect" failure frozen M44 `R-10` guards against, in a
milestone whose entire subject matter is exact citation of frozen sources.
Second, and materially, the compliance demonstration does not actually test the
candidate against the real rules: Law 1, Laws 3–12, `G2`, `G4`, and `G6` are
nowhere assessed. `G2` (lower may refine, never weaken) and `G4` (conflict is a
defect, resolved upward) are directly load-bearing for a planning candidate that
consumes frozen contracts across three governance levels — and `G2` is one of
the two rules `N-1` turns on.

The substantive constraints the candidate imposes elsewhere remain correct; the
propositions listed in §6.1 are, taken as propositions, sound engineering
commitments. The defect is that they are presented as the platform's Laws and
governance rules and are not.

**Required correction.** Rewrite §6.1 and §6.2 to cite the Laws and governance
rules by their exact constitutional titles, and state the candidate's compliance
against each as written — including Law 1 and Laws 3–12, and `G2`, `G4`, and
`G6`, which are presently unassessed. Where a Law is not engaged by a
documentary planning candidate, say so explicitly ("not engaged; M45 creates no
implementation") rather than substituting a different proposition under its
number. If the candidate wishes to retain its own engineering commitments, place
them in a separate, clearly labelled section that does not number them as Laws
or governance rules. Apply the same discipline to any restated rule elsewhere in
either artifact.

**Required focused re-review scope.** Architecture §6.1 and §6.2 in full,
checked title by title against
[Platform Architecture](../architecture/platform_architecture.md); plus a scan
of both artifacts for any other rule restated rather than cited. Re-review must
confirm that every numbered Law, governance rule, and vocabulary rule carries
its constitutional title and that the compliance claim addresses the rule as
written.

---

### N-3 — `MINOR` — WP7's terminal-branch enumeration omits a WP3 blocked outcome

**Affected artifact and section.**
[M45_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md](M45_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md)
§8 (WP7 Dependencies) and §9 stage 5A.

**Violated or endangered controlling rule.** The candidate's own fail-closed
requirement at architecture §12.3 and roadmap §12 ("Valid fail-closed M45 paths
after WP1" — including "owner evidence unavailable or incomplete" and "external
artifact competence or lifecycle invalid"), read with Law 13 (failure is loud)
and the candidate's §2.1 goal that every authority transition "fail closed."

**Explanation.** Roadmap §8 enumerates WP7's admissible predecessors as frozen
WP1 plus exactly one of: a frozen WP2 blocked intake; a frozen WP4 `STOP`; or
frozen WP6 intended-path completion. But roadmap §4 gives WP3 its own terminal
stop: "If an external defect is found, M45 records it and stops." A defect
discovered at assembly — an accepted artifact that proves insufficient only when
complete bytes are attempted — therefore produces a frozen WP3 blocked
determination that matches none of WP7's three listed branches. Roadmap §12
lists that outcome as a valid fail-closed path, so the artifacts disagree with
one another.

The practical risk is small but real and points the wrong way: a WP7 author
following §8 literally would find no admissible branch and would be pushed
either to route the WP3 stop through a WP4 disposition it was never given
evidence to make, or to treat the milestone as having no truthful closeout —
both of which defeat the fail-closed intent. Roadmap §9 stage 5A's "WP4 `STOP`
or earlier blocked branch" is the more accurate formulation and should govern.

**Required correction.** Add a fourth WP7 dependency branch: a frozen WP3
determination that complete Composition, `PMS1`, and `PAIM1` bytes are not
formable, or that an external defect blocks assembly. Align the wording of
roadmap §8, §9 stage 5A, and §12 so the three enumerations are identical, and
confirm architecture §12.3 covers the same set.

**Required focused re-review scope.** Roadmap §8 Dependencies, §9 stages 5A and
7, §12; architecture §12.3.

---

### 12.1 New advisory observations

`A-6` — Roadmap §5 (WP4) is silent on `G-4`. Frozen
[M44 G-3 Roadmap](M44_G3_CLOSURE_AND_WP6_ENTRY_ROADMAP.md) §13 states that
`G-4 OPEN — EFFECTIVE AND FROZEN` "does not block WP6 entry once the `G-3` and
checkpoint conditions above are satisfied." The candidate handles `G-4`
correctly everywhere it speaks (architecture §2.2, §6.3; roadmap §6), but a
future WP4 author reading only §5 could treat the open gate as a bar to
authorization. One sentence in WP4's scope recording that `G-4` neither blocks
authorization nor is cured by it would close the gap. Advisory only; the
candidate contains no statement to the contrary.

`A-7` — Roadmap §6 and §7 ground `I-7` and `I-8` in "the M43-WP7 dependency
model" without a section anchor, while citing
[M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §4.1 precisely
for the obligations themselves. Frozen
[M43-WP7](M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) is where
`G-5` is defined as the non-existence of the two universal specifications; a
section anchor there would let a WP7 author test `G-5` closure against its
definition rather than against the obligation register alone. Advisory only —
the obligation citations themselves are exact and were verified.

### 12.2 Correction to the original review record

Original review §4.2 stated that architecture §§5.1–5.3 "map Laws 1–15, G1–G6,
and V1–V4 without weakening any of them; the mappings were spot-checked against
the Platform Architecture positions cited and no misstatement was found." That
affirmation was not sufficiently granular: a title-by-title check against
[Platform Architecture](../architecture/platform_architecture.md) — performed in
this re-review and recorded at `N-2` — establishes that the numbered titles do
not match the constitution. Whether the defect pre-existed the corrections or
was introduced by the rewrite of that section cannot be determined from the
repository, since both candidates are untracked and no prior revision is
recoverable; the finding is raised against the corrected text, which is what
governs.

This paragraph corrects the review record additively. The original review
artifact is not modified.

---

## 13. Unresolved finding counts

| Class | Count | Identifiers |
| --- | --- | --- |
| Original findings `RESOLVED` | 10 | `F-1` … `F-10` |
| Original findings `PARTIALLY RESOLVED` | 0 | — |
| Original findings `NOT RESOLVED` | 0 | — |
| Original findings `SUPERSEDED BY NEW FINDING` | 0 | — |
| New `BLOCKING` | 0 | — |
| New `MAJOR` | 2 | `N-1`, `N-2` |
| New `MINOR` | 1 | `N-3` |
| New `ADVISORY` | 2 | `A-6`, `A-7` |
| **Total unresolved non-advisory** | **3** | `N-1`, `N-2`, `N-3` |

Advisory dispositions `A-1` … `A-5` are accurately recorded by the correction
author and none is upgraded to a defect.

---

## 14. Final disposition

**`CORRECTIONS REQUIRED`**

`APPROVED FOR INDEPENDENT CONFIRMATION` is not available: although `F-1`
through `F-10` are all `RESOLVED` and no `BLOCKING` finding survives, unresolved
`MAJOR` findings are 2 and unresolved `MINOR` findings are 1, and `N-1` is a
ratification blocker in its own right — a corpus that binds itself to the frozen
WP6-0 boundary must satisfy all five of its conditions before that binding can
be frozen.

Consequences:

- the M45 architecture is **not ratified**;
- the M45 work-package decomposition is **not ratified**;
- **M45-WP1 remains not authorized**, and neither is any other M45 work package;
- no gate state changes: `G-2` remains `RELEASED — FINAL RECORDING PENDING
  AUTHORIZED VEHICLE`, `G-3` remains `OPEN — PARTIAL`, `G-4` remains `OPEN`,
  `G-5` remains `OPEN`, and the historic M44 checkpoint remains `STOP`;
- M44 remains `COMPLETE AND FROZEN` and unmodified.

The corrected corpus is nonetheless a substantial advance on the reviewed
original. Both `BLOCKING` findings are resolved structurally rather than
rhetorically, and the two remaining `MAJOR` findings are of a different and
lesser kind: `N-1` is a missing entry condition in an otherwise sound chain, and
`N-2` is an accuracy defect in a compliance section whose substantive
commitments are correct. Both are correctable within documentary planning scope
and neither requires a new governance act.

## 15. Required next action

1. The candidate author issues an additive corrections response addressing
   `N-1`, `N-2`, and `N-3`, with `A-6` and `A-7` dispositioned, and revises both
   planning artifacts accordingly. The response must not declare the findings
   resolved.
2. A second focused independent re-review covers exactly the scopes named in
   `N-1`, `N-2`, and `N-3`, plus any downstream inconsistency those corrections
   create. `F-1` … `F-10` need not be re-tested except where a new correction
   touches their sections — in particular, any change to roadmap §5, §6, or §8
   must be re-checked against `F-1` and `F-5`.
3. Only if that re-review returns approval with unresolved `BLOCKING`, `MAJOR`,
   and `MINOR` findings all `NONE` may independent confirmation proceed, and
   only then ratification, then joint architecture freeze of both files by
   content identity, and then — as a separate act — WP1 authorization.

This record performs none of those acts and authorizes none of them. M45 remains
not ratified and M45-WP1 remains unauthorized.
