# BANPU-WP3 — Reference-Price Admissibility Clarification Record

**Artifact class:** Additive implementation clarification record (BANPU-WP3
governance corpus)
**Date:** 2026-08-11
**Issuing authority:** Architecture Owner / Constitutional Interpretation
Authority, recorded by the Additive Implementation Clarification Record
Authority
**Interpretation classification:** `A — IMPLEMENTATION CLARIFICATION, NO
PLANNING AMENDMENT REQUIRED`
**Disposition:** `BANPU-WP3 REFERENCE-PRICE ADMISSIBILITY CLARIFICATION
RECORDED`
**Authorized planning corpus identity (unchanged):**
`C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A`

---

## 1. Artifact classification

This record is:

- **Implementation clarification only.** It states what already-frozen
  canonical text means for implementation. It is not a planning artifact, not
  a design artifact, and not a review artifact.
- **Additive.** It adds one standalone artifact to the BANPU-WP3 governance
  corpus and changes no existing artifact.
- **Non-amending.** It alters no text, value, table, criterion, gate, decision,
  risk, or identity in any frozen BANPU-WP1, BANPU-WP2, or BANPU-WP3 artifact.
- **Non-authorizing.** It grants no implementation authority, extends no file
  surface, and opens no new work package.
- **Interpretive, not elective.** Every element below is derived from canonical
  text by citation. No element was chosen among admissible alternatives.

**This record creates no new planning decision.** It adds no PD, no acceptance
criterion, no gate, no obligation, and no residual. The frozen planning corpus
is complete and unchanged as to this subject.

**This record creates no new implementation authority.** WP3 implementation
authority is that already granted by
[BANPU_WP3_IMPLEMENTATION_AUTHORIZATION_RECORD.md](BANPU_WP3_IMPLEMENTATION_AUTHORIZATION_RECORD.md).
Nothing here enlarges it, and nothing here authorizes an act that the
Implementation Authorization Record did not already authorize.

## 2. Occasion

Independent Checkpoint C2 Review concluded `CHECKPOINT C2 — CHANGES REQUIRED`
with three blocking and two major findings. Two blocking findings were ordinary
implementation corrections. The third was not: it asserted that "decimal-exact"
reference-price admissibility is not sufficiently specified by the frozen WP3
planning corpus for provider evidence represented as Python `float` values, the
current WP3.2 implementation having accepted arbitrary finite positive floats as
decimal-exact.

The question was referred for constitutional interpretation. The interpretation
concluded that the corpus **is** sufficiently specified, that it supports a
unique answer, and that the premise shared by both the implementation and the
review finding — that a provider close is a "reference price" — is the actual
defect. This record fixes that conclusion durably, before any WP3.2 correction
relies upon it.

This record resolves **only** the meaning of decimal-exact reference-price
admissibility. It disposes of no other C2 finding.

## 3. Canonical referent of "reference price"

The referent is established by an unbroken citation chain, not by election.

**3.1 Origin of the residual.**
[BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md)
§16 states `MINOR-2` as: *"boundary-evidence decimal sign/range validation is
not yet consumer-specific … WP3 owns provider/reference-price admissibility;
WP5 owns mechanical continuity tolerance admissibility."*

The residual's subject is the `boundary_evidence` block of the
`POSITION_CONVERSION` payload.

**3.2 The WP3/WP5 split is a split between sibling fields of that one block.**

| `boundary_evidence` field | WP1 parse | Admissibility owner |
|---|---|---|
| `predecessor_reference_price` | `reader.decimal()` → `Decimal` | **WP3** |
| `successor_reference_price` | `reader.decimal()` → `Decimal` | **WP3** |
| `mechanical_nav_tolerance_pct` | `reader.decimal()` → `Decimal` | WP5 |
| `suspension_gap_annotation` | `reader.string()` → `str` | Not a numeric admissibility subject |

**3.3 Corroboration across the frozen corpora.**

| Source | Text | Effect |
|---|---|---|
| [BANPU_WP1_FREEZE_RECORD.md](BANPU_WP1_FREEZE_RECORD.md) §7 | "`MINOR-2` … WP3 for reference prices; WP5 for mechanical tolerance" | Same split, frozen at WP1 |
| [BANPU_WP1_CONFIRMATION.md](BANPU_WP1_CONFIRMATION.md) §5 | "WP3 reference-price validation and WP5 tolerance validation, each with focused rejection tests" | Same split, confirmed at WP1 |
| [BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md](BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md) §4.2 | "Reference-price admissibility: present, positive, finite, decimal-exact, and evidence-bound. Mechanical continuity tolerance is excluded and belongs to WP5." | The exclusion clause is coherent only if the property list describes that field's sibling — pinning the referent to `boundary_evidence` |
| [BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md](BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §9.2, A9 | Anchor column reads `` `MINOR-2`, WP3 half only`` | A9 inherits `MINOR-2`'s subject |
| Design §10 | "mechanical boundary value MUST reconcile within the payload tolerance using evidence-bound reference prices" | Reference prices and the tolerance they reconcile against are both payload-side |

**3.4 Established referent.** A "reference price" in BANPU-WP3 is exactly one of
the two `boundary_evidence` fields `predecessor_reference_price` and
`successor_reference_price` of a valid `POSITION_CONVERSION` payload, as parsed
by the frozen WP1 contract into
`transaction_canonicalizer.PositionConversionBoundaryEvidence`.

**3.5 Reading of plan §7.3.** The obligation phrase *"Reject inadmissible
provider and reference prices at the point of consumption"* is a conjunction of
two distinct obligations over two distinct value classes. It is not a compound
noun and does not make a provider close a reference price.

## 4. Provider closes are a distinct value class

Provider `current_close` and `previous_close` values are **not** reference
prices for purposes of `MINOR-2` or A9 decimal-exact admissibility.

| | Boundary-evidence reference price | Provider close |
|---|---|---|
| Origin | `POSITION_CONVERSION` ledger payload | Provider quote response |
| Canonical producer | Frozen WP1 parser | WP3.1 provider adapter |
| Canonical type | `decimal.Decimal` | Provider-supplied number |
| Governing canon | `MINOR-2` WP3 half; A9; Decomposition §4.2 | PD-4 E1–E5; design §10 "missing/non-positive prices" |
| Decimal-exact required | **Yes** | **No** |

Provider closes remain governed by E1–E5 together with presence, positivity,
and finiteness. **Extending the decimal-exact requirement to provider closes is
not authorized**; the corpus nowhere applies it to them, and E4 requires only
that current and previous close be derivable from a single response.

## 5. Exact admissibility rule

Two predicates. They are distinct and non-substitutable. Neither may be applied
to the other's operand class.

### 5.1 Reference-price admissibility (WP3's half of `MINOR-2`; A9)

Evaluated at the point of consumption, against a `boundary_evidence` reference
price. All five elements are required:

| # | Element | Meaning |
|---|---|---|
| 1 | **Present** | The field exists on a valid `PositionConversionParseResult` |
| 2 | **Decimal-exact** | The value **is** the `decimal.Decimal` supplied by the frozen WP1 parsed `boundary_evidence` contract. A value of any other type, or a `Decimal` constructed by any path other than the frozen WP1 parser, fails this element |
| 3 | **Finite** | `Decimal.is_finite()` |
| 4 | **Positive** | Strictly greater than zero — the sign half of `MINOR-2`'s "sign/range validation" |
| 5 | **Evidence-bound** | Read from a payload carrying the mandatory `evidence` block (`reference`, `source`, `captured_at`) |

Failure of any element yields the enumerated quarantine reason. Exactly one
enumerated reason is emitted, per A7.

**No decimal-place threshold, precision bound, significant-digit count, or
exponent range is imposed.** Decimal exactness is a property of type and
provenance, not of digit count. Any numeric threshold would be an invention and
is prohibited.

### 5.2 What decimal exactness protects against

Loss of base-10 identity between the authoritative broker or official reference
record and the value the platform later reconciles. Design §10 requires the
mechanical boundary value to reconcile within the payload tolerance using
evidence-bound reference prices; that verdict must not turn on binary
floating-point representation error, nor accept a non-canonical numeric form.
The frozen WP1 parser forecloses both at parse time: payload decimals must be
plain base-10 **strings** matching the canonicalizer's plain-decimal pattern,
and non-string input is rejected outright before any value exists.

### 5.3 Provider-close admissibility

Presence, positivity, finiteness, and E1–E5. Decimal exactness is not an
element. Whether this retains a separately named predicate in code is an
implementation decision under existing authority, constrained only by design
§10 and by A7's one-reason-per-quarantine invariant.

### 5.4 Structural guarantee of evidence-boundness

Both `boundary_evidence` and `evidence` are mandatory, non-optional members of
the frozen `PositionConversion` payload type, with required-key enforcement in
the frozen parser. Consuming a valid parsed payload therefore establishes
element 5 structurally. No provenance metadata need be carried alongside a
number, and none may be invented.

## 6. Prohibited construction path

**`Decimal(str(value))` may not be used to manufacture an admissible reference
price from a provider float, or from any other non-canonical source.**

It fabricates apparent base-10 exactness for a value that has already lost
base-10 identity, and it introduces a second construction path for a value
whose sole canonical construction path is the frozen WP1 parser. A raw Python
`float` does not satisfy decimal-exact reference-price admissibility, and no
conversion makes it satisfy it.

This prohibition is scoped exactly to reference-price construction. It says
nothing about the idiom's use elsewhere in the platform, including its existing
use inside the frozen WP1 module for legacy transaction fields, which is
outside this subject and unaffected.

## 7. Effect on WP3.1

**WP3.1 is unaffected and remains accepted.** No change is required to
`backend/services/market_data/yahoo_chart.py` or to its tests by reason of this
clarification.

Specifically:

- Provider close fields typed as `Optional[float]` are constitutionally
  admissible, because provider closes are not reference prices.
- WP3.1 evidence is **not** required to preserve an exact decimal representation
  of provider payload data.
- WP3.1 evidence is **not** required to carry the provider's original textual or
  base-10 representation.
- No E1–E5 element is added, removed, or reinterpreted.
- Altering provider-response decoding to preserve textual numeric form is not
  required by any canonical text and is **not authorized by this record**.

WP3.1 is not reopened.

## 8. Effect on WP3.2

**WP3.2 must re-base its reference-price admissibility predicate onto
`PositionConversionBoundaryEvidence`.**

The predicate in `backend/services/market_data/position_conversion_quote_contract.py`
is presently applied to provider close fields. Under the established referent it
is applied to the wrong operand class, and no code path in that module consults
either `boundary_evidence` reference price.

Consequences, recorded as facts:

- **`MINOR-2`'s WP3 half is undischarged.** It is not discharged too
  permissively; it is not discharged at all.
- **A9 is unsatisfied**, for the same reason.
- **Both remain undischarged until the correction is implemented and
  independently accepted.** Neither this record, nor the interpretation it
  records, discharges either one. Only implementation followed by independent
  acceptance can.
- The existing enumerated members `NON_DECIMAL_EXACT` and
  `REFERENCE_PRICE_INADMISSIBLE` remain valid. No new quarantine reason is
  required, and none is authorized here.
- The existing predicate shape — taking an object and a field selector rather
  than a bare number — was correct in form; only its operand class is wrong.
- Consuming a fourth read-only type from the frozen WP1 canonicalizer module is
  the same read-only relationship WP3.2 already has with three such types. It is
  **not** a file-surface change, and the frozen WP1 parser is not amended,
  imported for mutation, or otherwise touched.

**Correction is confined to WP3.2 implementation.** It changes no architecture,
no planning scope, no file surface, no gate, and no acceptance criterion.

This record does **not** perform that correction, does not prescribe its code,
and does not accept it.

## 9. WP5 ownership preserved

Mechanical continuity tolerance admissibility remains **WP5's**, exactly as
frozen. Specifically:

- `mechanical_nav_tolerance_pct` admissibility is WP5's, not WP3's.
- The boundary reconciliation of design §10 is WP5's, not WP3's.
- WP3 performs admissibility checking only; it performs no tolerance
  comparison, no reconciliation, and no continuity evaluation.
- No tolerance, reconciliation, or continuity parameter may enter WP3 code by
  reason of this clarification.
- Plan §7.2's statement that WP5 receives reference prices "already
  admissibility-checked" is preserved and is the reason WP3's half exists.

## 10. Preservation statements

**10.1 Frozen BANPU-WP3 planning artifacts.** Unchanged. Verified byte-identical
after creation of this record:

| Artifact | Bytes | Lines | SHA-256 |
|---|---|---|---|
| `BANPU_WP3_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` | 40,882 | 688 | `1F4E21FBC275FF5AA6CC061E2A7AD7972B41008926D8E8E4648C1C07A9C2F096` |
| `BANPU_WP3_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md` | 17,909 | 430 | `A6A4AB0AC4DE1E7B1813EEFFB01E2F48A662DA9B937F1BF1A45982B065294462` |
| `BANPU_WP3_PLANNING_FREEZE_RECORD.md` | 20,789 | 390 | `85FBDF9DB5B8EAC71A9DA7C82445E5A465E61548FD235A93D1E2A96E22924D90` |
| `BANPU_WP3_ALLOCATION_RECORD.md` | 15,730 | 287 | `05F248B5B5965314AA1DF060155FE5B40BA87C13DA054DF19D13F7917152E2CB` |
| `BANPU_WP3_IMPLEMENTATION_AUTHORIZATION_RECORD.md` | 22,934 | 406 | `E723CC426C87B956C125B4EE7C8407DC1739F02814BFB8E4CCEE42ABF51DA667` |

**10.2 Authorized planning corpus identity.** Recomputed over the two-member
authorized corpus under the canonical Git-canonical-LF convention and the
recorded manifest algorithm:
`C7B6CEEFF29565AC84C83FCF0F61E52303989B1D03DBAC6E1144566C0670638A` — unchanged.

**10.3 Frozen BANPU-WP1 and BANPU-WP2 artifacts.** Unchanged. No member of
either frozen corpus was modified. `backend/services/transaction_canonicalizer.py`
is byte-identical to its recorded WP1 identity
(`59339DCBAF1BF7838BE0E472F562C9BCCACE0990598A564301F5F0BD3BE4560E`, 31,416
bytes, under the per-row convention recorded at
[BANPU_WP3_PLANNING_FREEZE_RECORD.md](BANPU_WP3_PLANNING_FREEZE_RECORD.md)
§11.3).

**10.4 Implementation files.** No production file and no test file was created,
modified, or deleted by this act.

**10.5 No re-confirmation and no re-freeze.** No planning amendment is required,
so no re-confirmation of BANPU-WP3 planning occurs and no re-freeze occurs. The
Planning Freeze Record and the Allocation Record stand as issued.

**10.6 No WP3.3 authority is created.** This record creates no WP3.3 authority,
does not begin WP3.3, does not satisfy Gate S8, and does not wire the WP3.2
module into any consumer. WP3.2 remains deliberately unwired.

## 11. Excluded effects

This record does not:

- amend, reinterpret, or extend any frozen planning artifact;
- create a planning decision, acceptance criterion, gate, obligation, residual,
  or risk;
- create or extend implementation authority, file surface, or work-package
  scope;
- perform the WP3.2 correction, or prescribe its implementation;
- discharge `MINOR-2`'s WP3 half or A9;
- perform Checkpoint C2 re-review, or dispose of any other C2 finding;
- perform implementation review, confirmation, or freeze;
- alter WP5, WP4, or WP6 scope;
- authorize any commit, push, deployment, or release.

## 12. Verification performed after creation

| Check | Result |
|---|---|
| Only this record created by this act | `SATISFIED` |
| Frozen WP3 planning corpus identity unchanged | `SATISFIED` |
| All five prior WP3 governance artifacts byte-identical | `SATISFIED` |
| Frozen WP1 canonicalizer byte-identical | `SATISFIED` |
| No production file changed by this act | `SATISFIED` |
| No test file changed by this act | `SATISFIED` |
| Repository hygiene checks | `PASS` |

## 13. Disposition

`BANPU-WP3 REFERENCE-PRICE ADMISSIBILITY CLARIFICATION RECORDED`

## 14. Exact next act

**BANPU-WP3.2 Correction Round** — close all remaining Checkpoint C2 findings,
then rerun Independent Checkpoint C2 Review.

That round proceeds under the implementation authority already granted by the
Implementation Authorization Record. It is not performed by this record.
