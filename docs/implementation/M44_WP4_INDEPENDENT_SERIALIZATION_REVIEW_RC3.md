# M44-WP4 — Independent Serialization Review RC3

**Milestone:** M44

**Work package:** M44-WP4 only

**Artifact class:** Independent serialization review record

**Review candidate:** RC3

**Overall result:** `NOT APPROVED`

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

## Executive Summary

Two MAJOR serialization-documentation findings remain. The byte grammar is deterministic for position-defined opaque values, but it cannot mechanically reject a swap of opaque top-level payloads, and several positive “byte” specimens are not reproducible because their opaque bytes are unspecified.

## Top-Level Grammar Assessment

Raw 31-octet tag plus nine length-prefixed components is unambiguous and fully consumed. The exact fixed positional grammar is clear.

## Primitive Encoding Assessment

`u32` is exactly four unsigned big-endian octets; all stated boundary encodings are correct. `lp(x)` is unambiguous, supports an empty primitive, and required coordinates correctly prohibit empty payloads.

## Injectivity Assessment

Injective for the positional tuple of opaque byte strings plus OA/PA envelopes. It is not mechanically capable of identifying a semantic F2/F3 swap as a malformed ordering event, since the two slots carry unrestricted opaque bytes.

## Round-Trip Assessment

Mechanically established for fully specified positional inputs. Documentary proof is incomplete where PA/artificial payload bytes are left as undefined metavariables.

## Field-Framing Assessment

F2–F8 are consistently exactly one opaque `lp` value. No nested parsing, text conversion, or field-8-specific nested encoding is introduced. F9 and F10 use their separate envelopes.

## Owner-Attribution Envelope Assessment

OA has a fixed count, field order, exact owner literals, deterministic co-owner order, and explicit duplicate/unknown/trailing rejection. The positive OA specimen matches the production and owner table.

## Provenance-Association Envelope Assessment

PA’s production is mechanically sound: seven ordered field entries, bounded opaque items, and explicit duplicate/count/trailing rules. Its positive specimen is not byte-reproducible because `a2`, `a4_1`, and `a4_2` have no octet assignments.

## Schema-Tag Assessment

The literal `M42-WP7-PORTFOLIO-COMPOSITION-1` is exactly 31 US-ASCII octets, raw and unframed. Alternate tags, tag framing, Unicode variants, terminators, and suffixes are rejected.

## Positive-Vector Assessment

Primitive and OA vectors are mechanically correct. PA, order, and full round-trip vectors contain undefined placeholders (`a2`, `a4_1`, `a4_2`, `OA`, `PA`) rather than complete reproducible byte sequences.

## Negative-Vector Assessment

Most rejection vectors map to explicit normative rows and accurately describe malformed framing, counts, tags, lengths, and suffixes. `WP4-NV-ORDER-01` is not mechanically accurate: `lp(F3) || lp(F2)` is simply a different valid pair of opaque positional values to a decoder.

## Coverage and Traceability Assessment

- Normative rows: 32
- Positive vectors: 35
- Negative vectors: 50
- Dangling normative-row references: 0
- Orphan vectors: 0

The coverage ledger is structurally complete, but the undefined positive specimens prevent full byte-level proof.

## Determinism Assessment

Ordering, endian choice, tag bytes, counts, owner ordering, and opaque-byte preservation are explicitly fixed. No locale, platform, normalization, formatter, map iteration, or host-endian dependency is admitted.

## Failure-Mode Assessment

Malformed tags, prefixes, counts, envelope entries, duplicates, unknown entries, omissions, extra components, and trailing bytes fail closed. No two conforming readers should split a well-formed byte stream differently. The sole issue is that a named-field reorder of unrestricted opaque top-level values cannot be recognized from bytes.

## Findings

### CRITICAL

NONE

### MAJOR

- **M44-WP4-SER-001 — Opaque top-level reorder vector is not mechanically rejectable.**
  Affected artifact: [negative vectors](m44/fixtures/M44_WP4_NEGATIVE_DOCUMENTARY_VECTORS.md), `WP4-NV-ORDER-01`; contract §4.3 and `WP4-NR-009/-022`.
  Exact problem: after the tag, F2–F8 are only positional opaque `lp` values. A sequence described externally as `lp(F3) || lp(F2)` is decoded as a valid F2 value followed by a valid F3 value; no byte-level field identifier or semantic inspection exists to reject it.
  Reproducible example: use distinct non-empty bytes `F2=02`, `F3=03`; swapping the two produces a valid stream with positional values `F2=03`, `F3=02`.
  Required correction: revise the vector and related claim to distinguish a malformed extra/reordered *grammar component* from a valid stream containing different opaque slot values; do not claim byte-level rejection of an unobservable semantic swap.
  Blocks final point-4 confirmation: **YES**.

- **M44-WP4-SER-002 — Positive PA/order/round-trip specimens are underspecified.**
  Affected artifact: [positive vectors](m44/fixtures/M44_WP4_POSITIVE_DOCUMENTARY_VECTORS.md), [PA specimen](m44/fixtures/M44_WP4_POSITIVE_DOCUMENTARY_VECTORS.md), and `WP4-PV-RT-01`.
  Exact problem: `a2`, `a4_1`, `a4_2`, `OA`, and `PA` are placeholders without assigned octets or an expanded complete stream. The claimed byte-for-byte and round-trip results cannot be independently reproduced.
  Reproducible example: multiple distinct assignments satisfy “exact opaque artificial non-empty byte strings,” yielding different PA and whole-container bytes.
  Required correction: assign explicit artificial hex octets and provide fully expanded OA, PA, order, and full round-trip expected byte streams; alternatively relabel these as parameterized templates rather than byte vectors.
  Blocks final point-4 confirmation: **YES**.

### MINOR

NONE

### EDITORIAL

NONE

## Final Determination

Unresolved serialization findings:

- M44-WP4-SER-001
- M44-WP4-SER-002

Overall Result:

NOT APPROVED

Serialization review status:

COMPLETE

Eligibility for frozen M44 Architecture §12.5 point-4 confirmation:

NOT ELIGIBLE

G-3 status observed:

OPEN — PARTIAL

WP4 status:

OPEN AND UNFROZEN

No repository files were modified, and this review does not issue point-4 confirmation.
