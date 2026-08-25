# BANPU Mechanical Continuity — Design §10 Normative Clarification

**Artifact class:** Additive, human-authorized design-level normative clarification

**Decision date:** 2026-08-14

**Authorized by:** Human Repository/Design Owner (external authorization; see §1)

**Materialized by:** Repository analysis/governance-record mechanism (this session) acting solely on the scope of the authorization in §1 — not as an independent source of constitutional authority

**Provision clarified:** `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md` §10, sentence: *"Before activation, mechanical boundary value MUST reconcile within the payload tolerance using evidence-bound reference prices."*

**Governance outcome:** `DESIGN CLARIFICATION COMPLETE — HUMAN-AUTHORIZED NORMATIVE SEMANTICS ESTABLISHED — D7 NOT AUTHORIZED`

**Effect on `MINOR-2`:** `DESIGN SEMANTICS RESOLVED — IMPLEMENTATION OBLIGATION OPEN`

---

## 1. Human authorization provenance

Independent repository investigation (`BANPU_WP5_MECHANICAL_CONTINUITY_COMPETENT_AUTHORITY_DETERMINATION.md`, `BANPU_WP5_DESIGN_CLARIFICATION_COMPETENT_AUTHORITY_DETERMINATION.md`, `BANPU_DESIGN_AMENDMENT_AUTHORITY_DETERMINATION.md`) found no repository-internal standing authority competent to add new normative content to the frozen BANPU design. This normative act is authorized externally, by the **Human Repository/Design Owner**, in the prompt that requested this artifact. The authorization is explicit, bounded to D2/D4/D5/D6 only, and expressly withholds D7, implementation, mutation, deployment, and all WP5 lifecycle acts beyond this clarification.

The executing agent is acting only as the repository analysis and materialization mechanism for that external authorization. It is not the source of the constitutional authority exercised here, and this record makes no claim otherwise.

## 2. Live repository state independently re-verified

Re-confirmed unchanged from the immediately preceding act: WP5 Allocation `ALLOCATED`; Implementation Authorization `AUTHORIZED — LIMITED`; WPP `MATERIALIZED — NOT CONFIRMED/FROZEN`; prior reconciliation governance decision `PARTIAL`; both prior competent-authority determinations `OUTCOME C` / `BLOCKED`; design-amendment authority determination `BLOCKED`. No intervening act has resolved D2/D4/D5/D6. This is the first artifact in the chain to do so.

## 3. Preserved, unmodified prior authority

Unchanged and not reopened by this act:

- **D1 operands:** `boundary_evidence.predecessor_reference_price`, `boundary_evidence.successor_reference_price` (payload strings, `conversion_payload.boundary_evidence`).
- **D3 tolerance source:** `boundary_evidence.mechanical_nav_tolerance_pct`, governed by the existing WP5/`PD-WP5-1` admissibility determination. No second tolerance is introduced.
- **Numeric domain:** `Decimal` throughout; no binary floating-point conversion anywhere in this predicate.
- **Annotation field identity:** `boundary_evidence.suspension_gap_annotation`.
- **Suspension-gap invariant:** a genuine market return across the suspension gap remains genuine return; it is not zeroed, clamped, or reclassified as an external flow or repair.
- **`MINOR-2`:** this act resolves its design semantics only; the WP5 implementation obligation remains open.

## 4. Economic reconstruction

From design §5's accounting model and §6.2's payload contract:

- `Qp` = predecessor shares surrendered; `R` = conversion ratio (`conversion_payload.conversion_ratio`); `Qe = Qp × R` = successor shares entitled; `Qr` = successor shares actually received (`shares.received`); `Qf = Qe − Qr` settled in cash-in-lieu.
- `B0` = predecessor basis; `Bs` = basis carried to successor; `As = Bs / Qr` = successor average cost.
- Share-count and basis continuity (`Qp`↔`Qe`↔`Qr`, `B0`↔`Bs`) are **already** independently validated by the dedicated, distinctly-named §11 checks `POSITION_CONVERSION_SHARE_MISMATCH` and `POSITION_CONVERSION_BASIS_MISMATCH`. Design §10's mechanical-continuity obligation is a **separate** check, over a **separate** pair of operands (`predecessor_reference_price`, `successor_reference_price` — *market prices*, not share counts or basis), and must not duplicate or re-derive what those checks already own.
- `predecessor_reference_price` (`P_pre`) is the evidence-bound market price of the predecessor instrument at the boundary; `successor_reference_price` (`P_succ`) is the evidence-bound market price of the successor instrument at the boundary. They are prices of **two different instruments**, related to each other only through the conversion ratio `R` — not directly comparable as raw numbers.

## 5. What design §10 is validating

The ratio `R` fixes the defining economic relationship of the amalgamation: one predecessor share converts into `R` successor shares. Design §10's phrase *"mechanical boundary value... reconcile... using evidence-bound reference prices"* is, read against §5's own accounting model, a value-equivalence check derived from that same ratio: **the market value of one predecessor share must mechanically equal the market value of the `R` successor shares it converts into**, absent a genuine, evidenced market move across the suspension. This is a *price-level* check on the ratio's economic validity — distinct in kind and scope from the *quantity/basis-level* checks already owned by `SHARE_MISMATCH`/`BASIS_MISMATCH`.

## 6. D2 — Formula

### Alternatives evaluated

- **Alternative A (`abs(P_pre − P_succ)`):** Rejected. Predecessor and successor are different instruments; nothing in the design's economics implies their raw per-share prices should be numerically close whenever `R` differs materially from `1`. For BANPU (`R = 0.38242`), raw price proximity would be economically meaningless even with zero mechanical error.
- **Alternative B (raw relative difference):** Rejected for the same reason as A — normalizing an economically meaningless comparison does not repair it; `R` is not folded into the metric.
- **Alternative C (`P_pre` vs `R × P_succ`):** **Selected.** This is the direct, minimal expression of the ratio's own defining relationship (§5), and matches §10's "mechanical boundary value" language read as a ratio-implied value-equivalence check.
- **Alternative D (economic-value/NAV continuity using `Bs`, `Qr`, cash-in-lieu):** Rejected as the operand set for *this* check. It would duplicate the already-separately-owned `SHARE_MISMATCH`/`BASIS_MISMATCH` checks and blur their ownership boundary with §10's price-level obligation. Design §10 names *reference prices* as its operands, not basis or share counts.
- **Alternative E:** No other formulation is directly supported by the canonical economic model.

### Normative formula

Let `P_pre`, `P_succ`, `R` be parsed as `Decimal` from their payload string representations. Define:

```text
implied_successor_value = R × P_succ
absolute_gap = abs(P_pre − implied_successor_value)
metric_pct = (absolute_gap / P_pre) × 100
```

`metric_pct` is a percentage, denominated against `P_pre` (the known, evidence-bound predecessor reference price).

- **Zero/invalid denominator:** `P_pre` must be a positive, finite `Decimal`. A missing, non-positive, or malformed `P_pre` (or `P_succ`, or `R`) makes the predicate `NOT_EVALUABLE` (§11) rather than dividing by zero or defaulting to pass/fail. This is consistent with — and does not re-derive — design §10's own separately-listed quarantine reason "missing/non-positive prices," which excludes such rows upstream of this check.
- **Missing operand:** any of `P_pre`, `P_succ`, `R` absent from the payload → `NOT_EVALUABLE`.
- **Malformed operand:** any of the three not parseable as a finite, positive-where-required `Decimal` → `NOT_EVALUABLE`.

## 7. D3 — Tolerance compatibility

`mechanical_nav_tolerance_pct` is itself a percentage (its own name, and its example value `"0.50"` in the design's payload contract, confirm this). `metric_pct` as defined in §6 is also a percentage denominated the same way. **No dimensional conflict exists**; the already-governed tolerance applies directly with no reinterpretation of its units or scale.

## 8. D4 — Inclusivity

```text
PASS  iff  metric_pct <= mechanical_nav_tolerance_pct
FAIL  iff  metric_pct >  mechanical_nav_tolerance_pct
```

Equality (`metric_pct == mechanical_nav_tolerance_pct`) **passes**. This matches this same design document's own established phrasing convention for tolerance boundaries elsewhere (§6.3: "within the authoritative absolute basis tolerance," "within the authoritative absolute storage tolerance" — both naturally inclusive of the boundary value itself). No case is left for an implementation to guess between `<` and `<=`.

## 9. D5 — Decimal construction and rounding

- `P_pre`, `P_succ`, `R`, and `mechanical_nav_tolerance_pct` are each constructed as `Decimal` directly from their payload base-10 string representations (design principle #4: "Decimal strings in the payload are authoritative"). No binary float ever participates.
- `implied_successor_value`, `absolute_gap`, and `metric_pct` are computed as exact `Decimal` arithmetic at full ambient precision (no precision reduction below the repository's existing default `Decimal` context, which already applies to all other payload arithmetic in this design — no new precision policy is introduced).
- **No intermediate quantization** is applied to any of `implied_successor_value`, `absolute_gap`, or `metric_pct`.
- **No final quantization** is applied before comparison; `metric_pct` is compared against `mechanical_nav_tolerance_pct` as exact `Decimal` values, consistent with design principle #4 and with preferring exact comparison wherever it is sufficient (it is sufficient here: both operands are already exact Decimal quantities with no repeating-fraction risk beyond ordinary Decimal division, which is deterministic under a fixed context precision).
- **No rounding mode** is introduced by this predicate. If ordinary `Decimal` division in `metric_pct`'s computation requires rounding to fit context precision, the repository's existing ambient `Decimal` context governs — this act creates no new, competing precision or rounding policy.
- Non-finite (`NaN`, `Infinity`) or otherwise malformed values for any operand yield `NOT_EVALUABLE`, never a numeric comparison.

## 10. D6 — Annotation semantics

**Field:** `boundary_evidence.suspension_gap_annotation` (already-governed identity).

**Presence normalization:**

| Value | Classification |
|---|---|
| `null` | absent |
| `""` | absent |
| whitespace-only | absent (`.strip()` normalization required before evaluating presence) |
| non-empty after `.strip()` | present |

**Normative effect.** Design §10 states, in immediate sequence: *(a)* the mechanical boundary value must reconcile within tolerance; *(b)* *"a genuine price move over the trading suspension is recorded as investment return through `suspension_gap_annotation`; it is not an external flow or repair"*; and separately lists, as two distinct quarantine reasons, *"mechanical continuity failure"* and *"an unannotated boundary discontinuity."* Read together, these can only be jointly satisfiable if annotation has a defined, narrow effect on the D2/D4 result — otherwise every genuine suspension-gap move exceeding the (necessarily tight) percentage tolerance would be permanently unresolvable, contradicting the design's own express acceptance of genuine suspension-gap return as legitimate. This act therefore establishes:

- A `FAIL` result (`metric_pct > mechanical_nav_tolerance_pct`) with **no** annotation present is classified `MECHANICAL_CONTINUITY_FAILURE` — an unexplained numeric discontinuity, treated as a defect.
- A `FAIL` result **with** a present (non-empty, trimmed) annotation is classified `ANNOTATED_BOUNDARY_DISCONTINUITY` — an evidenced, accepted genuine-return case, distinct from a defect finding.
- A `PASS` result (`metric_pct <= mechanical_nav_tolerance_pct`) is `PASS` regardless of whether annotation is present; annotation never affects an already-passing result.
- `NOT_EVALUABLE` (§6) is unaffected by annotation; a malformed/missing operand cannot be cured by annotating the failure.

**Anti-bypass bound.** This is not a blanket bypass: it changes only the *classification* of an already-computed, specific, numeric `FAIL` for *this* conversion's *own* evidence-bound boundary — it never suppresses computation of `metric_pct`, never widens `mechanical_nav_tolerance_pct`, never affects any other check (`SHARE_MISMATCH`, `BASIS_MISMATCH`, quote-identity quarantine, etc.), and requires a genuine non-empty string tied to this specific payload, not a generic flag. An empty or whitespace-only annotation on a `FAIL` result does not reclassify it.

## 11. Suspension-gap invariant — how D2/D6 jointly preserve it

`metric_pct` is computed and preserved as a first-class numeric result in every case, including `ANNOTATED_BOUNDARY_DISCONTINUITY` — the genuine market movement it measures is never zeroed, clamped, smoothed, or discarded; it remains visible in the record precisely because the predicate reports a *classified* result (`PASS` / `MECHANICAL_CONTINUITY_FAILURE` / `ANNOTATED_BOUNDARY_DISCONTINUITY` / `NOT_EVALUABLE`), not a boolean that erases the underlying magnitude. Annotation changes only the *classification* attached to a real, unmodified numeric discontinuity — never the discontinuity itself, and never the accounting treatment of the return it represents (§3's preserved invariant: no external flow, no repair). An unannotated, unexplained discontinuity is not silently accepted as return; it remains `MECHANICAL_CONTINUITY_FAILURE`.

## 12. Failure-domain / semantic result taxonomy

```text
PASS
MECHANICAL_CONTINUITY_FAILURE
ANNOTATED_BOUNDARY_DISCONTINUITY
NOT_EVALUABLE
```

This is the minimum canonical result taxonomy required to make design §10 mechanically implementable. It defines the *semantic result* only — no module, exception class, invocation point, or enforcement locus is selected here; those are D7 (§14).

## 13. Effect on `MINOR-2`

`DESIGN SEMANTICS RESOLVED — IMPLEMENTATION OBLIGATION OPEN`. `MINOR-2`'s WP5-owned half is not implementation-complete. No code exists yet that computes or enforces this predicate; that is D7 plus WP5 implementation, both outside this act.

## 14. D7 remains unauthorized — downstream requirement

This act authorizes **no enforcement locus, no module, no invocation point, and no failure-gating behavior**. The subsequent, separate **WP5 Implementation Authorization amendment** must determine and grant:

- **Enforcement responsibility:** which WP5-owned component computes §6–§12's predicate and where in the pipeline it runs.
- **Expected locus type:** a read-only validation/classification helper — this act creates no basis for it to be a mutation-authoring or write-path component.
- **Fail-closed/read-only nature:** to be decided/authorized by that amendment; this act neither requires nor forecloses either.
- **Relationship to `POSITION_CONVERSION_REBUILD_BOUNDARY`:** the two are distinct WP5-owned obligations (already established); the amendment must state whether they share an invocation point without merging their semantics.
- **No production mutation authority is implied by this act or by the amendment it authorizes being sought.**

## 15. Amendment form and history preservation

This is a new, additive artifact. No byte of `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md` is modified. The original design's §10 sentence remains as written; this record clarifies its previously-silent D2/D4/D5/D6 content without altering, superseding, or reopening any other design provision. This clarification is immediately authoritative for the stated normative content (§6–§12) under the external human authorization recorded in §1; it does not itself constitute, and does not await, a separate design-level freeze act — no such freeze mechanism exists for the design document in this repository (per `BANPU_DESIGN_AMENDMENT_AUTHORITY_DETERMINATION.md` §3), and none is invented here.

## 16. Exclusions (restated)

This act does not: implement WP5; resolve or authorize D7; mutate production data; execute snapshot reconstruction; amend unrelated design requirements; modify WP1–WP4 semantics; perform WP5 Planning Confirmation or Freeze; deploy; or stage/commit/push.
