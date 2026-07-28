# M43-WP2 Negative Documentary Vectors

**Work package:** M43-WP2 only  
**Artifact class:** Constitutional documentary vectors  
**Status:** `CORRECTED AFTER INDEPENDENT REVIEW — NON-EXECUTABLE — NON-PRODUCTION`  
**Production-method authority:** `NONE`  
**Executable-validation authority:** `NONE`

## 1. Use boundary

These artificial vectors demonstrate fail-closed rejection under
[M43-WP2](../../M43_WP2_PORTFOLIO_MEASURE_DEFINITION_METHOD_VERSION_AND_APPLICABILITY_CONTRACT_SPECIFICATION.md).
They are not executable tests, method definitions, or production records.

## 2. Identity and revision rejection vectors

| ID | Artificial defect | Required result |
| --- | --- | --- |
| N-01 | A Definition candidate shares accepted identity `(pmd:example-a, 1)` but has a different semantic statement | Identity collision; reject the candidate and leave the accepted record unchanged |
| N-02 | A byte-equivalent Definition candidate shares accepted identity `(pmd:example-a, 1)` | Duplicate identity; reject the candidate, leave the accepted record unchanged, and never merge |
| N-03 | Definition revision is `01`, `0`, missing, or inferred as “latest” | Invalid identity; reject |
| N-04 | Revision `2` changes `PERFORMANCE` to `RISK` under the same definition identifier | Not a revision; requires a new identifier |
| N-05 | Revision `2` changes the question answered | Not a revision; requires a new identifier |
| N-06 | A Method Version binds `pmd:example-a` without an exact revision | Binding failure; reject |
| N-07 | Method version is `v1`, `1.0`, `1.0.0-beta`, `01.0.0`, `*`, or `latest` | Invalid identity; reject |
| N-08 | A Method Version candidate shares accepted identity `(pmd:example-a, 1, 1.0.0)` but has different dependencies | Identity collision; reject the candidate and leave the accepted record unchanged |
| N-09 | A consumer requests `1.0.0` and a future registry supplies compatible `1.0.1` | Forbidden substitution; fail closed |

## 3. Ownership and boundary rejection vectors

| ID | Artificial defect | Required result |
| --- | --- | --- |
| N-10 | Definition subject is a person, household, Workspace selection, or two Portfolios | Subject boundary failure; reject |
| N-11 | A Market Measure Definition is relabeled to accept Portfolio Composition | Cross-domain type widening; reject |
| N-12 | A Definition claims ownership of Ledger events or benchmark observations | Ownership leakage; reject |
| N-13 | A semantic statement recommends an action or grades a recommendation | Decision/Evaluation leakage; reject |
| N-14 | A Method Version cites a provider symbol as canonical identity | Provider leakage; reject |
| N-15 | A required field contains a module path, endpoint, ORM class, cache key, or implementation function | Implementation leakage; reject |
| N-16 | A Definition or Method claims production availability | Production-method authority breach; reject |

## 4. Applicability rejection vectors

| ID | Artificial defect | Required result |
| --- | --- | --- |
| N-17 | Requirement uses an operand category outside the closed five-category set | Malformed requirement; reject before evaluation |
| N-18 | Requirement authority says Portfolio Intelligence for a Ledger-owned operand | Owner mismatch; reject before evaluation |
| N-19 | `PRESENT` carries an expected literal | Operator/value mismatch; reject |
| N-20 | `COUNT_AT_LEAST` targets `PORTFOLIO_DECLARATION` | Operator/category mismatch; reject |
| N-21 | `IN` carries an empty, duplicated, or unsorted literal list | Non-canonical requirement; reject |
| N-22 | A required canonical literal has no encoding fixed by its owner or WP3–WP4 | Requirement cannot pass the future gate |
| N-23 | A Method requirement weakens or removes a Definition requirement | Cross-contract incompatibility; reject Method Version |
| N-24 | Required subject coordinate is missing from the documentary context | Requirement `UNMET`; overall `INAPPLICABLE` |
| N-25 | One of three requirements is `UNMET` | Overall `INAPPLICABLE`; no partial applicability |
| N-26 | `INAPPLICABLE` is mapped to Portfolio Computation Outcome, Portfolio Input Sufficiency, or Degraded State | State-axis conflation; reject interpretation |
| N-27 | `UNMET` selects another method or a fallback | Forbidden fallback; fail closed |

## 5. Dependency rejection vectors

| ID | Artificial defect | Required result |
| --- | --- | --- |
| N-28 | Dependency version is `^2`, `>=3`, `latest`, missing, or provider-resolved | Non-exact dependency; reject |
| N-29 | Two dependency records share a dependency key | Duplicate key; reject |
| N-30 | Two keys resolve to the same owner/kind/identifier/version tuple | Duplicate dependency; reject |
| N-31 | Dependency list is not ordered by dependency key | Non-canonical declaration; reject |
| N-32 | Direct dependency cannot resolve to exactly one governed version | Closure failure; reject |
| N-33 | A transitive dependency is unresolved | Closure failure; reject the declaring Method Version |
| N-34 | Graph is `A -> B -> A` | Cycle; reject |
| N-35 | Graph is `A -> A` | Self-cycle; reject |
| N-36 | Closure silently omits a transitive node | Incomplete closure; reject |
| N-37 | A live observation row is declared as a calculation dependency to avoid WP3 | Evidence/dependency conflation; reject |
| N-38 | An exact governed dependency is supplied as a caller override | Invocation/dependency conflation; reject |
| N-39 | A dependency is marked optional or given a fallback version | Non-closed dependency declaration; reject |

## 6. Compatibility rejection vectors

| ID | Artificial defect | Required result |
| --- | --- | --- |
| N-40 | `PATCH_COMPATIBLE` changes output for one predecessor-domain input | Wrong change class; reject |
| N-41 | `PATCH_COMPATIBLE` changes a dependency version | Wrong change class unless no dependency changed; reject |
| N-42 | `MINOR_COMPATIBLE` changes outputs in the predecessor domain | Wrong change class; require `MAJOR_CHANGE` |
| N-43 | Declaration is `MINOR_COMPATIBLE` but version moves `1.2.3` to `1.2.4` | Version/declaration mismatch; reject |
| N-44 | Declaration is `MAJOR_CHANGE` but version moves `1.2.3` to `1.3.0` | Version/declaration mismatch; reject |
| N-45 | A successor names a skipped or non-adjacent predecessor | Invalid lineage; reject |
| N-46 | Compatibility is used to auto-upgrade an exact invocation | Non-substitutability breach; fail closed |

## 7. Future gate and registry rejection vectors

| ID | Artificial defect | Required result |
| --- | --- | --- |
| N-47 | Thirteen of fourteen future-gate predicates pass | `REJECTED`; no partial acceptance |
| N-48 | A conforming framework record is described as a production method | Authority breach; production admission remains absent |
| N-49 | Registry resolves “latest compatible” | Exact-identity invariant breach; unusable build |
| N-50 | Registry merges identical duplicate identities | Uniqueness invariant breach; unusable build |
| N-51 | Registry builds with an unresolved reference and marks it degraded | Atomic closure invariant breach; unusable build |
| N-52 | Registry content varies with clock, build order, process, provider, or cache | Determinism invariant breach; unusable build |
| N-53 | Experience chooses a Method Version based on UI state | Experience-computation and ambient-selection breach; reject |

## 8. Frozen caller-override rejection vectors

| ID | Artificial defect | Required result |
| --- | --- | --- |
| N-54 | A request supplies a benchmark symbol or declaration to replace the exact M42 Portfolio Benchmark Declaration | Governed-declaration override; reject |
| N-55 | A request supplies a risk-free input, including a request-default value, to replace the method's governed binding | Governed-input/dependency override; reject |
| N-56 | A request supplies an annualization basis, including `252`, to replace the method's governed binding | Governed-input/dependency override; reject |
| N-57 | A request supplies a calendar or market-session authority to replace the exact governed calendar binding | Governed-authority override; reject |
| N-58 | Missing Portfolio Base Currency is inferred from request, account, asset, provider, or Workspace state | Frozen Ledger coordinate inference; reject |

None of these defects may be reclassified as an invocation-bound parameter.
No fallback, default, or caller consent cures the constitutional violation.

## 9. Additional required-field, revision, ordering, and ambient-state vectors

| ID | Artificial defect | Required result |
| --- | --- | --- |
| N-59 | A byte-equivalent Method Version candidate shares an accepted exact identity | Duplicate identity; reject the candidate, leave the accepted record unchanged, and never merge |
| N-60 | Two Definition candidates in one atomic candidate set share an identity, whether their content is equal or different | Reject both colliding candidates |
| N-61 | Two Method Version candidates in one atomic candidate set share an identity, whether their content is equal or different | Reject both colliding candidates |
| N-62 | A Definition omits semantic statement, measure-kind label, subject declaration, permitted input categories, or applicability requirement set | Required-field failure; reject without defaulting |
| N-63 | A Method Version omits specification reference, declared input-category use, dependencies, applicability requirements, compatibility declaration, or determinism conformance | Required-field failure; reject without deriving or defaulting |
| N-64 | A Definition semantic statement contains a formula or calculation body | Definition/method conflation; reject |
| N-65 | Definition revision `2` changes the subject declaration under the same identifier | Violates §5.5(3); requires a new identifier |
| N-66 | Definition revision `2` removes an input category used by a Method Version bound to revision `1` | Violates §5.5(4); reject as a revision |
| N-67 | Definition revision `2` weakens, contradicts, or otherwise makes a non-additive/non-narrowing applicability change | Violates §5.5(5); reject as a revision |
| N-68 | A Definition's permitted input-category set is not in ascending code-point order | Non-canonical required field; reject |
| N-69 | A Definition's applicability requirement set is not in ascending requirement-key order | Non-canonical required field; reject |
| N-70 | A Method Version's applicability requirement set is not in ascending requirement-key order | Non-canonical required field; reject |
| N-71 | A Method Version field contains a clock value, randomness, ambient default, or mutable process state | Forbidden normative content; reject |
| N-72 | Applicability infers a window, date, or operand from wall-clock time | Ambient inference; reject |
| N-73 | Applicability infers a subject, value, or operand from another Portfolio or cross-portfolio aggregate | Subject-boundary and ambient-state breach; reject |

## 10. Lineage, record-placement, and deferred-domain vectors

| ID | Artificial defect | Required result |
| --- | --- | --- |
| N-74 | A successor's predecessor binds a different Definition identifier, or the successor binds a higher revision that is not directionally `DEFINITION_COMPATIBLE` | Invalid lineage; successor must start a distinct `INITIAL` lineage or be rejected |
| N-75 | `PATCH_COMPATIBLE` moves `1.0.0` to `1.0.5` | Increment magnitude exceeds exactly one; reject |
| N-76 | A Definition-level applicability requirement names `INVOCATION_PARAMETER` | Record/category mismatch; malformed and reject |
| N-77 | A Definition-level applicability requirement names `CALCULATION_DEPENDENCY` | Record/category mismatch; malformed and reject |
| N-78 | A concrete `SUBJECT_COORDINATE` requirement is proposed before WP3 confirms the referenced field and exact operand name | Deferred evaluation domain; cannot pass the future gate |
| N-79 | A concrete `COUNT_AT_LEAST` requirement is proposed before WP3 confirms manifest-entry identity, duplicate, conflict, and count semantics | Deferred evaluation domain; cannot pass the future gate |
| N-80 | Determinism conformance is missing, qualified, conditional, waived, or differs from `CONFORMS_TO_PORTFOLIO_DETERMINISTIC_CALCULATION` | Required declaration failure; reject |

## 11. Expected aggregate conclusion

Every vector above fails closed without:

- a fallback or substitute;
- a partial applicability or partial gate result;
- a Degraded State invented by WP2;
- a runtime or production side effect; or
- reinterpretation of any frozen M1–M42 or M43-WP1 authority.
