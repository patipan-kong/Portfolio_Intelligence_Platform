# M42-WP2 — Independent Governance Review

**Document role:** Independent Governance Review Board

**Review target:** [M42-WP2 Portfolio Identity, Accounting Scope, Membership &
Base Currency Contract Specification](M42_WP2_PORTFOLIO_IDENTITY_ACCOUNTING_SCOPE_MEMBERSHIP_AND_BASE_CURRENCY_CONTRACT_SPECIFICATION.md)

**Review date:** 2026-07-24

**Mandate:** Independent review only. This review does not redesign M42, reopen
M42-WP1, author replacement contract text, or grant implementation, runtime,
persistence, provider, API, production, or executable-validation authority.

**Operating authority:** Platform Architecture, M34, M36, the M39–M41 corpus,
the M42 Architecture Proposal, the confirmed M42-WP1 dispositions, and the
M42-WP1 Roadmap Reconciliation are treated as frozen and authoritative as
directed by the review mandate. The repository discrepancies concerning the
recording of that authority are reviewed separately below and are not used to
re-litigate a frozen disposition.

**Final determination:** **APPROVED WITH REQUIRED CORRECTIONS**

**Implementation authority:** `NONE`

---

## 1. Executive determination

M42-WP2 preserves the primary ownership allocation: Ledger & Accounting owns
Portfolio Identity, Accounting Scope, Portfolio Membership, and Portfolio Base
Currency; Portfolio Intelligence receives no ownership of those coordinates.
The contract also correctly excludes Investment Universe content, lifecycle
transition authority, derived measures, ambient currency defaults, and live FX
values from the Base Currency coordinate.

The specification is not yet confirmable as written. Six required corrections
remain:

1. the boundary-integrity clause does not constitutionally distinguish a
   single-scope accounting fact from the holding or instrument that frozen
   Portfolio Membership permits to belong to one or more Accounting Scopes;
2. the mirrored-ledger-event sentence elevates descriptive Level-4 language
   into a normative cross-portfolio transfer rule;
3. the purported exact currency-reference format does not actually identify
   an exact reference format and overstates the currently registered Asset
   Foundation vocabulary;
4. the worked example authors an FX lookup and conversion behavior absent from
   the frozen Portfolio Calculation Rules;
5. the Non-owner discipline incorrectly says Portfolio Intelligence may not
   carry Base Currency, conflicting with the confirmed Portfolio Composition
   input and with the same specification's WP7 handoff; and
6. the specification relies on Portfolio Base Currency as confirmed canonical
   vocabulary while its confirmation-required Glossary registration is absent.

These defects are bounded and correctable without redesigning M42 or reopening
WP1, so rejection is not warranted.

---

## 2. Findings

### M42-WP2-IR-1 — Fact cardinality is not reconciled with Membership cardinality

**Classification:** REQUIRED CORRECTION

M42 Architecture validly freezes boundary integrity as “one Accounting Scope
per fact.” M34-D-0003 and the canonical Glossary separately freeze Portfolio
Membership as the Ledger fact that a **holding or instrument** belongs to “one
or more” Portfolio Accounting Scopes.

Section 5.4 of the reviewed specification lists “every holding” among the
portfolio-scoped facts that must resolve to exactly one Accounting Scope and
then declares anything resolving to more than one scope invalid. Section 5.3
repeats the frozen one-or-more Membership cardinality. The document never
states the constitutionally necessary distinction among:

- an individual accounting fact recorded inside one Accounting Scope;
- a holding or instrument that may be related to multiple scopes; and
- the Portfolio Membership relation recording that belonging.

Consequently, the same noun “holding” bears incompatible cardinalities inside
one contract. The core one-scope-per-fact invariant is supported, but its
application to holdings is not precise enough to show that M34-D-0003 remains
unchanged. The contract must reconcile these categories using only frozen
vocabulary and without narrowing Portfolio Membership or manufacturing a new
ownership rule.

**Governing authority:** M42 Architecture Proposal §§2 and 6; M34-D-0003;
`GLOSSARY.md` entries “Portfolio Membership” and “Accounting Scope.”

### M42-WP2-IR-2 — Mirrored-ledger-event language becomes a new normative transfer rule

**Classification:** REQUIRED CORRECTION

The replay-never-crosses-a-boundary invariant itself is supported by the
confirmed M42 Architecture Proposal and is a proper WP2 contract subject.
Section 5.5 goes further: it normatively requires money moving between
portfolios to cross as explicit, mirrored ledger events “on both sides.”

That sentence comes from the Portfolio Domain Model, which section 1.1 of WP2
correctly identifies as descriptive context rather than frozen or canonical
authority. Neither M34-D-0002/0003 nor the canonical Glossary defines a
mirrored event pair, its two-sided completeness rule, or a cross-portfolio
transfer protocol. The M42 Architecture authorizes WP2 to state replay
isolation, not to freeze a new transfer mechanism. Elevating the descriptive
sentence into a “Constitutional constraint” therefore creates normative
behavior from a lower-level citation.

The replay invariant may remain, but WP2 must not make the mirrored transfer
model a new WP2 rule.

**Governing authority:** Platform Architecture G1–G4; M42 Architecture
Proposal §6 and Negative Corpus; WP2 §1.1; Portfolio Domain Model §§1–2.

### M42-WP2-IR-3 — The exact currency-reference-format obligation is not discharged

**Classification:** REQUIRED CORRECTION

WP1 requires WP2 to supply an **exact currency-reference format**. Section 6.2
states only that the value names exactly one currency drawn from “the same
closed currency vocabulary Asset Foundation already uses.” It does not
identify the canonical reference kind, identity shape, or exact registered
vocabulary entry that two independent readers must use.

The cited Asset Foundation material establishes “currency of denomination” as
an Asset Classification dimension. The canonical `Unit Semantics` entry says
how a kind is counted. Neither cited text publishes the closed currency
reference list or makes Asset Classification itself a currency-code format.
Thus section 6.2 correctly assigns the upstream owner and forbids a parallel
taxonomy, but it does not provide the promised exact format and it conflates a
classification dimension with the reference vocabulary.

This is a contract-completeness defect, not a challenge to WP1's admitted
owner, subject, or one-currency-per-Portfolio-Identity rule.

**Governing authority:** M42-WP1 register §6.4, especially Permitted Inputs and
Future Contract Acceptance Evidence; `asset_foundation.md` §§2–3;
`GLOSSARY.md` entries “Asset Classification” and “Unit Semantics.”

### M42-WP2-IR-4 — The worked example authors new FX-enabled NAV behavior

**Classification:** REQUIRED CORRECTION

Section 6.4 says that a USD holding under a THB Base Currency is converted to
THB “inside the frozen NAV computation,” using a canonical FX observation
looked up “at computation time.” The frozen Portfolio Calculation Rules do not
state a Base Currency parameter, an FX operand, a currency-conversion step, or
an FX lookup. Their frozen NAV formula is `cash_balance + equity_value`, with
equity value defined as shares multiplied by current price.

The example therefore does more than distinguish a unit reference from a live
FX value. It assigns a new input and conversion behavior to a frozen
calculation and implies runtime lookup semantics. Market Intelligence's
ownership of canonical FX observations does not by itself authorize WP2 to
insert those observations into Ledger & Accounting arithmetic.

Portfolio Base Currency may name the reporting unit exactly as WP1 admitted.
WP2 may not claim that the existing calculation rules already consume it or
specify how an FX conversion is performed. Sections 0, 6.2, 6.4, 8, and
Acceptance Criterion 5 must be made mutually truthful without changing the
frozen formula.

**Governing authority:** M42-WP1 register §6.4; Portfolio Calculation Rules
§9; M42 Architecture Proposal Negative Corpus; WP2 §§2 and 10.

### M42-WP2-IR-5 — Non-ownership is incorrectly expanded into a no-carriage rule

**Classification:** REQUIRED CORRECTION

Section 6.6 says Portfolio Intelligence “does not own, does not carry, and may
not redefine” Portfolio Base Currency. Non-ownership and non-redefinition are
correct. The no-carriage assertion is not.

The confirmed WP1 Portfolio Composition record permits Portfolio Base Currency
as a cited input, the M42 Architecture assigns the terminal Composition to
Portfolio Intelligence, and WP2 §9 itself permits WP7 to cite Base Currency.
A Portfolio Intelligence-owned composition may therefore carry an exact
Ledger & Accounting reference without acquiring ownership. Treating carriage
as ownership both narrows the confirmed WP7 input and contradicts this
specification's own downstream consequence.

The correction must preserve Ledger & Accounting ownership while allowing the
already-confirmed citation/carriage boundary.

**Governing authority:** M42-WP1 register §§6.4–6.5; M42 Architecture Proposal
Components B and G; WP2 §§6.6 and 9.

### M42-WP2-IR-6 — Required canonical Glossary registration is absent

**Classification:** REQUIRED CORRECTION

WP1's confirmed `ADMIT` disposition requires “Portfolio Base Currency” to be
added to `GLOSSARY.md` in the same change in which confirmation is recorded.
WP2's front matter says that synchronization was performed at WP1 confirmation
and is not repeated here. No “Portfolio Base Currency” entry exists in the
current Glossary.

This is not a reason to reopen WP1's admitted owner or disposition. It is,
however, a present V2 defect: WP2 and its downstream consumers rely on a new
canonical noun that the repository's canonical vocabulary does not register.
Unlike the missing review-record files discussed in M42-WP2-IR-7, this gap is
part of WP1's substantive confirmation condition and must be closed before WP2
can be independently confirmed.

**Governing authority:** Platform Architecture V1–V2; M42-WP1 register §6.4
Glossary Synchronization Requirement; WP2 front matter and §11.

### M42-WP2-IR-7 — Architecture/WP1 confirmation records are absent or stale on disk

**Classification:** OBSERVATION

The repository shows all three current M42 upstream documents as added rather
than committed. The M42 Architecture Proposal still reports `READY FOR
INDEPENDENT ARCHITECTURE REVIEW`; no M42 Architecture Independent Review or
Independent Confirmation artifact is present. The WP1 register still reports
`READY_FOR_INDEPENDENT_CONFIRMATION`; no WP1 Independent Confirmation artifact
is present. The Roadmap Reconciliation still reports itself provisional
pending WP1 confirmation.

These are real governance-chain and repository-hygiene gaps; WP2's own
characterization is not independently demonstrated by the repository. Under
the explicit review instruction that M42 Architecture and M42-WP1 are complete,
confirmed, frozen, and authoritative, the missing record files do not block
this review from relying on those authorities and do not permit their
substance to be reopened. They should nevertheless be recorded so the
repository independently demonstrates the authority chain it asserts.

This observation does not include the missing Base Currency Glossary entry,
which is a separate required correction because WP1 made same-change
registration a substantive confirmation condition.

### M42-WP2-IR-8 — Recorded-change language is partly admitted and does not name a new lifecycle transition

**Classification:** OBSERVATION

The requirements to set Base Currency at portfolio creation, change it only by
an explicit recorded event, and preserve historical meaning are present in
WP1's admitted exact definition and constitutional constraints. Requiring an
effective point expresses the forward-only semantic application necessary to
avoid retroactive reinterpretation. The specification does not name a new
canonical event type, command, workflow, lifecycle state, lifecycle
transition, schema, or storage representation.

Accordingly, §§6.1–6.3 do not by themselves authorize a runtime or persistence
implementation. This conclusion does not cure M42-WP2-IR-4: an FX lookup “at
computation time” is a separate, newly asserted computation behavior.

### M42-WP2-IR-9 — Rejected candidates occur only in negative statements

**Classification:** OBSERVATION

Portfolio Policy and Investment Universe Membership occur textually in §§3,
7, and 10, despite Acceptance Criterion 6 saying they must not “appear
anywhere.” Each occurrence is an exclusion; neither is reintroduced as a
field, input, rule, or owned concept. The substantive negative-corpus
requirement passes. The acceptance criterion's literal wording is imprecise,
but it does not create semantic leakage.

---

## 3. Criteria determination

| Review criterion | Determination |
|---|---|
| Scope and ownership | **PASS WITH REQUIRED CORRECTIONS.** Ledger & Accounting remains owner; no Portfolio Intelligence ownership leakage. IR-5 corrects carriage/ownership conflation. |
| Reuse-only discipline | **FAIL AS WRITTEN.** The cited definitions in §§5.1–5.3 are faithful, but IR-1 and IR-2 add unresolved cardinality and transfer behavior. |
| Boundary-integrity invariant | **FAIL AS WRITTEN.** The invariant is frozen by M42 Architecture, but its application to “holding” is not reconciled with M34-D-0003. |
| Replay-never-crosses-a-boundary invariant | **FAIL AS WRITTEN.** Replay isolation is supported; the mirrored-event rule is not frozen authority. |
| Portfolio Base Currency contract | **FAIL AS WRITTEN.** Owner, subject, single-currency cardinality, no-default rule, no-rate content, and historical-meaning preservation pass; exact format and calculation separation fail under IR-3 and IR-4. |
| Recorded-change/event boundary | **PASS.** The high-level change semantics are admitted by WP1 and do not name a new lifecycle or runtime mechanism; see IR-8. |
| Constitutional and vocabulary compliance | **FAIL AS WRITTEN.** V1 ownership is preserved, but V2 registration is incomplete and a descriptive citation is elevated in IR-2. |
| Downstream consequences | **PASS WITH REQUIRED CORRECTION.** WP3 receives no Universe content, WP5 receives no Base Currency ownership, WP6 retains lifecycle authority, and WP7 receives no derived value; IR-5 must restore permitted citation/carriage. |
| Governance and repository consistency | **PASS FOR REVIEW RELIANCE, WITH ONE SUBSTANTIVE CORRECTION.** The explicit operating instruction makes stale/missing confirmation records non-blocking observations; the missing WP1-required Glossary entry remains blocking under IR-6. |

---

## 4. Acceptance-criterion verification

| §10 criterion | Result | Basis |
|---:|---|---|
| 1 | **NOT CONFIRMED** | IR-1 leaves Membership cardinality unresolved. |
| 2 | **NOT CONFIRMED** | The core invariants are inherited, but IR-2 adds a mirrored transfer rule. |
| 3 | **CONFIRMED** | Owner, `ADMIT`, and five-part-gate result match WP1 §6.4. |
| 4 | **NOT CONFIRMED** | IR-3 does not discharge exact format; IR-4 adds unadmitted calculation behavior. |
| 5 | **NOT CONFIRMED** | Section 6.4 parameterizes frozen NAV with an unstated FX conversion and lookup. |
| 6 | **CONFIRMED IN SUBSTANCE** | Rejected/unresolved candidates appear only as exclusions; see IR-9. |
| 7 | **CONFIRMED** | No lifecycle state, transition vocabulary, legitimacy rule, command, or workflow is authored. |
| 8 | **NOT CONFIRMED AS A WHOLE** | Formal authority fields remain `NONE`, but IR-4 nevertheless states computation-time lookup behavior. |

Because criteria 1, 2, 4, 5, and 8 are not independently confirmable, the
specification cannot proceed to Independent Confirmation in its current form.

---

## 5. Downstream boundary verification

- **M42-WP3:** No Investment Universe definition, membership predicate,
  evaluation, validation, or refusal semantics are supplied by WP2.
- **M42-WP5:** Portfolio Base Currency remains a Ledger & Accounting
  coordinate. WP5 may cite it and may not acquire ownership.
- **M42-WP6:** Portfolio Lifecycle State, its vocabulary, and all transition
  legitimacy remain outside WP2.
- **M42-WP7:** WP2 supplies only frozen Ledger coordinates and the admitted
  Base Currency unit reference. It supplies no rate, converted NAV, derived
  measure, verdict, policy, or membership-evaluation semantics. IR-4 must be
  corrected so the worked example does not become an unauthorized derived
  computation; IR-5 must be corrected so exact citation/carriage remains
  possible.

---

## 6. Authority determination

| Authority axis | Review result |
|---|---|
| Implementation | `NONE` |
| Runtime | `NONE` |
| Provider | `NONE` |
| Persistence | `NONE` |
| API | `NONE` |
| Production | `NONE` |
| Executable validation | `NONE` |

This review grants none of those authorities. It authorizes no code, schema,
event implementation, FX mechanism, calculation change, migration, or
production adoption.

---

## 7. Final determination

APPROVED WITH REQUIRED CORRECTIONS

