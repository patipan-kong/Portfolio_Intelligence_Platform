# Ledger & Accounting — LA-WP2 Documentary Implementation Candidate

**Artifact class:** LA-WP2 documentary implementation candidate

**Scope:** LA-1 Portfolio Identity and LA-2 Accounting Scope, with two package-local vector annexes

**Implementation authority:** LA-WP2 only

**Status:** `IMPLEMENTATION CANDIDATE — NOT REVIEWED, CONFIRMED, CONTENT-IDENTIFIED, FROZEN, OR CLOSED`

## 1. Boundary

This candidate implements only the two canonical reference forms assigned to
LA-WP2 by the frozen [Ledger & Accounting Architecture and Implementation
Plan](LEDGER_ACCOUNTING_CANONICAL_OWNER_DOMAIN_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
§3 and the frozen [Work-Package Decomposition and
Roadmap](LEDGER_ACCOUNTING_CANONICAL_OWNER_DOMAIN_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md)
§§1–2:

- **LA-1:** Portfolio Identity Canonical Reference Form;
- **LA-2:** Accounting Scope Canonical Reference Form; and
- one package-local vector annex for LA-1;
- one package-local vector annex for LA-2.

It defines representation only. It does not redefine Portfolio Identity or
Accounting Scope, create another accounting boundary, define Membership, Base
Currency, Asset Foundation content, Connectivity & Ingestion content,
Portfolio Intelligence content, runtime behavior, APIs, persistence, schemas,
implementation code, or any M45 artifact.

This candidate performs no review, confirmation, content-identity validation,
freeze, or closeout.

## 2. Authority and inherited semantic references

The normative implementation authority is the frozen planning pair:

| Frozen planning artifact | Git blob ID | SHA-256 |
| --- | --- | --- |
| [Architecture and Implementation Plan](LEDGER_ACCOUNTING_CANONICAL_OWNER_DOMAIN_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) | `6e68ab3e3f152d105e72bef4f84cd7c4afae9e1a` | `c6ac324a786953dec79d89363a712df07fcb190f7bdd93a635a97bcdb2fd595f` |
| [Work-Package Decomposition and Roadmap](LEDGER_ACCOUNTING_CANONICAL_OWNER_DOMAIN_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md) | `b812e31cb0473c16c324419e1efb6103af1e274a` | `eca5abc8e1a7fbfff7ca9f6c4e7e09479f93df3d73748cad936874574bb3ccfa` |

The following frozen artifacts are semantic references only. They supply no
additional representation authority and are not amended by this candidate:

| Semantic subject | Reference |
| --- | --- |
| Portfolio Identity | [Canonical Glossary](../GLOSSARY.md) “Portfolio Identity”; [M42-WP2 contract](M42_WP2_PORTFOLIO_IDENTITY_ACCOUNTING_SCOPE_MEMBERSHIP_AND_BASE_CURRENCY_CONTRACT_SPECIFICATION.md) §5.1 |
| Accounting Scope | [Canonical Glossary](../GLOSSARY.md) “Accounting Scope”; [M42-WP2 contract](M42_WP2_PORTFOLIO_IDENTITY_ACCOUNTING_SCOPE_MEMBERSHIP_AND_BASE_CURRENCY_CONTRACT_SPECIFICATION.md) §§5.2, 5.4, and 5.5 |
| Inherited baseline and non-amendment boundary | [Frozen LA-WP1 implementation candidate](LEDGER_ACCOUNTING_LA_WP1_AUTHORITY_BASELINE_AND_NON_AMENDMENT_REGISTER.md) §§2–4 |

### 2.1 Frozen LA-WP1 implementation identity

The inherited LA-WP1 implementation candidate is identified by the already
established [LA-WP1 Freeze record](LEDGER_ACCOUNTING_LA_WP1_FREEZE.md). This
is a citation of the frozen predecessor identity only; it makes no new
lifecycle determination.

| Item | Frozen identity |
| --- | --- |
| Candidate | [LA-WP1 Authority, Baseline, and Non-Amendment Register](LEDGER_ACCOUNTING_LA_WP1_AUTHORITY_BASELINE_AND_NON_AMENDMENT_REGISTER.md) |
| Git blob ID | `d6f4ff37c3af16e278dec95ec6afb619057fcd21` |
| SHA-256 | `3f3c6f3917e1b0247aa538de8ad6e070688529a65240893c57cd0e9d9cc274a4` |
| Freeze record | [LA-WP1 Freeze](LEDGER_ACCOUNTING_LA_WP1_FREEZE.md) |

The frozen semantic references establish meaning and ownership only. They do
not supply a lexical identifier form, scope-reference grammar, or byte
encoding; those are the LA-WP2 representation decisions below.

## 3. Common canonical byte rules

These rules apply to LA-1 and LA-2.

### 3.1 Byte and character encoding

1. A canonical payload is an exact sequence of US-ASCII bytes.
2. Every permitted character is encoded as its one-byte US-ASCII value.
3. No UTF-8 BOM, Unicode character, whitespace, carriage return, line feed,
   NUL byte, or trailing byte is permitted in a payload.
4. The payload is not a presentation string. It is compared byte-for-byte.
5. The identifier content decoded from `b64u` is opaque bytes. It is not
   interpreted as text, a UUID, a provider key, a database key, a URI, or any
   other semantic type.

### 3.2 Exact `b64u` encoding

`b64u` is canonical unpadded Base64 using exactly this alphabet:

```text
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_
```

The displayed line contains exactly the 64 characters shown; no space follows
the final underscore. More formally, `safe` is one of `A–Z`, `a–z`, `0–9`,
`-`, or `_`.

For a non-empty byte sequence, the canonical `b64u` token:

- contains at least two `safe` characters;
- has a length congruent to `0`, `2`, or `3` modulo `4`;
- has no `=` padding;
- uses zero in every unused trailing Base64 bit; and
- decodes to exactly the original non-empty byte sequence.

The encoding is bijective for the admitted byte sequences. Standard Base64
symbols `+` and `/`, padding, alternate alphabets, and non-zero unused bits
are invalid. No trimming, case-folding, Unicode normalization, percent
decoding, transliteration, or other normalization is authorized or performed.

The exact token grammar, before the zero-unused-bit canonicality check, is:

```text
safe = ALPHA / DIGIT / "-" / "_"
b64u = 4safe *(4safe) [2safe / 3safe] / 2safe / 3safe
```

### 3.3 Exact decimal length

`dec` is a positive base-10 byte count:

```text
dec = [1-9][0-9]*
```

It has no leading zero, and it counts the exact number of US-ASCII bytes in
the field it frames. There is no finite maximum length authorized by the
frozen planning corpus. Any finite implementation cap is outside this form
and cannot be used to change the canonical language.

### 3.4 Absence, defaults, and resolution

- Both forms require every field in their grammar. There is no optional field.
- Neither form has an affirmative absence value. Missing, unknown, null,
  empty, `NONE`, and `ABSENT` states have no in-band encoding.
- An absent form, an omitted field, an empty identifier, or an absence
  sentinel is invalid and fails closed.
- A token that happens to decode to bytes conventionally called “none” or
  “absent” has no absence meaning; identifier bytes remain opaque.
- No field is defaulted, inferred from ambient context, looked up live, or
  repaired from another field.

## 4. LA-1 — Portfolio Identity Canonical Reference Form

### 4.1 Inherited meaning

The form refers to the stable identifier of one portfolio container. It
establishes accounting identity only. It carries no strategy, goal, policy,
analytics, UI selection, lifecycle state, membership, currency, or other
meaning.

### 4.2 Field set, cardinality, and ordering

One LA-1 payload contains exactly one ordered occurrence of each field:

| Position | Field | Required content | Encoding |
| ---: | --- | --- | --- |
| 1 | `form_tag` | Literal `PI-1` | US-ASCII |
| 2 | `portfolio_identity_bytes` | One non-empty opaque identifier byte sequence | Canonical `b64u` |

The form has cardinality exactly one. It is not a list, map, tuple with
repeated fields, or concatenation of records.

### 4.3 Exact grammar

```text
portfolio-identity = "PI-1:" b64u
```

The colon is a required literal delimiter. `b64u` is the complete token to
the end of the payload; no extra delimiter or field is permitted.

### 4.4 Deterministic interpretation

1. Match the exact literal `PI-1:`.
2. Validate the remaining token as canonical `b64u`.
3. Decode it to one non-empty opaque byte sequence.
4. Interpret that sequence as the one Portfolio Identity reference carried by
   this payload.

Two valid LA-1 payloads refer to the same Portfolio Identity only when their
decoded identifier bytes are identical. No external lookup, display label,
case conversion, or semantic equivalence test is part of this form.

### 4.5 Invalid and prohibited states

The following are invalid:

- missing, empty, or truncated `portfolio_identity_bytes`;
- a non-canonical `b64u` token;
- a wrong, lower-case, versionless, or alternate form tag;
- any whitespace, BOM, Unicode, padding, extra delimiter, or extra field; and
- any attempt to use absence, default, ambient context, or a live lookup in
  place of the required identifier.

The following fields are prohibited: display name, owner name, account name,
strategy, goal, policy, analytics, UI selection, lifecycle state, membership,
currency, provider, database, tenant, timestamp, version beyond the fixed
form tag, or any other field not listed in §4.2.

### 4.6 Affirmative absence

LA-1 has no valid affirmative absence state. Absence is represented by failure
to supply a valid LA-1 payload, never by a sentinel payload. In particular,
`PI-1:` is invalid. A valid `b64u` token is always identifier content, even
when a human might read its decoded bytes as an absence word.

## 5. LA-2 — Accounting Scope Canonical Reference Form

### 5.1 Inherited meaning

The form refers to the Accounting Scope boundary to which one portfolio’s
holdings, transactions, cash, and balances belong. It binds the scope to one
explicit Portfolio Identity reference. It does not create a second scope,
permit cross-boundary replay, or define Membership or cross-portfolio
aggregation.

### 5.2 Field set, cardinality, and ordering

One LA-2 payload contains exactly one ordered occurrence of each field:

| Position | Field | Required content | Encoding |
| ---: | --- | --- | --- |
| 1 | `form_tag` | Literal `AS-1` | US-ASCII |
| 2 | `portfolio_identity_length` | Byte length of the following exact LA-1 payload | `dec` |
| 3 | `portfolio_identity_reference` | One complete canonical LA-1 payload | US-ASCII bytes |

The form has cardinality exactly one Accounting Scope reference bound to
exactly one Portfolio Identity reference. A standalone scope identifier is
not introduced: the frozen semantic corpus authorizes the scope boundary and
its portfolio binding, but does not authorize a separate scope-identity
coordinate. This omission is intentional and affirmative; it is not a
default, a lookup, or permission to omit the required binding.

### 5.3 Exact grammar

```text
accounting-scope = "AS-1:" dec ":" portfolio-identity
```

`dec` is the exact US-ASCII byte length of the complete following
`portfolio-identity` payload. The framed LA-1 payload is validated by the
complete LA-1 grammar; a merely prefix-shaped or truncated nested value is
not sufficient.

### 5.4 Deterministic interpretation

1. Match the exact literal `AS-1:`.
2. Parse canonical `dec` up to the next literal colon.
3. Consume exactly that many bytes as the nested LA-1 payload.
4. Require the nested payload to be a complete canonical LA-1 payload.
5. Interpret the resulting reference as the Accounting Scope corresponding
   to that explicitly supplied Portfolio Identity.

Every semantic projection of one portfolio that uses this form therefore
uses the same exact bound Portfolio Identity reference. A different bound
identity is a different scope reference. The form does not establish that a
portfolio or scope exists in a registry and does not perform semantic
resolution; consumers requiring such a fact must not infer or substitute it.

### 5.5 Invalid and prohibited states

The following are invalid:

- missing, zero, leading-zero, non-decimal, or incorrect `dec`;
- a missing, empty, truncated, malformed, or non-canonical nested LA-1
  payload;
- a nested payload whose bytes are not exactly the framed byte count;
- a wrong, lower-case, versionless, or alternate form tag;
- additional fields, repeated Portfolio Identity references, or multiple
  scope references;
- whitespace, BOM, Unicode, padding, or other non-ASCII bytes; and
- any default, ambient scope, live lookup, inferred binding, or repair.

The following fields are prohibited: standalone `scope_id`, scope name,
portfolio name, membership, holdings, transactions, cash, balances,
lifecycle state, currency, strategy, goal, policy, provider, tenant,
timestamp, cross-portfolio relation, or any field not listed in §5.2.

### 5.6 Affirmative absence

LA-2 has no valid affirmative absence state. Missing Accounting Scope or
missing Portfolio Identity binding is invalid; there is no `NONE`, `ABSENT`,
null, empty, or default scope payload. The required nested LA-1 reference is
the complete binding and must be supplied in every valid LA-2 payload.

## 6. Deterministic fail-closed decision

A payload conforms only if every byte rule, grammar rule, field rule,
cardinality rule, binding rule, and absence rule in this candidate succeeds.
Failure of any one rule rejects the payload. A conforming payload is not
proof of registry existence, ownership authorization, semantic history,
membership, or runtime admissibility. This candidate supplies no live
resolution or implementation behavior.

## 7. Package-local vector annexes

LA-WP2 has two distinct package-local vector annexes. Each annex is part of
this candidate, is exclusive to its parent form, and is not a runtime test
suite. The vectors are documentary examples of the exact written forms and
fail-closed boundaries.

### 7.1 LA-1 package-local vector annex

#### 7.1.1 Vector coverage map

| Required coverage | Vectors |
| --- | --- |
| LA-1 positive canonical forms | `LA-WP2-PV-PI-001` through `LA-WP2-PV-PI-005` |
| LA-1 minimum and identifier-content boundaries | `LA-WP2-BV-001` through `LA-WP2-BV-004`, and `LA-WP2-BV-007` |
| LA-1 absence, encoding, ordering, and prohibited-field negatives | `LA-WP2-NV-001` through `LA-WP2-NV-009` |

#### 7.1.2 Positive vectors

All payloads below are exact US-ASCII bytes and conform.

| ID | Payload | Deterministic interpretation |
| --- | --- | --- |
| `LA-WP2-PV-PI-001` | `PI-1:AA` | One-byte opaque identifier `00`. |
| `LA-WP2-PV-PI-002` | `PI-1:AQ` | One-byte opaque identifier `01`. |
| `LA-WP2-PV-PI-003` | `PI-1:_w` | One-byte opaque identifier `ff`; URL-safe `_` is required. |
| `LA-WP2-PV-PI-004` | `PI-1:AAE` | Two-byte opaque identifier `00 01`. |
| `LA-WP2-PV-PI-005` | `PI-1:AAECAw` | Four-byte opaque identifier `00 01 02 03`. |

#### 7.1.3 Boundary vectors

| ID | Payload or condition | Boundary result |
| --- | --- | --- |
| `LA-WP2-BV-001` | `PI-1:AA` | Smallest valid LA-1 identifier: one decoded byte. Zero decoded bytes are not admitted. |
| `LA-WP2-BV-002` | `PI-1:AAE` | Valid two-byte identifier; the unpadded `b64u` length may be `3`. |
| `LA-WP2-BV-003` | `PI-1:AAEC` | Valid three-byte identifier; the `b64u` length may be `4`. |
| `LA-WP2-BV-004` | `PI-1:AAECAw` | Valid four-byte identifier; longer finite identifiers continue under the same rule. |
| `LA-WP2-BV-007` | Any finite non-empty identifier byte sequence representable by canonical `b64u` | Valid regardless of byte content or finite length; no maximum or semantic identifier subtype is authorized. |

#### 7.1.4 Negative vectors

Every vector below is rejected.

| ID | Non-conforming payload or condition | Rejection reason |
| --- | --- | --- |
| `LA-WP2-NV-001` | `PI-1:` | Empty identifier; absence is not encoded. |
| `LA-WP2-NV-002` | Missing payload, `null`, `NONE`, or `ABSENT` | No in-band absence or default state exists. |
| `LA-WP2-NV-003` | `PI-1:A` | `b64u` length `1 mod 4`; invalid token. |
| `LA-WP2-NV-004` | `PI-1:AA=` or `PI-1:AA==` | Padding is prohibited. |
| `LA-WP2-NV-005` | `PI-1:+w` or `PI-1:/w` | Standard Base64 symbols are not in the `b64u` alphabet. |
| `LA-WP2-NV-006` | `PI-1:AB` | Non-zero unused trailing bits; not the canonical encoding of `00`. |
| `LA-WP2-NV-007` | `pi-1:AA` | Form tags are case-sensitive exact literals. |
| `LA-WP2-NV-008` | `PI-1:AA ` | Trailing whitespace is a payload byte and is prohibited. |
| `LA-WP2-NV-009` | `PI-1:AA:extra` | LA-1 has no extra field or delimiter. |

### 7.2 LA-2 package-local vector annex

#### 7.2.1 Vector coverage map

| Required coverage | Vectors |
| --- | --- |
| LA-2 positive canonical forms and exact binding | `LA-WP2-PV-AS-001` through `LA-WP2-PV-AS-004` |
| LA-2 length and binding boundaries | `LA-WP2-BV-005` through `LA-WP2-BV-006` |
| LA-2 absence, defaults, normalization, ordering, cardinality, and prohibited-field negatives | `LA-WP2-NV-010` through `LA-WP2-NV-020` |

#### 7.2.2 Positive vectors

All payloads below are exact US-ASCII bytes and conform.

| ID | Payload | Deterministic interpretation |
| --- | --- | --- |
| `LA-WP2-PV-AS-001` | `AS-1:7:PI-1:AA` | One Accounting Scope reference bound to `PI-1:AA`; `7` is the nested byte length. |
| `LA-WP2-PV-AS-002` | `AS-1:7:PI-1:AQ` | One Accounting Scope reference bound to `PI-1:AQ`. |
| `LA-WP2-PV-AS-003` | `AS-1:7:PI-1:_w` | One Accounting Scope reference bound to the opaque `ff` identity. |
| `LA-WP2-PV-AS-004` | `AS-1:11:PI-1:AAECAw` | One Accounting Scope reference with a four-byte nested identity; `11` is the nested byte length. |

#### 7.2.3 Boundary vectors

| ID | Payload or condition | Boundary result |
| --- | --- | --- |
| `LA-WP2-BV-005` | `AS-1:7:PI-1:AA` | Minimum valid LA-2 binding: the shortest valid complete LA-1 payload is framed exactly. |
| `LA-WP2-BV-006` | `AS-1:8:PI-1:AAE` | A length of `8` frames the complete nested `PI-1:AAE`; one-byte length changes are meaningful. |

#### 7.2.4 Negative vectors

Every vector below is rejected.

| ID | Non-conforming payload or condition | Rejection reason |
| --- | --- | --- |
| `LA-WP2-NV-010` | `AS-1:` | Missing required length and binding. |
| `LA-WP2-NV-011` | `AS-1:0::` | Length must be positive and a nested identity is required. |
| `LA-WP2-NV-012` | `AS-1:07:PI-1:AA` | `dec` has a leading zero. |
| `LA-WP2-NV-013` | `AS-1:6:PI-1:AA` | Framed length is shorter than the nested LA-1 payload. |
| `LA-WP2-NV-014` | `AS-1:8:PI-1:AA` | Framed length is longer than the nested LA-1 payload. |
| `LA-WP2-NV-015` | `AS-1:9:PI-1:AA==` | The framed bytes are not a canonical LA-1 payload. |
| `LA-WP2-NV-016` | `AS-1:7:PI-1:AA:AA` | A standalone scope identifier or extra field is prohibited. |
| `LA-WP2-NV-017` | `AS-1:15:PI-1:AA,PI-1:AQ` | Multiple Portfolio Identity references cannot bind one LA-2 form. |
| `LA-WP2-NV-018` | `AS-1:2:AA:PI-1` | Field order and nested LA-1 grammar are invalid. |
| `LA-WP2-NV-019` | `AS-1:7:PI-1:AA` followed by CRLF bytes | Line terminators and trailing bytes are prohibited. |
| `LA-WP2-NV-020` | Any payload that supplies a missing field from ambient context, a default, a live registry lookup, normalization, or repair | Deterministic interpretation is payload-only and fail-closed. |

## 8. Implementation omission register

The frozen planning corpus does not authorize the following, so this
candidate deliberately does not define them:

- a human-readable Portfolio Identity or Accounting Scope name;
- a UUID, URI, provider key, database key, tenant key, or external registry;
- a standalone Accounting Scope identifier separate from its required
  Portfolio Identity binding;
- a finite maximum identifier size;
- Unicode normalization or any alternate textual normalization;
- semantic existence, ownership, authorization, Membership, or historical
  resolution; and
- any runtime parser, validator, API, schema, persistence, or migration.

These omissions are fail-closed boundaries, not implicit defaults or
permission for a later consumer to invent a substitute.
