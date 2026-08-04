# Asset Foundation - AF-WP2 Package-Local Vector Annex

**Artifact class:** AF-WP2 package-local documentary vector annex  
**Parent form:** AF-2 Denomination Identifier Dimension Canonical Form, version v1  
**Status:** IMPLEMENTATION CANDIDATE - NOT REVIEWED, CONFIRMED, CONTENT-IDENTIFIED, FROZEN, OR CLOSED  
**Scope:** Positive, boundary, negative, and temporal documentary vectors for AF-2/v1 only  
**Implementation authority:** AF-WP2 only  
**Executable-test authority:** NONE

This annex is authored with and exclusively bound to
[ASSET_FOUNDATION_AF_WP2_AF_2_DENOMINATION_IDENTIFIER_DIMENSION_CANONICAL_FORM.md](ASSET_FOUNDATION_AF_WP2_AF_2_DENOMINATION_IDENTIFIER_DIMENSION_CANONICAL_FORM.md).
It is documentation-only. It is not a parser fixture, validator suite,
currency code list, registry dataset, provider mapping, production method, or
source of additional semantics.

The vectors use illustrative opaque 16-byte sequences. They do not assign
human-readable names, mint a denomination value, assert registry existence,
assume ISO 4217, or provide a provider or Ledger mapping.

No vector in this annex is canonical supply before the AF-WP2 pair completes
its later independent review, confirmation, content-identity validation, and
freeze lifecycle. The annex performs none of those acts.

## 1. Parent binding and annex identity

| Item | Value |
| --- | --- |
| Owner domain | Asset Foundation |
| Work package | AF-WP2 |
| Parent artifact | docs/implementation/ASSET_FOUNDATION_AF_WP2_AF_2_DENOMINATION_IDENTIFIER_DIMENSION_CANONICAL_FORM.md |
| Parent form | AF-2 |
| Parent form version | v1 |
| Annex artifact | docs/implementation/ASSET_FOUNDATION_AF_WP2_VECTOR_ANNEX.md |
| Annex revision | AF-WP2-VECTOR-ANNEX-1 |
| Parent content identity | Not yet validated; no hash asserted |
| Annex content identity | Not yet validated; no hash asserted |
| Predecessor | Frozen Asset Foundation planning corpus as scope authority; no prior AF-2 form |
| Supersedes | None |
| Lifecycle position | Post-authorization documentary implementation; pre-review |

The annex cannot be detached from, reordered against, summarized over, or
replaced for the parent form. Any material change to a vector or vector
meaning is a change to the AF-2 implementation pair.

## 2. Vector notation and interpretation

The payload column shows the exact lexical payload unless the row explicitly
states a byte suffix, prefix, or semantic provenance condition. Literal
payload rows contain no surrounding quotes or whitespace.

All positive and boundary payloads are documentary examples of owner-minted
opaque 16-byte dimension-value reference content. The examples deliberately
do not name the dimension value. They are examples of the selected
representation, not an enumeration.

CONFORMS means the bytes satisfy the AF-2/v1 documentary grammar. It does
not, by itself, prove that a token was lawfully minted, assigned to one
dimension value, or known to a consumer's authority. REJECT means the
payload cannot be accepted as a conforming AF-2/v1 reference for the stated
reason. FAIL CLOSED means no default, live lookup, inference, selection, or
provider substitution is permitted.

## 3. Coverage map

| Required coverage | Vector IDs |
| --- | --- |
| Exact positive AF-2/v1 single-denomination references | AF-WP2-PV-001 through AF-WP2-PV-005 |
| Fixed-length, delimiter, byte-content, framing, cardinality, and EOF boundaries | AF-WP2-BV-001 through AF-WP2-BV-010 |
| Missing, malformed, encoding, ordering, cardinality, normalization, and prohibited-field negatives | AF-WP2-NV-001 through AF-WP2-NV-018 |
| Owner assignment, unknown, ambiguity, multi-value, absence, and external-code failures | AF-WP2-NV-019 through AF-WP2-NV-028 |
| Stable dimension identity, time-varying asset assertions, provider changes, and successor rules | AF-WP2-TV-001 through AF-WP2-TV-010 |

## 4. Positive vectors

All payloads in this section are exact 30-byte US-ASCII sequences. Each has a
22-character canonical unpadded Base64url token that decodes to exactly 16
opaque bytes.

| ID | Exact payload | Decoded opaque bytes | Expected documentary interpretation |
| --- | --- | --- | --- |
| AF-WP2-PV-001 | AF-2:v1:AAECAwQFBgcICQoLDA0ODw | 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F | CONFORMS; one opaque reference for one owner-domain denomination value |
| AF-WP2-PV-002 | AF-2:v1:ABEiM0RVZneImaq7zN3u_w | 00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF | CONFORMS; leading zero and high bytes are retained without text meaning |
| AF-WP2-PV-003 | AF-2:v1:_____________________w | FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF | CONFORMS; URL-safe _ is required and remains opaque |
| AF-WP2-PV-004 | AF-2:v1:AAAAAAAAAAAAAAAAAAAAAA | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 | CONFORMS; all-zero bytes are not an absence sentinel |
| AF-WP2-PV-005 | AF-2:v1:AQIDBAUGBwgJCgsMDQ4PEA | 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10 | CONFORMS; one owner-domain dimension reference |

The positive vectors do not assert that any particular external currency,
provider code, Ledger coordinate, asset, or classification assertion exists.

## 5. Boundary vectors

| ID | Payload or condition | Expected boundary result |
| --- | --- | --- |
| AF-WP2-BV-001 | AF-2:v1:AAECAwQFBgcICQoLDA0ODw | CONFORMS; the fixed payload is exactly 30 US-ASCII bytes |
| AF-WP2-BV-002 | The exact eight-byte prefix AF-2:v1: followed by exactly 22 token bytes | CONFORMS only if all token and owner-domain rules pass; no alternate prefix is admitted |
| AF-WP2-BV-003 | Any valid 22-character token with exactly 16 decoded bytes | CONFORMS lexically; 22 characters is both the shortest and longest admitted token length |
| AF-WP2-BV-004 | AF-2:v1:AAAAAAAAAAAAAAAAAAAAAA | CONFORMS; leading and all-zero decoded bytes are preserved |
| AF-WP2-BV-005 | AF-2:v1:_____________________w | CONFORMS; all high-bit decoded bytes are representable without Unicode |
| AF-WP2-BV-006 | A token whose final Base64 sextet has zero unused low-order bits, such as the final w in ...ODw | CONFORMS; canonical unused-bit treatment is satisfied |
| AF-WP2-BV-007 | Any finite 16-byte sequence, including leading zero bytes, encoded with canonical unpadded Base64url | CONFORMS lexically; no byte position has business meaning |
| AF-WP2-BV-008 | The exact 30-byte payload with no following byte | CONFORMS; end-of-input is immediate and required |
| AF-WP2-BV-009 | One token and no dimension-name field | CONFORMS; the AF-2 form tag fixes the dimension-specific meaning |
| AF-WP2-BV-010 | One complete payload representing one opaque reference only | CONFORMS; cardinality is exactly one and no list or repeated field exists |

The fixed token width intentionally leaves no implementation-defined minimum,
maximum, or truncation boundary. The owner-domain meaning of the opaque bytes
is not inferred from their content.

## 6. Negative vectors

Every row below is rejected as an AF-2/v1 payload or denomination-reference
claim. Rows marked lexically valid / semantically rejected demonstrate the
distinction between byte shape and owner-domain admission.

| ID | Non-conforming payload or condition | Expected rejection and reason |
| --- | --- | --- |
| AF-WP2-NV-001 | AF-2:v1: | REJECT; empty identifier and no affirmative absence state |
| AF-WP2-NV-002 | Missing payload, null, NONE, ABSENT, or UNKNOWN | REJECT; omission and sentinels cannot represent a denomination value |
| AF-WP2-NV-003 | AF-2:v1:AAECAwQFBgcICQoLDA0OD | REJECT; token has 21 characters and cannot decode to the required 16 bytes |
| AF-WP2-NV-004 | AF-2:v1:AAECAwQFBgcICQoLDA0ODwA | REJECT; token has 23 characters and leaves unread material |
| AF-WP2-NV-005 | AF-2:v1:AAECAwQFBgcICQoLDA0ODx | REJECT; final Base64 sextet has non-zero unused bits |
| AF-WP2-NV-006 | AF-2:v1:AAECAwQFBgcICQoLDA0ODw= | REJECT; Base64 padding is forbidden |
| AF-WP2-NV-007 | AF-2:v1:AAECAwQFBgcICQoLDA0OD+/ | REJECT; + and / are outside the Base64url alphabet |
| AF-WP2-NV-008 | af-2:v1:AAECAwQFBgcICQoLDA0ODw | REJECT; form tag is an exact, case-sensitive literal |
| AF-WP2-NV-009 | AF-2:V1:AAECAwQFBgcICQoLDA0ODw | REJECT; version literal is case-sensitive |
| AF-WP2-NV-010 | AF-2:v2:AAECAwQFBgcICQoLDA0ODw | REJECT under AF-2/v1; no version negotiation is defined |
| AF-WP2-NV-011 | AF-2:AAECAwQFBgcICQoLDA0ODw | REJECT; version field is missing |
| AF-WP2-NV-012 | AF-2:v1:AAECAwQFBgcICQoLDA0ODw:extra | REJECT; extra delimiter and field |
| AF-WP2-NV-013 | AF-2:v1:AAECAwQFBgcICQoLDA0ODwAF-2:v1:ABEiM0RVZneImaq7zN3u_w | REJECT; concatenated duplicate records are not one AF-2 payload |
| AF-WP2-NV-014 | AF-2:v1:AAECAwQFBgcICQoLDA0ODw followed by byte 0A | REJECT; trailing line feed violates exact EOF |
| AF-WP2-NV-015 | Bytes EF BB BF followed by AF-2:v1:AAECAwQFBgcICQoLDA0ODw | REJECT; UTF-8 BOM is not part of the payload |
| AF-WP2-NV-016 | AF-2:v1:AAECAwQFBgcICQoLDA0ODw followed by a space | REJECT; trailing space is a forbidden byte |
| AF-WP2-NV-017 | AF-2:v1:AAECAwQFBgcICQoLDA0ODw%20 | REJECT; percent encoding and extra material are not decoded |
| AF-WP2-NV-018 | {"denomination":"AF-2:v1:AAECAwQFBgcICQoLDA0ODw"} | REJECT; JSON is not AF-2 framing |
| AF-WP2-NV-019 | AF-2:v1:USD or any ISO/provider/display code supplied as the token | REJECT; no external code is adopted, mapped, or padded |
| AF-WP2-NV-020 | A Ledger Base Currency coordinate, rate, conversion, or portfolio field appended to a valid payload | REJECT; Ledger and portfolio semantics are forbidden fields |
| AF-WP2-NV-021 | A second denomination_identifier_token field or a repeated token inside one claimed payload | REJECT; exact cardinality is one and no repeated fields exist |
| AF-WP2-NV-022 | AF-2:v1:AAECAwQFBgcICQoLDA0ODw followed by a second valid AF-2 payload | REJECT; multiple records cannot be ordered or collapsed |
| AF-WP2-NV-023 | A non-canonical token is trimmed, case-folded, padded, or re-encoded before comparison | REJECT; normalization cannot cure non-canonical bytes |
| AF-WP2-NV-024 | A lexically valid token was derived from a provider, display label, or ISO code and presented as owner supply | LEXICALLY VALID / SEMANTICALLY REJECTED; external derivation is not Asset Foundation ownership |
| AF-WP2-NV-025 | A lexically valid token has no established assignment to one Asset Foundation denomination value | LEXICALLY VALID / SEMANTICALLY UNKNOWN; fail closed and do not perform a lookup |
| AF-WP2-NV-026 | One lexically valid token is claimed for two distinct denomination values | LEXICALLY VALID / FAIL CLOSED; ambiguity is surfaced and no value is selected |
| AF-WP2-NV-027 | One asset-specific assertion supplies two or more denomination values or references | REJECT; AF-2 cannot select, sort, or collapse multiple values into one |
| AF-WP2-NV-028 | A missing or unknown assertion is filled by a current value, preferred value, ambient default, or live lookup | REJECT / FAIL CLOSED; no absence or unknown substitute is authorized |

The same byte payload can therefore be lexically conforming in one row and
semantically rejected in another when the owner-domain provenance condition is
different. The form never treats lexical shape as proof of owner assignment.

## 7. Temporal vectors

Each temporal row compares exact AF-2 payload bytes across a documentary event.
The event may change an external evidence or classification assertion, but it
does not silently change the AF-2 identity reference.

| ID | Before / after condition | Expected invariant |
| --- | --- | --- |
| AF-WP2-TV-001 | A human-readable denomination label or display translation changes while the same dimension value remains intended; AF-2 before and after is AF-2:v1:AAECAwQFBgcICQoLDA0ODw | PASS; label changes do not change dimension identity bytes |
| AF-WP2-TV-002 | A provider code changes or the provider mapping disappears; the same owner reference remains AF-2:v1:AAECAwQFBgcICQoLDA0ODw | PASS; provider evidence is external to AF-2 |
| AF-WP2-TV-003 | A provider recycles a code for a different denomination value; old value uses AAECAwQFBgcICQoLDA0ODw, new value uses ABEiM0RVZneImaq7zN3u_w | PASS; recycled external codes do not alias owner references |
| AF-WP2-TV-004 | An asset-specific assertion is restated at a later effective time with the same denomination value | PASS; a new dated assertion may exist, but the referenced AF-2 bytes remain unchanged |
| AF-WP2-TV-005 | An asset-specific assertion changes from dimension value D1 to distinct value D2 at an effective boundary | PASS; the later assertion cites D2's distinct reference and historical D1 remains unchanged |
| AF-WP2-TV-006 | A classification assertion is missing or unknown for an interval | PASS; no current, preferred, or default AF-2 reference is substituted |
| AF-WP2-TV-007 | The source renames, retires, splits, merges, or otherwise changes an external relationship for a value | PASS; an existing token is not retargeted; distinct new values require distinct references or a later governed successor |
| AF-WP2-TV-008 | The source discovers that a token was assigned the wrong meaning | PASS; the token is not silently repaired; the owner must block or produce an additive successor under later authority |
| AF-WP2-TV-009 | The same payload is replayed on different dates, locales, transports, or provider states | PASS; exact bytes and lexical interpretation are wall-clock and provider independent |
| AF-WP2-TV-010 | A future AF-2 successor version is introduced with an explicit supersession relation | PASS; AF-2:v1 retains v1 meaning and is never rewritten as the successor |

## 8. G-3 field and facet coverage

The annex supplies documentary coverage for the Asset Foundation-side
denomination identifier facet of the single joint Portfolio Base Currency G-3
element only.

| G-3 facet | Annex evidence |
| --- | --- |
| Exact positive single-denomination references | AF-WP2-PV-001 through AF-WP2-PV-005 |
| Fixed lexical and byte boundaries | AF-WP2-BV-001 through AF-WP2-BV-007 |
| Framing, EOF, dimension binding, and cardinality | AF-WP2-BV-008 through AF-WP2-BV-010; AF-WP2-NV-012 through AF-WP2-NV-022 |
| Missing, empty, and absence behavior | AF-WP2-NV-001 and AF-WP2-NV-002 |
| Grammar, version, token, and byte canonicality | AF-WP2-NV-003 through AF-WP2-NV-011 |
| Normalization and prohibited external fields | AF-WP2-NV-012 through AF-WP2-NV-024 |
| Unknown and owner-assignment behavior | AF-WP2-NV-025, AF-WP2-NV-026, and AF-WP2-NV-028 |
| Multiple values and ambiguity | AF-WP2-NV-021, AF-WP2-NV-022, AF-WP2-NV-026, and AF-WP2-NV-027 |
| Stable dimension identity and temporal assertion separation | AF-WP2-TV-001 through AF-WP2-TV-009 |
| Successor and supersession behavior | AF-WP2-TV-007, AF-WP2-TV-008, and AF-WP2-TV-010 |
| Joint-boundary limitation | Every section; no vector supplies a Ledger coordinate or G-3 closure |

This coverage record does not declare G-3 closed, release AF-WP2, release
AF-WP3 or AF-WP4, or release any downstream package. It is part of the AF-WP2
implementation candidate only.

## 9. Annex non-authority boundary

This annex does not:

- become an executable test suite, parser fixture, or validator;
- create a currency enumeration, ISO or provider code list, registry,
  database, schema, API, migration, provider mapping, or production method;
- author or supply a Ledger Base Currency coordinate, FX/conversion meaning,
  portfolio/reporting rule, asset record, or classification assertion;
- author AF-WP1, AF-WP3, AF-WP4, M42, M44, M45, Ledger & Accounting, or any
  downstream artifact;
- perform independent review, correction, focused re-review, confirmation,
  content-identity validation, freeze, release, or closeout; or
- amend, synchronize, or create a successor to the frozen planning corpus.

The annex's sole authority is to document AF-2/v1 examples and fail-closed
boundaries within AF-WP2.
