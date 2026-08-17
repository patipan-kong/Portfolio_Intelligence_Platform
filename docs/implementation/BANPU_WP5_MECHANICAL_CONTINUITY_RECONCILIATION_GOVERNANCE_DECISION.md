# BANPU-WP5 — Mechanical Continuity Reconciliation Governance Decision

**Artifact class:** Additive bounded constitutional governance decision record
**Decision date:** 2026-08-14
**Issuing authority:** BANPU-WP5 Bounded Mechanical Continuity Reconciliation Governance Decision Authority
**Question resolved:** the minimum constitutionally valid semantics for the `BANPU_WP5_WORK_PACKAGE_PLAN.md` §10.4 mechanical-continuity reconciliation blocker (operands, formula, tolerance source, boundary inclusivity, numeric/rounding behavior, annotation semantics, failure behavior)
**Governance outcome:** `PARTIAL — EXISTING AUTHORITY SUFFICIENT FOR OPERAND IDENTITY, TOLERANCE SOURCE, AND ANNOTATION-FIELD IDENTITY ONLY; THE RECONCILIATION FORMULA, BOUNDARY INCLUSIVITY, COMPARISON-LEVEL ROUNDING, ANNOTATION-SUFFICIENCY THRESHOLD, AND ENFORCEMENT LOCUS REMAIN A GENUINE SPECIFICATION GAP AND ARE REFERRED, NOT DECIDED`
**New reconciliation formula created:** `NONE`
**§10.4 blocker status after this act:** `NOT RESOLVED — DECOMPOSED AND SHARPENED; ONE NEW STRUCTURAL FINDING ADDED (§8)`
**Implementation performed:** `NO`
**WPP amendment performed:** `NO`
**Planning Confirmation, Planning Freeze, implementation review, WP6/WP7/WP8, or production authority created:** `NONE`

---

## 1. Nature and boundary of this act

This act exists to determine whether the BANPU-WP5 Work Package Plan §10.4
planning blocker — the missing mechanical-continuity reconciliation
semantics for the WP5 half of BANPU-WP1 residual `MINOR-2` — can be resolved
from already-authoritative repository text, and, only if a genuine gap is
independently confirmed, whether repository authority and precedent permit a
new **bounded** planning decision for any sub-dimension of that blocker.

This act is additive. It modifies no frozen artifact, no Allocation Record,
no Implementation Authorization Record, and — per explicit instruction — does
**not** modify `BANPU_WP5_WORK_PACKAGE_PLAN.md` itself. It performs no
implementation, no test edit, no Planning Confirmation, no Planning Freeze,
no implementation review, and no WP6/WP7/WP8 act. It stages, commits, and
pushes nothing.

The invoking prompt's characterization of the blocker was not accepted as
authority. Every finding below was independently re-derived from live
repository text read during this act.

## 2. Governance/WPP state independently verified

Recomputed this act, under the same Git-canonical-LF/uppercase-SHA-256
convention used throughout the BANPU corpus (strip `\r`, encode UTF-8, SHA-256,
uppercase hex), directly against the current working tree — not accepted from
the invoking prompt or from the cited values inside the WPP itself:

| Artifact | Recomputed bytes | Recomputed SHA-256 | Result |
|---|---|---|---|
| [`BANPU_WP5_ALLOCATION_RECORD.md`](BANPU_WP5_ALLOCATION_RECORD.md) | 15,590 | `D00D0AE886E6150F84663AA331338F764E193700EBCE944C88CB0D175CA8D687` | `EXACT` — matches the WPP's own citation, no drift |
| [`BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_RECORD.md`](BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_RECORD.md) | 19,039 | `DBCBC2BFCDB9F3A7D3E7912C6148445C68C39F5872A4DE2DEF58DF5B2BDE7F1E` | `EXACT` — matches the WPP's own citation, no drift |
| [`BANPU_WP5_WORK_PACKAGE_PLAN.md`](BANPU_WP5_WORK_PACKAGE_PLAN.md) | 42,903 | `0455ABA9787280B9C7C0156A48C5C4DA7B3C0A55BFFC7DEAC710E645961DF523` | Live identity, recorded here for the record; the WPP predates and does not self-cite this identity |

Disposition re-confirmed directly from file content: Allocation Record
`BANPU-WP5 ALLOCATED`; Implementation Authorization Record `BANPU-WP5
IMPLEMENTATION AUTHORIZED`; Work Package Plan `WORK PACKAGE PLAN
MATERIALIZED — NOT APPROVED — IMPLEMENTATION NOT PERFORMED — NOT CONFIRMED —
NOT FROZEN`, with `MINOR-2` (WP5 half) recorded as `PARTIALLY PLANNABLE —
TOLERANCE ADMISSIBILITY READY; RECONCILIATION FORMULA BLOCKED AT A PLANNING
BOUNDARY`. No BANPU-WP5 Planning Confirmation, Planning Freeze, or
implementation artifact exists in `docs/implementation/`.

The exact §10.4 blocker text was located and re-read directly from
`BANPU_WP5_WORK_PACKAGE_PLAN.md` lines 290–341 (§10.4 "Part (b) — the
reconciliation/comparison itself — `PLANNING BLOCKER`"), not summarized from
the invoking prompt.

## 3. `MINOR-2` traced to its original authority

`MINOR-2` originates at `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`
§16 (WP1 review deferrals and residuals): *"boundary-evidence decimal
sign/range validation is not yet consumer-specific … WP3 owns
provider/reference-price admissibility; WP5 owns mechanical continuity
tolerance admissibility."* It is frozen at that identity by
`BANPU_WP1_FREEZE_RECORD.md` §7 (row: *"Deferred consumer-domain validation
… WP3 for reference prices; WP5 for mechanical tolerance … Focused rejection
tests before either value is consumed"*) and confirmed again by
`BANPU_WP1_CONFIRMATION.md` §5 in materially identical language. It is
carried unchanged through `BANPU_WP1_RESIDUAL_IDENTITY_RECORD.md`,
`BANPU_WP2_IMPLEMENTATION_SPECIFICATION.md`,
`BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md` §4.2,
`BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` §9.2/A9, and
`BANPU_WP3_REFERENCE_PRICE_ADMISSIBILITY_CLARIFICATION_RECORD.md` §3 and §9
— all independently re-read this act — with no artifact ever narrowing,
widening, or reassigning the WP5 half.

`BANPU_WP3_REFERENCE_PRICE_ADMISSIBILITY_CLARIFICATION_RECORD.md` §9
("WP5 ownership preserved") independently states, as WP3's own governance
finding rather than a WP5 planning inference: *"`mechanical_nav_tolerance_pct`
admissibility is WP5's, not WP3's. The boundary reconciliation of design §10
is WP5's, not WP3's. WP3 performs admissibility checking only; it performs no
tolerance comparison, no reconciliation, and no continuity evaluation."* This
is independent, WP3-authored corroboration of exactly the split the WPP
relied on — the WPP's finding was not invented from a single reading.

## 4. Canonical evidence for mechanical continuity — exhaustive search

Every occurrence of `MINOR-2`, "mechanical continuity", "mechanical
boundary value", "reconcil*", `mechanical_nav_tolerance_pct`, "boundary
discontinuity", "suspension_gap_annotation", and "tolerance" was located
across `docs/implementation/` and `backend/` this act (excluding the
unrelated `M39_WP5_*`/`M40_WP5_*`/`M42_WP5_*`/`M44_WP5_*` milestone series,
already independently distinguished from BANPU-WP5 by the WPP §2, and
excluding domain-unrelated uses such as `optimizer.py`'s persona
"turnover_tolerance"). The complete result set of substantive text is:

- Design §6.2 payload contract: `boundary_evidence.mechanical_nav_tolerance_pct`
  (decimal string, example `"0.50"`, no unit definition beyond the field
  name) and `boundary_evidence.suspension_gap_annotation` (required `TEXT`
  field, no non-empty constraint stated).
- Design §10 (the entire canonical statement of the reconciliation
  requirement, verbatim): *"Before activation, mechanical boundary value
  MUST reconcile within the payload tolerance using evidence-bound reference
  prices. A genuine price move over the trading suspension is recorded as
  investment return through `suspension_gap_annotation`; it is not an
  external flow or repair."*
- Design §11 (quarantine): conversion holdings are quarantined for, among
  other reasons, *"mechanical continuity failure, or an unannotated boundary
  discontinuity,"* with quarantine's system-level consequence stated as
  blocking affected snapshots and downstream optimizer/evaluation refresh.
- Design §16's acceptance checklist: *"Mechanical continuity verified and
  suspension return annotated"* — a checklist item, not a formula.
- Design §5's accounting-model equations (`Qp`, `Qe = Qp × R`, `Qr`,
  `Qf = Qe − Qr`, `B0`, `Bs = B0 − Bf`, `As = Bs / Qr`) — read directly this
  act and confirmed to govern **share count and cost-basis allocation**,
  computed and consumed exclusively by WP4's frozen
  `execute_position_conversion()` write path. They do not reference
  `predecessor_reference_price`, `successor_reference_price`, or
  `mechanical_nav_tolerance_pct` anywhere, and no canonical artifact states
  that §5's equations are the mechanism §10 refers to.
- `backend/services/market_data/position_conversion_quote_contract.py` (WP3's
  frozen module): `assess_reference_price_admissibility()` — a single-field
  presence/finiteness/positivity/decimal-exactness check, structurally
  incapable of supplying a two-operand reconciliation formula; and the
  `QuarantineReason` enum, which — per its own class docstring, re-read this
  act — deliberately excludes both "mechanical continuity failure" and
  "unannotated boundary discontinuity" as "WP5-owned."
- `backend/manage.py` `_audit_nav_continuity()` — read directly this act
  (lines 851–875): a **generic, conversion-independent** snapshot-to-snapshot
  percentage-change check, `(current − previous) / abs(previous) × 100`,
  inclusive `<=` pass, values rounded to 2 places only for the reported
  `details` payload (the comparison itself is performed on unrounded floats).
  This is the repository's only existing percentage-tolerance comparison
  pattern anywhere in the codebase, but it compares portfolio total value
  snapshot-to-snapshot, not a predecessor/successor reference-price pair, and
  the WPP's own §5 explicitly forbids routing the payload tolerance through
  it or conflating the two mechanisms.

No other canonical or code location contains reconciliation semantics for
this predicate. The search is exhaustive within the current repository state.

## 5. Determination: is §10.4 a genuine specification gap?

**Yes, confirmed independently — not merely inherited from the WPP's own
claim.** Design §10's sentence is the *entire* canonical statement of this
requirement; it names the operand class ("evidence-bound reference prices")
but states no formula, no denominator, no boundary operator, no rounding
rule, and no annotation-sufficiency threshold. Design §5's equations govern a
different, already-implemented predicate (share/basis reconciliation, WP4's
closed surface) and supply no numeric pattern transferable to a price-level
reconciliation. WP3's sibling admissibility function validates one field in
isolation and supplies no two-operand comparison pattern. The only
percentage-tolerance comparison pattern anywhere in the codebase
(`_audit_nav_continuity`) is explicitly walled off from this mechanism by the
WPP's own frozen §5 boundary. This is confirmed a genuine specification gap,
not a WPP oversight of existing authority.

## 6. Dimension-by-dimension determination

Current implementation behavior is used below, where used at all, strictly
as tier-5 informative evidence per the evidence hierarchy — never as
authority, and never silently converted into a decision.

### D1 — Comparison operands: `EXISTING AUTHORITY SUFFICIENT`

Design §10's sentence names exactly two operands — "evidence-bound reference
prices" — and no canonical artifact anywhere names a third candidate pair
(NAV, an accounting-equivalent value, or otherwise). Read together with the
WP3 Reference-Price Admissibility Clarification Record §3.4's established
referent, the operands are precisely the two `boundary_evidence` fields
`predecessor_reference_price` and `successor_reference_price`, each already
required to be `ADMISSIBLE` (WP3's discharged half, plus WP5's own
already-planned PD-WP5-1 tolerance-value admissibility) before
consumption. **This is not a new decision; it is a restatement of what
design §10 already names**, and it was already implicit in the WPP's own
§10.2–§10.3 reading. No canonical text states or implies that the conversion
ratio `R` (a quantity-domain value from design §5, not a `boundary_evidence`
field) is a third operand, and none is added here.

### D2 — Comparison formula: `GENUINE GAP — REFERRED`

Confirmed unresolved by §4–§5 above. At minimum three structurally different,
individually plausible formulas exist (absolute difference; relative
difference with `predecessor_reference_price` as denominator; relative
difference with `successor_reference_price` as denominator; a further
candidate using their average), and canonical text is additionally silent on
whether the comparison is even performed on the two reference prices *as
recorded* or on some `R`-normalized transformation of them — a threshold
question this act cannot resolve, because economically a raw
predecessor/successor price comparison is not obviously meaningful when the
conversion entitlement ratio is not 1:1, yet no canonical artifact authorizes
or forbids incorporating `R`. Selecting any one formula here would be
inventing accounting semantics the design does not state, which both the
invoking instruction and the WPP's own §10.4 explicitly forbid. **Not
decided; referred (§8).**

### D3 — Tolerance source and value: `EXISTING AUTHORITY SUFFICIENT`

The only tolerance value named anywhere in the canonical corpus is the
payload's own `mechanical_nav_tolerance_pct` field, parsed by the frozen WP1
contract. No default, derived, or alternate tolerance value exists in any
artifact. WP5's own already-recorded PD-WP5-1 (WPP §10.3) already fixes this
field's admissibility rule. **Nothing new is decided here — the source is
already fixed by frozen authority, and this act creates no new tolerance
value.**

### D4 — Boundary inclusivity: `COUPLED TO D2 — NOT INDEPENDENTLY DECIDABLE`

Inclusivity is a property of a defined comparison predicate ("is the
computed value `<=` or `<` the tolerance"). With no comparison formula fixed
by D2, there is no predicate for an inclusivity operator to attach to.
Fixing `<=` or `<` now, before the comparison itself exists, would not be a
narrow decision — it would silently presuppose a formula. **Not decided;
referred jointly with D2 (§8).**

### D5 — Numeric representation and rounding: `PARTIALLY DECIDABLE`

The operand types are already fixed by the frozen WP1 parser as exact
`decimal.Decimal` values (`predecessor_reference_price`,
`successor_reference_price`, `mechanical_nav_tolerance_pct` are all
`Decimal`, per `transaction_canonicalizer.py`'s
`PositionConversionBoundaryEvidence`), and PD-WP5-1 already requires
`mechanical_nav_tolerance_pct` to be decimal-exact before use, mirroring
WP3's frozen decimal-exact pattern for the reference prices. **Whatever
comparison D2 eventually fixes must therefore operate on `Decimal` values
without float conversion — this narrow constraint is decidable now from
already-frozen authority and is recorded as binding on any future
resolution.** The comparison's internal precision, whether the tolerance
percentage itself is rounded before use, and whether reported values are
rounded before or after the pass/fail test are all coupled to the undefined
formula (D2) and are **not decided; referred (§8)**.

### D6 — Annotation semantics: `SPLIT`

- **Field identity and role — `EXISTING AUTHORITY SUFFICIENT`.** The only
  annotation field named anywhere is `boundary_evidence.suspension_gap_annotation`,
  already parsed by the frozen WP1 contract. Design line 324 directly ties it
  to "a genuine price move over the trading suspension... recorded as
  investment return... not an external flow or repair" — the same concept
  already governing the WPP's §12 suspension-gap-return treatment (passive,
  unclamped). This is one field serving one concept, consumed in two places
  (the passive return-computation path, already settled by the WPP and
  unaffected by this act; and the reconciliation/quarantine path, still
  undefined). **Not a new decision — restates what design line 324 already
  ties together.**
- **"Annotation present" threshold — `GENUINE GAP — REFERRED`.** The payload
  contract requires the field as a non-optional string but states no
  non-empty or non-whitespace constraint anywhere. Whether an empty string
  counts as "annotated" is unanswerable from canonical text. **Not decided;
  referred (§8).**
- **Effect of annotation on classification — `GENUINE GAP — REFERRED`.**
  Design §11 lists "mechanical continuity failure" and "unannotated boundary
  discontinuity" as two *separate* enumerated reasons, which is inconsistent
  with a reading where annotation-presence alone silently collapses a
  discontinuity into acceptance; equally, no text states that an annotated
  discontinuity still fails under "mechanical continuity failure" as a
  distinct condition. Both readings are textually available and neither is
  preferred by any canonical statement. **Not decided; referred (§8),
  bound by the guardrail in §7.**

### D7 — Failure behavior and enforcement locus: `GENUINE GAP — REFERRED, WITH A NEW STRUCTURAL FINDING`

See §8 — this dimension surfaces a finding not previously recorded by the
WPP.

## 7. Explicit separation: mechanical continuity vs. genuine suspension-gap return

This act changes nothing about the WPP §12 determination that genuine,
annotated suspension-gap return is passive and must not be clamped, smoothed,
or "repaired" — that determination is independently well-anchored (design
principle 9, Roadmap §7's acceptance criterion, design line 324) and is not
reopened here. This act's referral of D2/D4/D5/D6-threshold/D7 does not
create, imply, or authorize any interpretation in which:

- a future resolution of §10.4 could require genuine suspension-gap
  investment return to be forced toward zero or otherwise suppressed to
  satisfy a mechanical-continuity tolerance; or
- the annotation mechanism could be read as license for arbitrary annotation
  text to silently bypass a genuine mechanical/data discontinuity that is
  *not* a real suspension-period market move.

Any future decision resolving D2/D4/D5/D6/D7 must preserve this separation as
a binding constraint, not merely a preference.

## 8. New structural finding: enforcement locus (D7)

Independent inspection this act, beyond what the WPP recorded, finds a
structural tension the WPP's §10.4 did not surface:

1. Design §10–§11 frames "mechanical continuity failure" and "unannotated
   boundary discontinuity" as **quarantine** consequences — a fail-closed,
   blast-radius-limited mechanism that blocks affected snapshots and
   downstream optimizer/evaluation refresh (design §11, verbatim, re-read
   §4 above).
2. WP3's frozen `QuarantineReason` enum — the sole implemented quarantine
   mechanism in the repository — deliberately excludes both reasons, by its
   own docstring's explicit statement (re-confirmed §3 above via WP3's own
   Reference-Price Admissibility Clarification Record §9: WP3 "performs no
   tolerance comparison, no reconciliation, and no continuity evaluation").
   WP5's frozen Work Package Plan §5 and §20 independently forbid WP5 from
   adding a member to that enum or otherwise extending WP3's closed module.
3. WP5's own Implementation Authorization Record §4.1 bounds WP5's
   `manage.py` change strictly to `verify_snapshots`, which is a **read-only,
   non-blocking** audit command (confirmed by direct code inspection of
   `_cmd_verify_snapshots`/`_audit_portfolio`, `backend/manage.py` lines
   1123–1310, during the prior Work Package Plan act and re-confirmed
   structurally this act). The WPP's own §14 already records: *"Reconciliation
   comparison (§10.4): Not implemented by this plan; no failure path exists
   for it yet."*
4. Consequence: **no canonical artifact assigns any authorized, implemented,
   or implementable locus for a fail-closed "mechanical continuity failure" /
   "unannotated boundary discontinuity" consequence.** WP3's surface is
   closed and self-excludes it; WP5's only authorized surface for this
   obligation is explicitly non-blocking. If design §10–§11's quarantine
   framing is taken literally, satisfying it would require either
   (a) reopening WP3's closed, frozen module — forbidden by both WP3's
   closure and WP5's own plan boundary — or (b) a governance decision
   establishing a different, currently unauthorized enforcement locus and
   mechanism (e.g., a blocking check inside WP5's authorized production
   surface, which is not named as a quarantine-capable location by any
   canonical artifact, or a distinct future package).

This is structurally the same category of problem as
`BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` §6.4's `PD-3`
"quarantine predicate ownership" referral — an obligation named by design
text with no canonical artifact assigning its implementing locus — though it
is a distinct, later-arising instance of that category (PD-3 concerned the
WP2 validator's emission of a *different* finding, `POSITION_CONVERSION_QUOTE_QUARANTINED`,
and was resolved as to WP3's own scope by restatement of canonical text; it
does not itself resolve or subsume this D7 finding). This act does not
resolve D7. It records the finding and refers it using the same
referral mechanism WP3's own governance record established as precedent:
naming the gap precisely, assigning it to no unauthorized surface, and
leaving it for the authority governing the canonical design, roadmap, and
package inventory.

## 9. Alternatives considered for D2 (formula) and rejected as premature

Per the invoking instruction's requirement to identify the smallest
reasonable alternative set even where a decision is ultimately not made,
three candidate formulas were evaluated and none was selected:

| Alternative | Formula sketch | Why not selected |
|---|---|---|
| Absolute-difference | `abs(successor_reference_price − predecessor_reference_price) <= mechanical_nav_tolerance_pct` (treated as an absolute money unit) | Contradicts the field's own name (`..._pct`) and its example value (`"0.50"`), which read as a percentage, not a currency amount; not adopted |
| Relative-difference, predecessor-denominated | `abs(successor_reference_price − predecessor_reference_price) / predecessor_reference_price × 100 <= mechanical_nav_tolerance_pct` | Textually plausible and closest in shape to the repository's only sibling percentage-tolerance pattern (`_audit_nav_continuity`), but that pattern is explicitly walled off from this mechanism by the WPP's §5 boundary, and no canonical artifact adopts predecessor-denomination over successor-denomination; selecting it here would be inventing, not inheriting, semantics |
| Relative-difference, `R`-normalized | Same as above, but with `successor_reference_price` first multiplied by (or divided by) the conversion ratio `R` from design §5 before comparison | Would correctly account for a non-1:1 entitlement ratio, but no canonical artifact authorizes importing `R` — a design §5 (share/basis) concept — into the design §10 (reference-price reconciliation) predicate; doing so would bridge two canonical sections the corpus itself keeps textually separate |

Consistent with the invoking instruction's evidence hierarchy, none of these
alternatives is adopted. They are recorded so a future authority need not
re-derive the candidate space from nothing.

## 10. Effect on `MINOR-2`

`MINOR-2`'s WP5 half is **not** discharged, narrowed, or advanced toward
completion by this act. §6's D1/D3/D6-field-identity restatements were
already implicit in the WPP's own §10.2–§10.3 and PD-WP5-1; this act adds no
new implementation-ready semantics to the WP5 obligation. `MINOR-2` remains
open exactly as `BANPU_WP1_FREEZE_RECORD.md` §7 and the WPP recorded it, and
remains a gate on WP5 confirmation, freeze, and closure, per the WPP §10.4's
own consequence list, which this act does not alter.

## 11. Preserved prohibitions

This act creates:

- `NO` reconciliation formula, comparison operator, rounding rule, or
  annotation-sufficiency threshold;
- `NO` amendment to `BANPU_WP5_WORK_PACKAGE_PLAN.md`, the Allocation Record,
  or the Implementation Authorization Record;
- `NO` extension of WP3's `QuarantineReason` enum or any other change to
  `services/market_data/position_conversion_quote_contract.py`;
- `NO` new authorized file surface, capability, or acceptance criterion
  beyond those already bound by the Implementation Authorization Record;
- `NO` Planning Confirmation, Planning Freeze, implementation, implementation
  review, confirmation, freeze, or closeout of BANPU-WP5;
- `NO` WP6, WP7, or WP8 authority, and `NO` M46 authority; and
- `NO` production execution, snapshot mutation, or deployment authority.

## 12. Repository verification of this governance act

| Verification | Result |
|---|---|
| Only additive path created by this act | `SATISFIED` — `docs/implementation/BANPU_WP5_MECHANICAL_CONTINUITY_RECONCILIATION_GOVERNANCE_DECISION.md` |
| `BANPU_WP5_WORK_PACKAGE_PLAN.md` modified | `NONE` |
| Allocation Record or Implementation Authorization Record modified | `NONE` |
| Frozen BANPU artifacts (WP1–WP4) modified | `NONE` |
| Production, test, schema, migration, CLI, frontend, Decision Log, or INDEX file modified | `NONE` |
| Trailing-whitespace verification | see final report |
| Markdown relative-link target verification | see final report |
| Markdown fragment-heading verification | see final report |
| `git diff --check` | see final report |
| `git diff --cached --check` | see final report |
| `graphify update .` | see final report |
| Final `git status --short --untracked-files=all` | see final report |
| Commit created | `NO` |

## 13. Governance disposition and resulting state

**`PARTIAL — EXISTING AUTHORITY SUFFICIENT FOR D1 (OPERAND IDENTITY), D3
(TOLERANCE SOURCE), AND D6'S FIELD-IDENTITY SUB-QUESTION ONLY; D2 (FORMULA),
D4 (INCLUSIVITY), D5'S COMPARISON-LEVEL ROUNDING, D6'S ANNOTATION-SUFFICIENCY
THRESHOLD, AND D7 (ENFORCEMENT LOCUS) REMAIN UNRESOLVED AND ARE REFERRED, NOT
INVENTED.`**

`MINOR-2` (WP5 half): unchanged — still open, still a gate on WP5
confirmation, freeze, and closure. `POSITION_CONVERSION_REBUILD_BOUNDARY`:
unaffected by this act; remains `READY — FULLY DECOMPOSED` exactly as the
WPP §8 recorded. BANPU-WP5 allocation, implementation authorization, and
Work Package Plan states are all unchanged by this act. No BANPU-WP5
Planning Confirmation or Planning Freeze may proceed while §10.4's referred
dimensions remain open, to the same extent the WPP itself already recorded.

## 14. Exact next constitutional act

This act does not fully resolve §10.4, so the WPP's own two-track §22
disposition is **not simplified** by this act:

1. For the plannable majority of WP5 (§3's WP5-C1…C6 and WP5-C7 at §10.3):
   the exact next constitutional act remains **BANPU-WP5 Planning
   Confirmation**, unaffected by this record.
2. For §10.4 (D2, D4, D5's comparison-level rounding, D6's
   annotation-sufficiency threshold, and — newly identified by this act —
   D7's enforcement locus): the exact next act is **a governance-level
   determination, by an authority competent over the canonical design,
   roadmap, and package inventory** (the same class of authority the WPP's
   §22 already anticipated, now more precisely scoped by this act's §6/§8
   decomposition), fixing the reconciliation formula and its enforcement
   locus together — not two separate, sequential decisions, because §8
   establishes that a formula alone would still have no authorized place to
   execute without a companion locus determination.

This record performs neither act.
