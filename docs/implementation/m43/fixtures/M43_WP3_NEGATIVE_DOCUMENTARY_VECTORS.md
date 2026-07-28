# M43-WP3 Negative Documentary Vectors

**Work package:** M43-WP3 only
**Artifact class:** Constitutional documentary vectors
**Status:** `PROPOSED — NON-EXECUTABLE — NON-PRODUCTION`
**Runtime authority:** `NONE`
**Implementation authority:** `NONE`
**Production-method authority:** `NONE`
**Executable-validation authority:** `NONE`

## 1. Use boundary

These artificial vectors demonstrate fail-closed rejection under:

- the
  [Portfolio Measure Subject contract](../../M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md);
  and
- the
  [Portfolio Analytics Input Manifest contract](../../M43_WP3_PORTFOLIO_ANALYTICS_INPUT_MANIFEST_CONTRACT_SPECIFICATION.md).

They are not executable tests, validators, serializers, concrete source
records, method definitions, runtime invocations, or production records.

M42-WP7 §5 fixes the Portfolio Composition semantic tag and field order but
does not define exact Composition canonical bytes. Therefore no concrete
Portfolio Measure Subject or concrete Portfolio Analytics Input Manifest can
yet be formed. Every example is an artificial documentary placeholder only;
no encoding may be inferred or invented, and concrete formation fails closed
until separately authorized exact bytes exist.

“Reject” means that a canonical subject or manifest cannot be formed. WP3
does not map rejection to Portfolio Input Sufficiency, Portfolio Computation
Outcome, Degraded State, or Portfolio Measure Result; those contracts remain
reserved to WP5.

## 2. Subject shape and coordinate rejection vectors

| ID | Artificial defect | Required documentary result |
| --- | --- | --- |
| N-01 | Subject omits `portfolio_identity` | Missing coordinate; reject without inference |
| N-02 | Subject omits `accounting_scope` | Missing coordinate; reject without deriving it from Identity or Composition |
| N-03 | Subject omits `portfolio_composition` | Missing exact subject; reject without live lookup |
| N-04 | Subject includes an extra `workspace_id`, account list, display name, or provider field | Closed shape violation; reject |
| N-05 | Subject uses another or missing `contract_version` | Contract-shape mismatch; reject |
| N-06 | Portfolio Identity is empty, mutable, unresolved, or `latest` | Non-exact identity; reject |
| N-07 | Accounting Scope is empty, mutable, unresolved, or selected at runtime | Non-exact scope; reject |
| N-08 | Composition lacks exact `M42-WP7-PORTFOLIO-COMPOSITION-1` schema tag | Non-conforming Composition citation; reject |
| N-09 | Composition is incomplete under M42-WP7 | Incomplete source subject; reject |
| N-10 | A bare Composition row key, object pointer, URL, or digest without governed preimage replaces complete Composition bytes | Shadow/insufficient citation; reject |
| N-141 | Governing M42-WP7 Composition contract fixes a canonical semantic field order and tag but no exact byte representation | No conforming subject or manifest can be formed; fail closed without inventing an encoding |
| N-142 | `COUNT_AT_LEAST` is used for a `SUBJECT_COORDINATE` operand | Operator/category mismatch; reject the requirement as invalid |
| N-143 | `EQUALS` or `IN` is used for a subject coordinate whose owning frozen contract supplies no exact canonical literal or reference bytes | Required comparison literal is unavailable; requirement cannot pass the WP2 gate |
| N-144 | A required subject coordinate is present but non-canonical, mismatched, wrong-owner, provider-shaped, or ambiently selected | Subject candidate is invalid; for applicability the coordinate is unresolved and the requirement is `UNMET`, rather than treating the defective coordinate as valid or repairing it |

No missing coordinate becomes an explicit absence, default, partial subject,
Degraded State, or permission to continue.

## 3. Wrong-scope and cross-portfolio rejection vectors

| ID | Artificial defect | Required documentary result |
| --- | --- | --- |
| N-11 | `portfolio:alpha` is paired with non-corresponding `scope:beta` | Wrong-scope subject; reject |
| N-12 | Subject fields say `portfolio:alpha` / `scope:alpha`, while Composition says `portfolio:beta` / `scope:beta` | Cross-portfolio mismatch; reject entire subject |
| N-13 | Identity matches Composition but Accounting Scope differs | Coherence failure; reject without preferring either field |
| N-14 | Scope matches Composition but Portfolio Identity differs | Coherence failure; reject without repair |
| N-15 | One coordinate inside Composition belongs to `portfolio:beta` | M42 subject-coherence failure; reject |
| N-16 | Subject is two Portfolio Compositions, a person, household, Workspace, account collection, or Wealth aggregate | Forbidden subject shape; reject |
| N-17 | A Market Measure subject or provider portfolio object is relabeled as Portfolio Measure Subject | Cross-domain type widening; reject |
| N-18 | Subject Composition is assembled using data from another Accounting Scope | Replay/boundary breach; reject |
| N-19 | Manifest Ledger entry for `scope:beta` is bound to subject `scope:alpha` | Cross-portfolio evidence; reject manifest |
| N-20 | A cross-portfolio aggregate is supplied as `LEDGER_DERIVED_EVIDENCE` | Wrong input meaning and Wealth boundary breach; reject |

## 4. Ambient-selection and provider rejection vectors

| ID | Artificial defect | Required documentary result |
| --- | --- | --- |
| N-21 | Subject is obtained from Current Selection | Ambient Experience selection; reject |
| N-22 | Missing subject is filled from Workspace default | Ambient default; reject |
| N-23 | Route parameter, session, user preference, or last-opened Portfolio selects subject | Mutable caller/context selection; reject |
| N-24 | “Current Composition” is looked up at calculation time | Dynamic subject resolution; reject |
| N-25 | Wall-clock time chooses the Composition, evidence revision, or subject | Ambient time; reject |
| N-26 | Provider account code or provider portfolio identifier substitutes for Portfolio Identity | Provider-shaped identity; reject |
| N-27 | Ticker or provider symbol substitutes for Market or Asset canonical reference | Provider leakage; reject manifest |
| N-28 | Live provider answer is stored as `canonical_value` without a governed M39/M41 identity | Ungoverned live evidence; reject |
| N-29 | Cache key, database primary key, ORM object identity, or URL is the sole canonical reference | Storage/implementation identity leakage; reject |
| N-30 | Candidate chooses the newest, preferred, most liquid, or highest-quality source | Ambient/judgment selection; reject |

Caller consent, convenience, deployed legacy behavior, or provider
availability cures none of these defects.

## 5. Manifest shape and invocation-binding rejection vectors

| ID | Artificial defect | Required documentary result |
| --- | --- | --- |
| N-31 | Manifest omits subject, Method Version, entries, or contract version | Required-field failure; reject without defaulting |
| N-32 | Manifest contains an extra Definition field independently selectable from Method Version | Ambiguous/redundant binding; reject |
| N-33 | Manifest contains an extra runtime, provider, storage, cache, request, or UI field | Closed shape and authority breach; reject |
| N-34 | Method identity omits Definition revision or uses `latest`, wildcard, range, alias, or compatible selector | Non-exact WP2 identity; reject |
| N-35 | Manifest requests `1.0.0` but binds compatible `1.0.1` | Non-substitutability breach; reject |
| N-36 | Method Version does not resolve to its exact immutable normative record or specification | Unresolved prerequisite; reject |
| N-37 | Bound specification leaves an input role, category, owner, contract kind, or cardinality implicit | Completeness cannot be established; reject |
| N-38 | Two declared roles share one `binding_key` | Role ambiguity; reject |
| N-39 | A role is optional, preferred, defaulted, or variadic without exact bounds | Non-closed input declaration; reject |
| N-40 | Entries collection is empty | Missing mandatory Composition entry; reject |
| N-41 | Subject differs from the Composition entry's subject reference or value | Subject/manifest conflict; reject |
| N-42 | Method Version's bound Definition subject declaration is not satisfied | Invocation-binding failure; reject |

## 6. Entry shape, owner, and category rejection vectors

| ID | Artificial defect | Required documentary result |
| --- | --- | --- |
| N-43 | Entry omits category, binding key, owner, contract kind, reference, or value | Entry-shape failure; reject manifest |
| N-44 | Entry adds a field not admitted by §6.2 | Entry-shape failure; reject |
| N-45 | `input_category` is outside the closed seven WP2 tokens | Category closure failure; reject |
| N-46 | `binding_key` is empty, non-ASCII, invented, or unresolved in the exact specification | Role-binding failure; reject |
| N-47 | `owning_authority` differs from the controlling contract | Ownership mismatch; reject |
| N-48 | `contract_kind` is an implementation class, table, endpoint, provider product, or cache | Non-governed contract kind; reject |
| N-49 | Canonical reference or value is empty, mutable, unresolved, or requires live lookup | Non-reconstructable input; reject |
| N-50 | Portfolio Intelligence claims ownership of Ledger evidence, Market evidence, Asset reference, or Provenance | Ownership leakage; reject |
| N-51 | A non-Provenance entry carries `associated_entry_key` | Category/field mismatch; reject |
| N-52 | A Provenance entry omits its association or targets another Provenance entry | Invalid association; reject |
| N-53 | Provenance targets a missing or ambiguous binding key | Unresolved association; reject |
| N-54 | Composition entry uses a new Composition identifier instead of complete subject and Composition bytes | M42 shadow identity; reject |
| N-55 | Asset reference uses an unversioned taxonomy where the owner requires a version | Non-exact Asset Foundation reference; reject |
| N-56 | Ledger evidence omits an owner-required economic-time or record-time coordinate | Incomplete source-owned value; reject |

## 7. Manifest completeness and closure rejection vectors

| ID | Artificial defect | Required documentary result |
| --- | --- | --- |
| N-57 | Represented category set omits a Method Version declared category | Incomplete manifest; reject |
| N-58 | Represented category set includes a category not declared by Method Version | Surplus input; reject |
| N-59 | One positive-cardinality role is missing | Incomplete manifest; reject |
| N-60 | An undeclared binding key is present | Surplus/unknown role; reject |
| N-61 | Entry cardinality is less than or greater than the exact declared cardinality | Cardinality mismatch; reject |
| N-62 | Two Composition entries appear | Mandatory-one cardinality breach; reject |
| N-63 | Composition entry is absent but subject is present | Category/entry completeness failure; reject |
| N-64 | Evidence reference is present but the complete calculation value must be fetched later | Reconstructability failure; reject |
| N-65 | An unrelated “helpful” evidence entry is retained | Surplus input; reject |
| N-66 | Missing input is inferred from another entry | Inference/default breach; reject |
| N-67 | Missing input is treated as empty, zero, Explicitly None, or unavailable without owning-contract authority | Absence invention; reject |
| N-68 | Missing direct dependency result is assumed to be included transitively elsewhere | Dependency-input incompleteness; reject |
| N-69 | A transitive dependency is added as an entry although the method does not directly consume it | Surplus role; reject |
| N-70 | A structurally incomplete candidate is described as `Portfolio Input Sufficiency` or a computation outcome | WP5 authority leakage; reject interpretation |
| N-145 | A Method Version declares an input category whose every role has zero cardinality | No entry may represent the category, so category-set equality is impossible and no conforming manifest exists |

No extra input compensates for a missing required input.

## 8. Duplicate, equivalence, and count rejection vectors

| ID | Artificial defect | Required documentary result |
| --- | --- | --- |
| N-71 | The exact same entry-record tuple appears twice | Duplicate entry; reject without deduplication |
| N-72 | Two byte-equivalent representations share one binding key | Duplicate role; reject without merge |
| N-73 | Same binding key and reference are repeated with the same value | Duplicate key; reject |
| N-74 | A cardinality-one binding key is repeated with a different reference or value | Conflict; reject |
| N-75 | Same canonical reference is paired with two canonical values | Identity/value conflict; reject |
| N-76 | Same canonical reference is assigned two owners or contract kinds | Authority conflict; reject |
| N-77 | Equal payload values from identity-distinct evidence are collapsed | Forbidden semantic deduplication; reject interpretation |
| N-78 | Provider symbol or matching display label is used to claim identity equivalence | Invalid equivalence; reject |
| N-79 | One source input is repeated under invented keys to raise `COUNT_AT_LEAST` | Undeclared/surplus roles; reject before counting |
| N-80 | Duplicate entries are silently removed and then counted | Duplicate-repair violation; requirement operand remains unresolved and is `UNMET` |
| N-81 | Category count includes a Provenance entry again in its target category | Double count; reject evaluation |
| N-82 | A non-conforming manifest is counted anyway | WP2 evaluation breach; named category is unresolved and requirement is `UNMET` |

## 9. Conflict rejection vectors

| ID | Artificial defect | Required documentary result |
| --- | --- | --- |
| N-83 | Two identity-distinct Market candidates compete for one cardinality-one role | Unresolved conflict; reject |
| N-84 | Conflict is resolved by presentation order | Forbidden choice; reject |
| N-85 | Conflict is resolved by source/provider priority | Provider/source preference; reject |
| N-86 | Conflict is resolved by recency or wall-clock time | Ambient temporal choice; reject |
| N-87 | Conflict is resolved by payload similarity or equality | Unsupported semantic equivalence; reject |
| N-88 | Conflict is resolved by a quality, trust, reliability, or correctness score | Trust & Evaluation leakage; reject |
| N-89 | Conflict is resolved by caller preference or UI selection | Ambient invocation/Experience leakage; reject |
| N-90 | Conflict causes selection of another Method Version or dependency | Forbidden fallback/substitution; reject |
| N-91 | Conflict is retained as a partial manifest | Closed-manifest breach; reject |
| N-92 | Conflict is labeled a new WP3 outcome, sufficiency value, or Degraded State | Vocabulary and WP5 authority leakage; reject interpretation |
| N-93 | One Provenance reference carries different content or targets in two candidates | Provenance conflict; reject |
| N-94 | Owning contract reports ambiguous identity, but manifest chooses one candidate | Owner-authority and conflict breach; reject |

## 10. Invocation-parameter and governed-override rejection vectors

| ID | Artificial defect | Required documentary result |
| --- | --- | --- |
| N-95 | Parameter name is not expressly declared by exact method specification | Undeclared parameter; reject |
| N-96 | Parameter value is outside its exact canonical permitted domain | Invalid parameter value; reject |
| N-97 | Missing parameter receives a default | Ambient/default invocation; reject |
| N-98 | Request supplies a benchmark symbol or declaration to replace Portfolio Benchmark Declaration | Governed-declaration override; reject |
| N-99 | Request supplies a risk-free input or request-default rate | Governed input/dependency override; reject |
| N-100 | Request supplies annualization basis such as `252` | Governed input/dependency override; reject |
| N-101 | Request supplies calendar or market-session authority | Governed-authority override; reject |
| N-102 | Request, asset, provider, or Workspace state supplies missing Portfolio Base Currency | Frozen Ledger-coordinate inference; reject |
| N-103 | Parameter supplies lifecycle state, Provenance, Market evidence, Ledger evidence, or Asset classification | Governed evidence/parameter conflation; reject |
| N-104 | Parameter supplies or replaces a calculation dependency | Dependency/parameter conflation; reject |

None of these values becomes invocation-bound merely because a caller labels
it a parameter.

## 11. Calculation-dependency rejection vectors

| ID | Artificial defect | Required documentary result |
| --- | --- | --- |
| N-105 | Dependency entry key is absent from the exact WP2 declaration | Undeclared dependency; reject |
| N-106 | Dependency owner or contract kind differs from declaration | Exact-binding failure; reject |
| N-107 | Dependency identifier or version differs from declaration | Exact-binding failure; reject |
| N-108 | Reference uses a range, wildcard, alias, compatible version, provider resolution, or `latest` | Non-exact dependency; reject |
| N-109 | Dependency result/value is missing, mutable, or retrieved live | Non-reconstructable dependency input; reject |
| N-110 | Governing dependency contract lacks an exact immutable result/value representation | Concrete entry cannot conform; fail closed without inventing identity |
| N-111 | Ledger evidence or M39 Observation is relabeled a dependency to avoid evidence rules | Evidence/dependency conflation; reject |
| N-112 | Exact governed dependency is relabeled an invocation parameter | Dependency/parameter conflation; reject |
| N-113 | Compatible dependency result is substituted for the exact one | Non-substitutability breach; reject |
| N-114 | Full WP2 dependency closure is unresolved but manifest is described as complete | Prerequisite/closure failure; reject |

## 12. Provenance rejection vectors

| ID | Artificial defect | Required documentary result |
| --- | --- | --- |
| N-115 | Manifest captures or recaptures Provenance | Connectivity & Ingestion ownership breach; reject |
| N-116 | Provenance is reconstructed from provider, storage, or request metadata | Reconstruction/provider leakage; reject |
| N-117 | Provenance from two inputs is merged so associations are lost | Association and meaning loss; reject |
| N-118 | Provenance is normalized, translated, repaired, or provider-mapped | Source-meaning modification; reject |
| N-119 | Provenance is ranked, scored, or treated as proof of correctness or quality | Trust & Evaluation leakage; reject |
| N-120 | Already-captured Provenance supplied with an input is omitted, or the Method Version omits `CAPTURED_PROVENANCE` while such Provenance is supplied | Manifest incompleteness/category mismatch; reject |

## 13. Ordering, serialization, and identity rejection vectors

| ID | Artificial defect | Required documentary result |
| --- | --- | --- |
| N-121 | Subject serializes fields in a different order | Non-canonical `PMS1`; reject |
| N-122 | Subject canonical bytes use another tag, terminator, padding, extension, or trailing byte | Non-canonical subject; reject |
| N-123 | Manifest entries remain in presentation order instead of §10.2 order | Non-canonical `PAIM1`; reject |
| N-124 | Ordering uses locale, case-folding, normalized text, source priority, or signed-byte comparison | Wrong ordering rule; reject |
| N-125 | Entry count differs from decoded entry-record count | Non-round-trippable serialization; reject |
| N-126 | Manifest uses another tag, omitted length, optional field, terminator, padding, extension, or trailing byte | Non-canonical manifest; reject |
| N-127 | Same logical manifest produces different bytes because of input presentation order | Determinism failure; reject |
| N-128 | Decoder requires a registry default, provider, database, cache, clock, or external ordering rule | Non-self-contained identity; reject |
| N-129 | Digest, storage key, object identity, or file location replaces canonical bytes as manifest identity | Shadow identity; reject |
| N-130 | Two byte-distinct manifests are called identical because they share subject and Method Version | Entry-binding identity loss; reject interpretation |

## 14. Scope and authority rejection vectors

| ID | Artificial defect | Required documentary result |
| --- | --- | --- |
| N-131 | A vector contains a formula, named metric, worked calculation, or numerical expected result | WP6–WP8/production-method scope breach; remove from WP3 |
| N-132 | Manifest chooses measurement window boundaries, timezone, calendar, FX, rounding, risk-free input, or annualization convention | WP4 scope breach; reject |
| N-133 | Contract defines Portfolio Input Sufficiency values, Portfolio Computation Outcome values, result identity, or result serialization | WP5 scope breach; reject |
| N-134 | Contract prescribes a class, function, builder, validator, serializer library, schema, table, endpoint, cache, adapter, or UI | Implementation/persistence/API/UI breach; reject |
| N-135 | Documentary conformance is treated as executable validation | Executable-validation authority breach; reject interpretation |
| N-136 | Structurally conforming manifest is called a production invocation or production method | Production-method authority breach; reject interpretation |
| N-137 | Experience computes, selects, repairs, or substitutes subject/manifest inputs | Experience-computation breach; reject |
| N-138 | Portfolio Intelligence changes Ledger, Market, Asset, or Provenance meaning because it frames the entry | Ownership leakage; reject |
| N-139 | A new canonical noun or Glossary entry is inferred from a field/property phrase rejected by the vocabulary gate | Vocabulary-discipline breach; reject |
| N-140 | WP3 edits or reopens M1–M42, M43 Architecture, WP1, WP2, or `docs/GLOSSARY.md` | Work-package authority breach; reject change |

## 15. Expected aggregate conclusion

Every defect above fails closed without:

- inference, normalization, repair, deduplication, source preference, or
  fallback;
- a partial subject or partial manifest;
- a compatible method or dependency substitution;
- a caller override;
- a new constitutional noun, result, sufficiency value, outcome, or Degraded
  State;
- a live lookup or ambient choice;
- an implementation or executable side effect; or
- production-method admission.
