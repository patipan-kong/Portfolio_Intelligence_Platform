# Asset Foundation — AF-WP1 Package-Local Vector Annex

**Artifact class:** AF-WP1 package-local documentary vector annex  
**Parent form:** `AF-1` Asset Identity Canonical Lexical Form, version `v1`  
**Status:** `IMPLEMENTATION CANDIDATE — NOT REVIEWED, CONFIRMED, CONTENT-IDENTIFIED, FROZEN, OR CLOSED`  
**Scope:** Positive, boundary, negative, and temporal documentary vectors for AF-1/v1 only  
**Implementation authority:** AF-WP1 only  
**Executable-test authority:** `NONE`

This annex is authored with and exclusively bound to
[ASSET_FOUNDATION_AF_WP1_AF_1_CANONICAL_LEXICAL_FORM.md](ASSET_FOUNDATION_AF_WP1_AF_1_CANONICAL_LEXICAL_FORM.md).
It is documentation-only. It is not a parser fixture, validator suite,
registry dataset, production method, or source of additional semantics.

No vector in this annex is canonical supply before the AF-WP1 pair completes
its later independent review, confirmation, content-identity validation, and
freeze lifecycle. The annex performs none of those acts.

## 1. Parent binding and annex identity

| Item | Value |
| --- | --- |
| Owner domain | Asset Foundation |
| Work package | AF-WP1 |
| Parent artifact | `docs/implementation/ASSET_FOUNDATION_AF_WP1_AF_1_CANONICAL_LEXICAL_FORM.md` |
| Parent form | `AF-1` |
| Parent form version | `v1` |
| Annex artifact | `docs/implementation/ASSET_FOUNDATION_AF_WP1_VECTOR_ANNEX.md` |
| Annex revision | `AF-WP1-VECTOR-ANNEX-1` |
| Parent content identity | Not yet validated; no hash asserted |
| Annex content identity | Not yet validated; no hash asserted |
| Predecessor | Frozen Asset Foundation planning corpus as scope authority |
| Supersedes | None |
| Lifecycle position | Post-authorization documentary implementation; pre-review |

The annex cannot be detached from, reordered against, summarized over, or
replaced for the parent form. Any material change to a vector or vector meaning
is a change to the AF-1 implementation pair.

## 2. Vector notation and interpretation

The payload column shows the exact lexical payload unless the row explicitly
states a byte suffix, prefix, or semantic provenance condition. Literal payload
rows contain no surrounding quotes or whitespace.

All positive and boundary payloads are documentary examples of owner-minted
opaque 16-byte identity content. The examples do not mint an identity, assert
registry existence, or provide a provider mapping.

`CONFORMS` means the bytes satisfy the AF-1/v1 documentary grammar. It does
not, by itself, prove that a token was lawfully minted or is known to a
consumer's authority. `REJECT` means the payload cannot be accepted as a
conforming AF-1/v1 reference for the stated reason. `FAIL CLOSED` means no
default, live lookup, inference, or provider substitution is permitted.

## 3. Coverage map

| Required coverage | Vector IDs |
| --- | --- |
| Exact positive AF-1/v1 references | `AF-WP1-PV-001` through `AF-WP1-PV-005` |
| Fixed-length, delimiter, byte-content, and EOF boundaries | `AF-WP1-BV-001` through `AF-WP1-BV-008` |
| Missing, malformed, encoding, ordering, cardinality, normalization, and prohibited-field negatives | `AF-WP1-NV-001` through `AF-WP1-NV-022` |
| Unknown, ambiguous, and provider-derived semantic failures | `AF-WP1-NV-023` through `AF-WP1-NV-025` |
| Rename, recycling, lifecycle, relationship, successor, classification, provider, and clock invariants | `AF-WP1-TV-001` through `AF-WP1-TV-009` |

## 4. Positive vectors

All payloads in this section are exact 30-byte US-ASCII sequences and have a
22-character canonical unpadded Base64url token that decodes to exactly 16
opaque bytes.

| ID | Exact payload | Decoded opaque bytes | Expected documentary interpretation |
| --- | --- | --- | --- |
| `AF-WP1-PV-001` | `AF-1:v1:AAECAwQFBgcICQoLDA0ODw` | `00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F` | `CONFORMS`; one opaque identity reference |
| `AF-WP1-PV-002` | `AF-1:v1:ABEiM0RVZneImaq7zN3u_w` | `00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF` | `CONFORMS`; leading zero and high bytes are retained |
| `AF-WP1-PV-003` | `AF-1:v1:_____________________w` | `FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF` | `CONFORMS`; URL-safe `_` is required and opaque |
| `AF-WP1-PV-004` | `AF-1:v1:AAAAAAAAAAAAAAAAAAAAAA` | `00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00` | `CONFORMS`; all-zero bytes are not an absence sentinel |
| `AF-WP1-PV-005` | `AF-1:v1:AQIDBAUGBwgJCgsMDQ4PEA` | `01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10` | `CONFORMS`; one permanent opaque reference |

## 5. Boundary vectors

| ID | Payload or condition | Expected boundary result |
| --- | --- | --- |
| `AF-WP1-BV-001` | `AF-1:v1:AAECAwQFBgcICQoLDA0ODw` | `CONFORMS`; fixed shortest and longest admitted token are both 22 characters |
| `AF-WP1-BV-002` | Any valid 22-character token beginning with `A` and ending in a canonical final character | `CONFORMS`; delimiters are adjacent to the token and no padding follows |
| `AF-WP1-BV-003` | `AF-1:v1:AAAAAAAAAAAAAAAAAAAAAA` | `CONFORMS`; leading and all-zero decoded bytes are preserved |
| `AF-WP1-BV-004` | `AF-1:v1:_____________________w` | `CONFORMS`; all high-bit decoded bytes are representable without Unicode |
| `AF-WP1-BV-005` | The exact eight-byte prefix `AF-1:v1:` followed by exactly 22 token bytes | `CONFORMS` only if all remaining rules pass; no alternate delimiter or prefix is admitted |
| `AF-WP1-BV-006` | The exact 30-byte payload with no following byte | `CONFORMS`; end-of-input is immediate and required |
| `AF-WP1-BV-007` | A valid token whose final Base64 sextet has zero unused low-order bits, such as the final `w` in `...ODw` | `CONFORMS`; canonical unused-bit rule is satisfied |
| `AF-WP1-BV-008` | A token containing any permitted alphabet character at any position, with no semantic bit assignment | `CONFORMS` lexically when the fixed-length and unused-bit rules pass; character appearance carries no business meaning |

The fixed token width intentionally makes the shortest and longest admitted
token the same boundary. There is no implementation-defined maximum or
minimum to select later.

## 6. Negative vectors

Every row below is rejected as an AF-1/v1 payload or identity claim. Rows
marked `lexically valid / semantically rejected` demonstrate the distinction
between byte shape and owner-domain identity admission.

| ID | Non-conforming payload or condition | Expected rejection and reason |
| --- | --- | --- |
| `AF-WP1-NV-001` | `AF-1:v1:` | `REJECT`; empty identity token and no affirmative absence state |
| `AF-WP1-NV-002` | Missing payload, `null`, `NONE`, `ABSENT`, or `UNKNOWN` | `REJECT`; omission and sentinels cannot represent identity |
| `AF-WP1-NV-003` | `AF-1:v1:AAECAwQFBgcICQoLDA0OD` | `REJECT`; token has 21 characters and cannot decode to the required 16 bytes |
| `AF-WP1-NV-004` | `AF-1:v1:AAECAwQFBgcICQoLDA0ODwA` | `REJECT`; token has 23 characters and leaves unread material |
| `AF-WP1-NV-005` | `AF-1:v1:AAECAwQFBgcICQoLDA0ODx` | `REJECT`; final Base64 sextet has non-zero unused bits |
| `AF-WP1-NV-006` | `AF-1:v1:AAECAwQFBgcICQoLDA0ODw=` | `REJECT`; Base64 padding is forbidden |
| `AF-WP1-NV-007` | `AF-1:v1:AAECAwQFBgcICQoLDA0OD+/` | `REJECT`; `+` and `/` are outside the URL-safe alphabet |
| `AF-WP1-NV-008` | `af-1:v1:AAECAwQFBgcICQoLDA0ODw` | `REJECT`; form tag is an exact, case-sensitive literal |
| `AF-WP1-NV-009` | `AF-1:V1:AAECAwQFBgcICQoLDA0ODw` | `REJECT`; version literal is case-sensitive |
| `AF-WP1-NV-010` | `AF-1:v2:AAECAwQFBgcICQoLDA0ODw` | `REJECT` under AF-1/v1; no version negotiation is defined |
| `AF-WP1-NV-011` | `AF-1:AAECAwQFBgcICQoLDA0ODw` | `REJECT`; version field is missing |
| `AF-WP1-NV-012` | `AF-1:v1:AAECAwQFBgcICQoLDA0ODw:extra` | `REJECT`; extra delimiter and field |
| `AF-WP1-NV-013` | `AF-1:v1:AAECAwQFBgcICQoLDA0ODwAF-1:v1:ABEiM0RVZneImaq7zN3u_w` | `REJECT`; concatenated duplicate records are not one AF-1 payload |
| `AF-WP1-NV-014` | `AF-1:v1:AAECAwQFBgcICQoLDA0ODw` followed by byte `0A` | `REJECT`; trailing line feed violates exact EOF |
| `AF-WP1-NV-015` | Bytes `EF BB BF` followed by `AF-1:v1:AAECAwQFBgcICQoLDA0ODw` | `REJECT`; UTF-8 BOM is not part of the payload |
| `AF-WP1-NV-016` | `AF-1:v1:AAECAwQFBgcICQoLDA0ODw ` | `REJECT`; trailing space is a forbidden byte |
| `AF-WP1-NV-017` | `AF-1:v1:AAECAwQFBgcICQoLDA0ODw%20` | `REJECT`; percent encoding and extra material are not decoded |
| `AF-WP1-NV-018` | `{"asset_id":"AF-1:v1:AAECAwQFBgcICQoLDA0ODw"}` | `REJECT`; JSON is not AF-1 framing |
| `AF-WP1-NV-019` | `AF-1:v1:AAPL` | `REJECT`; display/provider text is not a 22-character opaque token |
| `AF-WP1-NV-020` | A second `asset_id_token` field or a repeated token inside one claimed AF-1 payload | `REJECT`; exact cardinality is one and no repeated fields exist |
| `AF-WP1-NV-021` | A non-canonical token is trimmed, case-folded, padded, or re-encoded before comparison | `REJECT`; normalization cannot cure non-canonical bytes |
| `AF-WP1-NV-022` | A different valid token is presented as an alias for `AAECAwQFBgcICQoLDA0ODw` | `REJECT the alias claim`; different opaque bytes are not alternate spellings |
| `AF-WP1-NV-023` | A syntactically valid token was derived from a provider symbol and is presented as an `asset_id` | `LEXICALLY VALID / SEMANTICALLY REJECTED`; provider-derived identity is not owner-minted AF-1 supply |
| `AF-WP1-NV-024` | A valid token is claimed for two distinct identities | `LEXICALLY VALID / FAIL CLOSED`; ambiguity is surfaced and no identity is selected |
| `AF-WP1-NV-025` | A valid token is not present in a consumer's already-bound identity authority | `LEXICALLY VALID / UNRESOLVED`; no live lookup, default, or inferred identity is permitted |

## 7. Temporal vectors

Each temporal row compares exact AF-1 payload bytes across a documentary event.
The event may change an external evidence or classification fact, but it does
not change the AF-1 identity reference.

| ID | Before / after condition | Expected invariant |
| --- | --- | --- |
| `AF-WP1-TV-001` | An external symbol changes while the same platform identity remains the subject; AF-1 before and after is `AF-1:v1:AAECAwQFBgcICQoLDA0ODw` | `PASS`; rename changes evidence/display facts, not identity bytes |
| `AF-WP1-TV-002` | A provider disappears or stops publishing a mapping; the same historical reference remains `AF-1:v1:AAECAwQFBgcICQoLDA0ODw` | `PASS`; provider disappearance is not an identity event |
| `AF-WP1-TV-003` | A provider recycles an old symbol for a new instrument; old identity uses `AAECAwQFBgcICQoLDA0ODw`, new identity uses `ABEiM0RVZneImaq7zN3u_w` | `PASS`; recycled evidence does not reuse the old token |
| `AF-WP1-TV-004` | The identity becomes delisted, suspended, merged, or archived | `PASS`; lifecycle status is external and historical AF-1 bytes remain valid |
| `AF-WP1-TV-005` | Two related-but-distinct listings share an economic relationship but have separate accounting facts | `PASS`; each listing has a distinct AF-1 token; relationship is not aliasing |
| `AF-WP1-TV-006` | A merger or conversion creates a successor identity | `PASS`; predecessor payload remains historical; successor receives a distinct token |
| `AF-WP1-TV-007` | Sector, region, currency-of-denomination assertion, or other classification fact changes on a dated record | `PASS`; classification is outside the payload and the token is unchanged |
| `AF-WP1-TV-008` | The same payload is replayed on different dates, locales, transports, or provider states | `PASS`; exact bytes and interpretation are wall-clock and provider independent |
| `AF-WP1-TV-009` | A future AF-1 successor version is introduced | `PASS`; `AF-1:v1` retains v1 meaning and is not rewritten or interpreted as the successor |

## 8. G-3 coverage record

The annex supplies documentary coverage for the Asset Foundation `asset_id`
lexical-form element only.

| G-3 facet | Annex evidence |
| --- | --- |
| Exact positive reference | `AF-WP1-PV-001` through `AF-WP1-PV-005` |
| Shortest/longest chosen-form boundary | `AF-WP1-BV-001` |
| Delimiter, content, and EOF boundaries | `AF-WP1-BV-002` through `AF-WP1-BV-008` |
| Missing, empty, and absence behavior | `AF-WP1-NV-001` and `AF-WP1-NV-002` |
| Grammar, version, token, and byte canonicality | `AF-WP1-NV-003` through `AF-WP1-NV-011` |
| Framing, trailing material, and normalization | `AF-WP1-NV-012` through `AF-WP1-NV-018`, `AF-WP1-NV-021` |
| Forbidden provider/display semantics | `AF-WP1-NV-019`, `AF-WP1-NV-023` |
| Cardinality and ambiguity | `AF-WP1-NV-020`, `AF-WP1-NV-024` |
| Unknown-state fail-closed behavior | `AF-WP1-NV-025` |
| Temporal identity permanence | `AF-WP1-TV-001` through `AF-WP1-TV-009` |

This coverage record does not declare `G-3 CLOSED`, release AF-WP1, or release
any downstream package. It is part of the AF-WP1 implementation candidate
only.

## 9. Annex non-authority boundary

This annex does not:

- become an executable test suite or validator;
- create a parser, registry, database, schema, API, migration, provider
  mapping, or production method;
- author AF-2, AF-3, AF-4, or any other work package;
- supply a whole asset record, identity adjudication, provenance, lifecycle,
  classification, price, portfolio, or Ledger meaning;
- perform independent review, correction, confirmation, content-identity
  validation, freeze, release, or closeout; or
- amend, synchronize, or create a successor to the frozen planning corpus.

The annex's sole authority is to document AF-1/v1 examples and fail-closed
boundaries within AF-WP1.
