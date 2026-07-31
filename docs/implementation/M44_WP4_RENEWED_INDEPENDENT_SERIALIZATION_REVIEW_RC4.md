# M44-WP4 — Renewed Independent Serialization Review RC4

**Milestone:** M44

**Work package:** M44-WP4 only

**Artifact class:** Renewed independent serialization review record

**Review candidate:** RC4

**Overall result:** APPROVED

**Serialization review status:** COMPLETE

**Point-4 confirmation eligibility:** ELIGIBLE

**Confirmation issued:** NO

**Freeze performed:** NO

**WP4 closed:** NO

**G-3 status:** OPEN — PARTIAL

**Runtime authority:** NONE

**Source-code authority:** NONE

**Persistence/schema/migration authority:** NONE

**API/transport authority:** NONE

**UI/presentation authority:** NONE

**Implementation authority:** NONE

**Provider authority:** NONE

**Production-method authority:** NONE

**Executable-validation authority:** NONE

**Capability-completion authority:** NONE

**Frozen-artifact-amendment authority:** NONE

**Gate-disposition authority:** NONE

**Ownership-determination authority:** NONE

**Vocabulary-admission authority:** NONE

**Encoding-selection authority:** NONE

---

## Executive Summary

Both carried serialization findings are resolved. The emitted grammar is
unchanged, the exact-stream recalculations match their documented streams, and
no new serialization finding exists.

## Carried Findings Disposition

### M44-WP4-SER-001

- Prior severity: MAJOR
- Disposition: RESOLVED
- Evidence: The contract clarifies F2–F8 positional opacity; `WP4-NV-ORDER-01`
  now uses an observable OA field-number-order defect.
- Remaining concern: NONE

### M44-WP4-SER-002

- Prior severity: MAJOR
- Disposition: RESOLVED
- Evidence: Explicit artificial payloads and exact OA, PA, and complete-stream
  bytes independently recalculate.
- Remaining concern: NONE

## Top-Level Grammar Assessment

The approved grammar uses a raw 31-octet schema tag, followed by exactly nine
length-prefixed components in fixed positional order. It requires complete
input consumption and rejects trailing bytes.

## Primitive Encoding Assessment

`u32` is exactly four unsigned octets in network byte order, with no alternate
integer representation. `lp` uses one canonical `u32` prefix equal to the
payload octet length, yielding unambiguous boundaries; truncation, mismatch,
and suffix material reject.

## Injectivity Assessment

Injectivity is established over the ordered tuple F2 through F8, OA, PA. An
unobservable producer semantic misassignment decodes as a different tuple and
does not create ambiguity or a second decode.

## Round-Trip Assessment

The exact artificial stream establishes:

`decode(encode(x)) = x`

and

`encode(decode(b)) = b`

with complete input consumption.

## Field-Framing Assessment

F2 through F8 remain opaque `lp` values. No nested parsing or normalization is
performed, no field-8-specific encoding is defined, and OA and PA retain their
distinct envelopes.

## Owner-Attribution Envelope Assessment

OA has count 10, contains fields 1 through 10 exactly once, and uses owner
counts `1, 1, 1, 1, 2, 2, 3, 1, 1, 2`. Owner and co-owner order is
deterministic. Malformed entries fail closed.

## Provenance-Association Envelope Assessment

PA has count 7 and fields 2 through 8, with item counts
`1, 0, 2, 0, 0, 0, 0`. Its exact artificial items are `a2`, `a4 01`, and
`a4 02`; their boundaries and item order are deterministic.

## Exact-Stream Recalculation

OA calculated length: 440 octets

OA documented length: 440 octets

OA equality: TRUE

PA calculated length: 77 octets

PA documented length: 77 octets

PA equality: TRUE

Complete stream calculated length: 591 octets

Complete stream documented length: 591 octets

Complete-stream equality: TRUE

| Component | Start | Length | End exclusive |
| --- | ---: | ---: | ---: |
| Raw schema tag | 0 | 31 | 31 |
| F2 | 31 | 5 | 36 |
| F3 | 36 | 5 | 41 |
| F4 | 41 | 5 | 46 |
| F5 | 46 | 5 | 51 |
| F6 | 51 | 5 | 56 |
| F7 | 56 | 5 | 61 |
| F8 | 61 | 5 | 66 |
| lp(OA) | 66 | 444 | 510 |
| lp(PA) | 510 | 81 | 591 |

## Positive-Vector Assessment

Every byte-level proof input is reproducible, and no unresolved proof
metavariable remains.

## Negative-Vector Assessment

`WP4-NV-ORDER-01` tests the observable OA order
`1, 3, 2, 4, 5, 6, 7, 8, 9, 10` and is correctly rejected. No vector claims
that semantic F2/F3 payload swaps are mechanically detectable.

## Coverage and Traceability Assessment

- Normative rows: 32
- Positive vectors: 35
- Negative vectors: 50
- Dangling normative-row references: NONE
- Dangling vector references: NONE
- Orphan positive vectors: NONE
- Orphan negative vectors: NONE
- Invalid range references: NONE

## Determinism Assessment

Output is independent of presentation order, map iteration, locale, Unicode
normalization, numeric formatting, library defaults, platform, and host
endianness.

## Failure-Mode Assessment

The approved fail-closed coverage rejects malformed tags, non-canonical
numbers, malformed lengths, truncation, excess payload, duplicate and unknown
entries, omission, excess components, explicit OA/PA order defects, and
trailing bytes.

## Documentary-Boundary Assessment

Artificial values retain:

- ARTIFICIAL
- NON-EFFECTIVE
- NON-CONFORMANCE-ESTABLISHING

They establish none of:

- source-owner conformance;
- G-3 closure;
- complete production Composition bytes;
- concrete PMS1;
- concrete PAIM1;
- implementation or runtime evidence.

## New Findings

NONE

## Final Determination

Carried serialization findings unresolved:
NONE

New serialization findings:
NONE

Overall Result:
APPROVED

Serialization review status:
COMPLETE

Eligibility for frozen M44 Architecture §12.5 point-4 confirmation:
ELIGIBLE

G-3 status observed:
OPEN — PARTIAL

WP4 status:
OPEN AND UNFROZEN

This review issues no point-4 confirmation, performs no freeze, performs no
closeout, and authorizes no implementation, runtime, checkpoint disposition,
M44-WP6, or M44-WP7.
