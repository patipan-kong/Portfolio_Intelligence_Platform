# M42-WP2 — Independent Confirmation

**Document role:** Independent Governance Review Board

**Confirmation target:** [M42-WP2 Portfolio Identity, Accounting Scope,
Membership & Base Currency Contract Specification](M42_WP2_PORTFOLIO_IDENTITY_ACCOUNTING_SCOPE_MEMBERSHIP_AND_BASE_CURRENCY_CONTRACT_SPECIFICATION.md)

**Review basis:** The six required corrections recorded in
[M42-WP2 Independent Governance Review](M42_WP2_INDEPENDENT_REVIEW.md),
IR-1 through IR-6.

**Mandate limit:** This is Independent Confirmation only. It does not perform
another Independent Review, redesign M42, reopen the Architecture Proposal or
M42-WP1, author replacement text, or grant implementation, runtime,
persistence, provider, API, production, or executable-validation authority.

---

## Unresolved findings

### IR-1 — Fact cardinality vs. Portfolio Membership cardinality

The correction properly removes the direct cardinality collision: it confines
the one-Accounting-Scope invariant to accounting facts and expressly preserves
Portfolio Membership's frozen one-or-more cardinality. It does so, however, by
introducing and normatively defining **“holding-record”** / **“holding-record
entry”** as the category that resolves to one Accounting Scope.

That term is not a frozen M34 coordinate, is not present in the canonical
Glossary, and is not merely an ordinary unqualified description: section 5.4
bolds and defines it as the distinction that makes the cardinality rule work.
The prior IR-1 correction required the distinction to use only frozen
vocabulary. As written, the correction resolves the conflict by creating an
unnamed semantic sibling rather than by a citation-only distinction. This is
also inconsistent with the requested no-new-governed-vocabulary confirmation
condition.

**Evidence:** WP2 §5.4; Platform Architecture V1–V2; M34-D-0003 and the
canonical `GLOSSARY.md` “Portfolio Membership” entry.

### IR-4 — Worked example / calculation-boundary correction

Section 6.4 is now purely semantic and no longer specifies an FX lookup,
conversion step, or computation-time behavior. The same IR-4 defect remains
elsewhere in the contract, however. Section 0 says Base Currency is the unit
coordinate “those formulas are parameterized by,” and the compatibility matrix
in section 8 says the frozen formulas “implicitly require” that coordinate.

The frozen Portfolio Calculation Rules contain neither a Base Currency
parameter nor an FX/currency operand. The earlier required correction expressly
covered sections 0 and 8 as well as the worked example, so these residual
assertions keep the contract from being mutually truthful about the frozen
formula without amending it.

**Evidence:** WP2 §0 item 5 and §8 row `PORTFOLIO_CALCULATION_RULES.md`;
Portfolio Calculation Rules §9; M42-WP2-IR-4.

---

REQUIRED CORRECTIONS REMAIN

