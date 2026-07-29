# M44-WP4 — Formal Serialization Response

**Milestone:** M44 — Portfolio Analytics Gate Closure and Normative Semantics Foundation

**Work package:** M44-WP4 only

**Artifact class:** Documentary serialization-correction response

**Review artifact:** [M44-WP4 Independent Serialization Review RC3](M44_WP4_INDEPENDENT_SERIALIZATION_REVIEW_RC3.md)

**Reviewed candidate:** `RC3`

**Corrected candidate:** `RC4`

**Review result:** `NOT APPROVED`

**Status:** `RC4 SERIALIZATION CORRECTIONS APPLIED; REQUIRES RENEWED INDEPENDENT SERIALIZATION REVIEW`

**Constitutional contract review:** `APPROVED` at RC3

**G-3:** `OPEN — PARTIAL`

**Confirmation issued:** `NO`

**Freeze performed:** `NO`

**WP4 closed:** `NO`

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
**Encoding-selection authority:** `NONE`

---

## 1. Response scope and effect

This response accepts and records the two `MAJOR` findings issued by the
[M44-WP4 Independent Serialization Review RC3](M44_WP4_INDEPENDENT_SERIALIZATION_REVIEW_RC3.md).
It records only the resulting RC4 serialization-documentation corrections to:

- [M44-WP4 Portfolio Composition Canonical Byte Representation Contract](M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md);
- [M44-WP4 Positive Documentary Vectors](m44/fixtures/M44_WP4_POSITIVE_DOCUMENTARY_VECTORS.md); and
- [M44-WP4 Negative Documentary Vectors](m44/fixtures/M44_WP4_NEGATIVE_DOCUMENTARY_VECTORS.md).

The emitted grammar remains unchanged. The raw schema tag, fixed field order,
`u32`, `lp`, `OA`, `PA`, opaque nested-byte boundary, ownership allocations,
and `G-3 OPEN — PARTIAL` determination are unchanged. No field identifier is
introduced into `F2` through `F8`, and no opaque nested byte is inspected or
reinterpreted.

This response does not perform renewed independent serialization review, issue
confirmation, freeze or close M44-WP4, declare the M44 §12.1.1 checkpoint
outcome, authorize implementation, or authorize M44-WP6 or M44-WP7.

## 2. Accepted correction dispositions

### 2.1 WP4-SR4-CORR-001

**Finding identifier:** `M44-WP4-SER-001`

**Severity:** `MAJOR`

**Disposition:** `ACCEPTED`

**Mechanical basis:** Top-level `F2` through `F8` are unrestricted opaque
length-prefixed values with no emitted field identifiers. A parser assigns
their semantic identities by fixed position. Swapping two payloads according
to producer intent therefore decodes as a different positional Composition
input; the semantic misassignment is not mechanically observable from bytes.

**Exact correction:** The contract now states the producer semantic-order
obligation, parser observability limits, and injectivity over the ordered tuple
of opaque values. It distinguishes mechanically malformed omission, excess,
duplicated framing, truncation, trailing bytes, and explicit `OA`/`PA`
field-number sequence errors from an unobservable semantic payload
misassignment. `WP4-NV-ORDER-01` now uses a reproducible explicit `OA`
field-number order defect. Related `PC-NGV-12`, checklist, duplicate-framing,
rejection, and coverage descriptions no longer claim that a semantic
`F2`/`F3`-style payload swap is rejected by byte decoding.

**Affected artifacts:**

- [M44-WP4 Portfolio Composition Canonical Byte Representation Contract](M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md); and
- [M44-WP4 Positive Documentary Vectors](m44/fixtures/M44_WP4_POSITIVE_DOCUMENTARY_VECTORS.md); and
- [M44-WP4 Negative Documentary Vectors](m44/fixtures/M44_WP4_NEGATIVE_DOCUMENTARY_VECTORS.md).

**Grammar changed:** `NO`

**G-3 changed:** `NO`

`M44-WP4-SER-001` was a vector and observability overclaim, not a grammar
ambiguity. The fixed positional grammar remains deterministic and injective
over its represented ordered inputs.

### 2.2 WP4-SR4-CORR-002

**Finding identifier:** `M44-WP4-SER-002`

**Severity:** `MAJOR`

**Disposition:** `ACCEPTED`

**Mechanical basis:** The RC3 positive PA, order, and round-trip specimens used
undefined `a2`, `a4_1`, `a4_2`, `OA`, and `PA` metavariables. Multiple byte
assignments satisfied those descriptions, so the asserted expected streams
could not be reproduced independently.

**Exact correction:** The positive vectors now assign exact artificial
payloads `a2 = a2`, `a4_1 = a4 01`, and `a4_2 = a4 02`; expand the exact
440-octet `OA` payload and exact 77-octet `PA` payload; and supply one complete
591-octet top-level stream with exact input components, decoded component
sequence, complete-consumption result, re-encoded stream, and equality
assertion. `WP4-PV-ORD-01` and `WP4-PV-RT-01` both identify that exact proof.
All synthetic payloads retain the mandatory `ARTIFICIAL`, `NON-EFFECTIVE`, and
`NON-CONFORMANCE-ESTABLISHING` labels and remain unusable as source-owner,
`G-3`, production Composition, `PMS1`, or `PAIM1` evidence.

**Affected artifacts:**

- [M44-WP4 Positive Documentary Vectors](m44/fixtures/M44_WP4_POSITIVE_DOCUMENTARY_VECTORS.md).

**Grammar changed:** `NO`

**G-3 changed:** `NO`

`M44-WP4-SER-002` was a documentary reproducibility gap, not an injectivity
failure. The emitted grammar remains unchanged.

## 3. Review lifecycle

Both findings are `ACCEPTED`, and their repository corrections are included in
the RC4 candidate. Renewed independent serialization review is required before
frozen M44 Architecture §12.5 point-4 confirmation can be considered.

Constitutional re-review is not required because these corrections change no
constitutional statement or authority boundary. If a later correction changes
either, constitutional re-review becomes required.

No confirmation is issued. No freeze is performed. M44-WP4 remains open and
unfrozen, and `G-3` remains `OPEN — PARTIAL`.
