# BANPU-WP4 — Provider-Identity Governance Decision

**Artifact class:** Additive bounded constitutional governance decision record
**Decision date:** 2026-08-13
**Issuing authority:** BANPU-WP4 Bounded Provider-Identity Governance Decision Authority
**Question resolved:** minimum constitutionally valid treatment of `conversion_payload.quote_binding.provider`
**Governance outcome:** `OUTCOME 1 — EXISTING AUTHORITY SUFFICIENT`
**Selected alternative:** none of A, C, D, or E; the existing frozen rule already determines the treatment
**Registry/schema/model extension authorized:** `NONE`
**Implementation performed:** `NO`
**Implementation review or confirmation performed:** `NO`
**Freeze, closeout, release, deployment, production execution, WP5+, or M46 authority:** `NONE`

---

## 1. Nature and boundary of this act

This act determines the minimum constitutionally valid canonical treatment of the
single payload field `conversion_payload.quote_binding.provider`. It exists
because the BANPU-WP4 bounded implementation correction reached an
authority/data-model boundary: the second-renewed Independent Implementation
Review requires "every authoritative provider identifier" to be assembled from
registry state, and the Asset Registry appears to carry provider-**symbol**
identity without carrying a per-asset quote-**provider** name.

This record is additive. It modifies no frozen artifact, no Work Package Plan,
no retry-order amendment, no Allocation Record, no Implementation Authorization
Record, no implementation or test byte, no Decision Log entry, and no
Implementation INDEX entry. It performs no Independent Review, Confirmation,
freeze, closeout, release, deployment, WP5+, or M46 work, and it stages,
commits, pushes, and merges nothing.

The bounded correction report was not accepted as proof. Every finding in §4 was
established from live repository bytes read during this act.

## 2. Authority identities verified from live repository bytes

All identities below were recomputed from the working tree at the start of this
act. The expected second-renewed review identity was supplied to this authority
and is confirmed exact.

| Artifact | Raw SHA-256 | Bytes | Result |
|---|---|---|---|
| [Original Work Package Plan](BANPU_WP4_WORK_PACKAGE_PLAN.md) | `F76DCF7867AB4D0D11774BF4343D43076DFE22A7C5CA12656959CBC137F2DCBE` | 30,266 | `EXACT` |
| [Retry-order Plan amendment](BANPU_WP4_RETRY_ORDER_WORK_PACKAGE_PLAN_AMENDMENT.md) | `52254EB873CB57A5B3C30E62897878CAC20A23DCEDC2AAF2E5EB969D5C1C4168` | 18,701 | `EXACT` |
| [Plan-amendment independent reapproval](BANPU_WP4_RETRY_ORDER_WORK_PACKAGE_PLAN_AMENDMENT_INDEPENDENT_REAPPROVAL.md) | `2258C1C3F40714FD371121645C3DECB2CA72946E825D816B789B586C2A5BFBF1` | 17,620 | `EXACT` |
| [Retry-order governance decision](BANPU_WP4_RETRY_ORDER_GOVERNANCE_DECISION.md) | `C82D4B31D8E32EAA9CFF16C3EA93DC29CF7A8C5C7AF5DF043F5141B16C623DAB` | 20,350 | `EXACT` |
| [Amendment binding/freeze record](BANPU_WP4_RETRY_ORDER_AMENDMENT_BINDING_FREEZE_RECORD.md) | `5E312392767737C8F0445F51182B32A87B2EDF42B4C886BFB0296164EE389669` | 17,306 | `EXACT` |
| [Amendment confirmation](BANPU_WP4_RETRY_ORDER_AMENDMENT_CONFIRMATION.md) | `41E1A23C5C09D095686E5675A37CF5DC191802060DC9BB104A99D2EEC2574BC8` | 17,832 | `EXACT` |
| [Amendment independent review](BANPU_WP4_RETRY_ORDER_AMENDMENT_INDEPENDENT_REVIEW.md) | `54C3CAC4DD263CEABA1ED70211529C56839A3C27D4A054A964DD3C68135463B4` | 22,686 | `EXACT` |
| [Allocation Record](BANPU_WP4_ALLOCATION_RECORD.md) | `CEE6F01C4113697BE6485AE56BB80FE0E9E99CB8555C08BC5D3E3CD67B94BAA9` | 11,180 | `EXACT` |
| [Implementation Authorization](BANPU_WP4_IMPLEMENTATION_AUTHORIZATION_RECORD.md) | `D8E89048BDC3B939731523937C8122A25E9659EDD5CE5B28F48DEAD022A6BCFA` | 17,221 | `EXACT` |
| [Original Independent Implementation Review](BANPU_WP4_INDEPENDENT_IMPLEMENTATION_REVIEW.md) | `D1033DC13E8BF6D0F7AEA39AFFC4EE660FC962AE24A9B6D96521B1FA0CB91450` | 21,397 | `EXACT` |
| [Renewed Independent Implementation Review](BANPU_WP4_RENEWED_INDEPENDENT_IMPLEMENTATION_REVIEW.md) | `AD6017FFCFA4CC0D23BBFDA51B0F387C8E4CA0351BECE47CF96FC216F42845F3` | 19,890 | `EXACT` |
| [Second Renewed Independent Implementation Review](BANPU_WP4_SECOND_RENEWED_INDEPENDENT_IMPLEMENTATION_REVIEW.md) | `994512F5E0C859C1E7406753C4B91A2DC92150D3745309B305A9E2791387DC3A` | 19,188 | `EXACT — MATCHES EXPECTED` |
| [Roadmap §1 reviewer confirmation](BANPU_WP4_ROADMAP_SECTION_1_REVIEWER_CONFIRMATION.md) | `361492715FCB70E4B7AFD8F2905BA83A37795AFFDA666828F7767890FB6885EB` | 14,303 | `EXACT` |
| [Historical canonical Design](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md) | `2D2ECE4391961C85DE4076091662C66DA4586C553C6CDD57094970168BF1CE76` | 28,653 | `EXACT` |

## 3. Exact constitutional question

The frozen corpus states, in three separate loci:

> Symbols and provider identifiers are registry-resolved, never trusted from
> arbitrary input strings.

— [Work Package Plan](BANPU_WP4_WORK_PACKAGE_PLAN.md) §1.2; substantively
identical text in [Implementation Authorization](BANPU_WP4_IMPLEMENTATION_AUTHORIZATION_RECORD.md)
§3 and in the historical Design §9.

The exact question is:

**Does that phrase require `conversion_payload.quote_binding.provider` — the
quote-provider/backend name — itself to be registry-resolved, or does it govern
provider _symbols/identifiers_ (the registry's `PROVIDER_SYMBOL` evidence
records) rather than provider implementation/backend selection?**

A subordinate question follows: if registry resolution is not required, what
canonical rule, if any, constrains the value, and does anything within WP4's
existing authority need to enforce it?

## 4. Current data-model findings

These are findings of fact from live repository bytes, independent of the
bounded correction report.

### 4.1 The registry stores no per-asset quote-provider name

`backend/models/asset.py` defines exactly four tables. `AssetIdentifier` carries
`asset_id`, `identifier_type`, `value`, `source`, `is_current`, `as_of`,
`created_at`. `Asset` carries `canonical_symbol`, `asset_type`, `market`,
`exchange`, `currency`, `status`, `display_symbol`, and four universal
tradability fields. `AssetRelationship` and `AssetClassification` carry no
provider field.

A repository-wide search of `backend/models/` for `provider` returns exactly two
unrelated classes of hit: the `ai_provider` columns on the AI-run tables and the
`provider` column on `UserUsage` (an LLM billing table). **No table anywhere in
the persistence layer carries a per-asset market-data provider name.**

### 4.2 `PROVIDER_SYMBOL` — exact meaning

`PROVIDER_SYMBOL` is a member of the closed `IdentifierType` enum in
`backend/services/asset_domain.py`, documented there as one of the
"evidence-tier identifier schemes … a small, closed set of real-world standards".
It names the **scheme** of an identifier row, alongside `ISIN`, `CUSIP`,
`SEDOL`, `FIGI`, and `BROKER_CODE`.

The identifier's `value` is the vendor's own spelling of the instrument's
ticker — `backend/services/provider_domain.py` calls `provider_symbol` "the
vendor's own spelling — evidence, never identity".

`PROVIDER_SYMBOL` therefore denotes **a symbol under a provider's naming
scheme**. It does not name a provider, and it carries no field that could.

### 4.3 `AssetIdentifier.source` — exact meaning, and why it is not provider identity

`source` is a free-form, caller-supplied, unconstrained `String` column. It is
required at every construction site but is governed by no enum, no closed set,
and no validation. The values actually written by production code are:

| Producer | `source` value |
|---|---|
| `services/registry_lookup.py` | `"registry_lookup"` |
| `services/ledger_evidence_builder.py` | `"ledger:historical"` |
| `services/identity_resolver.py` | `"resolution_adjudication"` |
| `services/asset_search/merge.py` | `f"discovery:{provider_name or 'unknown'}"` |
| `services/provider_adapter.py` | `f"provider:{provider_name}"` |
| `services/asset_registry.py` (`prepare_position_conversion_registry`) | caller-supplied keyword, no default, no vocabulary |
| existing test corpus | `"manual"`, `"yfinance"`, `"banpu-wp4"`, `"test"` |

`source` answers **who asserted this identifier**, not **which quote provider
serves this asset**. Three of the six production producers write a value that
contains no provider name at all, and the WP4 registry-preparation path takes it
verbatim from its caller.

This reading is not an inference. It is stated normatively by an existing frozen
repository specification, `docs/implementation/M39_WP1_Canonical_Boundary_Specification.md`
§9.1 ("Status: Canonical and frozen"):

> The Registry source namespace `yfinance` identifies the custody namespace of
> the required `PROVIDER_SYMBOL` record. It does not select a runtime provider
> and MUST NOT be interpreted as equivalent to `PRICE_PROVIDER=yfinance`.
>
> The normalized provider path, `PRICE_PROVIDER` selection, and Registry source
> namespace are distinct concepts. None SHALL be treated as an alias for another.

**`AssetIdentifier.source` is therefore expressly prohibited from being equated
with provider identity.**

### 4.4 A provider-selection mechanism exists, but it is runtime configuration

`backend/services/market_data/provider.py` exposes `get_provider(name=None)`,
which reads the `PRICE_PROVIDER` environment variable (default `"yahoo"`,
present in `backend/.env`) and returns `YahooChartProvider` or the legacy
`YahooFinanceProvider`. The `MarketDataProvider` ABC in `base.py` declares **no**
provider-identity attribute; the identity string lives as the private module
constant `_PROVIDER_ID = "yahoo_chart"` in `yahoo_chart.py`, and there is no
accessor for it.

M39-WP1 §9.1 classifies this mechanism as "Provider selection authority:
Server-owned; not client-selectable", and states that the same specification
"creates no … provider-routing authority". It is a **per-request runtime
deployment fact**, evaluated freshly on every call and mutable by environment
change.

### 4.5 `quote_binding.provider` — exact meaning and live consumers

The frozen WP1 canonicalizer (`services/transaction_canonicalizer.py`) parses
`quote_binding` into `PositionConversionQuoteBinding(provider,
predecessor_provider_symbol, successor_provider_symbol)`. The only constraint
imposed on `provider` is `reader.string(...)`: it must be present, a `str`, and
non-empty after stripping. The only cross-field invariant enforced anywhere is
`quote_binding.successor_provider_symbol == successor.provider_symbol`. All
three fields participate in the canonical payload fingerprint.

The field is **live and load-bearing**, not decorative. The frozen WP3 contract
`services/market_data/position_conversion_quote_contract.py`:

- maps it into `SuccessorQuoteBinding.provider` via
  `build_successor_quote_binding()` (IO-2);
- requires it non-empty in `check_missing_or_ambiguous_identifier()`, else
  `MISSING_OR_AMBIGUOUS_IDENTIFIER` quarantine;
- compares it against a caller-supplied `request_provider` in
  `evaluate_request_identity()`; and
- compares it against the runtime provider evidence's own `provider` attribute
  in `check_provider_symbol_mismatch()` — a mismatch yields
  `PROVIDER_SYMBOL_MISMATCH` quarantine.

`services/data_fetcher.py` consumes both entry points on the live quote/history
path. The runtime evidence value on the default path is `_PROVIDER_ID`, i.e.
`"yahoo_chart"`.

The historical Design confirms the two concepts are distinct coordinates, not
synonyms, in its own binding tuple:

```text
asset_id + provider + provider_symbol + quote_epoch_start_date + valuation_transition_date
```

### 4.6 No closed provider set exists in frozen authority

The literal `"YAHOO"` appears **exactly once** in the entire BANPU corpus:
Design line 167, inside the illustrative payload JSON, alongside equally
illustrative literals (`27`, `123`, `"BANPUU.BK"`, `"0.38242"`). The frozen and
existing test corpora use three mutually incompatible values:

| Surface | `quote_binding.provider` value |
|---|---|
| Historical Design payload illustration | `"YAHOO"` |
| WP1 canonicalizer vectors, WP2 replay/rebuilder/validator vectors, repair-consistency vectors | `"test-provider"` |
| Frozen WP3 quote-contract and quote-epoch-isolation vectors | `"yahoo_chart"` |
| WP4 candidate live-conversion module | `"YAHOO"` |

No canonical artifact enumerates an allowed set, and no code path validates
against one.

## 5. Determination of the constitutional question

**The frozen corpus does not require `quote_binding.provider` to be
registry-resolved. The phrase governs provider symbols/identifiers, not
provider implementation/backend selection.**

The determination rests on the frozen text read against the registry's own
vocabulary, not on implementation convenience:

1. **"Provider identifier" is a named registry object.** Every frozen locus
   pairs the phrase with operations that exist only on `AssetIdentifier` rows:
   the Roadmap §6 and Design Principle 7 speak of the **"current** provider
   identifier"; the Implementation Authorization §3 requires registry
   preparation to "establish the current successor `PROVIDER_SYMBOL`" and
   "retire the predecessor identifier". `is_current` and retirement are
   properties of `AssetIdentifier`; `PROVIDER_SYMBOL` is a member of the closed
   `IdentifierType` enum. A provider **name** has no `is_current` and cannot be
   retired. The registry contains exactly one object called a provider
   identifier, and it is the `PROVIDER_SYMBOL` record.

2. **The Design itself separates the two.** Its market-data binding tuple lists
   `provider` and `provider_symbol` as distinct coordinates (§4.5 above). The
   payload schema likewise names one `provider` and two `*_provider_symbol`
   fields. Only the latter two are identifiers in the registry's sense.

3. **The Plan's own step E4 expressly contemplates non-registry payload
   content.** Plan §3.2 E4 reads: "Resolve conversion inputs: symbols and
   provider identifiers from the registry; **decimals from the caller's typed
   facts**; `transaction_date` constructed solely from the payload's …
   `valuation_transition_date`". The registry-resolution clause is therefore an
   enumeration of *which* payload elements the registry owns, not a claim that
   the registry owns the whole payload.

4. **The broad reading is impossible, not merely inconvenient.** Under a reading
   in which "provider identifiers" includes the provider name, WP4 could not
   comply at all: the registry holds no such fact (§4.1), and the
   Implementation Authorization §11 grants "`NO` schema or migration authority
   and `NO` authority to modify `backend/models/asset.py`". A reading that makes
   a mandatory authorized capability unsatisfiable inside its own authorized
   surface, when a narrower reading matches the registry's actual vocabulary, is
   the wrong reading.

This determination is deliberately **not** the implementer-friendly one in the
respect that matters: it forecloses the "add a provider column" path
(Alternative A), forecloses a hard-coded constant (Alternative E), and grants no
new authority of any kind.

## 6. Alternatives evaluated

### 6.1 Alternative A — Registry extension

**Rejected.**

Adding canonical quote-provider identity to the Asset Registry would:

- **change Asset Registry constitutional scope.** The registry's documented
  purpose is permanent identity plus dated, provenance-tagged evidence. A
  runtime provider-routing fact is neither: it is server-owned deployment
  configuration (§4.4), and M39-WP1 §1 expressly states that using Registry
  identity to derive a provider request "creates no … provider-routing
  authority". Storing provider selection *in* the registry would convert the
  registry into a routing authority.
- **require schema/model/migration authority.** A new column or a new
  `IdentifierType` member both touch `backend/models/asset.py` and require an
  Alembic migration.
- **exceed WP4 Authorization.** Authorization §11 denies schema/migration
  authority and denies modification of `backend/models/asset.py` by name. Plan
  §1.3 and §2.4 restate the exclusion. It is not curable by interpretation.
- **not belong in WP4.** WP4's canonical purpose is "the only authorized atomic
  write path after safe replay and quote binding exist" — not registry
  capability expansion.
- **require, if pursued, a full chain:** canonical Design amendment (payload and
  §10 market-data protection), Roadmap/package-inventory amendment assigning the
  capability to a package, a distinct Allocation Record, a distinct
  Implementation Authorization granting schema/model/migration authority,
  Work Package Plan and independent reapproval, plus migration of every existing
  registry row.

It would also break frozen WP1/WP2/WP3 vectors, which carry three mutually
incompatible provider values (§4.6).

### 6.2 Alternative B — existing registry semantics already determine it

**Rejected — refuted by evidence.**

No existing registry fact canonically determines a provider name.

`AssetIdentifier.source` is the only candidate and it is **not** provider
identity: it is an unconstrained, caller-supplied provenance/custody tag whose
live production values are `"registry_lookup"`, `"ledger:historical"`,
`"resolution_adjudication"`, `"discovery:<x>"`, and `"provider:<x>"` (§4.3).
Equating it with provider identity is expressly prohibited by the frozen
M39-WP1 §9.1 non-aliasing rule.

Critically, `prepare_position_conversion_registry()` takes `source` verbatim from
its caller with no default and no vocabulary. Deriving `quote_binding.provider`
from it would **relocate** arbitrary caller control rather than eliminate it,
failing the first decision criterion outright.

`Asset.market` / `Asset.exchange` are venue facts, not provider facts, and no
mapping from venue to provider exists anywhere in the repository.

### 6.3 Alternative C — canonical platform/provider policy

**Rejected.**

An authoritative provider-selection mechanism *does* exist —
`get_provider()` / `PRICE_PROVIDER`, described by M39-WP1 §9.1 as "Server-owned;
not client-selectable" with normalized path `yahoo_chart`. This authority is
recorded here as a genuine repository fact, and it is what distinguishes
Alternative C from hard-coding.

It is nevertheless not usable as the canonical authority for this field:

1. **It destroys replay determinism and live/replay equality.** The value is
   persisted inside an immutable, append-only, fully fingerprinted
   `conversion_payload`. Deriving it at canonicalization time from a mutable
   environment variable would make a canonical fingerprint a function of
   deployment configuration: the same authored conversion would fingerprint
   differently on a host with `PRICE_PROVIDER=yfinance`, and a replay on such a
   host would not reproduce the live outcome. That directly violates two
   mandatory decision criteria and the frozen EQ-1 obligation.
2. **It is per-request, not per-conversion.** M39-WP1 §9.1 evaluates the
   effective provider freshly on every request and classifies the source
   `UNSUPPORTED` when it is not the expected path. A historical conversion fact
   cannot be a function of a value defined only at request time.
3. **No accessor exists.** `MarketDataProvider` declares no provider-identity
   member; `_PROVIDER_ID` is a private constant with no public path. Reaching it
   would be a new dependency from `portfolio_transactions.py` into the
   market-data layer, and is not among the authorized capabilities C-1…C-13.
4. **M39-WP1 is not BANPU authority.** It belongs to a separate milestone
   stream and expressly creates no provider-routing authority for others. WP4
   may cite it as evidence of repository semantics (as this record does) but may
   not adopt it as its own canonical rule without a governance act.

The distinction the task requires is therefore recorded explicitly: hard-coding
`"YAHOO"` to make tests pass would be **inventing a fact** (§4.6 shows the
literal is illustrative and would in fact quarantine under frozen WP3);
deriving from `PRICE_PROVIDER` would be **reading a real authority of the wrong
shape**. Both are rejected, for different reasons.

### 6.4 Alternative D — remove provider from canonical identity

**Rejected — and it is expressly excluded by the task's own condition.**

`quote_binding.provider` is not informational metadata. It is a live comparison
coordinate consumed by frozen WP3 (§4.5): `check_provider_symbol_mismatch()`
quarantines the successor holding when it disagrees with runtime provider
evidence, and `check_missing_or_ambiguous_identifier()` quarantines when it is
empty. Removing or de-identifying it would:

- **change the frozen canonical payload schema.** `provider` is a required
  member of the frozen WP1 `quote_binding` object and of
  `PositionConversionQuoteBinding`.
- **silently change an established fingerprint contract.** Every existing
  fingerprint over every existing vector would change value. The task forbids
  selecting this alternative on exactly that ground.
- **break replay determinism and retry identity.** Stored payloads would no
  longer regenerate their recorded fingerprints, invalidating the `E8-R`
  stored-payload regeneration required by the reapproved amendment §3.2.
- **destroy provider evidence.** Design §10 requires the converted holding's
  binding to carry a provider; WP3's IO-2 binding would lose a mandatory field.
- **break frozen WP1/WP2/WP3 behavior**, including the WP3 quarantine
  enumeration and the WP2 replay/validator/rebuilder vectors.

Provider-symbol binding would survive, but at the cost of every other
constraint. Rejected without qualification.

### 6.5 Alternative E — closed-set canonical value

**Rejected — refuted by evidence.**

Frozen authority defines no single allowed provider value and no closed provider
set. §4.6 records three mutually incompatible values across the frozen surfaces,
and the sole `"YAHOO"` occurrence is an illustration inside a schema example
whose sibling literals are equally illustrative. Notably, `"YAHOO"` would itself
**fail** frozen WP3's `check_provider_symbol_mismatch()` against the live
`"yahoo_chart"` evidence identity — the Design illustration is not a working
value.

A newly invented constant or enum is expressly insufficient, and the Work
Package Plan preamble forbids this lineage of artifacts from creating "any new
gate, new acceptance criterion, or new capability".

## 7. Selected outcome

**`OUTCOME 1 — EXISTING AUTHORITY SUFFICIENT`**

Existing frozen and authorized semantics already determine the canonical
treatment of `conversion_payload.quote_binding.provider`. No amendment, no
registry extension, no schema/model/migration authority, and no
Allocation/Authorization expansion is required.

## 8. The canonical provider-authority rule

The following rule is a reading of existing frozen authority, recorded for
reviewer inspection. It creates nothing and is subordinate to the frozen corpus;
where it and the frozen corpus differ, the frozen corpus governs and this record
is in error.

**Rule PIA-1 — scope of registry resolution.**
The frozen requirement that "symbols and provider identifiers are
registry-resolved, never trusted from arbitrary input strings" governs exactly
these payload members:

| Payload member | Registry authority |
|---|---|
| `predecessor.symbol` | predecessor `Asset` listing symbol |
| `successor.symbol` | successor `Asset` listing symbol |
| `successor.provider_symbol` | successor's current `PROVIDER_SYMBOL` `AssetIdentifier` value |
| `quote_binding.successor_provider_symbol` | same, via the frozen canonicalizer invariant `== successor.provider_symbol` |
| `quote_binding.predecessor_provider_symbol` | predecessor's most-recent `PROVIDER_SYMBOL` `AssetIdentifier` value, readable after E0 retirement because historical mappings are retained forever |

**Rule PIA-2 — `quote_binding.provider` is not registry-resolved.**
`quote_binding.provider` names the market-data provider/backend, not a registry
identifier. The Asset Registry holds no such fact, is not a provider-routing
authority, and is not required by any frozen artifact to hold one. WP4 must not
registry-resolve it, must not derive it from `AssetIdentifier.source`, must not
derive it from `PRICE_PROVIDER` or any environment/configuration read, and must
not normalize it against an invented constant or set.

**Rule PIA-3 — the governing authority is the frozen WP1 payload contract.**
The complete canonical constraint on the value is the one the frozen
canonicalizer already enforces: present, a string, non-empty after stripping,
and fully participating in the sole canonical payload fingerprint. It is an
operator-authored evidence value of the same class as `evidence.reference`,
`evidence.source`, `evidence.captured_at`, and
`boundary_evidence.suspension_gap_annotation` — all of which are authored, all
of which are fingerprinted, and none of which are registry-resolved.

**Rule PIA-4 — authored payload semantics are not caller-controlled *identity*.**
The canonical conversion identity is `POSITION_CONVERSION` + portfolio ID +
predecessor asset ID + canonical transition date (retry-order Governance
Decision §6.1 item 9). Every component is registry-resolved or payload-calendar
derived; none is arbitrary caller text. The **fingerprint** is a separate,
whole-payload digest whose sensitivity to authored semantics is the frozen
design: retry-order Governance Decision §7.3 states that "a different … evidence
value, or any other fingerprinted payload semantic … cannot be accepted as
`already_applied` even though the top-level conversion identity key matches".
A changed `provider` producing a controlled conflict at the same identity is
therefore **conformant fail-closed behavior, not a defect**.

## 9. Consequences

### 9.1 Fingerprint and retry consequences

None. Nothing changes. Canonical fingerprints remain deterministic, replay and
live outcomes remain equal, stored-payload fingerprint regeneration at `E8-R`
remains valid, and the WP1 partial unique index remains the concurrency
backstop. Every alternative that would have changed a fingerprint was rejected
on that ground.

### 9.2 Registry-authoritative provider symbols

Preserved and unaffected. PIA-1 leaves the registry as the sole authority for
all five symbol members, including on the existing-row revalidation path.

### 9.3 Required amendment / scope surface

`NONE`. No Design amendment, no Plan amendment, no Roadmap or Sequence
amendment, no new capability, no new file surface, no schema, no model, no
migration, no index, no endpoint, no CLI, no frontend path.

### 9.4 Allocation and Authorization effect

`NONE`. The [Allocation Record](BANPU_WP4_ALLOCATION_RECORD.md) and
[Implementation Authorization Record](BANPU_WP4_IMPLEMENTATION_AUTHORIZATION_RECORD.md)
remain valid, unchanged, and exactly as identified in §2. Capabilities C-1…C-13,
the §2.1 production surface, the §2.2 test surface, the §2.3 conditional
surface, and every §8 prohibition are untouched. No synchronization is required.

### 9.5 Carried observation — provider value versus runtime provider evidence

Recorded, referred out, and **gating nothing in WP4**.

A `quote_binding.provider` value that does not equal the effective runtime
provider evidence identity causes frozen WP3
`check_provider_symbol_mismatch()` to quarantine the converted successor
holding. On the current default path that identity is `"yahoo_chart"`; the
Design's illustrative `"YAHOO"` and the WP4 candidate module's `"YAHOO"` would
not match it.

This is a quote-admissibility concern owned by the market-data protection
contract, not a WP4 registry-state or write-path concern. WP4's E3 obligation is
registry state; Plan §1.3 excludes reader/accounting and snapshot behavior as
WP5/WP6 ownership; WP3 is confirmed, frozen, and closed. No WP4 acceptance
criterion in Plan §9 or amendment §5 depends on its disposition.

It is therefore referred to the authority governing the canonical design,
roadmap, and package inventory — the same treatment the corpus already applies
to the WP3 PD-3 emitter-locus item. This record neither resolves it, waives it,
assigns it a package, nor creates an obligation from it.

## 10. Effect on the current candidate and on the review findings

This act approves **no** implementation change. Every candidate correction
retains exactly the status it held on entry.

| Item | Status preserved |
|---|---|
| B1 numeric tolerance correction | `CANDIDATE CORRECTION ONLY — NOT INDEPENDENTLY CONFIRMED` |
| B2 predecessor provider-symbol correction | `CANDIDATE CORRECTION ONLY — NOT INDEPENDENTLY CONFIRMED` |
| B3 | `PREVIOUSLY RESOLVED` |
| B4 | `PREVIOUSLY RESOLVED` |
| B5 persisted-payload E13 correction | `CANDIDATE CORRECTION ONLY — NOT INDEPENDENTLY CONFIRMED` |
| B6 EQ-1 correction | `CANDIDATE CORRECTION ONLY — NOT INDEPENDENTLY CONFIRMED` |
| MINOR-1 | `PREVIOUSLY SATISFIED` |
| NEW-MINOR-A | `PREVIOUSLY SATISFIED` |

### 10.1 Effect on `WP4-IIR-B2`

B2 remains `PARTIALLY RESOLVED — BLOCKING` as recorded by the second-renewed
review. This act does not advance, close, or confirm it.

What this act supplies is the **bound** of B2's registry-resolution obligation:
under PIA-1 and PIA-2, B2 requires registry resolution of the five symbol
members and does **not** extend to `quote_binding.provider`. The next
Independent Implementation Reviewer applies that bound to the candidate; this
authority does not, and expressly performs no part of that review.

### 10.2 Effect on RTO-1, RTO-5, RTO-7, RTO-8, RTO-9

All five remain `PARTIAL — BLOCKING` exactly as recorded. Their determinations
each rest on two distinct grounds: a numeric-tolerance ground and a
provider-identity ground.

Under PIA-2 and PIA-4, the provider-identity ground is now bound: a stored
payload's `quote_binding.provider` is canonically valid when it satisfies the
frozen WP1 contract (PIA-3), and a differing value at the same canonical
identity is a controlled conflict rather than an unauthorized disposition. The
provider-**symbol** members remain subject to full registry revalidation before
any retry disposition, unchanged.

Whether each row is satisfied on that ground, and on the independent
numeric-tolerance ground, is for the renewed Independent Implementation Review
to determine against the corrected candidate and a complete evidence matrix.
This record makes no such determination.

### 10.3 Implementation reliance status

`IMPLEMENTATION MAY RELY ON RULES PIA-1 THROUGH PIA-4 AS A READING OF EXISTING
FROZEN AUTHORITY.`

Because this is `OUTCOME 1`, no successor approval, confirmation, binding, or
Plan reapproval chain is interposed: the rules restate authority that is already
frozen, authorized, and operative. Reliance is limited strictly to the bound of
the registry-resolution obligation. It creates no permission to skip any other
gate, to treat any B-finding as resolved, or to enter review.

The candidate remains **not ready for renewed Independent Implementation
Review** until the remaining bounded corrections are complete and a full
evidence matrix exists.

## 11. Preserved prohibitions

This act does not permit:

- any registry, schema, model, migration, or index change;
- any new `IdentifierType`, `RelationshipType`, or registry column;
- registry resolution, `AssetIdentifier.source` derivation, environment or
  configuration derivation, or invented-constant normalization for
  `quote_binding.provider`;
- removal of `provider` from the canonical payload or from the fingerprint;
- any change to the sole canonical fingerprint algorithm or to any frozen
  vector's expected value;
- any change to WP1, WP2, or WP3 frozen behavior;
- any endpoint, CLI, frontend, `LedgerRepair`, snapshot, replay, or
  repair-framework change;
- any Allocation, Authorization, Plan, amendment, Decision Log, or INDEX
  modification;
- treating any B-finding as resolved, waived, reclassified, or governed away; or
- release, deployment, production execution, production-data mutation, WP5+, or
  M46 work.

## 12. Repository verification of this governance act

| Verification | Result |
|---|---|
| Second-renewed review identity | `EXACT` — `994512F5E0C859C1E7406753C4B91A2DC92150D3745309B305A9E2791387DC3A`, matches the expected value |
| Operative Plan / amendment / reapproval identities | `EXACT` — all three as recorded in §2 |
| Allocation and Implementation Authorization identities | `EXACT` — unchanged |
| Historical Design identity | `EXACT` — `2D2ECE4391961C85DE4076091662C66DA4586C553C6CDD57094970168BF1CE76` |
| Implementation/test candidate bytes changed during this act | `NONE` — all six candidate files byte-identical before and after |
| WP1/WP2/WP3 continuity | `PRESERVED` — no working-tree diff outside the six authorized candidate files; `models/asset.py`, `services/market_data/`, and `models/` are unmodified |
| Decision Log and Implementation INDEX | `UNCHANGED` — no working-tree diff |
| Frozen BANPU governance artifacts modified | `NONE` |
| Only additive path created by this act | `SATISFIED` — `docs/implementation/BANPU_WP4_PROVIDER_IDENTITY_GOVERNANCE_DECISION.md` |
| Markdown relative-link target verification | `PASS` — all relative targets resolve to existing sibling artifacts |
| Markdown fragment-heading verification | `PASS` — no fragment links used |
| Trailing-whitespace verification | `PASS` |
| `git diff --check` | `PASS` |
| `git diff --cached --check` | `PASS` — nothing staged |
| `graphify update .` | `PASS` — code graph rebuilt; no implementation change introduced |
| Final `git status --short --untracked-files=all` | Exactly the pre-existing WP4 candidate entries plus this one additive record |
| Staged, committed, pushed, or merged | `NO` |

## 13. Governance disposition and resulting state

**`OUTCOME 1 — EXISTING AUTHORITY SUFFICIENT; QUOTE_BINDING.PROVIDER IS NOT
REGISTRY-RESOLVED`**

BANPU-WP4 remains:

- allocated;
- implementation-authorized within its existing bounded surface, unchanged;
- implementation candidate `NOT CONFIRMED`;
- blocked on candidate corrections B1, B2, B5, and B6 and a complete evidence
  matrix;
- not frozen, not closed, not release-ready; and
- without release, deployment, production execution, snapshot rebuild, WP5+, or
  M46 authority.

## 14. Exact next constitutional act

The exact next constitutional act is **bounded BANPU-WP4 implementation and
evidence correction under the existing Implementation Authorization**, exactly
as the second-renewed Independent Implementation Review §16 already specifies,
with its item 1 now bound by rules PIA-1 through PIA-4: authoritative provider
**symbols** are assembled from registry state, and `quote_binding.provider` is
left as the frozen WP1 payload contract governs it.

After those bounded corrections and a complete evidence matrix, another renewed
Independent Implementation Review is required. Implementation Confirmation
remains a separate later act.

This record performs no implementation, no review, and no confirmation, and
creates no successor authority.
