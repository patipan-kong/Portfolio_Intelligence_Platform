# Asset Foundation - AF-WP2 - AF-2 Denomination Identifier Dimension Canonical Form

**Artifact class:** AF-WP2 documentary implementation candidate  
**Status:** IMPLEMENTATION CANDIDATE - NOT REVIEWED, CONFIRMED, CONTENT-IDENTIFIED, FROZEN, OR CLOSED  
**Scope:** AF-2 Denomination Identifier Dimension Canonical Form only  
**Implementation authority:** AF-WP2 only  
**Runtime authority:** NONE  
**Source-code, persistence, schema, API, provider, and production-method authority:** NONE

This document is the documentary AF-2 implementation artifact authorized by
AF-WP2. It selects the literal representation that the frozen Asset
Foundation planning corpus left for AF-WP2 to determine. It defines one exact
opaque reference form for one value of the Asset Foundation
currency-of-denomination Classification dimension.

The form does not create a currency enumeration, assign a human-readable
currency name, assume ISO 4217, create a provider code list, or create a
Ledger code. It does not define the Ledger-owned Portfolio Base Currency
coordinate. It does not amend, redesign, or synchronize the planning corpus
or AF-WP1.

This candidate performs no independent review, correction, focused re-review,
independent confirmation, content-identity validation, freeze, release
attestation, closeout, or repository synchronization. Its package-local
vector annex is authored with this form and is governed as part of the same
AF-WP2 implementation candidate.

## 1. Normative source and boundary

The governing planning sources are the frozen paired corpus:

1. [Asset Foundation Canonical Owner-Domain Architecture and Implementation
   Plan](ASSET_FOUNDATION_CANONICAL_OWNER_DOMAIN_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
2. [Asset Foundation Canonical Owner-Domain Work-Package Decomposition and
   Roadmap](ASSET_FOUNDATION_CANONICAL_OWNER_DOMAIN_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md)

The planning lifecycle is consumed as supplied:

| Planning state | Consumed state |
| --- | --- |
| Independent Review | PASS |
| Independent Confirmation | CONFIRMED |
| Ratification | RATIFIED |
| Content Identity Validation | VERIFIED |
| Planning Freeze | FROZEN |
| Planning Closeout | COMPLETE |

The owner domain is Asset Foundation. AF-2 supplies only an opaque reference
to one value of the Asset Foundation currency-of-denomination Classification
dimension. It does not mint the value, resolve an asset claim, provide a
provider mapping, or establish the existence of the value in a consumer's
store.

The AF-WP1 implementation pair is frozen but is not an AF-WP2 predecessor and
is not incorporated into this form. AF-WP2 depends only on the separately
frozen and authorized Asset Foundation planning corpus. The Ledger-owned Base
Currency coordinate is a downstream compatibility edge, not a predecessor.

The implementation candidate is intentionally not content-identity validated.
No Git blob ID or SHA-256 value is asserted. Those are later identity
witnesses, not substitutes for the documentary form or its annex.

## 2. AF-2 purpose and semantic contract

AF-2 makes one Asset Foundation denomination-dimension reference lexically and
byte-wise determinate. The form carries exactly one opaque identifier token.
The token has no embedded ISO, provider, Ledger, label, rate, conversion,
portfolio, reporting, timestamp, or asset-specific assertion meaning.

The form refers to one value already established by the Asset Foundation
owner's authority in the currency-of-denomination Classification dimension.
The form itself:

- does not mint or enumerate denomination values;
- does not assign a human-readable name or display label;
- does not decide whether an asset-specific classification assertion is true;
- does not resolve a token through a Registry, database, provider, or live
  service;
- does not map ISO, provider, Ledger, or other external codes;
- does not infer a value from a missing, malformed, or unknown input; and
- does not establish that a referenced value is currently available to a
  consumer.

An asset-specific classification assertion is separate from the dimension
identifier. Such an assertion may identify an asset, carry an effective
interval, and state the source's claim about the asset's denomination. None of
those facts is encoded in AF-2/v1. A later assertion that changes from one
denomination value to another must cite a different AF-2 reference at its
effective boundary; it does not mutate either dimension identifier.

The form is reusable as an opaque Asset Foundation reference by the
Ledger-owned Portfolio Base Currency coordinate. Reuse does not transfer
ownership and does not permit Ledger to define, normalize, repair, version,
or substitute the denomination form. AF-2 supplies only the Asset Foundation
side of the joint Base Currency G-3 element.

## 3. Selected representation

AF-WP2 selects a fixed-width representation for determinacy:

| Property | AF-2 decision |
| --- | --- |
| Form tag | Literal AF-2 |
| Immutable form version | Literal v1 |
| Dimension identifier token | Exactly 16 opaque bytes, encoded as canonical unpadded Base64url |
| Token alphabet | ASCII A-Z, a-z, 0-9, -, _ |
| Token length | Exactly 22 ASCII characters |
| Payload length | Exactly 30 US-ASCII bytes |
| Outer framing | None; AF-2 is one complete payload |
| End of input | Required immediately after the 22-character token |
| Normalization | None |
| Absence state | No in-band affirmative absence value |

The fixed 16-byte token is an opaque capacity choice. It is not a currency
code, ISO 4217 code, provider key, Ledger key, UUID, integer, timestamp,
counter, database key, or namespace. No bit, byte, character position, prefix,
suffix, or value range carries business meaning.

The dimension meaning is fixed by the AF-2 form tag and version. There is no
additional dimension-name field in the payload. Adding such a field would
create a second syntax and would allow multiple spellings for the same
dimension-specific reference.

## 4. Field set, ordering, and cardinality

One AF-2/v1 payload contains exactly one ordered occurrence of each component:

| Position | Component | Required content | Encoding |
| ---: | --- | --- | --- |
| 1 | form_tag | Literal AF-2 | US-ASCII |
| 2 | form_version | Literal v1 | US-ASCII |
| 3 | denomination_identifier_token | One exact 16-byte opaque dimension-value reference | Canonical unpadded Base64url |

The two colons are required literal delimiters. The form is not a list, map,
tuple with repeated fields, concatenated record, query string, JSON object,
URI, or extensible envelope. There are no optional fields, defaulted fields,
unknown fields, or extension points in AF-2:v1.

The cardinality is exactly one denomination-dimension reference per payload.
Multiple values, multiple tokens, or a value plus a default cannot be
represented by one AF-2/v1 payload. An asset-specific assertion that supplies
multiple denomination values is an external ambiguity and cannot be reduced
to one AF-2 reference by ordering or selection.

## 5. Exact lexical grammar

The grammar below is the complete AF-2/v1 lexical grammar. ALPHA and DIGIT
mean their US-ASCII ranges only.

~~~abnf
af2-reference = "AF-2" ":" "v1" ":" denomination-id-token
denomination-id-token = 22b64u-char
b64u-char = ALPHA / DIGIT / "-" / "_"
ALPHA = %x41-5A / %x61-7A
DIGIT = %x30-39
~~~

The semantic canonicality constraint on denomination-id-token is mandatory
in addition to the character grammar:

1. Decode the token with unpadded Base64url using exactly the alphabet shown
   above.
2. The decoded result MUST contain exactly 16 bytes.
3. The four unused low-order bits in the final Base64 sextet MUST be zero.
4. The decoded bytes MUST be retained exactly, including leading and zero
   bytes.

No other Base64 alphabet, padding, alternate alphabet, or non-zero unused-bit
encoding is admitted.

### 5.1 Canonical byte representation

The canonical AF-2 byte sequence is the US-ASCII encoding of the complete
lexical payload. There is no character-decoding choice and no alternate byte
encoding.

For the documentary opaque bytes
00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F, the exact payload is:

~~~text
AF-2:v1:AAECAwQFBgcICQoLDA0ODw
~~~

The exact payload is 30 bytes:

~~~text
41 46 2D 32 3A 76 31 3A 41 41 45 43 41 77 51 46 42 67 63 49 43 51 6F 4C 44 41 30 4F 44 77
~~~

The following are not part of the canonical byte sequence and MUST NOT be
present:

- UTF-8 or any other non-ASCII character;
- UTF-8 BOM or any other signature;
- carriage return, line feed, tab, space, or other whitespace;
- NUL or any other trailing byte;
- Base64 padding =;
- an outer length, checksum, quote, escape, or framing byte; or
- an additional delimiter or field.

Line endings used to display this Markdown document are not part of an AF-2
payload. A payload is the exact 30-byte sequence defined above.

## 6. Deterministic interpretation

The documentary interpretation order is fixed:

1. Require exact input consumption from byte zero through byte 29.
2. Match the literal AF-2:v1: at the first eight bytes.
3. Validate the remaining 22 bytes against the ASCII Base64url alphabet.
4. Validate canonical unused-bit treatment.
5. Decode exactly 16 opaque bytes.
6. Treat those bytes as the one Asset Foundation denomination-dimension
   reference carried by the payload.

Two valid AF-2/v1 payloads refer to the same dimension value if and only if
their decoded 16-byte sequences are identical under the same owner-domain
identity. Because canonical Base64url is bijective under the fixed length and
zero-unused-bit rule, identical decoded bytes have exactly one valid AF-2/v1
lexical spelling.

The form does not inspect a Registry, database, provider, clock, locale,
transport, model output, or ambient context. Lexical validity does not prove
that an owner has issued the token, that the token identifies a known
dimension value, or that an asset-specific classification assertion is true.
Those are owner and consumer determinations outside this form.

## 7. Required, forbidden, and absent content

### 7.1 Required content

Every valid AF-2/v1 payload MUST contain:

- the exact AF-2 form tag;
- the exact v1 form version;
- exactly one 22-character canonical Base64url token; and
- exactly 16 decoded opaque identifier bytes.

The token MUST be an owner-minted reference to one value in the Asset
Foundation currency-of-denomination Classification dimension before it can
serve as semantic owner-domain supply. A syntactically valid token with no
such owner authority is not sufficient.

### 7.2 Forbidden content

The payload MUST NOT contain any field or meaning for:

- ISO 4217 or another external currency enumeration;
- provider code, vendor namespace, display code, ticker, alias, or label;
- Ledger code, Portfolio Base Currency coordinate, or accounting field;
- asset identity, asset-specific classification assertion, effective date,
  interval, source, confidence, provenance, or adjudication decision;
- FX rate, conversion amount, price, NAV, benchmark, quantity, or observation;
- Portfolio Identity, Accounting Scope, Membership, reporting, or portfolio
  policy;
- timestamp, currentness marker, sequence, revision counter, or lifecycle
  state;
- lookup key, database key, tenant, API, schema, signature, checksum, or
  runtime field; or
- extension, comment, wrapper, second token, or second record.

### 7.3 Absence behavior

AF-2/v1 has no NONE, ABSENT, NULL, UNKNOWN, empty, or default payload.
Missing denomination identity, absent denomination assertion, or unknown
denomination value is represented by failure to provide a conforming
owner-authorized reference, not by a sentinel token.

The all-zero 16-byte sequence is not an absence sentinel. If it is supplied
as an owner-minted opaque dimension-value reference, it is ordinary opaque
content. The form does not reserve or interpret it.

An affirmative absence state is not a denomination value and cannot satisfy
the Asset Foundation side of the joint Base Currency G-3 element.

### 7.4 Unknown-state behavior

Unknown state is not encoded in AF-2/v1:

- A token that is lexically valid but not known to the already-bound Asset
  Foundation authority is LEXICALLY VALID / SEMANTICALLY UNKNOWN. It is not
  owner-domain supply and cannot satisfy a required G-3 denomination reference.
- A token whose owner, dimension membership, or value assignment cannot be
  established without a live lookup is UNKNOWN for the applicable
  determination. The result is fail closed; no lookup, default, or inference
  is permitted.
- An unknown field or extension is invalid because the grammar has no
  extension point.
- An asset-specific assertion that gives multiple possible values or cannot
  determine one value is ambiguous/unknown outside this form. No token is
  selected by order, label, provider preference, or currentness.

## 8. Invalid-state and fail-closed behavior

Conformance requires every lexical, byte, field, cardinality, owner-domain,
and boundary rule to succeed. Failure of any one rule rejects the claimed
AF-2 reference. No default, lookup, inference, repair, or normalization cures
a failure.

| State or condition | AF-2 result |
| --- | --- |
| Missing payload, empty token, or omitted denomination reference | Reject; no denomination is represented |
| Missing tag, version, or delimiter | Reject |
| Wrong, lower-case, alternate, or versionless tag | Reject |
| Wrong version, including v2 under this form | Reject under AF-2/v1 |
| Token shorter or longer than 22 characters | Reject |
| Token containing +, /, =, :, whitespace, or non-ASCII bytes | Reject |
| Non-zero unused Base64 bits | Reject as non-canonical |
| Extra delimiter, field, record, wrapper, or trailing byte | Reject |
| NONE, ABSENT, NULL, UNKNOWN, or other sentinel | Reject |
| ISO, provider, display, or Ledger code supplied in place of the opaque token | Reject; no external code is translated or adopted |
| Lexically valid token with no established Asset Foundation owner assignment | Lexically valid but semantically unknown; fail closed for owner-domain use |
| Lexically valid token claimed for two distinct dimension values | Reject the claim as ambiguous; do not choose |
| One asset-specific assertion supplies multiple denomination references | Reject the assertion for this one-value boundary; do not select or order |
| Same dimension value is given two token spellings | Reject the non-canonical or conflicting claim; no aliasing is inferred |
| Token not known by a consumer's already-bound authority | Do not resolve live; remain unresolved for that consumer |
| A later source change would retarget an existing token to another value | Reject the retargeting; require an additive governed successor or block |

Lexical validity and semantic admission are distinct. The form can establish
that bytes have the AF-2/v1 shape; it cannot establish that an external claim
is decisive, that a token was lawfully minted, or that a consumer may use the
reference for its own contract.

## 9. Normalization rules

AF-2/v1 performs no normalization. A supplied payload is either already the
exact canonical byte sequence or it is rejected.

The following operations are expressly prohibited:

- trimming or collapsing whitespace;
- Unicode normalization, transliteration, or character substitution;
- case folding of the tag, version, or Base64url token;
- adding or removing Base64 padding;
- converting standard Base64 symbols to URL-safe symbols;
- decoding and re-encoding a non-canonical token to make it pass;
- percent-decoding, URI-decoding, JSON-unescaping, or quote removal;
- converting an ISO, provider, Ledger, display, or label value into the token;
- sorting or selecting among multiple denomination values;
- selecting a default or using a live lookup when the supplied bytes fail; and
- replacing an unknown token with a current, preferred, or locally available
  value.

Changing a Base64url character changes the opaque bytes or makes the encoding
non-canonical. It is not an alternate spelling of the same dimension value.

## 10. Temporal invariants

The AF-2 payload has no time-varying field. Once a dimension-value reference
is issued by its owner, its exact AF-2/v1 bytes remain the same across the
events below:

| Temporal event | AF-2 invariant |
| --- | --- |
| Human-readable label or display translation changes | The same dimension value keeps the same payload bytes |
| Provider code changes or a provider mapping disappears | External mappings may change or vanish; the payload does not |
| A provider recycles a code for another denomination value | The old and new values use distinct owner-domain references; codes do not alias tokens |
| An asset-specific denomination assertion is restated at a later effective time with the same value | The assertion may receive a new dated record; the referenced AF-2 bytes remain unchanged |
| An asset-specific denomination changes from value D1 to value D2 | The effective assertion cites D2's distinct AF-2 reference; historical D1 assertions retain their original reference |
| A classification assertion is missing or unknown for an interval | No default or current value is substituted; the applicable assertion fails closed |
| A source renames, retires, splits, merges, or otherwise changes an external value relationship | Existing AF-2 identity bytes are not retargeted; any distinct new value requires a distinct reference or a governed successor decision |
| A source discovers that an existing token was assigned the wrong meaning | The token is not silently repaired; the owner records a blocked or additive successor outcome under later authority |
| The same payload is replayed on different dates, locales, transports, or provider states | Exact bytes and lexical interpretation are wall-clock and provider independent |
| A future AF-2 successor version is introduced | Existing AF-2/v1 references retain v1 meaning and are not rewritten or interpreted as the successor |

The form contains no timestamp, currentness flag, provider state, effective
date, or lifecycle state. A time-varying classification assertion is not an
identity version and must not be embedded in the dimension identifier.

## 11. Versioning, predecessor, and supersession

### 11.1 Form version

v1 is an immutable form version. No version negotiation, fallback, or
consumer-selected interpretation is permitted. A payload beginning with
AF-2:v2: is not an AF-2/v1 payload and has no meaning under this candidate.

### 11.2 Predecessor

This is the initial AF-2 implementation candidate. It has no prior AF-2 form
predecessor. The frozen Asset Foundation planning corpus is the governance
and scope predecessor; it is not a lexical form and is not encoded in an
AF-2 payload.

AF-WP1 is a completed independent work package, not a semantic or lexical
predecessor of AF-WP2. No AF-WP1 field, token, annex, or identity is imported
into AF-2/v1.

### 11.3 Supersession

No AF-2 artifact is superseded by this candidate. Before the package is
frozen, any correction MUST be additive: it must produce a successor
implementation candidate or revision with an explicit predecessor identity;
no in-place replacement occurs. Focused re-review, if required, is a later
lifecycle act and is not performed here.

After a form-and-annex pair is frozen, any material change to grammar, bytes,
field rules, invalid-state rules, owner-domain assignment, or temporal rules
MUST be an additive successor with:

- a new exact form version or other expressly governed successor identity;
- a new documentary form artifact;
- a new package-local annex bound to that successor;
- an explicit supersedes relation to the exact predecessor identity; and
- a new independent lifecycle.

Supersession never rewrites, aliases, migrates, or retargets an existing v1
payload. Existing references remain interpretable under the version that
defined them.

## 12. Ownership and content-identity metadata

| Metadata item | AF-WP2 value |
| --- | --- |
| Owner domain | Asset Foundation |
| Representation owner | AF-WP2 |
| Authority source | AF-WP2 Authorization Determination supplied at implementation start |
| Artifact class | Documentary implementation candidate |
| Exact artifact path | docs/implementation/ASSET_FOUNDATION_AF_WP2_AF_2_DENOMINATION_IDENTIFIER_DIMENSION_CANONICAL_FORM.md |
| Form identifier | AF-2 |
| Form version | v1 |
| Candidate revision | AF-WP2-IMPLEMENTATION-CANDIDATE-1 |
| Package-local annex | docs/implementation/ASSET_FOUNDATION_AF_WP2_VECTOR_ANNEX.md |
| Predecessor | Frozen Asset Foundation planning corpus as scope authority; no prior AF-2 form; AF-WP1 is not a predecessor |
| Supersedes | None |
| Content identity | Not performed by this implementation; no hash asserted |
| Semantic identity | One opaque Asset Foundation reference to one value in the currency-of-denomination Classification dimension |
| Provenance authority | None; provenance is outside AF-2 |
| Runtime/implementation authority | Documentary AF-WP2 only; no runtime authority |
| Downstream relationship | Opaque upstream reference only; no Ledger coordinate or downstream contract is supplied |

The artifact path, form version, deterministic byte definition, annex path,
owner, authority source, predecessor relation, and lifecycle status together
identify the candidate's intended evidence boundary. Content Identity
Validation remains a distinct later act.

## 13. G-3 field and facet coverage

The covered M44 G-3 facet is the Asset Foundation-owned denomination
identifier dimension reference needed by the single joint Portfolio Base
Currency element. This candidate does not close G-3 and does not cover the
Ledger-owned Base Currency coordinate, its event/history semantics, Ledger
compatibility, or any downstream adequacy determination.

| G-3 field/facet | AF-WP2 coverage in this candidate |
| --- | --- |
| Owner and authority | Asset Foundation ownership and AF-WP2 authority boundary are stated |
| Dimension identity | The form is limited to one value of the currency-of-denomination Classification dimension |
| Form identity | AF-2 and immutable v1 are fixed |
| Lexical grammar | Complete ASCII grammar, delimiters, token alphabet, and EOF rule are fixed |
| Canonical bytes | Exact US-ASCII representation, length, BOM, newline, whitespace, and trailing-byte rules are fixed |
| Framing and field order | Three required ordered components and two literal delimiters are fixed; no outer framing exists |
| Cardinality | Exactly one dimension-value reference and one token are admitted |
| Denomination semantics | One opaque owner-domain reference; no currency name, code list, provider meaning, or Ledger meaning is carried |
| Required/forbidden content | Required literals/token and prohibited fields are enumerated |
| Absence and invalid states | Missing, empty, malformed, ambiguous, duplicate, sentinel, and multi-valued treatment is defined |
| Unknown state | Lexically valid but owner-unknown references fail closed for semantic supply |
| Normalization | No normalization, lookup, inference, repair, default, or external-code conversion is permitted |
| Determinism | Exact byte equality and canonical Base64url bijection are defined |
| Temporal invariants | Stable dimension identity is separated from time-varying asset assertions and external mappings |
| Predecessor/supersession | Initial predecessor and additive successor rules are defined |
| Vector completeness | Positive, boundary, negative, and temporal coverage is bound to the annex |
| Joint-boundary limitation | Only the Asset Foundation-side denomination reference is covered; the Ledger coordinate and G-3 closure remain outside scope |

The G-3 coverage row for the Asset Foundation denomination identifier is
complete within this implementation candidate, subject to the later
independent lifecycle. No coverage or closure claim is made for any other
owner-domain element.

## 14. Package-local annex and later lifecycle

The exclusive package-local vector annex is:

[AF-WP2 Package-Local Vector Annex](ASSET_FOUNDATION_AF_WP2_VECTOR_ANNEX.md)

The annex is authored with this form, not deferred to AF-WP3 or AF-WP4. It is
documentation-only and is not an executable test fixture, parser
specification, runtime validator, or production method.

The form and annex remain one AF-WP2 implementation candidate. Independent
review, correction/focused re-review, independent confirmation,
content-identity validation, and freeze must later act on the exact pair.
None of those acts is performed by this document. A missing, defective,
incomplete, or detached annex produces a fail-closed AF-WP2 result and cannot
be repaired by AF-WP3 aggregation.

## 15. Explicit non-authority boundary

This implementation candidate does not:

- create or assume ISO 4217, a provider code list, a Ledger code list, or any
  alternate currency taxonomy;
- create a currency universe, human-readable value vocabulary, provider
  mapping, label mapping, or external-code conversion;
- create a Portfolio Base Currency coordinate, Portfolio Identity,
  Accounting Scope, Membership, reporting rule, FX observation, conversion
  amount, NAV, benchmark, or portfolio semantics;
- define an asset record, asset-specific classification assertion, effective
  date, provenance, source ranking, confidence, lifecycle, or adjudication;
- create source code, parsers, executable validators, runtime behavior,
  persistence, database schemas, APIs, migrations, provider integrations, or
  production methods;
- author, amend, repair, normalize, version, or freeze Ledger content;
- allocate, authorize, execute, review, confirm, or close any other work
  package or domain;
- close G-3, release M45-WP2, determine downstream adequacy, or grant
  downstream authority;
- modify planning, AF-WP1, M42, M44, M45, Ledger & Accounting, the Decision
  Log, the Implementation INDEX, or repository synchronization; or
- perform independent review, correction, focused re-review, confirmation,
  content-identity validation, freeze, release, or closeout.

The only implementation authority exercised by this artifact is documentary
AF-WP2 authoring within the AF-2 boundary stated above.
