# BANPU-WP5 — Mechanical Continuity Competent-Authority Determination

**Artifact class:** Bounded canonical competent-authority determination record
**Decision date:** 2026-08-14
**Issuing authority:** BANPU-WP5 Mechanical Continuity Competent-Authority Determination Authority
**Question resolved:** whether BANPU-WP5-level governance authority is competent to fix the `BANPU_WP5_WORK_PACKAGE_PLAN.md` §10.4 reconciliation formula (D2), inclusivity (D4), comparison-level rounding (D5), annotation-sufficiency threshold (D6), and enforcement locus (D7) — jointly, per the prior act's own finding that D7 cannot be separated from D2–D6 — and, if not, exactly what higher authority and act is required
**Governance outcome:** `OUTCOME C — FURTHER AUTHORITY REQUIRED FOR D2/D4/D5(comparison)/D6(threshold)/D7, JOINTLY; NO NEW FORMULA, OPERATOR, ROUNDING RULE, THRESHOLD, OR ENFORCEMENT CAPABILITY IS CREATED BY THIS ACT`
**New reconciliation formula or enforcement capability created:** `NONE`
**§10.4 blocker status after this act:** `NOT RESOLVED — AUTHORITY GAP NAMED PRECISELY; TWO DISTINCT REQUIRED ACTS IDENTIFIED (§9)`
**Implementation performed:** `NO`
**WPP amendment performed:** `NO`

---

## 1. Nature and boundary of this act

This act resolves only the question the invoking instruction poses first and
foremost: **what repository authority is actually competent** to fix the
BANPU-WP5 §10.4 mechanical-continuity reconciliation semantics (D2/D4/D5/D6)
and their enforcement locus (D7), given that the immediately preceding
governance decision
([`BANPU_WP5_MECHANICAL_CONTINUITY_RECONCILIATION_GOVERNANCE_DECISION.md`](BANPU_WP5_MECHANICAL_CONTINUITY_RECONCILIATION_GOVERNANCE_DECISION.md))
found these dimensions to be a genuine specification gap and referred them
without inventing content.

This act is additive. It modifies no frozen artifact, no Allocation Record,
no Implementation Authorization Record, and does not modify
`BANPU_WP5_WORK_PACKAGE_PLAN.md`. It performs no implementation, no test
edit, no Planning Confirmation, no Planning Freeze, no implementation review,
and no WP6/WP7/WP8 act. It stages, commits, and pushes nothing. It creates no
new formula, operator, rounding rule, annotation threshold, or enforcement
capability — those remain exactly as undetermined as the prior act left them.

The invoking prompt's characterization of the prior decision was not
accepted as authority; the prior decision's live content was independently
re-read this act (§3).

## 2. WP5 lifecycle state independently verified

Recomputed this act, under the same Git-canonical-LF/uppercase-SHA-256
convention used throughout the BANPU corpus:

| Artifact | Verified state |
|---|---|
| [`BANPU_WP5_ALLOCATION_RECORD.md`](BANPU_WP5_ALLOCATION_RECORD.md) | present, disposition `BANPU-WP5 ALLOCATED` |
| [`BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_RECORD.md`](BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_RECORD.md) | present, disposition `BANPU-WP5 IMPLEMENTATION AUTHORIZED`, `LIMITED` implementation authority per its own header |
| [`BANPU_WP5_WORK_PACKAGE_PLAN.md`](BANPU_WP5_WORK_PACKAGE_PLAN.md) | present, disposition `WORK PACKAGE PLAN MATERIALIZED — NOT APPROVED — IMPLEMENTATION NOT PERFORMED — NOT CONFIRMED — NOT FROZEN`; §10.4 re-read directly at lines 290–341 |
| [`BANPU_WP5_MECHANICAL_CONTINUITY_RECONCILIATION_GOVERNANCE_DECISION.md`](BANPU_WP5_MECHANICAL_CONTINUITY_RECONCILIATION_GOVERNANCE_DECISION.md) | present, disposition `PARTIAL`, re-read in full this act (§3) |

No BANPU-WP5 Planning Confirmation, Planning Freeze, or implementation
artifact exists. `git status` (§10) confirms no WP5 production or test file
in the Authorization Record's §4 surface has been touched by any act in this
session.

## 3. Prior §10.4 decision independently re-verified

The prior governance decision was re-read in full this act, not trusted from
the invoking prompt's summary. Its findings, confirmed accurate on
re-reading:

- D1 (operands) and D3 (tolerance source): `EXISTING AUTHORITY SUFFICIENT` —
  restatements of design §10 and the WP1 payload contract, not new decisions.
- D6's field-identity sub-question: `EXISTING AUTHORITY SUFFICIENT` — same
  basis.
- D2 (formula), D4 (inclusivity), D5's comparison-level precision/rounding,
  D6's annotation-sufficiency threshold and classification effect, and D7
  (enforcement locus): `GENUINE GAP — REFERRED`.
- §8 of that record established a **new structural finding**: no canonical
  artifact assigns any authorized, implemented, or implementable locus for a
  fail-closed "mechanical continuity failure" / "unannotated boundary
  discontinuity" consequence, because WP3's `QuarantineReason` enum
  deliberately excludes both and WP5's only then-inspected authorized
  surface (`manage.py`'s `verify_snapshots`) is read-only/non-blocking.
- §14 named the next act as "a governance-level determination, by an
  authority competent over the canonical design, roadmap, and package
  inventory... fixing the reconciliation formula and its enforcement locus
  together." This act is that determination — it does not skip past it to
  perform the fixing itself, because §5 below finds that no authority
  available to this act can lawfully do so.

## 4. `MINOR-2` authority chain (re-traced)

Independently re-traced this act via the same citation chain the prior act
established and this act re-confirmed by direct read, not by inference from
the prior act's summary: `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`
§16 → `BANPU_WP1_FREEZE_RECORD.md` §7 → `BANPU_WP1_CONFIRMATION.md` §5 →
`BANPU_WP1_RESIDUAL_IDENTITY_RECORD.md` → WP2/WP3 carry-forward →
`BANPU_WP3_REFERENCE_PRICE_ADMISSIBILITY_CLARIFICATION_RECORD.md` §9, which
independently (as WP3's own governance finding) states: *"The boundary
reconciliation of design §10 is WP5's, not WP3's. WP3 performs admissibility
checking only; it performs no tolerance comparison, no reconciliation, and no
continuity evaluation."*

This confirms WP5 as the correct **conceptual owner** of the reconciliation
determination. It does not by itself confirm that WP5's *current
authorization* extends to enforcing it — that is a distinct question, §5–§7
below.

## 5. Competent governance authority determination

### 5.1 The Roadmap cannot itself supply the missing semantics

`BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md` states its own authority
explicitly at its header: **"Authority: `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`"**
and **"It does not authorize implementation by itself and cannot change the
canonical design."** The Roadmap's WP5 section (§7) lists "Recognize
evidence-annotated suspension-gap return without 'repairing' it away" as
scope, but states no reconciliation formula, and its "Universal package
rules" (§1) confirm packages operate strictly within, and cannot expand,
canonical design content. The Roadmap is therefore **not** independently
competent to originate a new reconciliation formula; it can, at most, be the
document a design-level decision is subsequently reflected into (as it
already was for WP1–WP5's scope tables).

### 5.2 WP5's own governance/planning authority is not competent, and says so about itself

Three independent lines of evidence, each re-verified directly this act,
converge on the same conclusion:

1. **The Implementation Authorization Record's capability list is exhaustive
   and does not include reconciliation enforcement.** §3 of that record
   states "Implementation authority covers exactly these capabilities" and
   enumerates six items — classification, cash-in-lieu/P&L inclusion,
   rebuild-boundary refusal, pre-boundary preservation, suspension-gap-return
   recognition, and successor-identity emission. A mechanical-continuity
   **reconciliation-result-driven refusal** is not among them. §6 of the same
   record treats `MINOR-2` (WP5 half) only as a **pre-use tolerance-value
   admissibility gate** ("focused rejection tests before the tolerance value
   is consumed") — input validation, not comparison-result enforcement. This
   is authorization text, not roadmap forecast language, and it is exact and
   closed ("no other `manage.py` change is authorized... a different file or
   capability requires a distinct constitutional authorization; it cannot be
   inferred from the roadmap's 'expected files' language" — Authorization
   Record §4.2).
2. **The one fail-closed capability WP5 does hold is scoped to a different
   predicate.** WP5 is authorized to "refus[e] a full or pre-boundary rebuild
   before any write or provider fetch" (Authorization Record §3) — this is
   `POSITION_CONVERSION_REBUILD_BOUNDARY`, already `READY — FULLY
   DECOMPOSED` per WPP §8, and is a distinct predicate (whether a rebuild
   spans the transition boundary at all) from the §10.4 reconciliation
   (whether predecessor/successor reference prices agree within tolerance).
   Re-reading WPP §7 confirms `portfolio_rebuilder.py`'s only authorized
   fail-closed behavior is this boundary refusal; extending it to also
   enforce a mechanical-continuity comparison result would exceed "exactly
   these capabilities" — the Authorization Record's own limiting language.
3. **The WPP itself already anticipated and named this exact fork.** WPP
   §10.4 states verbatim: *"full satisfaction of WP5's `MINOR-2` half
   requires either a separate planning decision fixing the reconciliation
   formula, or a reviewer determination that the formula is out of WP5's
   authorized scope entirely and belongs to a distinct, not-yet-identified
   act."* This is not this act inventing a new escalation path — the WPP's
   own planning authority already recorded that WP5-level planning might not
   be the correct locus, without itself deciding which branch applies. This
   act performs that determination and finds the second branch applies for
   D2/D4/D5-comparison/D6-threshold, and — because D7 is inert without a
   fixed D2 (per the prior decision's own coupling finding) — for D7 as well.

### 5.3 Why D2 is unlike prior WP-level "fill the gap" precedent (WP1/WP3 admissibility functions)

WP1's payload validation and WP3's `assess_reference_price_admissibility()`
are themselves WP-level inventions not spelled out verbatim by the design,
yet they were not treated as requiring design-level authority. The
distinguishing factor, checked directly against both precedents this act:

- Both are single-field presence/finiteness/positivity/decimal-exactness
  tests. Their content is effectively dictated by the field's own declared
  type and the residual register's own wording ("reject negative or
  otherwise inadmissible") — there is no second, economically distinct,
  textually equally plausible reading of "admissible." PD-WP5-1 (already
  recorded, not reopened here) followed the identical pattern for exactly
  this reason.
- D2, by contrast, has at least three structurally different, economically
  non-equivalent readings (absolute difference; predecessor-denominated
  relative difference; successor-denominated relative difference; and the
  further open question of `R`-normalization) with **no textual tiebreaker**
  and a genuine risk, flagged by the prior decision's §7 and §9, that
  choosing wrongly could either mask a genuine mechanical defect or erase
  legitimate suspension-gap investment return. This is a difference in kind,
  not degree: it is an economically consequential accounting choice of the
  same character as design §5's equations (share/basis allocation) — the
  only other place in the entire corpus where the design fixes an equation
  for an economically consequential quantity, and it does so at the design
  document itself, never delegated to a WP-level artifact.

### 5.4 Why the WP4 Retry-Order "Outcome 2" precedent does not extend here

`BANPU_WP4_RETRY_ORDER_GOVERNANCE_DECISION.md` is the corpus's one existing
example of a **governance-level** (not plain WP-planning-level) actor
proposing a bounded canonical amendment ("`OUTCOME 2 — BOUNDED CANONICAL
AMENDMENT REQUIRED`," issued by a "BANPU-WP4 Canonical Governance
Authority," selecting "`ALTERNATIVE C — BOUNDED RETRY PREFLIGHT`" as a
proposed, not-yet-binding candidate pending independent approval and Work
Package Plan reapproval). This was examined this act as the closest
available precedent for an "Outcome B" path here, and distinguished:

- That act resolved a **runtime-ordering conflict between two already-frozen
  requirements** discovered during Independent Implementation Review
  (`WP4-IIR-B1`) — first-application optimistic validation vs.
  post-materialization retry idempotency. Both constraints were already
  canonical; the task was reconciling their interaction, which has a
  narrowly bounded, engineering-determinable answer (an ordering choice)
  once both constraints are held fixed.
- D2 here is not a conflict between two already-fixed constraints; it is the
  **absence of any constraint at all** on an economically substantive
  choice, with the prior decision's own alternatives analysis (§9)
  concluding that selecting any candidate "would be inventing accounting
  semantics the design does not state."
- Accordingly, the Retry-Order precedent confirms that a **canonical
  governance authority** (a role distinct from ordinary WP-planning
  authority) can propose bounded amendments to reconcile already-fixed
  canonical constraints, but it does not establish that any authority below
  the design document itself may originate new economically substantive
  accounting content where the design is silent, not self-contradictory.
  This act does not adopt the Retry-Order pathway for D2.

### 5.5 D7 is a different kind of question, but is not independently resolvable right now

Unlike D2, "which authorization record needs an amendment to grant a new
capability" is exactly the kind of question the Retry-Order precedent (and
the Roadmap §1 "reviewer confirmation of strict necessity" mechanism, used
for `BANPU_WP4_ROADMAP_SECTION_1_REVIEWER_CONFIRMATION.md`'s conditional
file admission) shows the corpus already knows how to resolve at a
governance or reviewer level, without design-document-level intervention —
**provided the underlying capability requirement is already fixed**. Here it
is not: a locus cannot be authorized to enforce a predicate that does not yet
exist. The prior decision's own §8 finding ("a formula alone would still
have no authorized place to execute without a companion locus
determination") is symmetric — a locus determination has nothing to execute
without a formula. D7 is therefore correctly classified `GENUINE GAP —
REFERRED` not because it is intrinsically as hard as D2, but because it is
**coupled to** D2 and cannot be resolved first or independently (§8 of the
prior decision; reconfirmed here).

## 6. Mechanical-continuity economic meaning (independently reasoned)

Design §10's operands — evidence-bound predecessor/successor reference
prices — describe a comparison across an asset-identity transition, where
economic continuity is not automatically expected to be numerically tight
unless the conversion is understood to preserve value 1:1 at the reference
points. Design §5 fixes a conversion ratio `R` for **quantity and basis**
(`Qe = Qp × R`), but design §10 never states whether the reconciliation
predicate is expected to hold on raw reference prices or on an
`R`-normalized comparison. Both readings are economically coherent:

- Raw comparison treats the two reference prices as directly comparable
  spot values (correct only if the design intends "evidence-bound reference
  prices" to already be economically normalized before recording, e.g. both
  expressed per pre-conversion equivalent unit — the corpus never says this).
- `R`-normalized comparison treats reference-price continuity as a check
  that the successor's opening valuation, scaled by the same ratio governing
  share/basis allocation, tracks the predecessor's closing valuation —
  economically the more defensible reading for a conversion whose ratio is
  not 1:1, but unsupported by any canonical text bridging design §5 and §10.

This act does not resolve which reading governs (that is D2, referred). It
records this analysis so a future design-competent authority does not have
to re-derive it.

## 7. D2–D6 status (unchanged, reconfirmed)

No new formula, inclusivity operator, rounding rule, or annotation-threshold
rule is created by this act. §3 above reconfirms the prior act's
determination stands. This act's sole contribution to D2–D6 is §5's and
§6's authority-and-meaning analysis, not new normative content.

## 8. Suspension-gap separation (reaffirmed, not reopened)

This act changes nothing about WPP §12's determination that genuine,
annotated suspension-gap return is passive and must not be clamped or
"repaired." Nothing in this act's authority determination implies that a
future design-level formula decision may treat suspension-gap return as
subject to erasure via the reconciliation tolerance, nor that annotation
text may license bypassing a genuine mechanical/data discontinuity. Any
future act resolving D2/D4/D5/D6/D7 remains bound by this separation exactly
as the prior decision's §7 recorded it.

## 9. Effect on `MINOR-2`, and package/authorization consequences

`MINOR-2` (WP5 half) is **not** discharged, narrowed, or advanced by this
act. It remains open exactly as the WP1 Freeze Record §7 and the WPP
recorded it.

Resolving §10.4 requires, in this order, **two distinct acts by two distinct
authorities**, neither performed here:

1. **A design-competent determination fixing the reconciliation formula
   (D2), inclusivity (D4), comparison-level rounding (D5), and
   annotation-sufficiency threshold (D6)** — an authority operating at or
   above the level that originated design §5's equations, because the choice
   is economically substantive and canonically silent, not merely
   procedurally silent. This is additive to, and need not rewrite, the
   canonical design document; it may take the form of a design clarification
   record establishing the missing predicate, provided repository precedent
   for additive design-level clarification (not merely WP-level planning
   clarification) is followed. No such precedent currently exists in this
   corpus for a design-level (as opposed to WPP-level or WP4-canonical
   -governance-level) amendment; establishing one, or confirming an existing
   higher authority is willing to act in that capacity, is itself part of
   what the next act must determine.
2. **An amendment to the BANPU-WP5 Implementation Authorization Record** (and,
   if the resulting capability does not fit the roadmap's existing WP5 scope
   description, the Roadmap §7 capability list) **granting WP5 the
   enforcement capability**, once and only once (1) exists. This is a
   narrower, WP-governance-level act, structurally similar to the WP4
   Retry-Order Governance Decision → Work Package Plan Amendment →
   Independent Reapproval → Binding Freeze Record chain, and does not
   require design-document-level authority — it requires only that the
   capability being authorized already has fixed content to enforce.

Neither act may be performed out of order: authorizing a locus before a
formula exists would authorize an empty capability; fixing a formula without
authorizing a locus would leave `MINOR-2` open exactly as it is now.

## 10. Repository verification

| Verification | Result |
|---|---|
| Only additive path created by this act | `SATISFIED` — `docs/implementation/BANPU_WP5_MECHANICAL_CONTINUITY_COMPETENT_AUTHORITY_DETERMINATION.md` |
| `BANPU_WP5_WORK_PACKAGE_PLAN.md` modified | `NONE` |
| Allocation Record or Implementation Authorization Record modified | `NONE` |
| Prior governance decision record modified | `NONE` |
| Frozen BANPU artifacts (WP1–WP4) modified | `NONE` |
| Production, test, schema, migration, CLI, frontend, Decision Log, or INDEX file modified | `NONE` |
| Commit created | `NO` |

## 11. Governance disposition and resulting state

**`OUTCOME C — FURTHER AUTHORITY REQUIRED.`** WP5-level governance authority
(Allocation Record, Implementation Authorization Record, Work Package Plan,
or a WP5-scoped governance decision) is not competent to originate D2's
reconciliation formula, because the choice is economically substantive and
canonically silent rather than merely procedurally silent, and no corpus
precedent delegates formula-authority of that character below the design
document itself. D7 is coupled to D2 and is therefore also not resolvable
now, notwithstanding that its own type of question (authorization-capability
expansion) is ordinarily resolvable at a governance or reviewer level once
its content exists.

`MINOR-2` (WP5 half): unchanged, still open, still a gate on WP5
confirmation, freeze, and closure. `POSITION_CONVERSION_REBUILD_BOUNDARY`:
unaffected, remains `READY — FULLY DECOMPOSED`. WP5 allocation,
authorization, and Work Package Plan states are unchanged.

## 12. Exact next constitutional act

The WPP's own two-track disposition (§22) remains in force and is further
sharpened, not simplified, by this act:

1. For the plannable majority of WP5 (WP5-C1…C6, and WP5-C7 at WPP §10.3):
   the exact next constitutional act remains **BANPU-WP5 Planning
   Confirmation**, unaffected by this record.
2. For §10.4: the exact next act is **a design-competent clarification
   act, issued by an authority willing and empowered to originate
   economically substantive canonical content at or above the level of
   design §5** — not a further WP5-scoped governance decision — fixing D2,
   D4, D5's comparison-level rounding, and D6's annotation-sufficiency
   threshold together. Only after that act exists may a **second, narrower
   act** amend the BANPU-WP5 Implementation Authorization Record (and, if
   needed, the Roadmap §7 capability list) to grant WP5 the resulting
   enforcement capability (D7), following the amendment-and-reapproval
   pattern already established by the BANPU-WP4 Retry-Order governance
   chain.

This record performs neither act.
