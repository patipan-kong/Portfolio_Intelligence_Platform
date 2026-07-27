# M42-WP5 — Benchmark & Portfolio Base Currency Ownership Validation

**Document role:** Architecture Review ownership and admission validation

**Milestone:** M42 — Portfolio Intelligence Foundation

**Work package:** M42-WP5

**Validation date:** 2026-07-27

**Validation status:** `COMPLETE — SCOPE NARROWED`

**Authority posture:** M42 Architecture, M42-WP1, M42-WP2, M42-WP3, and the
M42-WP4 ownership investigation are accepted as complete and frozen under the
session mandate. This document cites that authority and does not reopen it.

**Contract-design authority:** `NONE`

**Implementation authority:** `NONE`

**Scope fence:** This document validates ownership, canonical status,
admission disposition, and work-package authority only. It defines no
contract, schema, runtime, persistence, API, serialization, implementation,
provider mapping, calculation, or enforcement behavior.

---

## 1. Executive Assessment

The two concepts are individually admissible, but **not as one
single-owner WP5 contract**.

| Candidate requested by WP5 | Canonical result | Disposition | Constitutional owner | Ownership proven? | WP5 contract authority |
| --- | --- | --- | --- | --- | --- |
| Benchmark, meaning the portfolio's declared comparison choice | **Portfolio Benchmark Declaration**; the bare word **Benchmark** remains reserved for Market Intelligence's observation type | **`ADMIT` under the confirmed compound name**; the historical WP1 disposition is `RENAME` because bare-name admission was invalid | Portfolio Intelligence | Yes, by confirmed M42-WP1 | **Yes, but only for a separately governed Portfolio Benchmark Declaration contract and only within the confirmed admission** |
| Portfolio Base Currency | **Portfolio Base Currency** | **`ADMIT`**, corrected by WP1 from an earlier proposed `REUSE` | Ledger & Accounting | Yes, by confirmed M42-WP1 and confirmed in M42-WP2 | **No.** Its contract was allocated to and completed by M42-WP2 |

The current canonical presence of both entries in
[GLOSSARY.md](../GLOSSARY.md) does not convert either historical candidate
disposition to `REUSE`. Both are present because confirmed WP1 admitted them.
Downstream documents reuse those confirmed meanings; their admission
classification remains the one established at WP1.

The original M42 Architecture correctly blocked the Base-Currency leg pending
owner proof. That proof now exists. It did not place the concept under
Portfolio Intelligence or unblock it inside WP5; it placed the coordinate
under Ledger & Accounting and routed its contract obligation to WP2.
M42-WP2 is complete and confirmed.

Accordingly:

- the portfolio benchmark declaration may proceed through WP5 under Portfolio
  Intelligence;
- Portfolio Base Currency must be excluded from WP5 contract design and cited
  only at its frozen WP1/WP2 meaning; and
- no Portfolio Base Currency ownership investigation remains open.

---

## 2. Benchmark Ownership Analysis

### 2.1 Canonical identity and disposition

The original M42 proposal used the shorthand **Benchmark**. Confirmed M42-WP1
found that the bare term already carries a different frozen meaning:
[Market Data Platform](../architecture/MARKET_DATA_PLATFORM.md) §7 and
[Provider Interface](../architecture/PROVIDER_INTERFACE.md) use Benchmark for
a Market Intelligence-owned canonical observation type and its provider/cache
surface.

Platform Architecture §12, V1 requires one term, one meaning, and one home.
WP1 therefore did not admit the portfolio declaration under the bare name. It
admitted the concept under the non-colliding compound name **Portfolio
Benchmark Declaration**, which now exists in the canonical Glossary.

For the outcome vocabulary allowed by this investigation:

- the portfolio-declaration concept is **`ADMIT`**, already confirmed under
  the required compound name;
- it is not `REUSE`, because no canonical term named the portfolio-scoped
  declaration before WP1;
- it is not `REJECT`, because the corrected concept passed ownership and
  admission; and
- the bare word Benchmark must never be used as an abbreviation for the
  Portfolio Benchmark Declaration.

The exact frozen WP1 record calls the corrective disposition `RENAME`. That
label records why the original candidate name could not be admitted; it does
not change the concept's successful admission under its compound name.

### 2.2 Constitutional owner

**Portfolio Intelligence is the proven owner.**

The coordinate records one portfolio's declared comparison choice. It is
descriptive portfolio meaning, not a market observation, accounting fact, or
decision constraint. Confirmed WP1 ran the five-part ownership-boundary gate
and established one term, one meaning, and one home under Portfolio
Intelligence.

Market Intelligence remains the owner of any referenced canonical Benchmark
observation series. The declaration cites that series without owning,
redefining, deriving, pricing, or maintaining it. The compound name is the
constitutional boundary between:

- **Benchmark** — the Market Intelligence observation type; and
- **Portfolio Benchmark Declaration** — the Portfolio Intelligence-owned
  portfolio choice.

### 2.3 Relationship to Portfolio Strategy Metadata

Portfolio Strategy Metadata is the Portfolio Intelligence-owned umbrella for
metadata describing a portfolio as an investment-strategy container.
Confirmed WP1 places Portfolio Benchmark Declaration as a **sibling declared
coordinate beside that umbrella**, analogous to the separately admitted
Investment Universe coordinate. It is compatible with Portfolio Strategy
Metadata but does not redefine it.

This relationship does not transfer ownership of the referenced Benchmark
series from Market Intelligence and does not pull Decision Policy or
accounting truth into Portfolio Strategy Metadata.

### 2.4 Decision Intelligence boundary

There is no overlap with Decision Intelligence for the confirmed declaration.
It states a comparison choice and carries no recommendation, policy envelope,
portfolio limit, target-allocation decision, constraint verdict, optimizer
behavior, or execution preference.

Confirmed WP1 withheld the proposed Policy-derived form because its
target-allocation input had no proven owner and touched Decision
Intelligence-adjacent territory. That withheld form remains unavailable to
WP5. Its exclusion is what preserves the clean ownership result; WP5 may not
use the admitted declaration as a route around the rejected Portfolio Policy
or around Decision Intelligence's frozen ownership.

### 2.5 Ledger & Accounting boundary

There is no overlap with Ledger & Accounting. The declaration belongs to one
Portfolio Identity and may cite its Accounting Scope, but it does not:

- establish or alter Portfolio Identity or Accounting Scope;
- record a transaction, holding, cash balance, or accounting event;
- define Portfolio Base Currency;
- calculate NAV or returns; or
- rewrite historical financial truth.

Subject-scoping by a Ledger-owned identity is a reference relationship, not
an ownership transfer.

### 2.6 Contract authority

M42 has authority for a future WP5 **Portfolio Benchmark Declaration**
contract because:

1. the concept was admitted and its owner proven by confirmed WP1;
2. the M42 Architecture already allocated the surviving benchmark-declaration
   leg to WP5; and
3. the post-WP1 roadmap reconciliation narrows WP5 to that leg.

This validation does not begin or design that contract. It grants no runtime,
provider, persistence, API, serialization, calculation, or implementation
authority.

---

## 3. Portfolio Base Currency Ownership Analysis

### 3.1 Canonical identity and disposition

Portfolio Base Currency now exists as an exact canonical Glossary entry.
Its governing disposition is **`ADMIT`**, not `REUSE`.

Confirmed WP1 found that neither Portfolio Identity nor Accounting Scope had
previously named this coordinate. WP1 therefore admitted it as a new,
distinctly named coordinate within Ledger & Accounting's constitutional
purview. The earlier `REUSE` theory was corrected because adjacency to
existing Ledger-owned concepts is not proof that their definitions silently
contained the coordinate.

Ownership is already proven. M42-WP2 then carried the admitted coordinate into
its separately governed contract, passed independent review and final
confirmation, synchronized the Glossary, and closed `COMPLETE AND CONFIRMED`.

### 3.2 Constitutional owner

**Ledger & Accounting is the sole proven owner.**

Portfolio Base Currency is an accounting-identity-adjacent unit-of-account
coordinate for one Portfolio Identity. It is not strategy metadata, a policy
choice, a market observation, or a display setting. Portfolio Intelligence
may cite and compose it at its frozen meaning but acquires no authority to
define, default, infer, mutate, or reinterpret it.

### 3.3 Distinction from Currency

**Currency** in the Investment Universe vocabulary is an Asset
Foundation-owned currency-of-denomination classification and its values.
It describes an asset-side fact that other domains may cite.

**Portfolio Base Currency** is the Ledger & Accounting-owned portfolio
coordinate that identifies the unit of account associated with one Portfolio
Identity. It references Asset Foundation's currency vocabulary without
redefining or owning that vocabulary.

The owner and semantic question differ:

| Concept | Question answered | Owner |
| --- | --- | --- |
| Currency / currency-of-denomination value | What currency classification or denomination does the referenced asset-side fact carry? | Asset Foundation |
| Portfolio Base Currency | What is the explicit portfolio-level unit-of-account coordinate for this Portfolio Identity? | Ledger & Accounting |

Neither concept is an FX rate, conversion, provider code, or computed monetary
value.

### 3.4 Distinction from Accounting Scope

Accounting Scope is the boundary to which a portfolio's holdings,
transactions, cash, and balances belong. Portfolio Base Currency is a separate
coordinate adjacent to that boundary.

They share a constitutional owner but are not synonyms:

- Accounting Scope answers **which accounting boundary** owns the financial
  facts.
- Portfolio Base Currency answers **which explicit currency reference** is
  the portfolio's unit-of-account coordinate.

WP1 admitted Portfolio Base Currency precisely because the existing
Accounting Scope definition did not already include that meaning. Admission
therefore adds a distinct named coordinate without redefining Accounting
Scope.

### 3.5 Distinction from Investment Universe Currency

An Investment Universe Currency criterion is an inert statement of intended
holding scope that cites Asset Foundation-owned currency-of-denomination
values. Portfolio Intelligence owns the declaration's citation, while Asset
Foundation retains ownership of the category and values.

Portfolio Base Currency is not a universe criterion and supplies no implicit
criterion value. The confirmed WP3 boundary states that the two must not
default, copy, constrain, convert, or reinterpret one another.

| Concept | Semantic role | Owner |
| --- | --- | --- |
| Investment Universe Currency criterion | Inert intended-scope criterion using cited asset-denomination values | Portfolio Intelligence owns the declaration; Asset Foundation owns the cited currency category and values |
| Portfolio Base Currency | Portfolio accounting/unit-of-account coordinate | Ledger & Accounting |

Adjacency in a future Portfolio Composition is citation only and cannot merge
the concepts.

### 3.6 Contract authority and blocking status

WP5 **may not define** the Portfolio Base Currency contract.

The original architecture made that leg conditional on WP1 proving its owner.
WP1 proved an owner outside WP5's Portfolio Intelligence scope and explicitly
routed the coordinate to M42-WP2. WP2 has already completed and confirmed the
contract. A second WP5 contract would duplicate frozen authority and violate
the one-implementation/one-definition discipline.

Therefore:

- ownership investigation does **not** continue;
- Portfolio Base Currency does **not** remain blocked;
- its disposition is confirmed `ADMIT` under Ledger & Accounting;
- its contract authority is already exhausted by frozen M42-WP2; and
- WP5 has citation-only authority for the coordinate when boundary clarity
  requires it.

---

## 4. Admission Analysis

### 4.1 Independent admission results

| Test | Portfolio Benchmark Declaration | Portfolio Base Currency |
| --- | --- | --- |
| Exact concept existed before WP1 | No | No |
| Confirmed WP1 disposition | `RENAME`, producing admission under the full compound name | `ADMIT`, corrected from `REUSE` |
| Outcome under this investigation's allowed labels | **`ADMIT`** | **`ADMIT`** |
| Current canonical entry | Yes | Yes |
| Proven owner | Portfolio Intelligence | Ledger & Accounting |
| Another authority owns adjacent meaning | Market Intelligence owns the referenced bare Benchmark observation series | Asset Foundation owns referenced Currency vocabulary; Ledger already owns adjacent Identity and Accounting Scope |
| Semantic overlap after frozen carve-outs | None; bare-name collision resolved and Decision-adjacent Policy-derived form withheld | None; distinct from Currency, Accounting Scope, and Investment Universe Currency |
| M42 contract authority | Yes, through the narrowed WP5 benchmark-declaration leg | Yes in M42 generally, but already allocated to and completed by WP2; none remains for WP5 |
| Blocking state | Unblocked for its separately governed WP5 contract | Not blocked; complete and frozen under WP2 |

### 4.2 Can both concepts remain in one WP5 contract?

**No.**

The original combined title represented an architecture-stage contingency,
not proof of shared ownership. The confirmed ownership results split the
concepts across Portfolio Intelligence and Ledger & Accounting. The
Architecture's own conditional branch and the post-WP1 reconciliation resolve
that contingency without amending frozen architecture:

- the Base-Currency leg leaves WP5 and is carried by WP2; and
- WP5 narrows to the Portfolio Benchmark Declaration leg.

A combined contract would either give Portfolio Intelligence false authority
over a Ledger coordinate or create a cross-owner contract with no single
semantic owner. Both are constitutionally inadmissible.

### 4.3 Admission versus downstream reuse

Because both concepts are now in the Glossary, a downstream reader **reuses**
their canonical meanings. That operational fact must not be confused with
their candidate dispositions:

- Portfolio Benchmark Declaration was newly admitted through WP1's required
  `RENAME`;
- Portfolio Base Currency was newly `ADMIT`ted by WP1; and
- neither candidate's historical disposition is retroactively changed to
  `REUSE`.

---

## 5. Recommendation

1. Retitle the executable scope of M42-WP5 to **Portfolio Benchmark
   Declaration Contract**, without editing the frozen M42 Architecture.
2. Permit a separately governed WP5 contract phase only for the confirmed
   Portfolio Benchmark Declaration admission and only under Portfolio
   Intelligence.
3. Never abbreviate Portfolio Benchmark Declaration to bare Benchmark. Cite
   the Market Intelligence Benchmark observation type only at its frozen
   meaning.
4. Preserve the confirmed Decision Intelligence and Ledger & Accounting
   exclusions. In particular, do not introduce the withheld Policy-derived
   benchmark form or any accounting semantics.
5. Remove Portfolio Base Currency from WP5's contract-design scope. Reuse it
   by citation only from confirmed M42-WP1/M42-WP2 authority.
6. Do not continue a Portfolio Base Currency ownership investigation and do
   not label the coordinate blocked. Its admission, owner, contract, and
   confirmation are complete.
7. Create no schema, runtime, persistence, API, serialization, provider, or
   implementation authority from this ownership validation.

---

## 6. Final Verdict

### Benchmark

**Verdict: `ADMIT` under the canonical name Portfolio Benchmark Declaration.**

- **Owner:** Portfolio Intelligence.
- **Canonical status:** already synchronized following confirmed WP1.
- **Portfolio Strategy Metadata relationship:** compatible sibling declared
  coordinate; not a redefinition.
- **Decision Intelligence overlap:** none within the confirmed admission; the
  Policy-derived form remains withheld.
- **Ledger & Accounting overlap:** none; identity/scope are citations only.
- **WP5 contract authority:** yes, for a future separately governed Portfolio
  Benchmark Declaration contract only.
- **Bare Benchmark:** reserved for Market Intelligence's canonical
  observation type and forbidden as an abbreviation for this declaration.

### Portfolio Base Currency

**Verdict: `ADMIT` under Ledger & Accounting; not a WP5 contract subject.**

- **Owner:** Ledger & Accounting.
- **Canonical status:** admitted by confirmed WP1 and contracted and confirmed
  by M42-WP2.
- **Distinctions:** not Asset Foundation Currency, not Accounting Scope, and
  not an Investment Universe Currency criterion.
- **Ownership investigation:** complete; no further investigation required.
- **Blocking state:** not blocked.
- **WP5 contract authority:** none; citation only.

### Work-package verdict

**The original combined Benchmark & Base-Currency contract may not proceed as
one WP5 contract. M42-WP5 may proceed only as the Portfolio Benchmark
Declaration contract work package.**

**Final status:** `COMPLETE — OWNERSHIP VALIDATED; WP5 SCOPE NARROWED`
