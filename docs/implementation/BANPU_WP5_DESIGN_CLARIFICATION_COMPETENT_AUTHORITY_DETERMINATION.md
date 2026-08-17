# BANPU-WP5 Design-Competent Mechanical Continuity Clarification — Competent Authority Determination

**Artifact class:** Bounded design-competent-authority clarification determination record (blocked)

**Decision date:** 2026-08-14

**Issuing authority:** BANPU-WP5 Design-Competent Mechanical Continuity Clarification Authority

**Question resolved:** Whether a competent repository authority exists to add new normative D2 (reconciliation formula), D4 (inclusivity operator), D5-comparison (comparison-level rounding), or D6-threshold (annotation presence effect) semantics to the frozen `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md` where that document is currently silent, without rewriting its frozen text.

**Governance outcome:** `DESIGN CLARIFICATION BLOCKED — COMPETENT AUTHORITY NOT ESTABLISHED`

**New design semantics created by this act:** `NONE`

**Phase 2 (economic analysis / D2 / D4 / D5 / D6 selection) performed:** `NO — NOT CONSTITUTIONALLY REACHED`

**Implementation performed:** `NO`

**WP5 WPP amended:** `NO`

**WP5 Implementation Authorization amended:** `NO`

---

## 1. Nature and boundary of this act

This is the design-clarification act named by [`BANPU_WP5_MECHANICAL_CONTINUITY_COMPETENT_AUTHORITY_DETERMINATION.md`](BANPU_WP5_MECHANICAL_CONTINUITY_COMPETENT_AUTHORITY_DETERMINATION.md) §9/§12 as the immediate next step for resolving D2/D4/D5-comparison/D6-threshold. It performs Phase 1 (authority determination) of the two-phase invocation that produced it. It modifies no frozen artifact, amends no WP5 WPP or Authorization Record, performs no Planning Confirmation/Freeze, implements nothing, and stages/commits/pushes nothing.

Because Phase 1 does not establish competent authority (§5), Phase 2 is not reached. No formula, operator, rounding rule, or annotation-threshold semantics are chosen anywhere in this record.

## 2. WP5 lifecycle state independently re-verified

| Artifact | State |
|---|---|
| `BANPU_WP5_ALLOCATION_RECORD.md` | `ALLOCATED` |
| `BANPU_WP5_IMPLEMENTATION_AUTHORIZATION_RECORD.md` | `AUTHORIZED — LIMITED` |
| `BANPU_WP5_WORK_PACKAGE_PLAN.md` | `MATERIALIZED — NOT APPROVED/CONFIRMED/FROZEN` |
| `BANPU_WP5_MECHANICAL_CONTINUITY_RECONCILIATION_GOVERNANCE_DECISION.md` | `PARTIAL` |
| `BANPU_WP5_MECHANICAL_CONTINUITY_COMPETENT_AUTHORITY_DETERMINATION.md` | `OUTCOME C — FURTHER AUTHORITY REQUIRED` |

No Planning Confirmation, Planning Freeze, implementation, or later-lifecycle artifact exists for WP5. Unchanged by this act.

## 3. Design §10 / `MINOR-2` authority chain (re-confirmed, not reopened)

`BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md` §10 (verbatim, re-verified this segment): *"Before activation, mechanical boundary value MUST reconcile within the payload tolerance using evidence-bound reference prices. A genuine price move over the trading suspension is recorded as investment return through `suspension_gap_annotation`; it is not an external flow or repair."* The design fixes the obligation's existence and its operands' names; it does not fix the comparison formula, the inclusivity operator, comparison-level rounding, or the annotation-threshold effect. This is the same gap identified by the prior determination and is not reopened here.

## 4. Governance corpus searched for design-amendment authority

Independently inspected this segment:

- `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md` — full header, §17 "Authority boundary."
- `BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md` header (re-confirmed from prior segment: "does not authorize implementation by itself and cannot change the canonical design").
- `docs/engineering/DECISION_LOG.md` — grepped for `BANPU`, `Architecture Owner`, `Design Owner`, `amend design`; read the BANPU-WP2/WP3/WP4 Decision Log Synchronization entries in full.
- `docs/governance/` directory — `CONSTITUTIONAL_PRECEDENT_INDEX.md` (read in full), `ARB_RESOLUTION_ADOPTION_OF_CONSTITUTIONAL_OPINION.md` (read in full). No `GOVERNANCE_HANDBOOK.md` exists at `docs/governance/` (the path referenced by `.claude/CLAUDE.md` is `docs/handbook/GOVERNANCE_HANDBOOK.md`, a different, general engineering-handbook document, not consulted further here as it governs documentation baseline, not design-amendment authority — no evidence found that it does).
- `docs/implementation/BANPU_WP4_RETRY_ORDER_GOVERNANCE_DECISION.md` header (re-confirmed from prior segment).
- BANPU-WP3 Decision Log Synchronization entry — newly identified this segment: cites a "BPA-1" (BANPU Planning Amendment 1) that produced an "amended and frozen governing planning corpus" for WP3, distinct from its "pre-amendment planning corpus."

No dedicated "canonical design amendment" artifact type, "Design Owner" role, or "Architecture Owner" role was found anywhere in this corpus.

## 5. Findings

### 5.1 The design document names no amendment authority

The design's own header states only its *origin* authority — *"Root Cause Analysis, Independent Architectural Review, and approved implementation design"* — describing how the document came to be approved, not who may add to it later. §17 "Authority boundary" states the specification is *"complete for implementation"* and lists categories requiring *"separate approval"* (new transaction families, generalized event dispatch, new corporate-action tables, editable conversion state, public authoring APIs, M46 changes, broader accounting redesign) — but names no role, body, or artifact form that constitutes "separate approval." The document contemplates that some matters lie outside its own authority; it does not say whose authority those matters belong to.

### 5.2 The Roadmap is disqualified (re-confirmed)

Already established and reconfirmed: the Roadmap is expressly subordinate to the design and cannot supply missing design content. Not a candidate authority.

### 5.3 WPP-level amendment precedent exists but does not reach the design document

Two precedents were examined:

- **BPA-1** (BANPU-WP3): amended WP3's own *planning corpus* (its Work Package Plan family), producing a distinct frozen "amended" identity. This is amendment of a WP-scoped planning artifact, not of the canonical design.
- **WP4 Retry-Order chain** (Governance Decision → WPP Amendment → Independent Reapproval → Binding Freeze Record): resolves a runtime-ordering conflict between two already-frozen WP4 requirements, again at WPP rank.

Both precedents confirm that WP-level planning corpora *can* be amended additively by WP-scoped governance acts. Neither precedent, nor any other found, extends that amending power upward to the canonical design document itself. The design sits one rank above every WPP in the document hierarchy already established (Roadmap: "cannot change the canonical design"); nothing in the corpus grants a WPP-rank amendment mechanism power over the rank above it.

### 5.4 The Architecture Review Board precedent fails on two independent grounds

The only repository body found with any claim to corpus-level constitutional-interpretive authority is the Architecture Review Board (ARB), evidenced by `docs/governance/ARB_RESOLUTION_ADOPTION_OF_CONSTITUTIONAL_OPINION.md` and `docs/governance/CONSTITUTIONAL_OPINION_LA_WP2.md`. It fails as a candidate for this act on two independent grounds:

**(a) Jurisdiction.** The ARB resolution's own §3 confines adoption to two specific, git-hash-identified Ledger & Accounting LA-WP2 planning artifacts, and its §5/Finding 5 states in terms: *"It is corpus-bound. It governs questions arising under Plan [hash] and Roadmap [hash]... It carries no force over a different or successor corpus, whose interpretation would proceed from that corpus's own text."* The BANPU canonical design is a different, textually unrelated corpus. No repository artifact extends ARB jurisdiction to it.

**(b) Form of power, even hypothetically within jurisdiction.** The resolution's own Finding 4 states plainly: *"NONE CREATED"* — *"The Opinion constitutes no actor, allocates no role, assigns no burden, imposes no duty, and confers no power on any party... adds no provision to either artifact; subtracts no provision from either artifact."* The ARB precedent is a body that reads and classifies textual silence; it is affirmatively documented as *not* a body that fills silence with new normative content. D2/D4/D5-comparison/D6-threshold require exactly the category of act — introducing new normative semantics where frozen text is silent — that the ARB's own adopted precedent disclaims performing.

An ARB-type body is therefore evidence that *a* constitutional-interpretive mechanism exists in this repository's governance vocabulary, but not evidence that any body currently holds either (i) jurisdiction over the BANPU corpus or (ii) content-creation power of the kind D2 requires.

### 5.5 No standing content-creation role exists

No "Design Owner," "Architecture Owner," or equivalent standing role naming an individual or body with power to add new normative content to an approved design was found anywhere in the design document, the Roadmap, the Decision Log, `docs/governance/`, or any WP1–WP5 record.

### 5.6 Conclusion

No currently constituted repository authority — WP5 governance, Roadmap, the WPP-amendment mechanism (BPA-1 / WP4 Retry-Order pattern), or the ARB precedent — is competent to add the missing D2/D4/D5-comparison/D6-threshold normative content to the frozen design without rewriting or reinterpreting beyond what each is documented to do. This is a genuine authority gap in the repository's governance vocabulary, not merely a power that exists but has gone unexercised.

## 6. Phase 2 disposition: not reached

Per the invocation's own instruction — *"If no authority exists... Do not choose D2/D4/D5/D6... Return `DESIGN CLARIFICATION BLOCKED`"* — Phase 2 is not performed. No economic-meaning analysis, no evaluation of Alternatives A/B/C/D for D2, no inclusivity operator, no Decimal/rounding specification, and no annotation-semantics selection appear anywhere in this record. §7–§12 of the invocation's requested final-report structure (formula, D3 compatibility, D4, D5, D6, suspension-gap treatment) are correspondingly `NOT APPLICABLE — PHASE 2 NOT REACHED`.

## 7. Effect on original frozen design identity/history

`NONE`. No byte of `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md` is read as modified, reopened, or reinterpreted beyond the plain text already cited in prior acts. This record proposes no amendment text.

## 8. Effect on `MINOR-2`

Unchanged. The WP5 half of `MINOR-2` remains open. Its design-semantics sub-question is not resolved by this act; it was not resolved before this act either. Status remains as recorded by the prior determination — no downgrade, no upgrade.

## 9. Downstream consequences — the minimum governance act necessary

The minimum act required to establish competent authority is one performed **at or above the rank that produced the design's own "APPROVED IMPLEMENTATION SPECIFICATION" status** (i.e., by whatever role or process is capable of exercising the same kind of authority recited in the design's own header — *"Root Cause Analysis, Independent Architectural Review, and approved implementation design"*), taking one of two forms:

1. **Direct design amendment** — an additive act that supplies the D2/D4/D5-comparison/D6-threshold content itself, preserving the original frozen design text unchanged and recording the amendment relationship explicitly (structurally analogous to BPA-1, but at design rank — a form with no existing precedent in this corpus; establishing that form is itself part of what such an act must do); or
2. **Jurisdiction-and-power extension** — an act that expressly constitutes, or extends the ARB's, jurisdiction to reach the BANPU canonical design corpus **and** expressly grants content-creation power over this specific silent provision (not merely interpretive power, per §5.4(b)) — before any such body could act on D2.

Neither form is available to WP5 governance, Roadmap governance, or the ARB as currently scoped. Until one occurs, D2/D4/D5-comparison/D6-threshold cannot lawfully be fixed by any act this invocation, WP5, or the Roadmap could perform, and D7 (already outside this invocation's scope) remains correspondingly unreachable.

## 10. Artifact created

`docs/implementation/BANPU_WP5_DESIGN_CLARIFICATION_COMPETENT_AUTHORITY_DETERMINATION.md` (this document). No other artifact created. Precedent for recording a blocked-authority determination as its own artifact is established by the LA-WP2 Governance Determination (`BLOCKED — GOVERNANCE`, per `docs/governance/CONSTITUTIONAL_OPINION_LA_WP2.md`'s recitation) and by this act's own immediate predecessor, `BANPU_WP5_MECHANICAL_CONTINUITY_COMPETENT_AUTHORITY_DETERMINATION.md`.

## 11. Repository verification

To be executed after write: enumerate added/modified paths; `git diff --check`; `git diff --cached --check`; trailing-whitespace check; relative-link/anchor verification; `graphify update .`; confirm no application/test code changed; confirm no other governance artifact changed; confirm nothing staged/committed; final `git status`.

## 12. Remaining unresolved issues

- D2/D4/D5-comparison/D6-threshold remain wholly unresolved.
- The identity of the specific role or process capable of exercising design-amendment or jurisdiction-extension authority (§9) is itself not established by any artifact found in this corpus — naming it is necessarily the first task of whatever act attempts §9(1) or §9(2).
- D7 (enforcement locus) remains outside this invocation's scope and additionally blocked by D2's unresolved status, per the prior determination.
- WP5 Planning Confirmation for the plannable majority (WP5-C1…C6, and C7 at WPP §10.3) remains available and unaffected by this blocked outcome.

## 13. Final disposition

`DESIGN CLARIFICATION BLOCKED — COMPETENT AUTHORITY NOT ESTABLISHED`

## 14. Exact next constitutional act

An act performed at design-authorship/approval rank — not WP5-scoped governance, not Roadmap-scoped governance, and not the ARB as currently jurisdictionally scoped — that either (a) directly supplies the missing D2/D4/D5-comparison/D6-threshold design content as an additive design amendment, or (b) first constitutes or extends a body with express content-creation jurisdiction over this specific silent provision, before that body acts. This record performs neither act.
