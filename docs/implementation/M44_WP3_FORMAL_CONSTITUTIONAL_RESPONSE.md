# M44-WP3 — Formal Constitutional Response

**Milestone:** M44 — Portfolio Analytics Gate Closure and Normative Semantics Foundation

**Work package:** M44-WP3 only

**Responds to:** [M44-WP3 Independent Constitutional Review](M44_WP3_INDEPENDENT_CONSTITUTIONAL_REVIEW.md)

**Corrected artifact:** [M44-WP3 Period-Return Ownership Governance Correction](M44_WP3_PERIOD_RETURN_OWNERSHIP_GOVERNANCE_CORRECTION.md) RC2

**Status:** `CORRECTIONS IMPLEMENTED — SUBMITTED FOR RENEWED INDEPENDENT REVIEW`

**Record date:** 2026-07-29

**Confirmation issued:** `NO`

**Freeze performed:** `NO`

---

## 1. Response scope and constitutional effect

This response accepts and addresses each constitutional finding `F-01` through
`F-05` from the independent review of RC1. It also records an explicit
disposition for each non-blocking editorial observation `F-06` through `F-08`.

This response does not resolve any finding by its own authority. It records
that corrections have been implemented in RC2 and submits the corrected
package for renewed independent constitutional review. Confirmation remains
ineligible unless renewed review and the later independent confirmation
sequence establish unresolved findings `NONE`
([M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §§12.4 and
16.2–16.5).

The response has no runtime, implementation, production, frozen-artifact
amendment, gate-closure, step-4-recording, downstream-authorization,
confirmation, freeze, or closeout authority.

## 2. F-01 — Mandatory extension-basis declaration absent

| Field | Response |
| --- | --- |
| Finding identifier and classification | `F-01 — MAJOR` |
| Disposition | `ACCEPTED` |
| Reviewer concern | RC1 invoked frozen M44 Architecture §5.3 while failing to name its sole extension basis, quote the exact frozen sentence supplying that basis, or rule out the other bases, contrary to `INV-C2`. |
| Controlling authority | Frozen [M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) §5.3 `E-3` and §6 `INV-C2`; §16.2; `INV-A2`. |
| Exact corrective action | Added a normative `Extension basis` section naming `E-3` as the sole basis; quoted the exact §5.3 sentence including the express `(G-2)` allocation; stated that §5.3 assigns rather than WP3 self-selects the basis; ruled `E-1` and `E-2` inapplicable with reasons; prohibited reliance on unstated silence; connected `E-3` to the exact M43 §8 row; and added a matching acceptance criterion. |
| Exact RC2 section changed | RC2 §4; RC2 §18 `Extension basis` acceptance row; downstream sections renumbered consistently. |
| Constitutional effect | RC2 now declares the complete assigned authority chain for its later-record supersession without extending the scope of `G-2` or amending a frozen source. |
| Verification evidence | RC2 §4 names `E-3`, reproduces the frozen sentence beginning “It supports supplying a repository-local record” and ending “defective frozen row (G-2),” rules out `E-1` and `E-2`, cites §5.3 and `INV-C2`, and identifies RC2 §§5 and 7 as the row and superseding ruling. RC2 §18 contains the corresponding criterion. |
| Renewed-review requirement | `YES` — the correction is submitted for renewed independent review and is not resolved by this response. |

## 3. F-02 — Citation to a non-existent section

| Field | Response |
| --- | --- |
| Finding identifier and classification | `F-02 — MINOR` |
| Disposition | `ACCEPTED` |
| Reviewer concern | RC1 §1 cited M44-WP2 Freeze Record §§5 and 11 even though the record ends at §8 and those pinpoints do not prove the asserted predecessor state. |
| Controlling authority | [M44-WP2 Freeze Record](M44_WP2_FREEZE_RECORD.md) §4 and §8; frozen M44 Architecture §16.2 and `INV-A2`. |
| Exact corrective action | Replaced the invalid §§5 and 11 citation with §§4 and 8. |
| Exact RC2 section changed | RC2 §1, strict-predecessor evidence paragraph. |
| Constitutional effect | The predecessor assertion now resolves to §4 for `G-1` `CLOSED` and `EFFECTIVE` through completed independent confirmation and §8 for M44-WP2 `COMPLETE AND FROZEN`. No predecessor or gate result changes. |
| Verification evidence | RC2 §1 cites `[M44-WP2 Freeze Record] §§4 and 8`; the cited source contains the stated gate result in §4 and completion/freeze declaration in §8. |
| Renewed-review requirement | `YES` — mechanically required for a corrected citation under frozen M44 Architecture §12.4. |

## 4. F-03 — Accounting semantics subordinated to formula inputs

| Field | Response |
| --- | --- |
| Finding identifier and classification | `F-03 — MINOR` |
| Disposition | `ACCEPTED` |
| Reviewer concern | RC1’s normative ownership table used “including,” which could recast accounting semantics as a subtype of formula inputs rather than a coordinate Ledger & Accounting concern. |
| Controlling authority | Frozen [M43-WP1](M43_WP1_PORTFOLIO_ANALYTICS_VOCABULARY_AND_OWNERSHIP_REGISTER.md) §7.3(2); [Platform Architecture](../architecture/platform_architecture.md) §6.3. |
| Exact corrective action | Replaced “formula inputs, including the accounting semantics” with coordinate wording: “formula inputs, and the accounting semantics.” |
| Exact RC2 section changed | RC2 §6, first ownership-table row. |
| Constitutional effect | Financial truth, canonical formula inputs, and accounting semantics remain distinct coordinate concerns under the same sole owner. No ownership is transferred, duplicated, narrowed, or enlarged. |
| Verification evidence | RC2 §6 first row reads: “Financial truth and the canonical return and metric formulas' inputs, and the accounting semantics that determine what enters period return.” |
| Renewed-review requirement | `YES` — the correction changes a normative allocation row and requires renewed review. |

## 5. F-04 — Effectiveness trigger stated inconsistently

| Field | Response |
| --- | --- |
| Finding identifier and classification | `F-04 — MINOR` |
| Disposition | `ACCEPTED` |
| Reviewer concern | RC1 §11 item 1 could be read as making confirmation and freeze a joint effectiveness trigger, whereas confirmation is the operative event and freeze is a separate D-1 prerequisite. |
| Controlling authority | Frozen M44 Architecture §§8.2, 11 M44-WP3, 17 OQ-5, 4.5, and 12.4; [M44-WP1 Register](M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md) §7 `G-2` row. |
| Exact corrective action | Recast the prerequisite so independent confirmation with unresolved findings `NONE` makes the release-condition discharge and standing-block disposition effective, followed by an express separate requirement that M44-WP3 is frozen. |
| Exact RC2 section changed | RC2 §12 item 1. |
| Constitutional effect | The operative effect is attributed only to confirmation, while freeze remains independently required before D-1 can become reachable. |
| Verification evidence | RC2 §12 item 1 uses “which makes” for confirmation’s effect and then states “also frozen as a separate D-1 prerequisite.” |
| Renewed-review requirement | `YES` — the lifecycle correction is submitted for renewed independent review. |

## 6. F-05 — Residual OPEN state restated incompletely

| Field | Response |
| --- | --- |
| Finding identifier and classification | `F-05 — MINOR` |
| Disposition | `ACCEPTED` |
| Reviewer concern | RC1 omitted the exact owner from its hypothetical `OPEN` description, narrowing the closed vocabulary. |
| Controlling authority | Frozen M44 Architecture §16.2; [M44-WP1 Register](M44_WP1_INHERITED_GATE_INVENTORY_AND_CLOSURE_REGISTER.md) §8.1. |
| Exact corrective action | Restored both mandatory components: the exact missing element and its exact owner. |
| Exact RC2 section changed | RC2 §13, residual-state paragraph. |
| Constitutional effect | RC2 consumes the `OPEN` vocabulary without extension or narrowing; it does not assert `OPEN` as the current or successful `G-2` state. |
| Verification evidence | RC2 §13 states: “the residual permitted result is `OPEN`, with the exact missing element and its exact owner named.” |
| Renewed-review requirement | `YES` — the corrected terminal-state wording requires renewed review. |

## 7. Editorial observations

Editorial observations are not constitutional blockers and are excluded from
the constitutional-finding count.

### F-06 — Present-tense supersession wording

**Disposition:** `ADOPTED`

The executive sentence now states within the sentence itself that
supersession occurs upon successful independent confirmation. This removes
the possible premature-effect reading while preserving the same conditional
substance.

**RC2 section changed:** §0.

### F-07 — Source-row re-layout

**Disposition:** `ADOPTED`

RC2 expressly describes the four quoted fields as a faithful re-layout of the
original tab-delimited row, not a literal Markdown-table transcription. No
field value was changed.

**RC2 section changed:** §5.

### F-08 — Explicit G-5 prerequisite

**Disposition:** `ADOPTED`

RC2 names `G-5 CLOSED` expressly for clarity and ties it to the already
required confirmed and frozen M44-WP6 and M44-WP7 component results. This
introduces no new prerequisite and preserves the WP6-before-WP7 ordering.

**RC2 section changed:** §12 item 4.

## 8. Disposition summary

| Identifier | Class | Disposition | RC2 location | Blocking status after this response |
| --- | --- | --- | --- | --- |
| `F-01` | `MAJOR` | `ACCEPTED` | §§4 and 18 | Correction implemented; renewed review required |
| `F-02` | `MINOR` | `ACCEPTED` | §1 | Correction implemented; renewed review required |
| `F-03` | `MINOR` | `ACCEPTED` | §6 | Correction implemented; renewed review required |
| `F-04` | `MINOR` | `ACCEPTED` | §12 | Correction implemented; renewed review required |
| `F-05` | `MINOR` | `ACCEPTED` | §13 | Correction implemented; renewed review required |
| `F-06` | `EDITORIAL` | `ADOPTED` | §0 | Not a constitutional blocker |
| `F-07` | `EDITORIAL` | `ADOPTED` | §5 | Not a constitutional blocker |
| `F-08` | `EDITORIAL` | `ADOPTED` | §12 | Not a constitutional blocker |

## 9. Submission for renewed independent review

The preserved review, this response, and corrected RC2 form the complete
authorized correction package. All five constitutional findings remain
findings of record until a renewed independent reviewer verifies the
corrections. This response asserts only:

`F-01 THROUGH F-05 ACCEPTED; CORRECTIONS IMPLEMENTED AND SUBMITTED FOR RENEWED INDEPENDENT REVIEW`

It does not assert unresolved findings `NONE`, issue confirmation, make the
RC2 supersession effective, disposition the standing block, establish the
`G-2` terminal state, perform step 4, freeze or close M44-WP3, or authorize
downstream work.
