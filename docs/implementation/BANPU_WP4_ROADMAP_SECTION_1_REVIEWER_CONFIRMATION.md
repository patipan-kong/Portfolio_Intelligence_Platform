# BANPU-WP4 — Roadmap Section 1 Reviewer Confirmation

**Artifact class:** Independent roadmap Section 1 reviewer confirmation record
**Confirmation date:** 2026-08-13
**Review authority:** Independent roadmap Section 1 reviewer
**Strict-necessity determination:** `CONFIRMED`
**Conditional surface disposition:** `ADMITTED — MINOR-1 ONLY`
**Implementation performed:** `NO`
**MINOR-1 state:** `OPEN — IMPLEMENTATION AND EVIDENCE REQUIRED`
**Planning amendment performed:** `NO`
**Release, deployment, production execution, or production-data authority:** `NONE`
**BANPU-WP5+ authority:** `NONE`
**M46 authority:** `NONE`

---

## 1. Review boundary

This record answers only the conditional-file question established by
[the BANPU remediation roadmap](BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md)
Section 1, [the BANPU-WP4 Implementation Authorization Record](BANPU_WP4_IMPLEMENTATION_AUTHORIZATION_RECORD.md)
Section 4.3, and [the BANPU-WP4 Work Package Plan](BANPU_WP4_WORK_PACKAGE_PLAN.md)
Sections 2.3 and 4.4.

The question is whether strict necessity has been demonstrated for admitting
exactly these frozen WP1-family files into the bounded BANPU-WP4 implementation
surface:

- `backend/services/transaction_canonicalizer.py`, solely for the minimal
  `MINOR-1` fingerprint-precision correction; and
- `backend/tests/test_transaction_canonicalizer.py`, solely for the focused
  canonicalization vectors required to prove that correction.

This is a confirmation of file-surface necessity. It is not implementation,
implementation review, Work Package Plan approval, planning amendment, freeze,
closeout, release, deployment, or production execution.

## 2. Canonical authority inspected

The review preserved and applied, without amendment or reinterpretation:

- [the canonical implementation design](BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md),
  including the version-1 payload contract and the `MINOR-1` residual;
- [the work-package roadmap](BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md),
  including the Section 1 conditional-production-file rule;
- [the mandatory implementation sequence](BANPU_IMPLEMENTATION_SEQUENCE.md),
  including BANPU-WP4 live-materialization scope;
- [the BANPU-WP4 Allocation Record](BANPU_WP4_ALLOCATION_RECORD.md);
- [the BANPU-WP4 Implementation Authorization Record](BANPU_WP4_IMPLEMENTATION_AUTHORIZATION_RECORD.md),
  especially Section 4.3;
- [the BANPU-WP4 Work Package Plan](BANPU_WP4_WORK_PACKAGE_PLAN.md),
  especially Sections 2.3, 3.1, and 4; and
- the applicable frozen WP1, WP2, and WP3 evidence, including the WP1 residual
  and freeze records.

The live repository implementation and focused canonicalizer tests were then
inspected independently. The Work Package Plan's conclusion was not treated as
proof.

## 3. Defect locus and independently reproduced mechanism

### 3.1 Exact production locus

The canonical version-1 payload parser in
`backend/services/transaction_canonicalizer.py` accepts a syntactically valid
finite base-10 string and constructs `Decimal(value)` directly. That
construction preserves the input coefficient and exponent exactly and does not
round to the ambient context precision.

The same file alone constructs the canonical POSITION_CONVERSION fingerprint:

1. `parse_position_conversion_payload()` builds the typed payload and passes
   it to `_payload_fingerprint()`;
2. `_payload_fingerprint()` recursively calls
   `_canonical_fingerprint_value()`, JSON-encodes its result, and SHA-256 hashes
   the encoded bytes; and
3. the nonzero `Decimal` branch returns
   `format(value.normalize(), "f")`.

`Decimal.normalize()` applies the ambient Decimal context. It therefore rounds
a coefficient longer than the active precision before insignificant trailing
zero removal and plain-form formatting. The fingerprint serialization is thus
context-dependent even though parsing is exact.

### 3.2 Reproducible non-committed full-payload probe

The probe used two otherwise identical valid payloads based on the existing
canonicalizer fixture. Only
`boundary_evidence.predecessor_reference_price` differed:

```text
A = "1.12345678901234567890123456781"
B = "1.12345678901234567890123456782"
```

At the default ambient precision of 28, the observed results were:

```text
Decimal(A) != Decimal(B)                                      True
parsed A                                                      1.12345678901234567890123456781
parsed B                                                      1.12345678901234567890123456782
canonical serialized A                                       1.123456789012345678901234568
canonical serialized B                                       1.123456789012345678901234568
canonical serializations equal                               True
fingerprint A                                                 bbae90b2c0b75f90676525c64b256166bf4dae758321fb2db8f81d4298da7411
fingerprint B                                                 bbae90b2c0b75f90676525c64b256166bf4dae758321fb2db8f81d4298da7411
fingerprints equal                                            True
```

Both full payloads parsed as valid. Their exact Decimal tuples differed in the
final coefficient digit and both had exponent `-29`.

Repeating the serialization under ambient precisions 10, 28, and 50 produced:

| Precision | Serialization A | Serialization B | Equal |
|---:|---|---|---|
| 10 | `1.123456789` | `1.123456789` | `YES` |
| 28 | `1.123456789012345678901234568` | `1.123456789012345678901234568` | `YES` |
| 50 | `1.12345678901234567890123456781` | `1.12345678901234567890123456782` | `NO` |

This independently demonstrates both the precision collision and its dependence
on ambient Decimal context. The probe modified no repository file.

## 4. Strict necessity of the conditional production file

The currently authorized BANPU-WP4 production files were inspected directly:

- `backend/services/portfolio_transactions.py` contains transaction execution
  services and local legacy numeric conversion helpers, but no canonical
  POSITION_CONVERSION payload parser, fingerprint serializer, or fingerprint
  hash implementation;
- `backend/services/asset_registry.py` contains registry service behavior and
  delegates persistence primitives to `asset_repository`; it does not
  participate in transaction canonicalization or fingerprinting; and
- `backend/services/asset_repository.py` contains asset persistence primitives
  and does not participate in transaction canonicalization or fingerprinting.

None imports or calls `_canonical_fingerprint_value()` or
`_payload_fingerprint()`, and none controls the bytes hashed for the canonical
fingerprint. A change confined to the currently authorized production surface
cannot make A and B serialize or hash differently while retaining the one
canonical identity defined at the canonicalizer locus.

Accordingly, `MINOR-1` cannot be correctly satisfied without modifying
`backend/services/transaction_canonicalizer.py`. Strict necessity for that
conditional production file is independently demonstrated.

## 5. Rejected alternatives

### 5.1 WP4-local second fingerprint

Computing another fingerprint in `portfolio_transactions.py` would give the
live service an identity distinct from the fingerprint carried by the canonical
typed payload. It would create a competing canonical identity, split retry and
conflict semantics from replay canonicalization, and add an algorithm not
authorized by the frozen canonical design. It corrects neither the canonical
serializer nor fingerprints produced by other canonicalizer consumers.

This alternative is rejected and does not eliminate strict necessity.

### 5.2 Rejecting coefficients longer than ambient precision

The frozen version-1 contract admits finite base-10 decimal strings and parses
them exactly. Rejecting an otherwise valid payload because its significant
digits exceed the current Decimal context precision would add a new limit to
that contract. It would replace a serialization correction with service-level
refusal and make payload acceptance depend on ambient runtime configuration.

This alternative is rejected as an unauthorized narrowing of the frozen WP1
payload contract and does not eliminate strict necessity.

## 6. Minimal admitted correction boundary

The narrowest sufficient production correction is confined to the nonzero
`Decimal` branch of `_canonical_fingerprint_value()`:

- derive plain base-10 notation directly from the exact Decimal coefficient and
  exponent, without any context-applying arithmetic or `normalize()` call;
- remove only insignificant fractional trailing zeroes and a now-empty decimal
  point;
- retain the existing canonical zero behavior, including negative zero to
  `"0"`; and
- leave every datetime, date, dataclass, mapping, sequence, JSON encoding, hash,
  payload parsing, validation, and fingerprint field behavior unchanged.

One minimal expression of that boundary is context-independent
`format(value, "f")`, followed only when a decimal point is present by
fractional trailing-zero and trailing-point removal. This describes the
admitted correction boundary; this record does not apply or mandate a wider
refactor.

A non-committed in-memory probe of that narrow behavior showed:

- the existing full-payload canonical vector remained
  `09e4e2d3b9f3d5789dc14f2adea727f448cdca51f74e4b15b2e63d1f070374d0`;
- A and B retained their complete exact serializations and produced distinct
  fingerprints at ambient precisions 10, 28, and 50; and
- each value's fingerprint was identical across those three precisions.

The admitted correction changes no schema, payload acceptance rule, accepted
payload shape, hash algorithm, identity owner, or unrelated canonicalization
behavior.

## 7. Strict necessity of the focused test file

The defect and correction both reside at the canonical fingerprint locus.
Focused proof therefore belongs in
`backend/tests/test_transaction_canonicalizer.py`; service-level retry and
conflict tests cannot by themselves prove exact serialization or context
independence and would leave the corrected canonical primitive without direct
regression coverage.

Admission of that test file is strictly necessary and is limited to these
focused `MINOR-1` vectors:

1. the exact A/B payload pair above parses to distinct exact Decimals and
   produces distinct canonical representations and fingerprints;
2. the existing key-order, equivalent-decimal-form, timestamp-normalization,
   and other canonicalizer vectors retain their expected behavior, with the
   existing full-payload fingerprint above available as a fixed non-regression
   vector; and
3. the same exact payload value and fingerprint are invariant under controlled
   ambient Decimal precisions, while A and B remain distinct.

Retry/no-op and conflicting-retry behavior remains in the authorized WP4 live
service test surface. It does not widen this canonicalizer-test admission.

## 8. Authority fit and exact admitted surface

The admission fits the frozen `MINOR-1` residual because it corrects only the
recorded loss of distinctions beyond the default Decimal precision at the
required WP4 pre-use point. It fits the BANPU-WP4 Allocation and Implementation
Authorization Section 4.3 because canonical-fingerprint idempotency is an
allocated WP4 capability and that section expressly makes these two files
editable upon roadmap Section 1 reviewer confirmation. It satisfies the
roadmap's strict-necessity rule and unblocks only the Work Package Plan's
conditional T7/T8 boundary.

The admitted implementation surface is exactly:

**Production**

- `backend/services/transaction_canonicalizer.py` — solely for the minimal
  context-independent `MINOR-1` Decimal fingerprint-serialization correction.

**Tests**

- `backend/tests/test_transaction_canonicalizer.py` — solely for the focused
  `MINOR-1` canonicalization vectors in Section 7.

No other production, test, schema, migration, documentation, CLI, frontend,
WP1 residual, or canonicalizer behavior is admitted or reopened.

## 9. Confirmation disposition and resulting state

**`ROADMAP SECTION 1 STRICT NECESSITY — CONFIRMED`**

The conditional `MINOR-1` surface in Section 8 is admitted into the bounded
BANPU-WP4 implementation surface. Admission is limited solely to the minimal
precision correction and its required focused vectors.

This confirmation:

- performs no implementation and approves no implementation candidate;
- leaves `MINOR-1` **OPEN** until the correction is implemented and all focused
  canonicalizer plus WP4 retry/conflict evidence passes;
- reopens no other WP1 residual or canonicalizer behavior;
- amends no plan, allocation, authorization, roadmap, sequence, design, frozen
  artifact, Decision Log, or Implementation INDEX;
- creates no release, deployment, production execution, cache mutation,
  portfolio conversion, or production-data authority;
- creates no BANPU-WP5 or later-package authority; and
- creates no M46 authority.

BANPU-WP4 implementation remains `AUTHORIZED — BOUNDED` and not started by
this record. Only the conditional T7 reviewer gate is satisfied; T8 remains an
unperformed implementation task.

## 10. Repository verification

This additive review act is verified by:

- `git diff --check`;
- `git diff --cached --check`;
- repository-wide trailing-whitespace verification for Markdown files changed
  by this act;
- relative Markdown link and fragment verification for this record;
- `graphify update .`; and
- final `git status --short --untracked-files=all`.

No file is staged or committed. Exact command results are reported with the
review handoff.

## 11. Exact next constitutional act

The exact next constitutional act is **BANPU-WP4 implementation under the
existing bounded authorization and Work Package Plan**, beginning with the
remaining dependency-ordered implementation tasks and including Work Package
Plan T8 only within the exact two-file admission above.

For `MINOR-1`, T8 must implement the minimal correction, add the focused
canonicalizer vectors, and then prove the required live retry/no-op and
conflicting-retry evidence before fingerprint idempotency becomes active.
Independent BANPU-WP4 implementation review remains a later act after every
Work Package Plan exit criterion passes.
