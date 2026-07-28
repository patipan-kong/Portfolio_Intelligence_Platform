# M43-WP2 Positive Documentary Vectors

**Work package:** M43-WP2 only  
**Artifact class:** Constitutional documentary vectors  
**Status:** `CORRECTED AFTER INDEPENDENT REVIEW — NON-EXECUTABLE — NON-PRODUCTION`  
**Production-method authority:** `NONE`  
**Executable-validation authority:** `NONE`

## 1. Use boundary

These vectors test only the contract in
[M43-WP2](../../M43_WP2_PORTFOLIO_MEASURE_DEFINITION_METHOD_VERSION_AND_APPLICABILITY_CONTRACT_SPECIFICATION.md).
All identifiers, statements, values, and contexts are artificial. No vector
admits a concrete Portfolio Measure Definition, Portfolio Method Version,
formula, named measure, registry record, or production method.

## 2. P-01 — Stable Definition identity

Illustrative normative fields:

```text
Definition identifier:           pmd:example-a
Revision:                        1
Semantic statement:              Describes one artificial performance question
                                 about exactly one Portfolio Composition.
Measure-kind label:              PERFORMANCE
Subject declaration:             Portfolio Measure Subject constrained to one
                                 exact M42 Portfolio Composition.
Permitted input-category set:    [CALCULATION_DEPENDENCY,
                                  LEDGER_DERIVED_EVIDENCE,
                                  PORTFOLIO_COMPOSITION]
Applicability requirement set:   []
```

Expected documentary findings:

- canonical identity is exactly `(pmd:example-a, 1)`;
- list order is ascending by code point;
- the identity is independent of file location and display text; and
- the record is structurally reviewable but remains non-production.

## 3. P-02 — Exact Method Version identity

```text
Bound Definition:                (pmd:example-a, 1)
Method version:                  1.0.0
Specification reference:        documentary-only:example-spec-a:revision-1
Declared input-category use:     [PORTFOLIO_COMPOSITION]
Declared dependencies:           []
Applicability requirements:      []
Compatibility declaration:      INITIAL
Determinism conformance
declaration:                     CONFORMS_TO_PORTFOLIO_DETERMINISTIC_CALCULATION
```

Expected identity:

```text
(pmd:example-a, 1, 1.0.0)
```

Expected findings:

- the empty dependency list is closed;
- declared input use is an exact subset of the bound Definition's permitted
  categories and contains the required Portfolio subject category;
- the determinism declaration exactly cites the frozen PA-V10 obligation;
- no prior version is inferred;
- the identity cannot be substituted by `1.0.1`; and
- the specification reference admits no formula or production method.

## 4. P-03 — Applicability is deterministic

Definition requirement:

```text
key:                r-01
operand category:   SUBJECT_COORDINATE
operand authority:  M42 Portfolio Composition contract
operand name:       exact_portfolio_composition
operator:           PRESENT
expected value:     absent
```

Method requirement:

```text
key:                r-02
operand category:   INPUT_CATEGORY
operand authority:  Ledger & Accounting
operand name:       LEDGER_DERIVED_EVIDENCE
operator:           COUNT_AT_LEAST
expected value:     1
```

Documentary context:

```text
exact_portfolio_composition: present and exact
LEDGER_DERIVED_EVIDENCE count: 2
```

Expected results:

```text
r-01: MET
r-02: MET
overall: APPLICABLE
```

The result says nothing about Portfolio Input Sufficiency, computation
outcome, value presence, production admission, or runtime availability.
Because WP3 has not yet confirmed the concrete Portfolio Measure Subject
operand names or manifest-entry counting rules, this vector demonstrates
binary evaluation only from its expressly supplied documentary context. Its
requirements cannot yet pass the future gate.

## 5. P-04 — Direct dependency traversal demonstration

The illustrative Method Version declares:

```text
dependency key:           dep-calendar-a
owning domain:            Market Intelligence
dependency contract kind: artificial-governed-calendar-contract
dependency identifier:    calendar:example-a
dependency version:       3

dependency key:           dep-period-a
owning domain:            Portfolio Intelligence
dependency contract kind: artificial-non-production-portfolio-method
dependency identifier:    period:example-a
dependency version:       1.0.0
```

The list is ordered `dep-calendar-a`, then `dep-period-a`. Each artificial
dependency declares an empty dependency list.

Expected traversal set:

```text
{
  (Market Intelligence,
   artificial-governed-calendar-contract,
   calendar:example-a,
   3),
  (Portfolio Intelligence,
   artificial-non-production-portfolio-method,
   period:example-a,
   1.0.0)
}
```

Two traversals yield the same set. No evidence record is reclassified as a
calculation dependency.

This vector demonstrates only direct-set construction and traversal
determinism. Its artificial contract kinds cannot match controlling frozen
authority under WP2 §8.2(2), so this vector does not demonstrate closure
acceptance and cannot pass the future gate.

## 6. P-05 — Transitive dependency traversal demonstration

Artificial graph:

```text
method:example-top:1.0.0
  -> dependency-a:2
       -> dependency-c:7
  -> dependency-b:4
```

Expected traversal set:

```text
{ dependency-a:2, dependency-b:4, dependency-c:7 }
```

Expected findings:

- all references are exact;
- no node repeats in a traversal;
- the closure is acyclic and independent of traversal order; and
- the top Method Version cannot omit `dependency-c:7` from its closure merely
  because it is transitive.

This artificial graph demonstrates only transitive traversal, complete-set
construction, and cycle absence. It supplies no owner or governed contract
kind capable of satisfying WP2 §8.2(2), does not demonstrate closure
acceptance, and cannot pass the future gate.

## 7. P-06 — Definition revision compatibility

Artificial revision `2` retains:

- definition identifier `pmd:example-a`;
- the same semantic statement;
- `PERFORMANCE`;
- the same subject declaration; and
- all input categories used by already-bound Method Versions.

It adds one narrowing applicability requirement for future bindings. Revision
`1` remains unchanged and exactly addressable.

Expected findings:

```text
revision 2 relative to revision 1: DEFINITION_COMPATIBLE
method bound to revision 1:       remains bound to revision 1
automatic rebinding:              forbidden
```

## 8. P-07 — Method compatibility without substitution

Artificial predecessor:

```text
(pmd:example-a, 1, 1.0.0)
```

Artificial successor:

```text
(pmd:example-a, 1, 1.0.1)
predecessor:             (pmd:example-a, 1, 1.0.0)
declaration:             PATCH_COMPATIBLE
documentary relationship: same output and applicability for every predecessor
                          input; non-semantic clarification only
```

Expected findings:

- the version increment matches `PATCH_COMPATIBLE`;
- the two identities are distinct and non-substitutable; and
- no consumer may request `1.0.0` and receive `1.0.1`.

## 9. P-08 — Future gate accepts only a non-production specification

Assume an artificial record passes all fourteen WP2 future-gate predicates.

Expected gate result:

```text
ACCEPTED_FOR_NON_PRODUCTION_SPECIFICATION
```

Expected authority:

```text
production method:       NOT ADMITTED
runtime registration:    NOT AUTHORIZED
implementation:          NOT AUTHORIZED
registry construction:   NOT AUTHORIZED
```

## 10. P-09 — `EQUALS` and `IN` canonical-literal evaluation

These two Definition-level requirements cite the exact four Portfolio
Benchmark Declaration form labels frozen by M42-WP5. The list is in ascending
code-point order.

```text
key:                r-03
operand category:   PORTFOLIO_DECLARATION
operand authority:  Portfolio Intelligence — M42-WP5
operand name:       Portfolio Benchmark Declaration form
operator:           EQUALS
expected value:     Explicitly None

key:                r-04
operand category:   PORTFOLIO_DECLARATION
operand authority:  Portfolio Intelligence — M42-WP5
operand name:       Portfolio Benchmark Declaration form
operator:           IN
expected value:     [Category, Composite, Explicitly None, Single]
```

Documentary context:

```text
Portfolio Benchmark Declaration form: Explicitly None
```

Expected results:

```text
r-03: MET
r-04: MET
overall: APPLICABLE
```

The vector reuses exact frozen declaration labels. It neither selects a
Benchmark nor authorizes a request override.

## 11. P-10 — Exact `MINOR_COMPATIBLE` increment

```text
predecessor identity:      (pmd:example-minor, 1, 1.0.1)
successor identity:        (pmd:example-minor, 1, 1.1.0)
declaration:               MINOR_COMPATIBLE
documentary relationship:  outputs are identical throughout the predecessor
                           domain; applicability broadens only within the
                           bound Definition's permitted boundary
```

Expected findings:

- MINOR increases from `0` to `1` exactly;
- MAJOR remains `1`;
- PATCH resets from `1` to `0`;
- the identities remain non-substitutable; and
- no production method is admitted.

## 12. P-11 — Exact `MAJOR_CHANGE` increment

```text
predecessor identity:      (pmd:example-major, 1, 1.4.3)
successor identity:        (pmd:example-major, 1, 2.0.0)
declaration:               MAJOR_CHANGE
documentary relationship:  one calculation-significant specification rule
                           may differ
```

Expected findings:

- MAJOR increases from `1` to `2` exactly;
- MINOR and PATCH reset to `0`;
- the declaration grants no substitution or production authority; and
- no concrete differing rule or formula is specified by this vector.

## 13. P-12 — Compatible cross-revision method lineage

Definition revision `2` is directionally `DEFINITION_COMPATIBLE` with revision
`1` under P-06. An artificial method lineage declares:

```text
predecessor identity:      (pmd:example-a, 1, 1.0.0)
successor identity:        (pmd:example-a, 2, 2.0.0)
declaration:               MAJOR_CHANGE
documentary relationship:  revision 2's narrowing applicability is honored;
                           the predecessor remains bound to revision 1
```

Expected findings:

- both methods bind the same Definition identifier;
- the successor may bind the directionally compatible higher revision;
- the exact MAJOR increment and resets are valid;
- revision `1` and its Method Version remain immutable; and
- no automatic rebinding or substitution occurs.
