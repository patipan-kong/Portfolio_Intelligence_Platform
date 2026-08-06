# M46 — Independent Planning Corpus Review

**Artifact class:** Independent planning corpus review record
**Lifecycle stage:** Independent review of the complete M46 planning corpus
**Reviewer role:** M46 Independent Planning Corpus Reviewer, exercising the independent-review role constituted by [allocation §8](../governance/M46_CORPORATE_ACTION_PORTFOLIO_ACCOUNTING_PLANNING_ALLOCATION_RECORD.md)
**Planning mandate:** [M46 Planning Allocation / Commissioning Record](../governance/M46_CORPORATE_ACTION_PORTFOLIO_ACCOUNTING_PLANNING_ALLOCATION_RECORD.md)
**Review date:** 2026-08-05
**Review disposition:** `REQUIRES CORRECTION`
**Implementation authority:** `NONE`
**Work-package allocation or authorization:** `NONE`

---

## 1. Review authority

This record is a new, first-hand Independent Planning Corpus Review. It is not
a reconstruction, a persistence of a prior review, or a restatement of another
actor's findings. Every finding below was reached by this review, directly
against the current planning corpus and the repository authorities that corpus
cites.

### 1.1 Role and independence

The reviewer acts solely in the independent-review role constituted by
[allocation §8](../governance/M46_CORPORATE_ACTION_PORTFOLIO_ACCOUNTING_PLANNING_ALLOCATION_RECORD.md),
which requires independence from candidate and correction authorship and
permits the issuance of findings and one disposition only. The reviewer is
independent of:

- the M46 planning allocation authority;
- the M46 architecture candidate author;
- the M46 Planning Candidate Correction Author;
- the M46 second-candidate (roadmap) author;
- the M46 Planning Corpus Correction Author; and
- any confirmation authority.

### 1.2 Acts not performed

This review does not author, edit, or correct any reviewed artifact. It does
not perform correction, focused re-review, confirmation, ratification,
content-identity validation, freeze, closeout, work-package allocation,
work-package authorization, implementation, schema or runtime change,
migration, cutover, production correction, or release. It grants no authority.

### 1.3 Treatment of the prior reconstruction at this path

A prior artifact occupied this repository path and described itself as a
persisted historical record of a review whose reviewer prose was not
recoverable. It has been constitutionally determined insufficient, because
review evidence must issue from the review act itself. Its exact identity is
recorded here so that its supersession is auditable rather than silent:

| Superseded artifact at this path | Lines | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Prior reconstruction record | `285` | `13,557` | `BFF3EE94B630EB37B949F2E26B65A2B4CD69CF05479D1D6142F41A22125D117F` |

That artifact was read once, solely to confirm its character. Nothing in it
was reused as evidence, as a finding, as a severity, or as a disposition. The
findings below carry new identifiers in the `M46-IPCR-Fn` series precisely so
that they cannot be confused with the unanchored `M46-PCR-Fn` identifiers
discussed in §6.4.

## 2. Scope

### 2.1 In scope

1. Constitutional authority: whether the corpus derives its mandate correctly
   and asserts no authority it does not hold.
2. Planning corpus completeness against [allocation §7](../governance/M46_CORPORATE_ACTION_PORTFOLIO_ACCOUNTING_PLANNING_ALLOCATION_RECORD.md).
3. Architecture / roadmap consistency: package inventory, purposes,
   dependency edges, gates, entry and exit boundaries.
4. Identity model; accounting model; replay model; quote model; migration
   model.
5. Dependency graph acyclicity and constitutional sequencing.
6. Work-package decomposition and its authority preconditions.
7. Acceptance vectors and their genericity.
8. Authority boundaries and implementation separation.
9. Independent verification of every repository authority the corpus relies
   upon for a load-bearing determination.

### 2.2 Out of scope

This review does not evaluate source code, production data, the BANPU
incident, or any owner-domain artifact on its own merits. It evaluates the
corpus's *characterization* of those artifacts against their actual text.

### 2.3 Method

Each load-bearing claim was traced to the cited repository artifact and read
at the cited location. Mechanical validation (local links, anchors, content
identity, structure) was performed and is reported in §12. Where the corpus
asserts a status for another artifact — `frozen`, `unresolved`, `absent`,
`available` — that status was checked against the artifact itself and against
the governance record that would establish it.

## 3. Corpus identities reviewed

Reviewed at these exact working-tree identities:

| # | Artifact | Lines | Bytes | SHA-256 |
| --- | --- | ---: | ---: | --- |
| 1 | [M46 Planning Allocation / Commissioning Record](../governance/M46_CORPORATE_ACTION_PORTFOLIO_ACCOUNTING_PLANNING_ALLOCATION_RECORD.md) | `296` | — | recorded by its own act |
| 2 | [M46 Architecture and Implementation Plan](M46_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) | `1654` | `91,526` | `D564405C3B976A1960548D77F33CC5FECA9C2C10FCD7995F7D404F1D098DECB5` |
| 3 | [M46 Architecture Corrections Response](M46_ARCHITECTURE_CORRECTIONS_RESPONSE.md) | `116` | `11,224` | `1DE8DD0D0F8256EAC5708689C84457E24BD8C041A220431DD7D93B034B7EFA29` |
| 4 | [M46 Planning Corpus Supplementary Correction Record](M46_PLANNING_CORPUS_SUPPLEMENTARY_CORRECTION_RECORD.md) | `163` | `12,342` | `EB377D68EA117CEC0AEFFEE832503A1E805582ECB041D3249B7EA73F88814D9E` |
| 5 | [M46 Work-Package Decomposition and Roadmap](M46_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md) | `840` | `49,580` | `7F4C288206F3CB123742E95A1B58E3AA378E6033A89FA2D8BD992F807D18AE3C` |

Two content-identity claims made by the corpus were independently recomputed
and **verify exactly**:

- the architecture identity asserted by [Supplementary Correction Record §3](M46_PLANNING_CORPUS_SUPPLEMENTARY_CORRECTION_RECORD.md)
  (`1654` lines, `D564405C…098DECB5`); and
- the corrected roadmap identity asserted by [Supplementary Correction Record §8](M46_PLANNING_CORPUS_SUPPLEMENTARY_CORRECTION_RECORD.md)
  (`7F4C2882…18AE3C`).

The historical architecture identity `8C48A812…8227139` recorded by
[Corrections Response §6](M46_ARCHITECTURE_CORRECTIONS_RESPONSE.md) is
superseded and cannot be reverified from the working tree. Its supersession is
correctly and narrowly scoped by the Supplementary Correction Record §5.

## 4. Executive conclusion

The M46 planning corpus is architecturally strong and constitutionally
disciplined. Its identity model, accounting model, replay model, quote model,
failure model, and migration model are internally coherent, generic, and
consistent with the platform constitution. Its authority hygiene is unusually
good: implementation, work-package, runtime, migration, cutover, and release
authority are declared `NONE` in every artifact, and no reviewed sentence
grants an authority the corpus does not hold. Architecture and roadmap are in
exact parity on package inventory, purposes, dependency edges, and gates.
BANPU appears only as a parameterized acceptance vector, as required.

The corpus is nonetheless **not fit to proceed to independent confirmation**,
for a reason that recurs in two places and is the same reason both times: the
corpus asserts the *governance status of other domains' artifacts* without
having verified those artifacts against the repository record.

- It declares structural-event adjudication ownership `UNRESOLVED` and hard-
  blocks three of eight work packages, when the repository already contains an
  expressly recorded reconciliation of exactly that conflict, and when the
  question is in any case answered upward at constitutional level 1
  (`M46-IPCR-F1`, Major).
- It correctly records that Ledger & Accounting has no present authoring path
  for WP4, but does not apply the same test to Asset Foundation, whose
  owner-domain lifecycle closed on 2026-08-04 recording `SUCCESSOR AUTHORITY:
  NONE` — leaving WP3, the sole predecessor of both WP4 and WP6, presented as
  reachable when its authoring path is not established (`M46-IPCR-F2`, Major).

Neither finding is a design defect. Both are evidence defects, and both are
correctable additively without touching the architecture's semantics, package
definitions, dependency model, or authority boundaries. Three Minor and one
Editorial finding follow.

**Disposition: `REQUIRES CORRECTION`.**

## 5. Findings

Six findings are issued: one Critical (`NONE`), two Major, three Minor, one
Editorial.

### 5.1 Critical

`NONE.`

No finding of this review alleges that the corpus grants an authority it does
not hold, permits an unsafe act, transfers owner-domain ownership, amends a
frozen predecessor, or would allow a wrong action to proceed. Both Major
findings are over-restrictive or under-evidenced, not permissive.

### 5.2 Major

#### `M46-IPCR-F1` — the §2.1.1 `UNRESOLVED` G4 determination misstates the repository record and blocks WP2–WP4 on a premise the repository contradicts

**Severity:** `Major`

**Subject:** [Architecture §2.1.1](M46_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md),
and every dependent statement: §2.3, §5.1 ownership matrix row 2, §5.2A, §5.3,
§8.3, §8.4 step 1, §12.1 row 1, §15 WP1–WP2, §16.3 G1, §19, §22; and
[roadmap](M46_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md) §2, §4 assumption 6,
§5 decision node `O`, §7 WP2 row, §8.1–§8.2, §12 item 4, §15, §18, §19 item 1.

**What the corpus asserts.** Architecture §2.1.1 states that
[asset_foundation.md](../architecture/asset_foundation.md) §§3.4 and 4.4 and
[CORPORATE_ACTION_DOMAIN.md](../architecture/CORPORATE_ACTION_DOMAIN.md) §§1–4
conflict on structural-event adjudication ownership; that this candidate
"does not silently select either answer"; that a *future* competent governance
act "MUST record one of the two G4-compliant outcomes"; and that "until that
reconciliation exists, structural-event adjudication ownership and ownership of
the both-or-neither guarantee are `UNRESOLVED`".

**Repository evidence.**

1. The reconciliation already exists and is already recorded, in the same
   document the candidate cites as one party to the conflict.
   [asset_foundation.md](../architecture/asset_foundation.md) §3, third
   load-bearing decision, states: *"Corporate Actions is not a bridge domain —
   it is interpretation homed here, consequences exported… Under the
   nine-domain constitution there are no bridge domains: every concept has
   exactly one home… What the level-4 document calls a bridge is,
   constitutionally, one subdomain with two well-behaved boundary crossings
   (§4.4). Nothing in that document's discipline changes; only its address
   does."*
2. The same document's governance section makes the reconciliation explicit
   and records it as such. [asset_foundation.md](../architecture/asset_foundation.md)
   §9: *"One alignment note is recorded rather than hidden:
   CORPORATE_ACTION_DOMAIN.md's self-description as a standalone 'bridge
   domain' is superseded by §3's homing of structural-event interpretation
   inside Asset Foundation; its interior discipline is unchanged and remains
   binding at level 4."* This is precisely the first of the two G4-compliant
   outcomes — the lower artifact brought into conformance, and the
   reconciliation recorded.
3. The two artifacts are not peers. [asset_foundation.md](../architecture/asset_foundation.md)
   §9 and its header place it at **level 2** and place
   CORPORATE_ACTION_DOMAIN.md at **level 4** as a technical design bound by it
   under rule G2. Under [platform_architecture.md](../architecture/platform_architecture.md)
   §11 G2, a level-4 artifact "may never relax a law, reinterpret a boundary,
   or carve an exception" — it cannot assert a competing ownership intent
   against the level above it.
4. The question is in any case answered upward at **level 1**, independent of
   asset_foundation.md's ratification status.
   [platform_architecture.md](../architecture/platform_architecture.md) §5
   enumerates nine domains and contains no Corporate Action domain; §6.1
   assigns Asset Foundation the responsibility of *"adjudicating identity
   evidence — symbols, listings, renames, corporate restructurings — into
   identity facts"*; and §6.4 assigns Connectivity & Ingestion the proposal
   and review pipeline the candidate relies on. G4 itself directs that a
   conflict be *resolved upward*, which is the operation the candidate
   declined to perform.
5. [ROADMAP.md](../architecture/ROADMAP.md) Phase 3 lists "Corporate Actions"
   under the **Asset Foundation** heading, not as a separate domain — further
   repository evidence of the same homing.

**Why this is a defect.** The candidate cites §§3.4 and 4.4 of
asset_foundation.md while omitting §3's dispositive homing paragraph and §9's
express supersession note. On that partial reading it declares an
`UNRESOLVED` state and imposes a hard block on M46-WP2, M46-WP3, M46-WP4 and
"every M46 admission". A planning corpus whose declared method is exact
repository evidence must not derive a blocking determination from a selective
reading of the very document it cites. The consequence is real: WP2–WP4 are
three of eight packages and sit upstream of WP5–WP8, so the corpus currently
represents the entire M46 path as gated on an act that has, in substance,
already occurred.

**What genuinely remains open.** There is a real residual, and it is narrower
than the candidate states. [asset_foundation.md](../architecture/asset_foundation.md)
is marked *"Status: draft, pending ratification"* and becomes a level-2 Domain
Constitution only upon ratification; and CORPORATE_ACTION_DOMAIN.md's own text
still describes itself as a bridge "owning neither", conformed by §9's note
rather than by its own revision. The truthful requirement is therefore
**ratification of the recorded reconciliation and/or textual conformance of the
level-4 document**, not a fresh reconciliation of a conflict already recorded.

**Required correction.**

1. Restate §2.1.1 against the complete record: cite asset_foundation.md §3 and
   §9, platform_architecture.md §5, §6.1 and §11 G2/G4, and ROADMAP.md Phase 3.
2. Replace the `UNRESOLVED` ownership determination with the determination the
   evidence supports, or state precisely why the recorded reconciliation is
   held insufficient, citing its text.
3. Reduce the WP1 / G1 precondition to the genuine residual (ratification
   status and level-4 textual conformance) and restate the WP2–WP4 block
   accordingly.
4. Propagate the corrected determination to every dependent location listed
   under **Subject** above, in both artifacts, so that architecture and roadmap
   remain in parity.

This review takes no position on whether Asset Foundation *should* own the
adjudication. It finds only that the corpus's account of what the repository
currently records is wrong, and that the resulting block is asserted on a
false premise.

#### `M46-IPCR-F2` — WP3 presumes an available Asset Foundation authoring path; the Asset Foundation owner-domain lifecycle closed with `SUCCESSOR AUTHORITY: NONE`

**Severity:** `Major`

**Subject:** [Architecture §15](M46_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
WP3 row and the paragraph following the work-package table; §16.2; §16.3 G2–G3;
[roadmap](M46_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md) §6 milestone `M3`, §7
`M46-WP3` row, §8.3 dependencies and entry criteria, §15.

**What the corpus asserts.** Architecture §15 lists WP3's principal
dependencies as "WP1–WP2; frozen AF-1/AF-2 supply; Asset Foundation authority",
and its candidate exit evidence as an "Asset Foundation-owned contract or
explicit owner-domain block". Roadmap §8.3 requires "Asset Foundation
allocation and authorization for the bounded contract" as an ordinary
dependency. Neither artifact records any impediment to obtaining that
authority.

By contrast, the corpus does apply exactly this test to Ledger & Accounting.
Architecture §15, immediately after the table, records that the
[Ledger Owner-Domain Final State](../governance/LEDGER_ACCOUNTING_OWNER_DOMAIN_FINAL_STATE.md)
"records no remaining governance obligation and grants no implementation
authority. M46-WP4 therefore has no present authoring path", and requires a new
competent governance act. Roadmap §4 assumption 7, §7 WP4 row, §8.4 and §15
carry the same stop.

**Repository evidence.**

1. [ASSET_FOUNDATION_AF_WP4_CLOSEOUT_RECORD.md](../governance/ASSET_FOUNDATION_AF_WP4_CLOSEOUT_RECORD.md)
   §5 states that the closeout does not "create downstream implementation or
   intake authority" and does not "create successor authority, successor
   allocation, or successor authorization".
2. The same record's §7 final disposition states, in terms:
   `DOWNSTREAM AUTHORITY: NONE`, `SUCCESSOR AUTHORITY: NONE`, and "No authority
   beyond governance completion is granted by this record."
3. [DECISION_LOG.md](../engineering/DECISION_LOG.md), entry dated 2026-08-04,
   records that "Asset Foundation Planning and AF-WP1 through AF-WP3 are
   `COMPLETE`, `FROZEN`, and `CLOSED`" and AF-WP4 is "`COMPLETE`, `FROZEN`,
   `RELEASE ATTESTED`, and `CLOSED`".
4. This state predates the M46 allocation (2026-08-05) and was therefore
   available to the corpus.

**Why this is a defect.** The Asset Foundation owner-domain governance
lifecycle is in a terminal posture structurally analogous to Ledger &
Accounting's, and the corpus's own reasoning — accepted in the correction chain
as `M46-R-F9` — requires that a package whose authoring path does not presently
exist say so. WP3 is not a peripheral package: architecture §16.2 and roadmap
§5 both make WP3 the sole M46 predecessor of WP4 and WP6, so a WP3 whose
authority is unestablished silently propagates to four downstream packages. The
asymmetry also weakens the corpus's credibility on the point it gets right: a
reader cannot tell whether the WP4 stop reflects a general rule or a single
observed case.

**Required correction.**

1. Record the current Asset Foundation owner-domain state, with citation, in
   architecture §2.2 and §15 and roadmap §4 and §8.3.
2. Either establish that a present Asset Foundation authoring path exists —
   citing the record that supplies it — or state that WP3, like WP4, requires a
   new competent governance act establishing successor owner, role, scope, and
   documentary authority, and is otherwise blocked.
3. Propagate the consequence to WP4 and WP6 entry conditions and to the roadmap
   dependency matrix and allocation checkpoints, preserving architecture /
   roadmap parity.
4. State the rule generally, so that any owner domain in a closed or terminal
   posture is treated the same way.

### 5.3 Minor

#### `M46-IPCR-F3` — the frozen Asset Foundation predecessor inventory is incomplete

**Severity:** `Minor`

**Subject:** [Architecture §2.2](M46_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md);
[roadmap §2](M46_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md) and §8.1/§8.3
predecessor lists.

**Evidence.** Architecture §2.2 cites the AF-WP1 and AF-WP2 freeze records and
the AF-1 canonical lexical form only. The repository additionally records
AF-WP3 as `COMPLETE`, `FROZEN`, `CLOSED` — its frozen output being the AF-3
Owner Evidence Manifest and Conformance-Annex Index
([AF-WP3 Freeze Record](../governance/ASSET_FOUNDATION_AF_WP3_FREEZE_RECORD.md),
[AF-WP3 Closeout Record](../governance/ASSET_FOUNDATION_AF_WP3_CLOSEOUT_RECORD.md))
— and AF-WP4 as `COMPLETE`, `FROZEN`, `RELEASE ATTESTED`, `CLOSED`
([AF-WP4 Freeze Record](../governance/ASSET_FOUNDATION_AF_WP4_FREEZE_RECORD.md),
[AF-WP4 Release Attestation](../governance/ASSET_FOUNDATION_AF_WP4_RELEASE_ATTESTATION.md)).

**Why this is a defect.** Roadmap §8.1 makes "frozen-predecessor identity
verification" a WP1 deliverable and §9 item 6 makes an unresolved frozen
predecessor an entry blocker. A predecessor inventory that omits two frozen,
closed packages of the very owner domain WP3 depends on cannot discharge that
duty, and AF-3 is on its face relevant evidence supply for WP1 and WP3.

**Required correction.** Extend the frozen-predecessor inventory in both
artifacts to AF-WP3 and AF-WP4 with exact citations, and state what each does
and does not supply to M46.

#### `M46-IPCR-F4` — `G4` denotes two different things in the same corpus, sometimes without a disambiguator

**Severity:** `Minor`

**Subject:** [Architecture §2.1.1](M46_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md),
§12.1, §15, §16.3 items 2 and 5, §19;
[roadmap](M46_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md) §4 assumption 6, §5,
§7 `M46-WP7` row, §8.7, §12 item 4, §18.

**Evidence.** The corpus uses `G4` for the constitution's conflict rule
([platform_architecture.md](../architecture/platform_architecture.md) §11,
"Conflict is a defect, resolved upward") and, independently, for its own
fifth gate (architecture §16.3 item 5, "Replay/quote/performance gate"). Both
senses appear in both artifacts. Several occurrences carry no disambiguator:
roadmap §7's `M46-WP7` row — "Cannot start when: G4 evidence, exact WP5/WP6
identities, or the baseline is incomplete" — reads as the gate, while §12 item
4's "G4 conflict and Ledger successor-authority stops" reads as the rule, and
§18's risk table uses both senses in adjacent rows.

**Why this is a defect.** The corpus's method is exactness, and its gates are
the mechanism by which future allocation and authorization acts are judged. A
gate identifier that collides with a constitutional rule identifier invites a
future authorizing actor to check the wrong condition. It also degraded the
readability of the very WP7 row that a prior correction act had to repair.

**Required correction.** Rename the M46 gate series so it cannot collide (for
example `M46-G0`…`M46-G7`), or qualify every occurrence of both senses at
point of use. Apply the change identically in both artifacts.

#### `M46-IPCR-F5` — the corpus states two different next constitutional acts

**Severity:** `Minor`

**Subject:** [Architecture §16.1 and §22](M46_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md);
[roadmap §21](M46_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md);
[Supplementary Correction Record §10](M46_PLANNING_CORPUS_SUPPLEMENTARY_CORRECTION_RECORD.md).

**Evidence.** The architecture header, §16.1 and §22 and the roadmap header and
§21 all state that the next constitutional act is **Independent Planning Corpus
Review**. The Supplementary Correction Record §10 states, in capitals, that the
next constitutional act is **Focused Independent Planning Corpus Re-review**.
The two candidate artifacts and the most recent correction record therefore
disagree on the corpus's own lifecycle position.

**Why this is a defect.** A planning corpus that will be handed to a
confirmation authority must state one lifecycle position. Under the governing
constitutional determination that no valid repository Independent Planning
Corpus Review existed, the candidates' statement was the correct one and the
Supplementary Correction Record's was not; but the corpus should not require an
external determination to resolve which of its own artifacts to believe.

**Required correction.** Reconcile the next-act statement across all three
artifacts against the disposition of this review, and record the correction
additively rather than by editing the historical records' rationale.

### 5.4 Editorial

#### `M46-IPCR-F6` — list-conjunction defects introduced at correction seams

**Severity:** `Editorial`

**Subject and evidence.** In
[the architecture](M46_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md):

- §1.1: item 9 ends "…without issuer-specific engine branches; and" while items
  10, 11 and 12 follow, so the terminal conjunction sits three items early;
- §1.2: the bullet "realized and unrealized profit or loss inputs; and" is
  followed by a bullet also ending "; and", then by "downstream regeneration
  boundary." — two terminal conjunctions in one list; and
- §7.3: the bullet ending "…its exact quantity and total-basis instruction
  controls; and" is followed by a bullet also ending "and", then by the
  residue-rule bullet — the same defect.

Each occurs where the correction act inserted an item into an existing list.
No meaning is ambiguous, and nothing normative is affected.

**Required correction.** Repair the conjunctions so each list carries exactly
one terminal "and".

## 6. Constitutional assessment

### 6.1 Mandate and authority hygiene — `CONFORMING`

Both candidates cite the M46 allocation as their sole M46 planning mandate, as
[allocation §12](../governance/M46_CORPORATE_ACTION_PORTFOLIO_ACCOUNTING_PLANNING_ALLOCATION_RECORD.md)
item 1 requires. Both are marked `REVIEW CANDIDATE` with implementation
authority `NONE`, satisfying item 5. Every reviewed artifact declares `NONE`
for implementation, work-package allocation and authorization, runtime, schema,
migration, cutover, production correction, and release authority. This review
found no sentence in the corpus that grants, implies, or could be read as
granting any of those. All eight proposed packages are stated `UNALLOCATED` and
`UNAUTHORIZED` in both artifacts.

### 6.2 Domain ownership — `CONFORMING`, subject to `M46-IPCR-F1` and `M46-IPCR-F2`

The ownership matrix (architecture §5.1) is consistent with
[platform_architecture.md](../architecture/platform_architecture.md) §6.1–§6.5:
identity to Asset Foundation, observations to Market Intelligence, financial
truth to Ledger & Accounting, the admission pipeline to Connectivity &
Ingestion, derived measures to Portfolio Intelligence. M46 is correctly framed
as a coordinating initiative and not a constitutional domain, matching
[allocation §6](../governance/M46_CORPORATE_ACTION_PORTFOLIO_ACCOUNTING_PLANNING_ALLOCATION_RECORD.md).
No reviewed statement transfers ownership. The two Major findings concern the
corpus's account of ownership *status*, not its allocation of ownership.

### 6.3 Human sovereignty and the ingestion gate — `CONFORMING`

Architecture §2.3, P3, P4, §5.1, §8.4 and §13.3 route every externally derived
consequence through the Connectivity & Ingestion pipeline and require either an
explicit, specific, versioned, auditable and revocable standing policy or human
confirmation. This matches
[platform_architecture.md](../architecture/platform_architecture.md) §6.4
("human-confirmed by default, auto-accepted only under explicit, revocable,
per-source delegation") and
[asset_foundation.md](../architecture/asset_foundation.md) §4.4 item 3 and §7.7
("the domain never holds a privileged pen"). Architecture §8.4 item 9 and
§12.1's admission-failure row make the failure path inert.

### 6.4 Provenance of the `M46-PCR-Fn` finding identifiers — recorded, not found against

Two artifacts in the corpus respond to findings `M46-PCR-F1` and `M46-PCR-F2`
attributed to an Independent Planning Corpus Review for which no valid
repository record exists. This review does not raise that as a finding against
the candidates: the governing constitutional determination already addresses
it, and re-litigating it would exceed this review's role. It is recorded here
for the confirmation authority's benefit, together with this reviewer's
independent verification of the substance:

- the identity discrepancy that `M46-PCR-F1` describes is real and is correctly
  and narrowly reconciled by the Supplementary Correction Record §§3–5, whose
  SHA-256 claims this review recomputed and verified; and
- the WP7 defect that `M46-PCR-F2` describes is no longer present: roadmap §7's
  `M46-WP7` row now makes G4, WP5/WP6 identities and the baseline the start
  boundary, and G5 appears only as exit evidence in §8.7, in agreement with the
  matrix.

Both corrections therefore stand on independently verifiable ground regardless
of the provenance of the identifiers they answer.

### 6.5 Frozen predecessor preservation — `CONFORMING`, subject to `M46-IPCR-F3`

No frozen artifact is modified by any corpus artifact; the working tree
contains only the six untracked M46 files. The corpus's characterizations of
its cited predecessor contracts were checked individually:

| Cited as | Verified status | Evidence |
| --- | --- | --- |
| M39-WP6 Observation Identity | Frozen | [M39 Epic Closeout](M39_EPIC_CLOSEOUT.md) — "M39-WP1 through M39-WP6 are complete, canonically represented, and frozen" |
| M41-WP2 / M41-WP3 Stage B contracts | Confirmed; carried as frozen authority by downstream M41 records | [M41-WP2 Stage B Confirmation](M41_WP2_STAGE_B_INDEPENDENT_CONFIRMATION.md), [M41-WP3 Closeout](M41_WP3_CLOSEOUT.md) |
| M42-WP2 Accounting Scope / Base Currency | Frozen | [M42 Epic Closeout](M42_EPIC_CLOSEOUT.md), [M42-WP2 Closeout](M42_WP2_CLOSEOUT.md) |
| M43-WP3 Analytics Input Manifest | Frozen | [M43 Epic Closeout](M43_EPIC_CLOSEOUT.md) — milestone `COMPLETE AND FROZEN` |
| AF-1 canonical lexical form | Frozen | [AF-WP1 Freeze Record](../governance/ASSET_FOUNDATION_AF_WP1_FREEZE_RECORD.md) |
| Ledger & Accounting planning corpus and final state | Frozen; LA-WP2 terminal, LA-WP3–LA-WP7 unauthorized | [Ledger Owner-Domain Final State](../governance/LEDGER_ACCOUNTING_OWNER_DOMAIN_FINAL_STATE.md) §2 |
| M45 `ACTIVE — WAITING FOR EXTERNAL SUPPLY` | Accurate | [M45 Milestone Status Record](M45_MILESTONE_STATUS_RECORD.md) |

Several of these specification files carry stale in-file status headers that
predate their freeze records; the corpus's "frozen" characterization is
nevertheless correct against the governing closeout and freeze records, and no
finding is issued. The gap addressed by `M46-IPCR-F3` is inventory
completeness, not mischaracterization.

### 6.5.1 Line-range citations

The allocation record's line-range citations into
[platform_architecture.md](../architecture/platform_architecture.md) (Laws
69–111; §6.1 at 175–185; §6.3 at 203–213; §6.4 at 217–227; §6.5 at 231–241) and
into [ROADMAP.md](../architecture/ROADMAP.md) (Phase 3 at 136–160) were read at
those exact lines and are accurate.

### 6.6 Implementation separation — `CONFORMING`

Architecture §3 and roadmap §20 enumerate non-goals that exclude code, schema,
migration, runtime, provider, cutover, release, and closeout acts. Roadmap
§§15–16 keep allocation and authorization distinct and state the cascade
explicitly: documentary authorization does not authorize code; implementation
authorization does not authorize runtime; no-write authorization does not
authorize migration; migration does not authorize cutover; cutover does not
authorize release. This is the correct reading of
[allocation §9](../governance/M46_CORPORATE_ACTION_PORTFOLIO_ACCOUNTING_PLANNING_ALLOCATION_RECORD.md).

### 6.7 Constitutional sequencing — `CONFORMING`, subject to `M46-IPCR-F5`

The lifecycle in architecture §16.1 and roadmap §§12–14 preserves the
allocation §8 role separation and never permits an actor to accept its own
corrections. Roadmap §9 item 8 explicitly forbids self-review and
self-confirmation. The only sequencing defect found is the divergent next-act
statement recorded as `M46-IPCR-F5`.

## 7. Architecture assessment

### 7.1 Identity model — `SOUND`

Permanent `asset_id` with effective-dated external identifiers (§6.1–§6.2), the
symbol-change rule producing zero accounting effect (§6.3), the transformation
rule requiring adjudication rather than substitution (§6.4), and fail-closed
identity behaviour with no current-symbol fallback (§6.5) are correct and are
consistent with [ASSET_REGISTRY.md](../architecture/ASSET_REGISTRY.md) §3 and
[asset_foundation.md](../architecture/asset_foundation.md) §§3.1, 3.5. The
invariant that resolution at time `t` requires a unique decisive binding whose
interval contains `t` is exactly stated, and the interval convention is
correctly deferred to the owner (§6.2, Open Question 4).

### 7.2 Accounting model — `SOUND`

The nine-effect algebra (§7.2) is closed, platform-owned and free of market
taxonomy; the normalization matrix (§7.4) maps every listed event story into it
without an issuer branch. The separation of total cost basis as replay state
from average cost as a derived read value (P6, §7.3, §10.3) is correct and is
the right prevention for the failure it names. The cost-basis invariants close
exactly, and §7.3's refusal to guess an allocation from post-event prices or a
desired average-cost result is the correct fail-closed posture. The
single-cash-scalar treatment (§5.2D, §7.1, Open Question 12) correctly declines
to redefine Base Currency and is consistent with the
[M42-WP2 contract](M42_WP2_PORTFOLIO_IDENTITY_ACCOUNTING_SCOPE_MEMBERSHIP_AND_BASE_CURRENCY_CONTRACT_SPECIFICATION.md).

### 7.3 Performance continuity — `SOUND AND CORRECTLY EVIDENCED`

P13, §7.4 and §11.5 assert that a structural event produces zero investment
return by itself, and that the frozen return contract has no corporate-action
continuity term. This reviewer verified the underlying claim directly:
[PORTFOLIO_CALCULATION_RULES.md](../investment/PORTFOLIO_CALCULATION_RULES.md)
defines `net_external_cash_flow`, `imported_asset_value` and
`manual_adjustment_value` as the only strip terms, and contains no
corporate-action or split continuity term. The candidate's prohibition on
routing a structural effect through one of those unrelated strips, its refusal
to invent a second return formula, and its explicit `UNCOMPUTABLE` fail-closed
state are correct. This is the corpus's strongest piece of independent
verification work, and it is consistent with
[CORPORATE_ACTION_DOMAIN.md](../architecture/CORPORATE_ACTION_DOMAIN.md) §3,
which states that a split must have "*zero* performance effect — any design in
which a split moves a return number is wrong by definition."

### 7.4 Replay model — `SOUND`

The single canonical Transaction stream (§9.1), the canonical ordering tuple
with immutable event identity as final tie-break (§9.2), the ten-step
projection algorithm (§9.3), the ledger semantic postconditions expressed as
postconditions rather than as a second stream (§9.4), and the replay invariants
(§9.5) are coherent and consistent with
[ADR-001](../decisions/ADR-001_TRANSACTION_LEDGER_SINGLE_SOURCE_OF_TRUTH.md),
[ADR-003](../decisions/ADR-003_TWO_TIMELINE_RULE.md) and
[ADR-005](../decisions/ADR-005_REPLAY_CORRECTNESS_BASELINE.md). The explicit
exclusion of Corporate Action Cases, proposal bundles and announcements from
replay input is correct, and Open Question 6 is properly narrowed so that no
answer can create a second stream. Open Question 13's preservation of the
`created_at` versus `transaction_date` distinction is accurate against
[PORTFOLIO_CALCULATION_RULES.md §2](../investment/PORTFOLIO_CALCULATION_RULES.md#2-time-attribution-policy).

### 7.5 Quote model — `SOUND`

The valuation request dimensions (§11.2), the conjunctive quote-binding
predicate (§11.3), the double-adjustment prohibition (§11.4) and the refusal of
related-security fallback are correct and preserve the M39/M41 boundaries
without redefining them. The distinction between Observation Identity and
Asset Foundation subject identity is correctly maintained.

### 7.6 Migration model — `SOUND`

Phases A–F (§14) are additive, prove-then-promote, and never rewrite history.
The partitioned shadow comparison — parity for unaffected portfolios,
pre-declared explained differences for affected ones, visible quarantine for
unresolved ones — is the right shape, and §14.4's statement that "different
from legacy is not automatically failure when the legacy result is the known
defect being corrected" is correctly paired with the ADR-005 baseline
requirement in §14.1.

### 7.7 Failure model — `SOUND`

The fifteen failure classes (§12.1) each carry a required behaviour, and §12.2
contains failures at the smallest truthful boundary. No class resolves to a
guess, a default, or a substitution.

## 8. Planning corpus assessment

### 8.1 Completeness — `COMPLETE`

Both artifacts named by
[allocation §7](../governance/M46_CORPORATE_ACTION_PORTFOLIO_ACCOUNTING_PLANNING_ALLOCATION_RECORD.md)
exist at their exact intended paths and were reviewed together. The
artifact-absence condition recorded by the earlier correction act is discharged
as a matter of fact.

### 8.2 Architecture / roadmap parity — `EXACT`

Independently verified by this review, not adopted from the corpus's own
verification table:

| Parity dimension | Result |
| --- | --- |
| Package identifiers and names | 8 of 8 identical between architecture §15 and roadmap §8.1–§8.8 |
| Package purposes | Roadmap expands without redefining; no purpose diverges |
| Dependency edges | 9 of 9 identical (`W1→W2`, `W2→W3`, `W2→W4`, `W3→W4`, `W3→W6`, `W4→W5`, `W5→W7`, `W6→W7`, `W7→W8`); the roadmap adds the external `Ledger successor act → W4` supply edge and the G4-reconciliation decision node, both correctly marked external rather than as M46 packages |
| Gate inventory | `G0`–`G7` preserved; roadmap entry criteria cite G0/G1/G2/G3/G4/G6 consistently with their architecture definitions |
| WP7 entry / exit | Matrix and detail agree: G4 entry, G5 exit; write and cutover are separate later authorities |
| Authority declarations | `NONE` in both, in identical scope |

### 8.3 Dependency graph — `ACYCLIC AND WELL-FORMED`

The graph is a DAG. Every package has at least one predecessor except WP1, and
WP1 depends only on the frozen planning corpus. Both permitted overlaps
(WP3/WP4 documentary coordination; WP6 alongside WP4/WP5) are conditioned on
stable frozen handoffs and separate authorizations, and neither creates a
cycle. External supply — the G4 reconciliation and the Ledger successor act —
is correctly modelled as supply rather than as M46 work.

### 8.4 Work-package decomposition — `SOUND`

Each package has a bounded objective, explicit scope, explicit exclusions,
named predecessors, deliverables, entry and exit criteria, review requirements,
and confirmation/freeze requirements. Roadmap §10's admission that a truthful
blocked result may be a terminal state but is not successor supply is
constitutionally correct and worth preserving verbatim through correction.

### 8.5 Acceptance vectors — `SOUND AND GENERIC`

Architecture §17 and roadmap §17 cover the required action families, the
cross-cutting identity/ordering/idempotency/basis/quote dimensions, the
confirmation-path negatives, and the migration and downstream cases. BANPU
appears only as a parameterized fixture whose terms must come from approved
evidence, and both artifacts require that no `BANPU` conditional, ratio,
exception, or alias exist in code or configuration. This satisfies
[allocation §10](../governance/M46_CORPORATE_ACTION_PORTFOLIO_ACCOUNTING_PLANNING_ALLOCATION_RECORD.md)
item 1. No issuer-, market-, jurisdiction-, broker-, or provider-specific rule
was found anywhere in the corpus.

### 8.6 Open questions — `VISIBLE AND OWNED`

All sixteen architecture open questions name an owner and a fail-closed
consequence, and roadmap §19 restates the deferred supply with the same
discipline. None can be silently defaulted during implementation. Open
Question 1 (vocabulary) correctly keeps M46 terms out of the
[Canonical Glossary](../GLOSSARY.md) pending owner review, satisfying
[platform_architecture.md](../architecture/platform_architecture.md) §12 rule
V1.

## 9. Recommendation

1. **Disposition: `REQUIRES CORRECTION`.** The corpus may not proceed to
   independent confirmation in its present state.
2. Correction of `M46-IPCR-F1` and `M46-IPCR-F2` is required before
   confirmation. Both are evidence corrections; neither requires architectural
   redesign, and this review expects no change to the effect algebra, identity
   model, replay model, quote model, migration phases, package inventory,
   dependency edges, or authority boundaries.
3. Correction of `M46-IPCR-F3`, `M46-IPCR-F4` and `M46-IPCR-F5` is required in
   the same act, since each affects a statement a future allocating or
   authorizing actor will rely on.
4. `M46-IPCR-F6` should be repaired in the same pass.
5. Corrections must be additive and must preserve architecture / roadmap parity
   on every propagated statement.
6. No correction may declare any finding of this review resolved. Only a
   competent focused independent re-review may determine that.
7. No work package may be allocated or authorized as a consequence of this
   review, of any correction answering it, or of the corpus's overall quality.

## 10. Scope limitations

1. This review evaluates documentary planning artifacts. It executed no code,
   ran no test, and inspected no production data.
2. It reviewed the corpus's characterization of other domains' artifacts, not
   the merits of those artifacts. Where a cited artifact's own header conflicts
   with its governing freeze or closeout record, this review followed the
   governance record and said so (§6.5).
3. The historical architecture identity `8C48A812…8227139` cannot be reverified
   from the working tree and is accepted as historical fact on the authority of
   the unchanged Corrections Response.
4. The superseded reconstruction previously at this path was read once to
   establish its character and is recorded at its exact identity in §1.3. Its
   content was not used as evidence and does not survive at this path; it
   remains referenced by the governance determination that set it aside.
5. This review takes no position on the substantive ownership of
   structural-event adjudication, on whether Asset Foundation should be granted
   a successor authoring path, or on any owner-domain decision. It reports only
   what the repository currently records.
6. Findings are limited to what repository evidence supports. Where this review
   could not establish a defect, it issued no finding rather than a caution.
7. This record grants no authority and changes no reviewed artifact.

## 11. Reviewer declaration

- **Acting role:** M46 Independent Planning Corpus Reviewer, exercising the
  independent-review role constituted by allocation §8.
- **Independence:** independent of the allocation authority, the architecture
  candidate author, the correction author, the second-candidate author, the
  supplementary correction author, and any confirmation authority. No part of
  the reviewed corpus was authored, edited, or corrected by this reviewer.
- **Basis:** every finding was reached first-hand from the current working-tree
  corpus and the repository authorities cited in each finding. No prior
  review's findings, severities, wording, or disposition were adopted,
  inherited, or assumed.
- **Completeness:** the whole corpus was read — all five artifacts in full —
  and every load-bearing external citation was opened and read at the cited
  location.
- **Acts performed:** reading, verification, finding, and disposition only.
- **Acts not performed:** authorship, correction, focused re-review,
  confirmation, ratification, content-identity validation, freeze, closeout,
  allocation, authorization, implementation, migration, cutover, production
  correction, and release.
- **Disposition issued:** `REQUIRES CORRECTION`.
- **Authority granted by this record:** `NONE`.
- **Implementation, runtime, schema, migration, cutover, production-correction,
  and release authority:** `NONE`.
- **Work-package allocation or authorization:** `NONE` — all eight proposed
  packages remain `UNALLOCATED` and `UNAUTHORIZED`.

## 12. Verification performed by this review

| Check | Result |
| --- | --- |
| Corpus read in full | `PASS` — 5 artifacts, 3,069 lines |
| Local link and anchor resolution across the reviewed corpus | `PASS` — 94 repository-local links, 26 anchors, 0 broken |
| Architecture content identity vs. Supplementary Correction Record §3 | `PASS` — recomputed `D564405C…098DECB5`, 1,654 lines |
| Roadmap content identity vs. Supplementary Correction Record §8 | `PASS` — recomputed `7F4C2882…18AE3C` |
| Architecture / roadmap package-name parity | `PASS` — 8 of 8 |
| Architecture / roadmap dependency-edge parity | `PASS` — 9 of 9; graph acyclic |
| WP7 entry/exit gate parity (matrix vs. §8.7) | `PASS` — G4 entry, G5 exit |
| Governing-source verification: platform_architecture §5, §6.1, §6.4, §11 G1–G6, §12 | `PASS` — read at source |
| Governing-source verification: asset_foundation §2, §3, §3.4, §4.4, §7.7, §9 | `FINDING` — see `M46-IPCR-F1` |
| Governing-source verification: CORPORATE_ACTION_DOMAIN §§1–4 | `PASS` — read at source |
| Governing-source verification: PORTFOLIO_CALCULATION_RULES strip terms and §2 | `PASS` — no corporate-action continuity term exists |
| Governing-source verification: ROADMAP Phase 3 Corporate Actions homing | `FINDING` — see `M46-IPCR-F1` |
| Predecessor status verification: M39, M41, M42, M43, AF-1, Ledger final state, M45 | `PASS` — see §6.5 |
| Predecessor inventory completeness: AF-WP3, AF-WP4 | `FINDING` — see `M46-IPCR-F3` |
| Owner-domain authority verification: Ledger successor path | `PASS` — corpus states it correctly |
| Owner-domain authority verification: Asset Foundation successor path | `FINDING` — see `M46-IPCR-F2` |
| Allocation line-range citation accuracy | `PASS` — all sampled ranges accurate |
| Authority audit across the corpus | `PASS` — no implementation, work-package, runtime, migration, cutover, or release authority granted anywhere |
| Frozen-artifact modification audit | `PASS` — no tracked or frozen file modified; working tree contains only untracked M46 files |
| `git diff --check` / `git diff --cached --check` | `PASS` |

## 13. Disposition and next constitutional act

**Review disposition: `REQUIRES CORRECTION`.**

**Findings:** Critical `0`; Major `2` (`M46-IPCR-F1`, `M46-IPCR-F2`); Minor `3`
(`M46-IPCR-F3`, `M46-IPCR-F4`, `M46-IPCR-F5`); Editorial `1`
(`M46-IPCR-F6`).

Because the disposition is `REQUIRES CORRECTION` and not `APPROVED` or
`APPROVED WITH MINOR FINDINGS`, independent confirmation may not proceed.

**Next constitutional act:** an additive correction act by the **M46 Planning
Candidate Correction Author** under
[allocation §8](../governance/M46_CORPORATE_ACTION_PORTFOLIO_ACCOUNTING_PLANNING_ALLOCATION_RECORD.md),
answering findings `M46-IPCR-F1` through `M46-IPCR-F6` against the exact corpus
identities recorded in §3. That act may not declare any finding resolved. It
must be followed by a **focused independent re-review** by an actor independent
of candidate and correction authorship, before independent confirmation,
ratification, content-identity validation, and freeze — each a separate later
act, none of which is performed, implied, or pre-approved by this record.
