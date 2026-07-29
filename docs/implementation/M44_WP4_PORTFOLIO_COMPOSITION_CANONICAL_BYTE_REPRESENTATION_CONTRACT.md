# M44-WP4 — Portfolio Composition Canonical Byte Representation Contract

**Milestone:** M44 — Portfolio Analytics Gate Closure and Normative Semantics Foundation

**Work package:** M44-WP4 only

**Artifact class:** Normative documentary constitutional contract

**Status:** `RC4 — SERIALIZATION CORRECTED; NOT INDEPENDENTLY SERIALIZATION-APPROVED OR CONFIRMED`

**Revision:** RC4. Supersedes RC3 in full for renewed independent serialization
review. The constitutionally approved canonical grammar and
`G-3 OPEN — PARTIAL` determination remain unchanged.

**Constitutional contract review:** `APPROVED` at RC3

**Normative contract confirmation:** `NOT CONFIRMED`

**Freeze performed:** `NO`

**WP4 closed:** `NO`

**G-3 determination:** `OPEN — PARTIAL`

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
**Ownership-determination authority:** `NONE`
**Vocabulary-admission authority:** `NONE`
**Encoding-selection authority:** `LIMITED TO THE PORTFOLIO COMPOSITION CONTAINER REPRESENTATION ALLOCATED TO M44-WP4`

This contract defines documentary canonical-byte conformance for the Portfolio
Composition container only. It creates no serializer, executable fixture,
runtime behavior, persistence form, API form, production method, or source-owned
coordinate encoding.

---

## 1. Normative status and controlling authority

The governing frozen authorities are:

1. [M44 Architecture and Implementation Plan](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
   RC2, frozen by the
   [M44 Architecture Freeze Record](M44_ARCHITECTURE_FREEZE_RECORD.md);
2. the binding [M44-WP1 Roadmap and Current-State Reconciliation](M44_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md)
   §§6.3–6.7, frozen by the
   [M44-WP1 Freeze Record](M44_WP1_FREEZE_RECORD.md) §11.1;
3. [M42-WP7 Portfolio Composition Contract](M42_WP7_PORTFOLIO_COMPOSITION_CONTRACT_SPECIFICATION.md);
4. the source-owning M42 contracts cited by the binding inventory; and
5. [M43-WP3 Portfolio Measure Subject Contract](M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md)
   §7.1.

The confirmed
[M44-WP4 Architecture and Implementation Plan](M44_WP4_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
is non-normative planning guidance. Its
[Independent Constitutional Architecture Confirmation](M44_WP4_INDEPENDENT_CONSTITUTIONAL_ARCHITECTURE_CONFIRMATION.md)
permits this allocated documentary authorship only. It does not confirm this
contract or satisfy frozen M44 Architecture §12.5 point 4.

### 1.1 Exclusive extension bases

`E-1` and `E-2` are the exclusive extension bases.

`E-1` is frozen M42-WP7 §5:

> “A representation may claim canonical bytes only if it preserves this tag,
> this order, exact citations, owner attributions, Provenance associations, and
> the explicit-absence distinction.”

Its second constitutive sentence is:

> “Their exclusion does not remove or defer the frozen canonical-byte obligation.”

This second limb defeats every silence-based removal, deferral, or weakening of
the obligation merely because frozen M42-WP7 excludes byte-encoding mechanism
from its own scope.

`E-2` is frozen M43-WP3 Subject §7.1:

> “until a separately authorized contract supplies the exact Composition
> canonical bytes, no concrete Portfolio Measure Subject—and consequently no
> concrete Portfolio Analytics Input Manifest—can be formed.”

**WP4-NR-001 — Exclusive authority.** Constitutional silence is not authority.
No declared or undeclared silence, including any omission in a frozen contract,
may be used to create encoding, ownership, vocabulary, implementation, or
production authority. WP4 defines only the Portfolio Composition container
representation. Nested source-owned canonical bytes remain opaque. A missing
source-owned encoding may not be invented.

**WP4-NR-002 — Non-amendment.** This contract preserves every frozen M42 and M43
meaning, owner, co-owner, coordinate, field order, explicit-absence rule, and
Provenance rule. It does not amend a frozen artifact.

**WP4-NR-032 — Own-domain nested-form boundary.** Ownership of the Investment
Universe Declaration or Benchmark Declaration meaning by Portfolio Intelligence
does not authorize M44-WP4 to define, repair, infer, or select the missing
nested canonical forms. Container authority does not become nested amendment authority
merely because the nested noun is owned by Portfolio Intelligence.

This negative determination is controlled directly by frozen
[M44-WP1 Reconciliation](M44_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md)
§6.6; frozen
[M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §17 `OQ-1`;
[M42-WP7](M42_WP7_PORTFOLIO_COMPOSITION_CONTRACT_SPECIFICATION.md) §5,
which states that the container “does not define nested field order inside any source-owned coordinate”;
M42-WP7 §9 item 11; frozen `PC-NGV-14`; and frozen M44 `INV-C1`. The
non-normative WP4 architecture plan is not the source of this authority
boundary.

## 2. Frozen noun, schema tag, order, and ownership

The governed noun remains Portfolio Composition. The exact schema tag is:

`M42-WP7-PORTFOLIO-COMPOSITION-1`

The exact frozen semantic order and allocation are:

| # | Exact frozen field | Exact frozen ownership or co-ownership |
| ---: | --- | --- |
| 1 | `schema_version` | Portfolio Intelligence — container framing |
| 2 | `portfolio_identity` | Ledger & Accounting |
| 3 | `accounting_scope` | Ledger & Accounting |
| 4 | `portfolio_membership` | Ledger & Accounting |
| 5 | `portfolio_base_currency` | Ledger & Accounting — coordinate; Asset Foundation — currency-of-denomination dimension |
| 6 | `investment_universe_declaration` | Portfolio Intelligence — declaration; Asset Foundation — criterion vocabulary |
| 7 | `portfolio_benchmark_declaration` | Portfolio Intelligence — declaration; Market Intelligence — series; Asset Foundation — `asset_id` |
| 8 | `portfolio_lifecycle_state` | Ledger & Accounting |
| 9 | `coordinate_owner_attributions` | Portfolio Intelligence — association only |
| 10 | `coordinate_provenance_associations` | Connectivity & Ingestion — Provenance meaning and capture; Portfolio Intelligence — association only |

**WP4-NR-003 — Frozen noun preservation.** The tag, all ten field names, their
order, every ownership and co-ownership allocation, exact coordinate-owner
attribution, coordinate-specific Provenance association, and the
explicit-absence distinction are immutable inputs to this contract.

**WP4-NR-004 — Preservation check.** UTF-8 or locale processing is not used to
obtain the tag or field order. The 31 octets of raw
`ASCII("M42-WP7-PORTFOLIO-COMPOSITION-1")` are emitted first. The remaining
components are emitted in field-number order 2 through 10. This is
byte-order-identical to frozen M42-WP7 §5: field 1 is the exact tag and fields
2–10 follow in the exact frozen sequence. No alternate tag or order conforms.

## 3. Binding frozen WP1 pre-inventory

The following field and facet tables are carried verbatim from frozen
[M44-WP1 Reconciliation](M44_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md)
§§6.3–6.4. WP4 does not re-derive, reclassify, widen, narrow, repair, or
reinterpret any cell. A perceived divergence is a contract-review finding, not
a WP4 resolution.

### 3.1 Per-field inventory — verbatim carriage

| # | §5 field | Owner (M42-WP7 §3) | (a) Reference exactness | (b) Written-form determinacy | Frozen evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | `schema_version` | Portfolio Intelligence (container framing, M42-WP7 §5) | `SUPPLIED — EXACT` | `SUPPLIED — EXACT LITERAL` | M42-WP7 §5: "The schema-version tag is exactly M42-WP7-PORTFOLIO-COMPOSITION-1"; §9 item 10 |
| 2 | `portfolio_identity` | Ledger & Accounting | `SUPPLIED — EXACT` — the coordinate is itself "the stable identifier of one portfolio container" | `NOT SUPPLIED` — no identifier syntax, value domain, or lexical form is frozen | `GLOSSARY.md` "Portfolio Identity"; `M34-D-0002`; M42-WP2 §5.1 "This contract adds no field, exception, or alternate meaning" |
| 3 | `accounting_scope` | Ledger & Accounting | `SUPPLIED — EXACT` — an exact corresponding-scope citation is required and owner-supplied | `NOT SUPPLIED` — no scope-reference form is frozen | `GLOSSARY.md` "Accounting Scope"; `M34-D-0002`; M42-WP2 §5.2; M42-WP7 §3 "Exact corresponding-scope citation" |
| 4 | `portfolio_membership` | Ledger & Accounting | `NOT SUPPLIED` — the coordinate is an "Exact Ledger fact"; no canonical representation of the membership set, its elements, its cardinality, or its order is frozen | `NOT SUPPLIED` | M42-WP7 §3; M42-WP2 §5.3; `M34-D-0003` |
| 5 | `portfolio_base_currency` | Ledger & Accounting (coordinate); Asset Foundation (the currency-of-denomination dimension) | `SUPPLIED — EXACT` — "a single reference to Asset Foundation's currency-of-denomination coordinate for one Portfolio Identity" | `NOT SUPPLIED — EXPRESSLY` | M42-WP2 §6.2: "this contract does not itself mint a format, because none is frozen for it to cite yet"; "Until Asset Foundation publishes that exact format..." |
| 6 | `investment_universe_declaration` | Portfolio Intelligence (declaration); Asset Foundation (criterion vocabulary) | `SUPPLIED — EXACT` — the complete six-facet declaration of M42-WP3 Stage B §9.1 | `NOT SUPPLIED` — no identifier syntax, no envelope, no nested order | M42-WP3 Stage B header `Serialization authority: NONE`; §5.3 "deliberately defines no identifier syntax... not a WP3-defined string, code, URI, key, or byte representation"; §9.1 "does not prescribe a serialized envelope, field order, schema, identifier, bytes, transport"; NGV-26 |
| 7 | `portfolio_benchmark_declaration` | Portfolio Intelligence (declaration); Market Intelligence (series); Asset Foundation (`asset_id`) | `SUPPLIED — EXACT` for all four forms, including Explicitly None | `PARTIAL` — see the facet breakdown at §6.4 | M42-WP5 §§4.2–4.5; M42-WP7 §4.4 |
| 8 | `portfolio_lifecycle_state` | Ledger & Accounting | `SUPPLIED — EXACT` | `SUPPLIED — CLOSED LITERAL VOCABULARY` — exactly `active`, `archived`, `closed`, with no fourth value admissible | M42-WP6 §4.1 item 2, §4.2, §4.3; `GLOSSARY.md` "Portfolio Lifecycle State" |
| 9 | `coordinate_owner_attributions` | Portfolio Intelligence (association only) | `SUPPLIED — EXACT` — the owner names are the frozen domain names of M42-WP7 §3 | `NOT SUPPLIED` — no attribution form is frozen; framing is available to M44-WP4 because the element is the container's own | M42-WP7 §5: "Owner attribution and Provenance association preserve association only; neither creates a new owner or Provenance meaning" |
| 10 | `coordinate_provenance_associations` | Connectivity & Ingestion (meaning and capture); Portfolio Intelligence (association only) | `NOT SUPPLIED` for the Provenance content — no capture format, evidence class, storage shape, or completeness test is frozen | `NOT SUPPLIED` — the association is framable; the carried content is not | M42-WP6 §5.1: "It does not define what must have been captured, a capture format, a confidence threshold, an evidence class, a storage shape, or a completeness test"; §5.2 forbids parsing, normalization, and summarization |

### 3.2 Facet breakdown — verbatim carriage

**Field 6 — Investment Universe declaration** (facets exactly as frozen M42-WP3
Stage B §9.1 enumerates them):

| Facet | (a) | (b) | Note |
| --- | --- | --- | --- |
| Exact Portfolio Identity citation | `SUPPLIED` | `NOT SUPPLIED` | Inherits field 2 |
| Exact corresponding Accounting Scope citation | `SUPPLIED` | `NOT SUPPLIED` | Inherits field 3 |
| Explicit declared name | `SUPPLIED` | `NOT SUPPLIED` | Stage B §4.2: "This contract defines no lexical encoding, length limit, normalization, uniqueness rule, localization rule, or serialization for declared names" |
| Every present criterion-category coordinate | `SUPPLIED` | `NOT SUPPLIED` | No category order is frozen; NGV-26 records that Stage B does not supply one to a downstream serializer |
| Each criterion's set-or-range extent and exact Asset Foundation references | `SUPPLIED` | `NOT SUPPLIED` | Stage B §5.3: exactness "means semantic identity with the source-owned reference, not a WP3-defined string, code, URI, key, or byte representation" |
| The immutable-until-explicitly-revised semantic condition | `SUPPLIED` | `NOT SUPPLIED` | A semantic condition with no frozen representation |

**Field 7 — Portfolio Benchmark Declaration:**

| Facet | (a) | (b) | Note |
| --- | --- | --- | --- |
| Benchmark series references (Single, Composite, Category) | `SUPPLIED — EXACT` | `PARTIAL` | M42-WP5 §4.4 requires "the frozen `asset_id` format: the platform's own permanent, opaque identifier, owned by Asset Foundation and defined once at UNIVERSAL_ASSET_ARCHITECTURE.md §2–3." The reference form is frozen and named; the identifier is expressly **opaque**, and no lexical form is published for it |
| The explicit declared name | `SUPPLIED` | `NOT SUPPLIED` | M42-WP5 §4.2: "WP5 defines no name syntax, identifier format, uniqueness scope, localization, normalization, storage, or serialization rule" |
| The closed form discriminator | `SUPPLIED` | `CONSTRAINED — NOT SUPPLIED` | M42-WP5 §4.3: "The four form labels classify the declaration only. They do not authorize runtime discriminators, **serialized tags**, API values, database enumerations, or implementation constants." A canonical byte form must distinguish the four forms without using the labels as tags; no frozen authority supplies how |
| Explicitly None | `SUPPLIED — EXACT` | `NOT SUPPLIED` | An affirmative state distinct from missing (M42-WP7 §4.4, PC-NGV-10); no representation is frozen, and the distinction must survive encoding |
| Composite weights | Not applicable | Not applicable | M42-WP5 §4.3 places "calculation, weighting, construction, maintenance, and observation values" outside the declaration; no encoding obligation arises |

**Field 10 — Coordinate Provenance associations:**

| Facet | (a) | (b) | Note |
| --- | --- | --- | --- |
| The association between one Provenance item and its exact coordinate | `SUPPLIED` | `NOT SUPPLIED` — framable by the container | M42-WP6 §5.1 items 2 and 5; M42-WP7 §5 |
| The already-captured Provenance content itself | `NOT SUPPLIED` | `NOT SUPPLIED` | M42-WP6 §5.1; encoding it would require parsing or normalizing it, both prohibited by §5.2 |
| Separation of one coordinate's Provenance from another's | `SUPPLIED` | `NOT SUPPLIED` | M42-WP6 §5.1 item 2 and §5.2 — combination "in a way that obscures which origin belongs to which coordinate" is prohibited, which is an encoding constraint, not a form |

### 3.3 Binding tally and routing

Written-form determinacy is satisfied for two fields, partially satisfied for
one, and unsatisfied for seven. Six source-owned coordinates lack a frozen
written form; field 7 lacks it in part. Reference exactness is additionally
unsatisfied for `portfolio_membership` and the carried Provenance content.
Field 8, `portfolio_lifecycle_state`, remains `SUPPLIED — EXACT` and
`SUPPLIED — CLOSED LITERAL VOCABULARY`; it is not an unsupplied or routed
element. Those inventory axes answer which semantic written values are
admitted. They do not grant WP4 authority to choose the octet encoding of those
values. Field 8 is supplied under the frozen inventory and carried as opaque,
Ledger & Accounting-supplied canonical bytes. The container does not inspect or
select the internal encoding.

The following routing paragraph and table carry frozen M44-WP1 §6.5 verbatim:

For every unsatisfied cell, the obligation routes to the frozen owner named
below. **This map is a record, not a request.** M44 holds no authority in any
domain but Portfolio Intelligence (frozen RC2 INV-C4), and frozen RC2 §17
`OQ-1` alternative (b) — soliciting per-coordinate records from owning domains
— is expressly "constitutionally unavailable to M44 in any case."

| Unsupplied element | Frozen owner it routes to | M44 authority over it |
| --- | --- | --- |
| Portfolio Identity reference form | Ledger & Accounting | `NONE` |
| Accounting Scope reference form | Ledger & Accounting | `NONE` |
| Portfolio Membership canonical representation | Ledger & Accounting | `NONE` |
| Portfolio Base Currency identifier format | Asset Foundation (the dimension), Ledger & Accounting (the coordinate) | `NONE` |
| Investment Universe declaration nested form and order | Portfolio Intelligence, under the frozen M42-WP3 Stage B contract | `NONE` without amending a frozen M42 artifact, which INV-C1 forbids — see §6.6 |
| Benchmark declared-name form; form-discriminator representation; Explicitly None representation | Portfolio Intelligence, under the frozen M42-WP5 contract | Same as above |
| `asset_id` lexical form | Asset Foundation | `NONE` |
| Provenance content representation | Connectivity & Ingestion | `NONE` |

Within the verbatim carriage, `§6.6` means frozen M44-WP1 Reconciliation §6.6.
`WP4-NR-032` carries that own-domain negative resolution into this contract:
Portfolio Intelligence ownership of the nested meaning does not grant WP4
nested-form amendment authority.

**WP4-NR-005 — Inventory binding.** Both axes and every facet above bind the
disposition without alteration. Routing records an obligation; it does not
discharge it.

## 4. Exact canonical byte grammar

This section admits one and only one container representation.

### 4.1 WP4-local primitives

For this WP4 corpus only:

- `||` is exact byte concatenation;
- `ASCII(s)` is the one-octet-per-character US-ASCII encoding of the stated
  fixed contract literal;
- `u32(n)` is one unsigned 32-bit integer in network byte order, with
  `0 <= n <= 4,294,967,295`;
- `lp(x) = u32(byte_length(x)) || x`;
- unsigned byte equality compares every octet without normalization; and
- every length is the length in octets, never characters or code points.

[M43-WP3 Subject](M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md)
§7.1 is mechanical precedent only. It grants no cross-corpus convention or
authority. These primitives are WP4-local documentary mechanics.

**WP4-NR-006 — Canonical integers.** `u32` is always exactly four octets and
network-byte-order. No decimal text, variable-length integer, signed integer,
shortened leading-zero form, host byte order, or library-default number form
conforms.

**WP4-NR-007 — Canonical length prefix.** Every `lp(x)` contains the one
canonical `u32(byte_length(x))` followed immediately by exactly those octets.
Length overflow, underflow, mismatch, truncation, and suffix material reject the
container.

### 4.2 Schema-tag decision

The schema tag is exactly the 31 raw, fixed, unframed US-ASCII octets:

```text
ASCII("M42-WP7-PORTFOLIO-COMPOSITION-1")
```

**WP4-NR-008 — Single admitted tag form.** The raw form above is the only
admitted schema-tag framing. A length-prefixed tag, UTF-8 byte-order mark,
terminator, padding, case variation, alternate character encoding, abbreviated
tag, or any other tag is rejected. Raw `ASCII("PMS1")` in frozen M43-WP3 §7.2
is precedent for this decision only; it is not an authority grant.

### 4.3 Top-level grammar

Let `F2` through `F8` be the exact, finite, non-empty canonical byte sequences
supplied by the frozen owners of fields 2 through 8. Let `OA` be the
Composition-owned owner-attribution envelope in §4.4 and `PA` the
Composition-owned Provenance-association envelope in §4.5.

The canonical bytes are exactly:

```text
ASCII("M42-WP7-PORTFOLIO-COMPOSITION-1")
lp(F2)  # portfolio_identity
lp(F3)  # accounting_scope
lp(F4)  # portfolio_membership
lp(F5)  # portfolio_base_currency
lp(F6)  # investment_universe_declaration
lp(F7)  # portfolio_benchmark_declaration
lp(F8)  # portfolio_lifecycle_state
lp(OA)  # coordinate_owner_attributions
lp(PA)  # coordinate_provenance_associations
```

Line breaks and comments above are documentary notation and emit no octets.

**WP4-NR-009 — One grammar and fixed order.** The concatenation above is the
only canonical grammar. All ten fields are required. No key names, delimiters,
maps, objects, tags between fields, optional slots, extensions, or alternate
orders are admitted. A conforming producer must emit the source-owned fields in
their frozen semantic order. Because `F2` through `F8` have no emitted field
identifiers, a parser assigns their semantic identities by fixed position.

**WP4-NR-010 — Required owner bytes.** `F2` through `F8` must each be
owner-supplied canonical bytes. Each field must contain at least one octet and
at most `4,294,967,295` octets. A label, example identifier, display value,
database key, provider value, inferred representation, or WP4-authored
substitute is not owner-supplied canonical bytes. This contract cannot
independently verify or prescribe the internal byte encoding of field 8.

### 4.4 Owner-attribution association envelope

`OA` associates every fixed field number with the exact frozen owner-domain
name or names. It defines association framing only.

```text
OA   = u32(10) || OA_1 || OA_2 || ... || OA_10
OA_i = u32(i) || u32(owner_count_i) || lp(ASCII(owner_1)) || ... || lp(ASCII(owner_k))
```

For every `OA_i`, `k = owner_count_i`; the production contains exactly `k`
owner literals.

The exact entries and co-owner order are:

| Field | Exact owner-domain sequence |
| ---: | --- |
| 1 | `Portfolio Intelligence` |
| 2 | `Ledger & Accounting` |
| 3 | `Ledger & Accounting` |
| 4 | `Ledger & Accounting` |
| 5 | `Ledger & Accounting`, `Asset Foundation` |
| 6 | `Portfolio Intelligence`, `Asset Foundation` |
| 7 | `Portfolio Intelligence`, `Market Intelligence`, `Asset Foundation` |
| 8 | `Ledger & Accounting` |
| 9 | `Portfolio Intelligence` |
| 10 | `Connectivity & Ingestion`, `Portfolio Intelligence` |

These exact ASCII domain-name literals are WP4 grammar tokens for the
Composition-owned field-9 association envelope. They are not specimen or
presentation text substituted for source-owned nested coordinate bytes.

The role qualifiers in §2 remain normative: field 5 preserves coordinate versus
dimension ownership; field 6 declaration versus criterion-vocabulary
ownership; field 7 declaration, series, and `asset_id` ownership; fields 9 and
10 preserve `Portfolio Intelligence — association only`; and Connectivity &
Ingestion retains field-10 Provenance meaning and capture.

**WP4-NR-011 — Exact attribution framing.** `OA` has exactly ten entries in
field order. Exact ASCII domain names, owner counts, co-owner order, and role
allocations are fixed. Unknown, omitted, duplicate, reordered, renamed, merged,
or added owners reject. The envelope does not create shared ownership or
transfer meaning.

### 4.5 Provenance-association envelope

`PA` frames an association between each source-coordinate slot 2 through 8 and
the already-captured Provenance items supplied for that exact coordinate:

```text
PA       = u32(7) || PA_2 || PA_3 || ... || PA_8
PA_i     = u32(i) || u32(item_count_i) || lp(P_i_1) || ... || lp(P_i_n)
P_i_j    = exact finite non-empty owner-supplied canonical Provenance bytes
```

For every `PA_i`, `n = item_count_i`; the production contains exactly `n`
Provenance items.

The container preserves the exact item sequence supplied by Connectivity &
Ingestion. It does not sort or otherwise reorder the sequence. A zero
`item_count_i` states only that the authoritative supplied sequence for that
coordinate contains no already-captured item; it does not infer completeness,
missingness, correctness, or quality. Conformance requires the owner to supply
the canonical item boundaries, bytes, sequence, and completeness needed for the
association. Frozen WP1 records that no such content representation or
completeness test is supplied.

**WP4-NR-012 — Association-only framing.** `PA` has exactly seven
source-coordinate entries, fields 2 through 8 in frozen order. Schema framing,
owner attributions, and the association envelope itself do not acquire
Provenance entries. Each item remains opaque and attached to one exact
coordinate. Duplicate items within one coordinate, duplicate coordinate
entries, moved items, detached items, merged sequences, alternate coordinate
order, and trailing material reject.

**WP4-NR-013 — Provenance ownership.** Connectivity & Ingestion retains
ownership of Provenance meaning, capture, carried content, item boundaries, and
source-supplied sequence. Portfolio Intelligence owns only the fixed association
envelope. WP4 does not capture, parse, normalize, summarize, validate,
reconstruct, rank, score, trust-grade, or reinterpret Provenance.

## 5. Opaque nested-byte and absence boundary

**WP4-NR-014 — Opaque nested bytes.** For every source-owned coordinate and
every carried Provenance item, the container consumes only owner-supplied
canonical bytes. It does not parse, normalize, reorder, case-fold, Unicode-
normalize, numerically rewrite, reinterpret, derive, repair, enrich, infer, or
substitute specimen labels or presentation text. Unsigned byte identity is the
only container-level comparison.

For field 8 specifically, WP4 does not define, select, inspect, normalize,
validate, or reinterpret its nested byte encoding. The container cannot
independently verify or prescribe that internal encoding.

**WP4-NR-015 — Missing required coordinate.** A missing required coordinate has
no conforming byte representation. It must not be represented as empty bytes,
zero length, null, a sentinel, omission, an inferred default, or any invented
form. If any required owner-supplied bytes are missing, no complete conforming
Composition byte sequence exists.

**WP4-NR-016 — Affirmative absence is present.** An affirmative owner-defined
absence, including a valid Benchmark Declaration `Explicitly None`, is a
present coordinate represented only by the owner-supplied canonical bytes for
that affirmative state. It remains distinct from missingness. Because frozen
authority does not supply those bytes for `Explicitly None`, WP4 does not
invent them.

**WP4-NR-017 — Benchmark discriminator constraint.** The Benchmark form
discriminator is `CONSTRAINED — NOT SUPPLIED`. The four frozen presentation
labels classify declarations only. They must not be used as serialized tags,
runtime discriminators, API values, database values, implementation constants,
or canonical bytes. The missing nested form routes to Portfolio Intelligence
under frozen M42-WP5; the `asset_id` lexical form routes to Asset Foundation.

## 6. Canonical decode, determinism, and rejection

**WP4-NR-018 — Decode.** A documentary decoder matches the 31 exact tag octets,
then decodes exactly nine top-level `lp` values. It treats `F2`–`F8` as opaque,
parses `OA` only by §4.4, parses `PA` only by §4.5 while leaving every `P_i_j`
opaque, requires complete input consumption, and reconstructs the ten ordered
fields without information loss.

**Serialization-observability clarification.** The parser can detect structural
component omission, excess, truncation, trailing bytes, and explicit
field-number sequence errors inside `OA` or `PA`. Top-level `F2` through `F8`
have no emitted field identifiers. If a producer places semantically wrong
opaque bytes in an otherwise valid position, the parser cannot detect the
producer's semantic misassignment: it decodes the stream as a different
positional Composition input. This does not create a second decode of the same
byte stream and does not make the grammar ambiguous. Upstream semantic and
subject-coherence obligations remain binding and are not independently
verified by the byte parser.

**WP4-NR-019 — Injectivity and round trip.** One conforming logical container
has exactly one byte sequence, and one conforming byte sequence reconstructs
exactly one logical container. Decode followed by encode and encode followed by
decode preserve every octet, field boundary, fixed order, owner association,
coordinate-Provenance association, and affirmative-absence distinction.
Injectivity is defined over the ordered tuple of opaque byte strings
`(F2, F3, F4, F5, F6, F7, F8)`, followed by the exact `OA` and `PA` envelopes.
Distinct producer intent that is not represented in those bytes is not a
second admitted decode.

**WP4-NR-020 — Presentation independence.** Presentation order, map iteration,
document order, locale, collation, Unicode normalization, numeric formatting,
library defaults, platform byte order, runtime state, storage, provider,
clock, session, and ambient context cannot affect canonical bytes.

The following rejection rules are mandatory:

| Normative row | Rejected input |
| --- | --- |
| `WP4-NR-021` | Unknown fields, extension fields, or material outside the fixed grammar |
| `WP4-NR-022` | Mechanically observable alternate forms, including alternate schema tags, tag framing, field framing, omitted, excess, or duplicated top-level framing components, or explicit field-number order errors inside `OA` or `PA`; this row does not claim byte-level detection of an opaque semantic payload misassignment |
| `WP4-NR-023` | Duplicate keys, repeated fields, duplicate owner entries, duplicate coordinate-association entries, or duplicate Provenance association items within one coordinate |
| `WP4-NR-024` | Non-canonical numbers, including non-four-octet lengths, non-network order, signed, textual, variable-width, overflowing, or mismatched lengths |
| `WP4-NR-025` | Any trailing byte, unread suffix, padding, terminator, byte-order mark, or material after field 10 |
| `WP4-NR-026` | Unicode ambiguity, normalization, case-folding, locale transformation, or text-dependent alternate representation |
| `WP4-NR-027` | Omitted required coordinates or substitution by empty, null, sentinel, omission, inferred default, or invented owner bytes |
| `WP4-NR-028` | Presentation text, specimen labels, frozen form labels, provider identifiers, database keys, API values, or implementation constants used as canonical nested bytes |

Rejection means documentary non-conformance. It grants no executable-validation
or runtime authority.

## 7. Frozen PC-NGV non-triggering proof

No frozen shape is narrowed, dismissed, superseded, or declared inapplicable.
Each remains binding.

| Frozen vector | Direct conformance statement | Negative documentary vector |
| --- | --- | --- |
| `PC-NGV-01` | **Direct:** subject coherence remains a frozen semantic obligation under `WP4-NR-002` and frozen M42-WP7 §4.1. The opaque-byte container cannot independently verify semantic coherence across nested bytes. WP4 framing neither discharges nor weakens that obligation; a cross-subject claim is rejected at the Portfolio Composition conformance level. | `WP4-NV-PC-01` |
| `PC-NGV-02` | §§2 and 4.4 preserve exact ownership; association creates no Portfolio Intelligence ownership of Ledger or Provenance facts. | `WP4-NV-PC-02` |
| `PC-NGV-03` | `WP4-NR-014`, `-020`, and `-026` prohibit normalization and source-vocabulary substitution. | `WP4-NV-PC-03` |
| `PC-NGV-04` | `WP4-NR-015` and `-027` reject filled, defaulted, ambient, or inferred missing coordinates. | `WP4-NV-PC-04` |
| `PC-NGV-05` | The grammar carries coordinates only and admits no measure, calculation, rate, weight, or valuation field. | `WP4-NV-PC-05` |
| `PC-NGV-06` | No Membership, eligibility, permission, compatibility, or tradability result is admitted. | `WP4-NV-PC-06` |
| `PC-NGV-07` | No policy, leverage, cash-floor, allocation, or execution rule is admitted. | `WP4-NV-PC-07` |
| `PC-NGV-08` | Lifecycle bytes remain opaque and cannot authorize action, transition, or currentness. | `WP4-NV-PC-08` |
| `PC-NGV-09` | `WP4-NR-012` and `-013` preserve coordinate-specific supplied Provenance and prohibit generation, detachment, merging, reconstruction, or trust judgment. | `WP4-NV-PC-09` |
| `PC-NGV-10` | `WP4-NR-015` and `-016` make missingness and owner-defined affirmative absence non-colliding. | `WP4-NV-PC-10` |
| `PC-NGV-11` | **Direct:** the exact frozen shape is “A database, JSON, API, service, runtime object, byte encoding, or storage form is prescribed.” At Composition-specimen scope, frozen M44 Architecture §8.3 C3 prescribes nothing inside a Composition specimen. M44-WP4 instead defines a downstream canonical container-framing contract under `E-1` and `E-2`, including the bounded container byte encoding in §4. Frozen M43-WP3 §7.2 is precedent, not an authority grant. This contract prescribes no nested-coordinate byte encoding and no runtime, storage, API, JSON, database, service, persistence, executable, or implementation form. | `WP4-NV-PC-11` |
| `PC-NGV-12` | **Direct:** `WP4-NR-003`, `-004`, and `-009` require the producer to preserve the exact §5 semantic order and treat every source field as opaque rather than WP4-normalized. The parser assigns `F2` through `F8` by position and cannot detect an otherwise well-framed semantic payload misassignment; frozen subject-coherence and producer-conformance obligations remain binding. | `WP4-NV-PC-12` |
| `PC-NGV-13` | **Direct:** `WP4-NR-008` admits only raw `ASCII("M42-WP7-PORTFOLIO-COMPOSITION-1")` and rejects every alternate tag. | `WP4-NV-PC-13` |
| `PC-NGV-14` | **Direct:** `WP4-NR-010`, `-014`, `-015`, `-017`, `-028`, and `-032` prohibit WP4 from defining upstream encoding, fields, schema, identifiers, discriminator bytes, or missing nested forms, including for Portfolio Intelligence-owned frozen coordinates. | `WP4-NV-PC-14` |
| `PC-NGV-15` | The artifact class and authority block deny Ledger-truth, runtime-model, analytical-model, valuation-model, optimization-model, policy-engine, and recommendation-engine authority. | `WP4-NV-PC-15` |

## 8. M42-WP7 checklist conformance

| Checklist item | Direct proof | Negative documentary vector |
| --- | --- | --- |
| 10 | **Direct:** `WP4-NR-003`, `-004`, `-008`, and `-009` require a producer to emit the exact 31-octet tag first and the exact frozen ten-field semantic order. Parser-visible order defects are limited to malformed component structure and explicit `OA` or `PA` field-number sequence errors; opaque `F2`–`F8` semantic misassignment is not independently observable. | `WP4-NV-CL-10` |
| 11 | **Direct:** `WP4-NR-010`, `-014`, `-018`, and `-032` treat all source-owned nested bytes, including field 8, as opaque and prohibit reorder, normalization, encoding, reinterpretation, and own-domain amendment. | `WP4-NV-CL-11` |
| 12 | **Direct:** this contract discharges only the allocated container framing; both limbs of `E-1` and `WP4-NR-001`, `-002`, `-015`, `-017`, and `-032` preserve every remaining canonical-byte obligation without invention, removal, deferral, or weakening. | `WP4-NV-CL-12` |

The preservation specimen `WP4-PV-PR-01` and boundary specimen
`WP4-PV-ORD-01` directly check that the tag and ten-field sequence are
byte-order-identical to frozen M42-WP7 §5.

### 8.1 Additional RC4 conformance findings

| Finding | Direct proof | Negative documentary vector |
| --- | --- | --- |
| Own-domain nested-form scoping | `WP4-NR-032` resolves the frozen M44-WP1 §6.6 and M44 §17 `OQ-1` question in the negative directly from frozen M42-WP7 §5, §9 item 11, `PC-NGV-14`, and M44 `INV-C1`. Portfolio Intelligence meaning ownership does not become WP4 nested amendment authority. | `WP4-NV-PC-14`, `WP4-NV-AUTH-01` |
| Field 8 boundary | The frozen inventory supplies field 8 on both inventory axes and admits the semantic written values `active`, `archived`, and `closed`. It does not grant WP4 authority to choose their octet encoding. Under `WP4-NR-010`, `-014`, and `-018`, field 8 remains supplied and unrouted while its Ledger & Accounting-supplied canonical bytes remain opaque. | `WP4-NV-F08` |

## 9. Inherited M34-D-0010 matter

The inherited decision is `M34-D-0010 — Decompose the instrument-analysis
product contract`, recorded in the
[M34 decision register](m34/audit/registers/decision_register.md)
§`M34-D-0010`.
The only consequence relied upon is:

> “Every field preserves semantic owner, source and temporal provenance, and
> applicable degraded state.”

Frozen M44 Architecture §8.3 describes this input as “M34-D-0010 Provenance
association rules,” while the underlying decision has the different exact
title above. **WP4-NR-029 — Inherited characterization.** WP4 records that
inherited divergence and neither corrects nor recharacterizes it.

## 10. G-3 terminal determination

The binding frozen inventory is unchanged. `G-3` therefore has exactly one
terminal state:

**G-3 OPEN — PARTIAL**

The missing elements and routes are the eight rows in §3.3. In summary:

- Ledger & Accounting: Portfolio Identity reference form, Accounting Scope
  reference form, Portfolio Membership canonical representation, and the Base
  Currency coordinate form;
- Asset Foundation: Base Currency denomination identifier format and `asset_id`
  lexical form;
- Portfolio Intelligence under frozen M42-WP3 Stage B: Investment Universe
  nested form and order;
- Portfolio Intelligence under frozen M42-WP5: Benchmark declared-name form,
  form-discriminator representation, and Explicitly None representation; and
- Connectivity & Ingestion: canonical Provenance content representation,
  boundaries, supplied sequence, and completeness basis.

Field 8 is supplied and is not missing or routed. Its frozen inventory records
semantic written-value admission, not a WP4-selected octet encoding. Field 8 is
carried only as opaque Ledger & Accounting-supplied canonical bytes, and the
container neither inspects nor selects their internal encoding. For the
own-domain field-6 and field-7 gaps, `WP4-NR-032` controls: Portfolio
Intelligence ownership of meaning does not authorize WP4 to define, repair,
infer, or select the absent nested forms.

**WP4-NR-030 — Gate rule.** `CLOSED` is permitted only when reference exactness
and written-form determinacy are supplied at field and facet level for every
required owner-supplied canonical form. Routing is not supply. Artificial
specimens are not supply. Because the condition is not met, `CLOSED` is not
asserted.

**WP4-NR-031 — Partial consequence.** No complete conforming Portfolio
Composition bytes, concrete `PMS1` subject, or concrete `PAIM1` manifest are
claimed. `G-3 OPEN — PARTIAL` blocks M44-WP6 and M44-WP7 without exception
pending the independently confirmed M44 §12.1.1 checkpoint. WP4 does not
declare that checkpoint outcome. WP4 may complete while `G-3` remains
`OPEN — PARTIAL`.

The exact inherited gate and consequence are recorded at
[M44-WP1 Inherited Gate Inventory and Closure Register](M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md)
§4.3.

## 11. Documentary coverage ledger

Vectors derive from the normative rows above. No normative row derives from a
fixture.

| Normative row | Positive or boundary coverage | Negative coverage |
| --- | --- | --- |
| `WP4-NR-001` | `WP4-PV-AUTH-01` | `WP4-NV-AUTH-01`, `WP4-NV-PC-14` |
| `WP4-NR-002` | `WP4-PV-AUTH-01` | `WP4-NV-PC-02`, `WP4-NV-PC-15` |
| `WP4-NR-003` | `WP4-PV-PR-01`, `WP4-PV-F01`–`WP4-PV-F10` | `WP4-NV-PC-02`, `WP4-NV-PC-12` |
| `WP4-NR-004` | `WP4-PV-PR-01`, `WP4-PV-ORD-01` | `WP4-NV-CL-10` |
| `WP4-NR-005` | `WP4-PV-INV-01` | `WP4-NV-INV-01`, `WP4-NV-G3-01` |
| `WP4-NR-006` | `WP4-PV-U32-00`–`WP4-PV-U32-06` | `WP4-NV-NUM-01`, `WP4-NV-PC-11` |
| `WP4-NR-007` | `WP4-PV-LP-00`–`WP4-PV-LP-06` | `WP4-NV-LEN-01`, `WP4-NV-TRAIL-01` |
| `WP4-NR-008` | `WP4-PV-PR-01` | `WP4-NV-TAG-01`, `WP4-NV-PC-13`, `WP4-NV-CL-10` |
| `WP4-NR-009` | `WP4-PV-ORD-01`, `WP4-PV-PERM-01` | `WP4-NV-ORDER-01`, `WP4-NV-PC-12` |
| `WP4-NR-010` | `WP4-PV-F02`–`WP4-PV-F08` | `WP4-NV-OWNER-01`, `WP4-NV-PC-14` |
| `WP4-NR-011` | `WP4-PV-OA-01` | `WP4-NV-DUP-OA-01`, `WP4-NV-PC-02` |
| `WP4-NR-012` | `WP4-PV-PA-01` | `WP4-NV-DUP-PA-01`, `WP4-NV-PC-09` |
| `WP4-NR-013` | `WP4-PV-PA-01` | `WP4-NV-PC-09`, `WP4-NV-PC-15` |
| `WP4-NR-014` | `WP4-PV-OPAQUE-01` | `WP4-NV-UNICODE-01`, `WP4-NV-PRESENT-01`, `WP4-NV-CL-11` |
| `WP4-NR-015` | `WP4-PV-ABS-01` | `WP4-NV-MISSING-01`, `WP4-NV-PC-04` |
| `WP4-NR-016` | `WP4-PV-ABS-01` | `WP4-NV-ABS-01`, `WP4-NV-PC-10` |
| `WP4-NR-017` | `WP4-PV-F07` | `WP4-NV-BENCH-01`, `WP4-NV-PRESENT-01` |
| `WP4-NR-018` | `WP4-PV-RT-01` | `WP4-NV-UNKNOWN-01`, `WP4-NV-TRAIL-01` |
| `WP4-NR-019` | `WP4-PV-RT-01` | `WP4-NV-LEN-01`, `WP4-NV-DUP-KEY-01` |
| `WP4-NR-020` | `WP4-PV-PERM-01` | `WP4-NV-UNICODE-01`, `WP4-NV-NUM-01` |
| `WP4-NR-021` | `WP4-PV-RT-01` | `WP4-NV-UNKNOWN-01` |
| `WP4-NR-022` | `WP4-PV-PR-01`, `WP4-PV-ORD-01` | `WP4-NV-TAG-01`, `WP4-NV-ORDER-01` |
| `WP4-NR-023` | `WP4-PV-OA-01`, `WP4-PV-PA-01` | `WP4-NV-DUP-KEY-01`, `WP4-NV-DUP-OA-01`, `WP4-NV-DUP-PA-01` |
| `WP4-NR-024` | `WP4-PV-U32-00`–`WP4-PV-U32-06` | `WP4-NV-NUM-01`, `WP4-NV-LEN-01` |
| `WP4-NR-025` | `WP4-PV-RT-01` | `WP4-NV-TRAIL-01` |
| `WP4-NR-026` | `WP4-PV-OPAQUE-01`, `WP4-PV-PERM-01` | `WP4-NV-UNICODE-01`, `WP4-NV-PC-03` |
| `WP4-NR-027` | `WP4-PV-ABS-01` | `WP4-NV-MISSING-01`, `WP4-NV-ABS-01` |
| `WP4-NR-028` | `WP4-PV-OPAQUE-01` | `WP4-NV-PRESENT-01`, `WP4-NV-INVENT-01` |
| `WP4-NR-029` | `WP4-PV-M34-01` | `WP4-NV-M34-01` |
| `WP4-NR-030` | `WP4-PV-INV-01` | `WP4-NV-G3-01`, `WP4-NV-INCOMPLETE-01` |
| `WP4-NR-031` | `WP4-PV-INV-01` | `WP4-NV-DOWNSTREAM-01`, `WP4-NV-INCOMPLETE-01` |
| `WP4-NR-032` | `WP4-PV-AUTH-01`, `WP4-PV-INV-01` | `WP4-NV-AUTH-01`, `WP4-NV-PC-14`, `WP4-NV-CL-12` |

`WP4-PV-F01` through `WP4-PV-F10` provide per-field documentary coverage.
`WP4-NV-F01` through `WP4-NV-F10` provide the corresponding per-field negative
coverage. The complete vector definitions are in:

- [M44-WP4 Positive Documentary Vectors](m44/fixtures/M44_WP4_POSITIVE_DOCUMENTARY_VECTORS.md); and
- [M44-WP4 Negative Documentary Vectors](m44/fixtures/M44_WP4_NEGATIVE_DOCUMENTARY_VECTORS.md).

## 12. Review, confirmation, and freeze boundary

This RC4 contract and its two documentary fixture artifacts preserve the
approved RC3 constitutional contract review result. The RC4 corrections are
limited to serialization observability and reproducible documentary byte
proofs, do not change a constitutional statement or authority boundary, and
require renewed independent serialization review. Constitutional re-review is
not required for this correction. Any later correction that changes a
constitutional statement or authority boundary requires review by the
constitutional discipline.

The later
`docs/implementation/M44_WP4_INDEPENDENT_CONSTITUTIONAL_CONFIRMATION.md` is the
frozen M44 Architecture §12.5 point-4 M44-WP4 confirmation. It has not been
issued. The architecture-stage confirmation is planning-lifecycle evidence
only and does not substitute for it.

This contract does not confirm, freeze, or close M44-WP4; authorize the
§12.1.1 checkpoint; authorize M44-WP6 or M44-WP7; or claim capability
completion.
