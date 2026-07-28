# M43-WP3 Positive Documentary Vectors

**Work package:** M43-WP3 only
**Artifact class:** Constitutional documentary vectors
**Status:** `PROPOSED — NON-EXECUTABLE — NON-PRODUCTION`
**Runtime authority:** `NONE`
**Implementation authority:** `NONE`
**Production-method authority:** `NONE`
**Executable-validation authority:** `NONE`

## 1. Use boundary

These vectors test only:

- the
  [Portfolio Measure Subject contract](../../M43_WP3_PORTFOLIO_MEASURE_SUBJECT_CONTRACT_SPECIFICATION.md);
  and
- the
  [Portfolio Analytics Input Manifest contract](../../M43_WP3_PORTFOLIO_ANALYTICS_INPUT_MANIFEST_CONTRACT_SPECIFICATION.md).

All identifiers, roles, references, byte labels, values, and specifications
are artificial documentary placeholders. They do not admit a concrete
Portfolio Composition, Portfolio Measure Definition, Portfolio Method
Version, formula, named measure, result, registry entry, executable fixture,
runtime invocation, or production method.

The notation `bytes("...")` denotes bytes stipulated only for an artificial
documentary placeholder as though the named owning contract supplied them.
It does not assert that such bytes currently exist and is not a provider,
JSON, storage, or wire-format claim.

M42-WP7 §5 fixes the Portfolio Composition semantic tag and field order but
does not define exact Composition canonical bytes. Therefore no concrete
Portfolio Measure Subject or concrete Portfolio Analytics Input Manifest can
yet be formed. Every byte expression below is an artificial documentary
placeholder only; no encoding may be inferred or invented, and concrete
formation fails closed until separately authorized exact bytes exist.

## 2. P-01 — Exact coherent Portfolio Measure Subject

Artificial source-owned references:

```text
Portfolio Identity:       bytes("portfolio:alpha")
Accounting Scope:         bytes("scope:alpha")
M42 Composition bytes:    bytes("M42-WP7-PORTFOLIO-COMPOSITION-1|alpha")
Composition Identity:     bytes("portfolio:alpha")
Composition Scope:        bytes("scope:alpha")
```

Documentary subject:

```text
contract_version:         M43-WP3-PORTFOLIO-MEASURE-SUBJECT-1
portfolio_identity:       bytes("portfolio:alpha")
accounting_scope:         bytes("scope:alpha")
portfolio_composition:    bytes("M42-WP7-PORTFOLIO-COMPOSITION-1|alpha")
```

The exact Composition is stipulated complete and conforming under M42-WP7.
Its own carried subject coherence evidences that `scope:alpha` corresponds to
`portfolio:alpha` and carries the same exact references; no runtime or live
Ledger & Accounting lookup is performed.

Expected findings:

- exactly one Portfolio and corresponding Accounting Scope are bound;
- all three subject coordinates are present and coherent;
- canonical bytes are exactly the `PMS1` framing of the three supplied byte
  sequences;
- no independent Composition identity is minted; and
- the subject remains documentary and non-production.

## 3. P-02 — Subject identity changes with Composition content

Two artificial M42 Compositions cite the same Portfolio Identity and
Accounting Scope but differ in one exact source-owned coordinate:

```text
subject A Composition bytes: bytes("...|composition-content-a")
subject B Composition bytes: bytes("...|composition-content-b")
```

Expected findings:

- the two complete `PMS1` byte sequences differ;
- the two Portfolio Measure Subjects are different;
- equal Portfolio Identity and Accounting Scope do not collapse them; and
- neither subject is described as a new version of the other.

## 4. P-03 — Closed subject-coordinate applicability

Artificial M43-WP2 requirements:

```text
key:                subject-composition-present
operand category:   SUBJECT_COORDINATE
operand authority:  Portfolio Intelligence — M42-WP7
operand name:       portfolio_composition
operator:           PRESENT
expected value:     absent

key:                subject-id-present
operand category:   SUBJECT_COORDINATE
operand authority:  Ledger & Accounting — M34/M42-WP2
operand name:       portfolio_identity
operator:           PRESENT
expected value:     absent

key:                subject-scope-present
operand category:   SUBJECT_COORDINATE
operand authority:  Ledger & Accounting — M34/M42-WP2
operand name:       accounting_scope
operator:           PRESENT
expected value:     absent
```

Applied to P-01, expected documentary results are:

```text
subject-composition-present:    MET
subject-id-present:             MET
subject-scope-present:          MET
```

Conditional on WP3 independent confirmation, these results demonstrate only
the admitted operand names and WP2 binary evaluation. They do not establish
Portfolio Input Sufficiency, computation, runtime availability, or production
admission.

## 5. P-04 — Minimal complete manifest

Artificial exact Method Version:

```text
identity:                    (pmd:documentary-only-a, 1, 1.0.0)
declared input categories:   [PORTFOLIO_COMPOSITION]
declared role:
  binding_key:               composition-input
  category:                  PORTFOLIO_COMPOSITION
  owning authority:          Portfolio Intelligence — M42-WP7
  contract kind:             M42 Portfolio Composition
  cardinality:               1
declared dependencies:       []
```

Documentary entry:

```text
input_category:              PORTFOLIO_COMPOSITION
binding_key:                 composition-input
owning_authority:            Portfolio Intelligence — M42-WP7
contract_kind:               M42 Portfolio Composition
canonical_reference:         P-01 complete PMS1 subject bytes
canonical_value:             P-01 exact M42 Composition bytes
associated_entry_key:        absent
```

Expected findings:

- the manifest has one exact subject and exact Method Version;
- its represented category set exactly equals the declared set;
- the Composition entry matches the subject;
- the entry count is one;
- no hidden input or default exists; and
- the candidate is structurally complete but remains non-executable and
  non-production.

## 6. P-05 — Complete seven-category manifest

An artificial Method Version's declared input-category use is in exact
ascending code-point order:

```text
[ASSET_FOUNDATION_REFERENCE,
 CALCULATION_DEPENDENCY,
 CAPTURED_PROVENANCE,
 INVOCATION_PARAMETER,
 LEDGER_DERIVED_EVIDENCE,
 MARKET_EVIDENCE,
 PORTFOLIO_COMPOSITION]
```

Its immutable specification declares these unique positive-cardinality
roles:

```text
asset-input             ASSET_FOUNDATION_REFERENCE
dependency-input        CALCULATION_DEPENDENCY
provenance-input        CAPTURED_PROVENANCE
parameter-input         INVOCATION_PARAMETER
ledger-input            LEDGER_DERIVED_EVIDENCE
market-input            MARKET_EVIDENCE
composition-input       PORTFOLIO_COMPOSITION
```

The exact WP2 dependency record for `dependency-input` is:

```text
owning domain:            Market Intelligence
dependency contract kind: documentary-governed-reference-contract
dependency identifier:    documentary-reference-a
dependency version:       1
```

Artificial entries:

| Category | Binding key | Owning authority | Contract kind | Canonical reference | Canonical value | Association |
| --- | --- | --- | --- | --- | --- | --- |
| `PORTFOLIO_COMPOSITION` | `composition-input` | Portfolio Intelligence — M42-WP7 | M42 Portfolio Composition | P-01 subject bytes | P-01 Composition bytes | absent |
| `LEDGER_DERIVED_EVIDENCE` | `ledger-input` | Ledger & Accounting | artificial immutable ledger evidence | `bytes("ledger-ref-a")` | `bytes("ledger-value-a,economic-time,record-time")` | absent |
| `MARKET_EVIDENCE` | `market-input` | Market Intelligence | artificial M39 Observation | `bytes("observation-ref-a")` | `bytes("observation-value-a")` | absent |
| `ASSET_FOUNDATION_REFERENCE` | `asset-input` | Asset Foundation | artificial versioned classification | `bytes("classification-ref-a,revision-1")` | `bytes("classification-value-a")` | absent |
| `INVOCATION_PARAMETER` | `parameter-input` | Portfolio Intelligence — bound method specification | exact artificial method specification | `bytes("parameter-a")` | `bytes("choice-a")` | absent |
| `CALCULATION_DEPENDENCY` | `dependency-input` | Market Intelligence | documentary-governed-reference-contract | exact WP2 dependency tuple bytes | `bytes("dependency-value-a")` | absent |
| `CAPTURED_PROVENANCE` | `provenance-input` | Connectivity & Ingestion | Provenance | `bytes("provenance-ref-a")` | `bytes("provenance-value-a")` | `(LEDGER_DERIVED_EVIDENCE, ledger-input, bytes("ledger-ref-a"))` |

Documentary stipulations:

- every artificial contract/reference is treated only as a shape placeholder;
- `ledger-input` belongs to P-01's exact Accounting Scope;
- `parameter-a = choice-a` is expressly permitted by the artificial
  specification and is not a governed override;
- the dependency tuple exactly matches the Method Version declaration; and
- Provenance was already captured and remains associated with
  `ledger-input`.

Expected findings:

- the represented category set equals the declared seven-category set;
- every positive-cardinality role appears exactly once;
- all entries are attributable and self-contained;
- canonical order is determined by category token and then the remaining
  §10.2 components;
- no entry changes ownership; and
- the vector demonstrates structure only and cannot pass any production gate.

## 7. P-06 — Presentation-order permutation

Take the seven valid entry records from P-05 and present them in:

```text
order A: composition, ledger, market, asset, parameter, dependency, provenance
order B: provenance, dependency, parameter, asset, market, ledger, composition
```

Expected findings:

- both candidates sort to the same §10.2 canonical order;
- both produce the same entry count;
- both produce byte-identical `PAIM1` serialization;
- both denote one manifest identity; and
- input presentation order supplies no precedence or conflict resolution.

## 8. P-07 — Exact round-trip reconstruction

Use the complete P-04 manifest. Its canonical form is abstractly:

```text
ASCII("PAIM1")
lp(P-01 PMS1 bytes)
lp(bytes for (pmd:documentary-only-a, 1, 1.0.0))
u32(1)
lp(canonical composition-entry bytes)
```

Expected findings:

- decoding identifies the same exact subject;
- decoding identifies the same exact Definition identifier, revision, and
  Method Version;
- entry count is exactly one;
- the Composition reference and value reconstruct exactly;
- re-encoding produces byte-identical bytes; and
- no database, provider, clock, cache, default, or external ordering rule is
  consulted.

## 9. P-08 — One governed input in two declared roles

An artificial Method Version declares input-category use exactly:

```text
[MARKET_EVIDENCE, PORTFOLIO_COMPOSITION]
```

Its immutable specification declares the mandatory
`PORTFOLIO_COMPOSITION` role plus two distinct Market-evidence roles:

```text
composition-role
market-role-a
market-role-b
```

The same exact artificial M39 identity and value are explicitly valid for
both roles. The manifest contains:

```text
(PORTFOLIO_COMPOSITION, composition-role, P-01 subject bytes,
 P-01 exact M42 Composition bytes)
(MARKET_EVIDENCE, market-role-a, observation-ref-a, observation-value-a)
(MARKET_EVIDENCE, market-role-b, observation-ref-a, observation-value-a)
```

Expected findings:

- the globally unique binding keys create two distinct entry records;
- no source Observation identity is duplicated or changed;
- the `PORTFOLIO_COMPOSITION` category count is exactly `1`;
- the `MARKET_EVIDENCE` category count is exactly `2`;
- the represented category set equals the declared category set;
- neither Market entry may exist unless the immutable method specification
  declares its role; and
- repetition under one binding key would instead be rejected.

## 10. P-09 — Deterministic category-count applicability

Applied to the conforming P-08 manifest:

```text
key:                market-count
operand category:   INPUT_CATEGORY
operand authority:  Market Intelligence
operand name:       MARKET_EVIDENCE
operator:           COUNT_AT_LEAST
expected value:     2
```

Expected result:

```text
market-count: MET
```

The count is performed only after full manifest conformance. It counts the
two valid role-bound entry records; it does not silently deduplicate the
shared source identity and does not count associated Provenance. The same
manifest has exactly one valid `PORTFOLIO_COMPOSITION` entry.

## 11. P-10 — Exact invocation parameter

Artificial immutable specification declaration:

```text
binding_key:          parameter-input
parameter name:       parameter-a
permitted values:     [choice-a, choice-b]
cardinality:          1
```

Artificial entry:

```text
input_category:          INVOCATION_PARAMETER
binding_key:             parameter-input
owning_authority:        Portfolio Intelligence — bound method specification
contract_kind:           exact artificial method specification
canonical_reference:     bytes("parameter-a")
canonical_value:         bytes("choice-b")
associated_entry_key:    absent
```

Expected findings:

- the parameter name and value are explicit;
- no absence or default is used;
- no benchmark declaration, Base Currency, risk-free input, annualization
  basis, calendar authority, evidence, Provenance, or dependency is
  overridden; and
- changing `choice-b` to another expressly permitted value would produce a
  different manifest identity.

## 12. P-11 — Exact calculation-dependency binding

Artificial exact WP2 declaration:

```text
dependency key:           dependency-input
owning domain:            Market Intelligence
dependency contract kind: artificial exact governed contract
dependency identifier:    dependency-a
dependency version:       4
```

Artificial manifest entry:

```text
input_category:          CALCULATION_DEPENDENCY
binding_key:             dependency-input
owning_authority:        Market Intelligence
contract_kind:           artificial exact governed contract
canonical_reference:     exact tuple bytes for
                         (Market Intelligence,
                          artificial exact governed contract,
                          dependency-a,
                          4)
canonical_value:         bytes("exact-dependency-value-a")
associated_entry_key:    absent
```

Expected findings:

- key, owner, kind, identifier, and version match exactly;
- the dependency result/value is self-contained;
- no version range, compatible substitution, caller override, or live lookup
  occurs; and
- the artificial kind demonstrates binding shape only and is not a governed
  production dependency.

## 13. P-12 — Exact already-captured Provenance association

Artificial non-Provenance target:

```text
binding_key: ledger-input
```

Artificial Provenance entry:

```text
input_category:          CAPTURED_PROVENANCE
binding_key:             provenance-input
owning_authority:        Connectivity & Ingestion
contract_kind:           Provenance
canonical_reference:     bytes("provenance-ref-a")
canonical_value:         bytes("complete-already-captured-provenance-a")
associated_entry_key:    (LEDGER_DERIVED_EVIDENCE,
                          ledger-input,
                          bytes("ledger-ref-a"))
```

Expected findings:

- the Provenance remains owned by Connectivity & Ingestion;
- the association points to exactly one existing non-Provenance entry;
- no Provenance is recaptured, reconstructed, scored, or used as correctness
  proof;
- the Provenance entry counts once in `CAPTURED_PROVENANCE` and not in
  `LEDGER_DERIVED_EVIDENCE`; and
- changing the association changes manifest identity.

## 14. P-13 — Distinct evidence in distinct declared roles

Two exact identity-distinct M39 Observations have different governed values.
The immutable method specification declares two different roles and requires
both:

```text
market-coordinate-a -> observation-ref-a
market-coordinate-b -> observation-ref-b
```

Expected findings:

- both entries remain distinct;
- different values are not a conflict because the roles are distinct and
  retain both;
- equal payloads would not collapse the identities; and
- neither entry receives provider, source-priority, quality, or correctness
  semantics.

## 15. P-14 — Structural completeness remains separate from later axes

Assume an artificial manifest conforms to every WP3 structural rule.

Expected documentary conclusions:

```text
Portfolio Measure Subject exact:       YES
Manifest structurally complete:        YES
Manifest canonical identity exact:     YES
Applicability:                          NOT INFERRED BY THIS FACT
Portfolio Input Sufficiency:            NOT DEFINED BY WP3
Portfolio Computation Outcome:          NOT DEFINED BY WP3
Portfolio Measure Result:               NOT CREATED
Runtime invocation:                     NOT AUTHORIZED
Production method:                      NOT ADMITTED
```

This is the terminal positive conclusion of WP3.
