# Asset Foundation — AF-WP1 — AF-1 Asset Identity Canonical Lexical Form

**Artifact class:** AF-WP1 documentary implementation candidate  
**Status:** `IMPLEMENTATION CANDIDATE — NOT REVIEWED, CONFIRMED, CONTENT-IDENTIFIED, FROZEN, OR CLOSED`  
**Scope:** `AF-1` Asset Identity Canonical Lexical Form only  
**Implementation authority:** AF-WP1 only  
**Runtime authority:** `NONE`  
**Source-code, persistence, schema, API, provider, and production-method authority:** `NONE`

This document is the documentary AF-1 implementation artifact authorized by
AF-WP1. It selects the literal representation that the frozen planning corpus
left for AF-WP1 to determine. It does not amend, redesign, or synchronize the
planning corpus.

This candidate performs no independent review, correction, focused re-review,
independent confirmation, content-identity validation, freeze, release
attestation, closeout, or repository synchronization. Its package-local vector
annex is authored with this form and is governed as part of the same AF-WP1
implementation candidate.

## 1. Normative source and boundary

The governing planning sources are the frozen paired corpus:

1. [Asset Foundation Canonical Owner-Domain Architecture and Implementation
   Plan](ASSET_FOUNDATION_CANONICAL_OWNER_DOMAIN_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
2. [Asset Foundation Canonical Owner-Domain Work-Package Decomposition and
   Roadmap](ASSET_FOUNDATION_CANONICAL_OWNER_DOMAIN_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md)

The planning lifecycle is consumed as supplied:

| Planning state | Consumed state |
| --- | --- |
| Independent Review | `PASS` |
| Independent Confirmation | `CONFIRMED` |
| Ratification | `RATIFIED` |
| Content Identity Validation | `VERIFIED` |
| Planning Freeze | `FROZEN` |
| Planning Closeout | `COMPLETE` |

The owner domain is Asset Foundation. AF-1 supplies only an opaque reference
to one permanent platform identity. It does not create a whole asset record,
resolve an external claim, or provide a provider mapping.

The implementation candidate is intentionally not content-identity validated.
No Git blob ID or SHA-256 value is asserted here. Those are later identity
witnesses, not substitutes for the documentary form or its annex.

## 2. AF-1 purpose and semantic contract

AF-1 makes one permanent `asset_id` reference lexically and byte-wise
determinate. The form carries exactly one opaque identity token. The token has
no embedded issuer, venue, market, currency, lifecycle, classification,
price, accounting, portfolio, provider, display, or timestamp meaning.

The form is a representation of an identity reference already established by
the owning authority. The form itself:

- does not mint an identity;
- does not decide whether an external claim is decisive;
- does not resolve a token through a Registry or any live service;
- does not map a symbol, ISIN, CUSIP, FIGI, broker code, or provider value;
- does not infer identity from a missing or malformed value; and
- does not establish that a referenced identity exists in a consumer's store.

A downstream consumer may use the exact reference under its own already-bound
authority. Opaque carriage or citation does not transfer ownership.

## 3. Selected representation

AF-WP1 selects a fixed-width representation for determinacy:

| Property | AF-1 decision |
| --- | --- |
| Form tag | Literal `AF-1` |
| Immutable form version | Literal `v1` |
| Identity token | Exactly 16 opaque bytes, encoded as canonical unpadded Base64url |
| Token alphabet | ASCII `A–Z`, `a–z`, `0–9`, `-`, `_` |
| Token length | Exactly 22 ASCII characters |
| Payload length | Exactly 30 US-ASCII bytes |
| Outer framing | None; AF-1 is one complete payload |
| End of input | Required immediately after the 22-character token |
| Normalization | None |
| Absence state | No in-band affirmative absence value |

The fixed 16-byte token is an opaque capacity choice. It is not a UUID, an
integer, a timestamp, a counter, a database key, or a provider namespace. No
bit, byte, character position, prefix, suffix, or value range carries business
meaning.

The fixed width makes the form's complete length, field cardinality, framing,
and byte identity mechanically determinate without a parser choosing a finite
implementation limit.

## 4. Field set, ordering, and cardinality

One AF-1 payload contains exactly one ordered occurrence of each component:

| Position | Component | Required content | Encoding |
| ---: | --- | --- | --- |
| 1 | `form_tag` | Literal `AF-1` | US-ASCII |
| 2 | `form_version` | Literal `v1` | US-ASCII |
| 3 | `asset_id_token` | One exact 16-byte opaque identity token | Canonical unpadded Base64url |

The two colons are required literal delimiters. The form is not a list, map,
tuple with repeated fields, concatenated record, query string, JSON object,
URI, or extensible envelope. There are no optional fields, defaulted fields,
unknown fields, or extension points in `AF-1:v1`.

## 5. Exact lexical grammar

The grammar below is the complete AF-1/v1 lexical grammar. `ALPHA` and `DIGIT`
mean their US-ASCII ranges only.

```abnf
af1-reference = "AF-1" ":" "v1" ":" asset-id-token
asset-id-token = 22b64u-char
b64u-char = ALPHA / DIGIT / "-" / "_"
```

The semantic canonicality constraint on `asset-id-token` is mandatory in
addition to the character grammar:

1. Decode the token with unpadded Base64url using exactly the alphabet shown
   above.
2. The decoded result MUST contain exactly 16 bytes.
3. The four unused low-order bits in the final Base64 sextet MUST be zero.
4. The decoded bytes MUST be retained exactly, including leading and zero
   bytes.

No other Base64 alphabet, padding, alternate alphabet, or non-zero unused-bit
encoding is admitted.

### 5.1 Canonical byte representation

The canonical AF-1 byte sequence is the US-ASCII encoding of the complete
lexical payload. There is no character decoding choice and no alternate byte
encoding.

For example, the opaque identity bytes
`00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F` are represented as:

```text
AF-1:v1:AAECAwQFBgcICQoLDA0ODw
```

The exact payload is 30 bytes:

```text
41 46 2D 31 3A 76 31 3A 41 41 45 43 41 77 51 46 42 67 63 49 43 51 6F 4C 44 41 30 4F 44 77
```

The following are not part of the canonical byte sequence and MUST NOT be
present:

- UTF-8 or any other non-ASCII character;
- UTF-8 BOM or any other signature;
- carriage return, line feed, tab, space, or other whitespace;
- NUL or any other trailing byte;
- Base64 padding `=`;
- an outer length, checksum, quote, escape, or framing byte; or
- an additional delimiter or field.

## 6. Deterministic interpretation

The documentary interpretation order is fixed:

1. Require exact input consumption from byte zero through byte 29.
2. Match the literal `AF-1:v1:` at the first eight bytes.
3. Validate the remaining 22 bytes against the ASCII Base64url alphabet.
4. Validate canonical unused-bit treatment.
5. Decode exactly 16 opaque bytes.
6. Treat those bytes as the one `asset_id` reference carried by the payload.

Two valid AF-1/v1 payloads refer to the same identity reference if and only if
their decoded 16-byte sequences are identical. Because canonical Base64url is
bijective under the fixed length and zero-unused-bit rule, identical decoded
bytes have exactly one valid AF-1/v1 lexical spelling.

The form does not inspect a Registry, database, provider, clock, locale,
transport, model output, or ambient context. A syntactically valid token is
not proof of current registry existence or ownership authorization.

## 7. Required, forbidden, and absent content

### 7.1 Required content

Every valid AF-1/v1 payload MUST contain:

- the exact `AF-1` form tag;
- the exact `v1` form version;
- exactly one 22-character canonical Base64url token; and
- exactly 16 decoded opaque identity bytes.

### 7.2 Forbidden content

The payload MUST NOT contain any field or meaning for:

- canonical symbol, display symbol, ticker, name, label, or alias;
- provider identifier, exchange identifier, ISIN, CUSIP, FIGI, broker code,
  or vendor namespace;
- issuer, venue, market, currency, asset type, classification, or lifecycle
  state;
- evidence source, confidence, provenance, resolution result, or adjudication
  decision;
- price, quantity, amount, rate, NAV, FX, benchmark, or observation;
- Portfolio Identity, Accounting Scope, Membership, Base Currency, or any
  Ledger coordinate;
- timestamp, effective date, wall-clock value, sequence, revision counter, or
  currentness marker; and
- extension, comment, signature, checksum, database, tenant, API, or runtime
  field.

### 7.3 No affirmative absence

AF-1/v1 has no `NONE`, `ABSENT`, `UNKNOWN`, `NULL`, empty, or default payload.
Missing identity, absent identity, or unknown identity is represented by the
failure to provide a conforming identified reference, not by a sentinel token.

The all-zero 16-byte sequence is not an absence sentinel. If it is supplied
as an owner-minted opaque identity, it is ordinary opaque content. The form
does not reserve or interpret it.

## 8. Invalid-state and fail-closed behavior

Conformance requires every lexical, byte, field, cardinality, ownership, and
boundary rule to succeed. Failure of any one rule rejects the claimed AF-1
reference. No default, lookup, inference, repair, or normalization cures a
failure.

| State or condition | AF-1 result |
| --- | --- |
| Missing payload or empty token | Reject; no identity is represented |
| Missing tag, version, or delimiter | Reject |
| Wrong, lower-case, alternate, or versionless tag | Reject |
| Wrong version, including `v2` under this form | Reject under AF-1/v1 |
| Token shorter or longer than 22 characters | Reject |
| Token containing `+`, `/`, `=`, `:`, whitespace, or non-ASCII bytes | Reject |
| Non-zero unused Base64 bits | Reject as non-canonical |
| Extra delimiter, field, record, wrapper, or trailing byte | Reject |
| `NONE`, `ABSENT`, `NULL`, `UNKNOWN`, or other sentinel | Reject |
| Provider-derived, display-derived, or label-derived token | Reject the identity claim as non-conforming, even if the token is lexically valid |
| Token not known by a consumer's already-bound authority | Do not resolve live; fail closed as unresolved for that consumer |
| Same token claimed for multiple identities | Surface ambiguity and reject the claim; do not choose |
| Same identity supplied more than once in one AF-1 payload | Reject the payload as a duplicate/extra record |
| Different token used for a supposed lexical alias | Treat as a different opaque reference; do not normalize or alias |

Lexical validity and identity admission are distinct. The form can establish
that bytes have the AF-1/v1 shape; it cannot establish that an external claim
is decisive or that a token has been lawfully minted. The owning authority and
consumer contract retain those determinations.

## 9. Normalization rules

AF-1/v1 performs no normalization. A supplied payload is either already the
exact canonical byte sequence or it is rejected.

The following operations are expressly prohibited:

- trimming or collapsing whitespace;
- Unicode normalization, transliteration, or character substitution;
- case folding of the tag, version, or Base64url token;
- adding or removing Base64 padding;
- converting standard Base64 symbols to URL-safe symbols;
- decoding and re-encoding a non-canonical token to make it pass;
- percent-decoding, URI-decoding, JSON-unescaping, or quote removal;
- interpreting a display/provider value as the opaque token; and
- selecting a default or using a live lookup when the supplied bytes fail.

Changing a Base64url character changes the opaque bytes or makes the encoding
non-canonical. It is not an alternate spelling of the same identity.

## 10. Temporal invariants

The AF-1 payload has no time-varying field. Once an identity reference is
issued by its owner, its exact AF-1/v1 bytes remain the same across the events
below:

| Temporal event | AF-1 invariant |
| --- | --- |
| Canonical or display symbol rename | The same identity keeps the same payload bytes |
| Provider symbol change or provider disappearance | Evidence mappings may change or vanish; the payload does not |
| Provider symbol recycled to another instrument | The original and new instruments use different opaque references |
| Listing delisted, suspended, merged, or archived | Lifecycle status is external; historical AF-1 references remain unchanged |
| Related-but-distinct listing, ADR, wrapper, or venue | Each distinct identity has its own token; relationships do not alias payloads |
| Merger, conversion, or successor relationship | A successor receives a distinct identity reference; the predecessor is not retargeted |
| Classification or denomination assertion changes | Dated classification/evidence facts remain outside the payload |
| Replay on a later date or under a different locale/provider | The same input bytes have the same AF-1 meaning |
| Form successor is introduced | Existing `AF-1:v1` references retain v1 meaning; no successor rewrites them |

The form contains no timestamp, currentness flag, provider state, or lifecycle
state. Historical identity references do not expire because a descriptive fact
or evidence mapping changes.

## 11. Versioning, predecessor, and supersession

### 11.1 Form version

`v1` is an immutable form version. No version negotiation, fallback, or
consumer-selected interpretation is permitted. A payload beginning with
`AF-1:v2:` is not an AF-1/v1 payload and has no meaning under this candidate.

### 11.2 Predecessor

This is the initial AF-1 implementation candidate. It has no prior AF-1 form
predecessor. The frozen planning pair is a governance and scope predecessor;
it is not a lexical form and is not encoded in an AF-1 payload.

### 11.3 Supersession

No AF-1 artifact is superseded by this candidate. Before the package is frozen,
corrections are additive. Before the package is frozen, any implementation
correction MUST produce an additive successor implementation candidate or
revision; no in-place replacement occurs. The successor MUST retain an
explicit predecessor identity, and focused re-review MUST be performed where
applicable. A freeze MUST always apply to the exact confirmed successor bytes.
After a form-and-annex pair is frozen, any material change to grammar, bytes,
field rules, invalid-state rules, or temporal rules MUST be an additive
successor with:

- a new exact form version or other expressly governed successor identity;
- a new documentary form artifact;
- a new package-local annex bound to that successor;
- an explicit `supersedes` relation to the exact predecessor identity; and
- a new independent lifecycle.

Supersession never rewrites, aliases, migrates, or retargets an existing v1
payload. Existing references remain interpretable under the version that
defined them.

## 12. Ownership and content-identity metadata

| Metadata item | AF-WP1 value |
| --- | --- |
| Owner domain | Asset Foundation |
| Representation owner | AF-WP1 |
| Authority source | AF-WP1 Authorization Authority determination supplied at implementation start |
| Artifact class | Documentary implementation candidate |
| Exact artifact path | `docs/implementation/ASSET_FOUNDATION_AF_WP1_AF_1_CANONICAL_LEXICAL_FORM.md` |
| Form identifier | `AF-1` |
| Form version | `v1` |
| Candidate revision | `AF-WP1-IMPLEMENTATION-CANDIDATE-1` |
| Package-local annex | `docs/implementation/ASSET_FOUNDATION_AF_WP1_VECTOR_ANNEX.md` |
| Predecessor | Frozen Asset Foundation planning corpus as scope authority; no prior AF-1 form |
| Supersedes | None |
| Content identity | Not performed by this implementation; no hash asserted |
| Semantic identity | One permanent opaque `asset_id` reference only |
| Provenance authority | None; provenance is outside AF-1 |
| Runtime/implementation authority | Documentary AF-WP1 only; no runtime authority |

The artifact path, form version, deterministic byte definition, annex path,
owner, authority source, predecessor relation, and lifecycle status together
identify the candidate's intended evidence boundary. Content Identity
Validation remains a distinct later act.

## 13. G-3 field and facet coverage

The covered M44 G-3 element is the Asset Foundation-owned `asset_id` lexical
form. This candidate does not close G-3 and does not cover AF-2's denomination
identifier dimension or the jointly evidenced Portfolio Base Currency element.

| G-3 field/facet | AF-WP1 coverage in this candidate |
| --- | --- |
| Owner and authority | Asset Foundation ownership and AF-WP1 authority boundary are stated |
| Form identity | `AF-1` and immutable `v1` are fixed |
| Lexical grammar | Complete ASCII grammar, delimiters, token alphabet, and EOF rule are fixed |
| Canonical bytes | Exact US-ASCII representation, length, BOM, newline, whitespace, and trailing-byte rules are fixed |
| Framing and field order | Three required ordered components and two literal delimiters are fixed |
| Cardinality | Exactly one reference and one token are admitted |
| Identity semantics | One opaque permanent identity reference; no business or provider meaning |
| Required/forbidden content | Required literals/token and prohibited fields are enumerated |
| Absence and invalid states | Missing, malformed, ambiguous, duplicate, unknown, and sentinel handling is defined |
| Normalization | No normalization, lookup, inference, repair, or default is permitted |
| Determinism | Exact byte equality and canonical Base64url bijection are defined |
| Temporal invariants | Rename, recycling, delisting, relationship, successor, classification, and provider-change behavior is defined |
| Predecessor/supersession | Initial predecessor and additive successor rules are defined |
| Vector completeness | Positive, boundary, negative, and temporal coverage is bound to the annex |

The G-3 coverage row for `asset_id` is complete within this AF-WP1
implementation candidate, subject to the later independent lifecycle. No
coverage claim is made for any other G-3 owner-domain element.

## 14. Package-local annex and later lifecycle

The exclusive package-local vector annex is:

[AF-WP1 Package-Local Vector Annex](ASSET_FOUNDATION_AF_WP1_VECTOR_ANNEX.md)

The annex is authored with this form, not deferred to AF-WP3 or AF-WP4. It is
documentation-only and is not an executable test fixture, parser specification,
runtime validator, or production method.

The form and annex remain one AF-WP1 implementation candidate. Review,
correction/focused re-review, confirmation, content-identity validation, and
freeze must later act on the exact pair. A missing, defective, incomplete, or
detached annex produces a fail-closed AF-WP1 result and cannot be repaired by
AF-WP3 aggregation.

## 15. Explicit non-authority boundary

This implementation candidate does not:

- create source code, parsers, validators, runtime behavior, or executable
  tests;
- create registry tables, persistence, database schemas, APIs, migrations, or
  provider integrations;
- define a whole Asset record, identity adjudication, claim resolution, or
  provider mapping;
- define canonical symbols, display symbols, evidence records, provenance,
  classification, lifecycle, relationships, prices, FX, NAV, or benchmarks;
- define AF-2, AF-3, AF-4, Portfolio Base Currency, Ledger coordinates, or
  downstream G-3 adequacy;
- authorize or allocate AF-WP2, AF-WP3, or AF-WP4;
- perform review, confirmation, content-identity validation, freeze, release,
  closeout, or downstream intake; or
- amend or synchronize any planning or governance artifact.

The only implementation authority exercised by this artifact is documentary
AF-WP1 authoring within the AF-1 boundary stated above.
