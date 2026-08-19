# BANPU-WP7 — Identity Ingress Design Clarification

**Artifact class:** Additive implementation clarification record (BANPU-WP7
governance corpus)
**Date:** 2026-08-18
**Issuing authority:** Architecture Owner / Constitutional Interpretation
Authority, recorded by the Additive Implementation Clarification Record
Authority
**Interpretation classification:** `A — IMPLEMENTATION CLARIFICATION, NO
PLANNING AMENDMENT REQUIRED`
**Disposition:** `BANPU-WP7 IDENTITY INGRESS CLARIFIED — CLI PORTFOLIO INPUT;
WORKSPACE DERIVED`
**Bound WPP identity (unchanged by this record):**
`docs/implementation/BANPU_WP7_WORK_PACKAGE_PLAN.md`, 35,827 bytes, 496 lines,
SHA-256 `2bdb77dd5ce9ce4da1649be276820b71aa48689ba2f45852c5265e6f55964eef`

---

## 1. Artifact classification

This record is:

- **Implementation clarification only.** It states what the frozen canonical
  design, roadmap, and sequence — read together with live, already-frozen
  service and schema code — jointly require for one specific operator-input
  mechanism. It is not a planning artifact, not a design artifact, and not a
  review artifact.
- **Additive.** It adds one standalone artifact to the BANPU-WP7 governance
  corpus and changes no existing artifact.
- **Non-amending.** It alters no text, table, criterion, gate, decision, or
  identity in any frozen BANPU-WP1–WP6 artifact, and no text in the WP7
  Allocation Record, Implementation Authorization Record, or Work Package
  Plan.
- **Non-authorizing.** It grants no implementation authority beyond what the
  Implementation Authorization Record already grants, extends no file
  surface, and does not perform Planning Confirmation.
- **Interpretive, not elective.** Every element in §6 is derived from
  canonical text and live frozen code by citation, not chosen among
  freely admissible alternatives.

**This record creates no new planning decision, acceptance criterion, gate,
obligation, or residual.** It resolves one silent gap in the WP7 Work Package
Plan (§7.1/§8 Open Item #1) so a future bounded WPP revision can incorporate a
determinate answer instead of an invented one.

## 2. Occasion

The independent BANPU-WP7 Work Package Plan review concluded:

`BANPU-WP7 WPP INDEPENDENT REVIEW FAILED — PLAN REVISION REQUIRED`

identifying, among its findings, one genuine implementation-critical
ambiguity already self-flagged by the WPP itself at §8, row 1:

> How does the CLI receive `portfolio_id`/`ws_id`? — `OPEN — REQUIRES
> RESOLUTION BEFORE PLANNING CONFIRMATION`.

This record resolves **only** that question. It disposes of no other
independent-review finding and does not itself revise the WPP.

## 3. Service identity requirements (live evidence)

`backend/services/portfolio_transactions.py:1104`, `execute_position_conversion`:

```python
def execute_position_conversion(
    db: Session,
    ws_id: int,
    portfolio_id: int,
    conversion_payload: dict,
    *,
    currency: str = "THB",
    exchange_rate: float = 1.0,
    notes: str | None = None,
) -> dict:
```

`ws_id` and `portfolio_id` are mandatory positional parameters, distinct from
`conversion_payload`. The frozen service does not derive them from the
payload dict; the caller must supply both. Whatever mechanism the WP7 CLI
uses to obtain them, it must resolve to exactly these two integers before
calling this frozen function.

`backend/services/asset_registry.py:351`, `prepare_position_conversion_registry`:

```python
def prepare_position_conversion_registry(
    db: Session,
    predecessor_asset_id: AssetId,
    successor_asset_id: AssetId,
    successor_provider_symbol: str,
    *,
    source: str,
    effective_date: Optional[datetime] = None,
) -> AssetRelationship:
```

This function takes no `portfolio_id` or `ws_id` parameter at all — it
operates purely on asset identity. It cannot be a source of portfolio or
workspace identity for the CLI (see §7).

## 4. Canonical manifest identity findings

Design §6.2's `conversion_payload` schema (`schema_version: 1`) is closed and
frozen. Its members are exactly: `schema_version`, `predecessor` (`asset_id`,
`symbol`, `shares_surrendered`), `successor` (`asset_id`, `symbol`,
`provider_symbol`, `shares_entitled`, `shares_received`),
`conversion_ratio`, `basis`, `cash_in_lieu`, `dates`, `quote_binding`,
`boundary_evidence`, `evidence`. **No member names, carries, or reserves a
portfolio or workspace identity field.** Design §6.3's invariant list
("Predecessor and successor asset IDs are non-null, distinct, and
registry-resolved... Exactly one `POSITION_CONVERSION` may exist for the same
portfolio, non-null predecessor asset ID...") treats `portfolio_id` as an
ambient fact the row is inserted against, never as a payload-carried value.

No canonical artifact — Design, Roadmap, Sequence, or either WP7 lifecycle
record — authorizes extending this frozen schema. Per the decision criteria
this record must apply, that is strong, undefeated evidence against Option B
(manifest identity).

## 5. CLI precedent findings

`backend/manage.py` already establishes a mechanically reusable pattern for
operator-supplied portfolio identity, used by multiple existing subcommands:

```text
python manage.py apply_repair --portfolio 4 --plan repair_plan_4.json
python manage.py rebuild_portfolio --portfolio 4
python manage.py rebuild_portfolio --portfolio 4 --dry-run
```

`_cmd_apply_repair` (`manage.py:4047`) reads `portfolio_id: int = args.portfolio`
directly from the operator-supplied `--portfolio` flag; it is never parsed out
of a file. This is the operator-facing, deterministic, explicit-intent
mechanism required by §9's decision criteria.

Design Roadmap §9 states directly, in the WP6→WP7 boundary language: *"Keep
operator access service-only; CLI wiring is deferred to WP7."* This is direct
canonical confirmation that the frozen corpus deliberately left CLI-level
operator-input mechanics — including how identity reaches the command — to be
decided at WP7, not fixed upstream.

## 6. Workspace derivation findings

`backend/models/database.py:87`, `Portfolio.workspace_id`:

```python
workspace_id = Column(Integer, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
```

This is a non-nullable, indexed foreign key. Every `Portfolio` row has
exactly one owning `workspace_id`, persisted and canonical. Given a resolved
`--portfolio` id, loading that `Portfolio` row and reading its
`workspace_id` column yields a unique, unambiguous, already-canonical
workspace identity with no multi-workspace ambiguity — the relationship is
enforced at the schema level, not inferred.

This is distinct from the pattern already used by `_cmd_apply_repair` and
`_cmd_regenerate_paper_portfolios`, which both derive `ws_id` via
`db.query(Workspace).first()` — an implementation shortcut that assumes
exactly one `Workspace` row exists in the deployment. That shortcut is not a
canonical design rule; it is an existing single-tenant convenience found in
two prior CLI commands, and it is strictly weaker than deriving `ws_id`
directly from the target portfolio's own `workspace_id` FK. Deriving from
`Portfolio.workspace_id` for the specific `--portfolio` row satisfies §9's
requirement of "the smallest clarification compatible with existing
authority" more precisely, because it ties the derived workspace to the
actual portfolio being converted rather than to an assumption about how many
`Workspace` rows exist in the database, and it produces the identical result
under the current single-workspace deployment while additionally failing
closed correctly (no matching portfolio ⇒ no result) rather than succeeding
against the wrong or an incidental workspace.

Caller-supplied `ws_id` (a second operator flag) is therefore unnecessary:
requiring the operator to separately specify a value that is already
deterministically recoverable from `--portfolio` would only introduce a new
class of operator error (a mismatched pair) with no corresponding safety
benefit, and Design nowhere calls for it.

## 7. Registry-derived identity findings

Option C (deriving portfolio/workspace identity from registry state) is
rejected on two independent grounds:

1. `prepare_position_conversion_registry` (§3 above) takes no `portfolio_id`
   or `ws_id` parameter — registry rows are keyed by asset identity only, not
   by portfolio. There is no registry-side field to read a portfolio or
   workspace identity from.
2. Even disregarding (1), registry preparation is itself one of the WP7
   preflight steps that occurs *after* the CLI must already know which
   portfolio it is operating against (registry preparation and conversion
   execution both act on a specific portfolio's holdings). Treating registry
   state as an identity source would require identity to already be resolved
   in order to read the very state proposed to resolve it — a circular
   ordering forbidden by §7 of the governing prompt for this act.

Option C is rejected.

## 8. Canonical invocation reconciliation

Design §9's example invocation —

```text
python manage.py apply_position_conversion --manifest FILE --dry-run
python manage.py apply_position_conversion --manifest FILE --commit
```

— appears under the heading "The only write entry point is an operator CLI,"
immediately followed by "No public API or frontend authoring surface is
added." Read in context, "only" modifies **entry-point class** (CLI, not
API/frontend) — the same contrast Design draws throughout §9 — not an
assertion that the two shown flags exhaust the command's full argument
surface.

This reading is not merely permissive; it is necessary. `execute_position_conversion`
requires `ws_id` and `portfolio_id` as separate, mandatory parameters (§3). If
Design §9's illustrative invocation were exhaustive, the documented CLI could
never actually call the frozen service it exists to invoke — an internal
contradiction. Combined with Roadmap §9's explicit statement that CLI wiring
is deferred to WP7 (§5 above), the documented invocation is determined to be
**illustrative and non-exhaustive**, not a closed argparse specification.
Competent clarification may therefore narrow it by adding one required
operator-identity flag without amending the frozen architecture: dry-run
remains the default, `--commit` remains the only mutating path, the CLI
remains the only write entry point, and the manifest remains the sole payload
carrier.

## 9. Options considered and rejected

| Option | Disposition | Reason |
|---|---|---|
| A — CLI portfolio identity | **Selected** | Matches existing precedent, requires no manifest change, deterministic, fail-closed, smallest clarification compatible with existing authority |
| B — Manifest identity | Rejected | §6.2 payload contract is closed/frozen and carries no portfolio/workspace field; no canonical artifact authorizes extension; would be a substantive manifest-contract amendment, not an implementation detail |
| C — Registry-derived identity | Rejected | `prepare_position_conversion_registry` takes no portfolio/workspace parameter; deriving identity from registry state would also be circular relative to preflight ordering |
| D — Another mechanism fixed by frozen authority | Not applicable | Design, Roadmap, and Sequence are silent on this mechanism; Roadmap §9 explicitly defers CLI wiring to WP7, so no other frozen mechanism exists to point to |

## 10. Identity-ingress determination

**`BANPU-WP7 IDENTITY INGRESS CLARIFIED — CLI PORTFOLIO INPUT; WORKSPACE
DERIVED`**

1. **Operator input:** a required `--portfolio`/`-p` flag on
   `apply_position_conversion`, matching the exact flag name and short form
   already established by `apply_repair` and `rebuild_portfolio`.
2. **`portfolio_id`:** explicit — taken directly from the operator-supplied
   `--portfolio` value. No default; omission is a usage error.
3. **`ws_id`:** derived, not operator-supplied — obtained by loading the
   `Portfolio` row identified by `--portfolio` and reading its persisted
   `workspace_id` column.
4. **Canonical lookup/derivation source:** `Portfolio.workspace_id`
   (`backend/models/database.py:87`), the non-nullable, indexed foreign key
   already canonical and frozen at the schema level.
5. **Failure behavior:** fail closed. If `--portfolio` does not resolve to an
   existing `Portfolio` row, the command exits non-zero with a clear error
   and performs no write, mirroring the existing `apply_repair`/
   `regenerate_paper_portfolios` "not found" convention. No conversion
   preflight or write proceeds without a resolved, unique `(portfolio_id,
   ws_id)` pair.
6. **Manifest contract:** **unchanged.** Design §6.2's `conversion_payload`
   schema gains no field by reason of this record.
7. **Canonical CLI surface:** **clarified, not amended.** Design §9's
   invocation example is narrowed by one required flag; dry-run-default,
   explicit-`--commit`, CLI-only-write-path, and manifest-driven-payload
   invariants are all preserved unchanged.
8. **Implication for the WPP revision:** the future bounded WP7 Work Package
   Plan revision should close §8 Open Item #1 by specifying `--portfolio`/
   `-p` (required) with FK-derived `ws_id` and fail-closed lookup, exactly as
   determined in items 1–5 above. This record does not itself perform that
   revision.

## 11. Manifest-contract impact

None. No field is added to, removed from, or reinterpreted within Design
§6.2's `conversion_payload` schema. The schema remains exactly as frozen.

## 12. Preservation statements

**12.1 WP7 lifecycle artifacts.** Unchanged. Verified byte-identical after
creation of this record:

| Artifact | Bytes | Lines | SHA-256 |
|---|---|---|---|
| `BANPU_WP7_ALLOCATION_RECORD.md` | 19,609 | 329 | `1aa24cd242c95039b81df1a43f061b04140ea0ed5e0a2e7405ae18945900f4f1` |
| `BANPU_WP7_IMPLEMENTATION_AUTHORIZATION_RECORD.md` | 20,963 | 361 | `e7a6b235c84abbfff9159c7e91e2477e746b314128e1c1b1ee0b46d6e5faeb6c` |
| `BANPU_WP7_WORK_PACKAGE_PLAN.md` | 35,827 | 496 | `2bdb77dd5ce9ce4da1649be276820b71aa48689ba2f45852c5265e6f55964eef` |

**12.2 Frozen WP1–WP6 artifacts.** Unchanged. No member of any frozen WP1–WP6
corpus was modified by this act.

**12.3 Implementation files.** No production file and no test file was
created, modified, or deleted by this act. `backend/manage.py`,
`backend/services/portfolio_transactions.py`,
`backend/services/asset_registry.py`, and `backend/models/database.py` were
read only, for interface facts, and remain unmodified.

**12.4 No re-confirmation and no re-freeze.** No planning amendment is
performed by this record, so no WP7 Planning Confirmation and no Planning
Freeze occurs here. The Allocation Record and Implementation Authorization
Record stand as issued. The Work Package Plan stands as materialized —
`WORK PACKAGE PLAN MATERIALIZED — NOT APPROVED — IMPLEMENTATION NOT
PERFORMED — NOT CONFIRMED — NOT FROZEN` — and is not itself edited by this
record.

**12.5 No implementation authority created.** This record creates no
authority beyond that already granted by the Implementation Authorization
Record. It does not begin implementation, does not touch the database,
cache, or any test/fixture file, and does not perform Planning Confirmation.

## 13. Excluded effects

This record does not:

- amend, reinterpret, or extend any frozen WP1–WP6 planning or design
  artifact, or the Design §6.2 manifest contract;
- create a planning decision, acceptance criterion, gate, obligation, or
  residual;
- create or extend implementation authority, file surface, or work-package
  scope;
- revise the Work Package Plan, or perform Planning Confirmation or Planning
  Freeze;
- resolve WPP §8 Open Item #2 (rehearsal-environment provisioning), registry/
  preflight sequencing beyond what is necessary to explain identity ingress,
  quote-gate integration, continuity-check integration, broker-fact
  integration, dual-replay integration, `MINOR-5`, `NEW-MINOR-A`, `PD-3`, or
  WP8 release evidence;
- perform implementation, review, confirmation, or freeze;
- authorize any commit, push, deployment, or release.

## 14. Repository/diff verification

Performed after this record's creation:

| Check | Result |
|---|---|
| Only this record created by this act | `SATISFIED` |
| WP7 Allocation Record byte-identical to §12.1 | `SATISFIED` |
| WP7 Implementation Authorization Record byte-identical to §12.1 | `SATISFIED` |
| WP7 Work Package Plan byte-identical to §12.1 | `SATISFIED` |
| No frozen WP1–WP6 artifact changed | `SATISFIED` |
| No production file changed by this act | `SATISFIED` |
| No test/fixture file changed by this act | `SATISFIED` |
| Decision Log and Implementation INDEX unchanged | `SATISFIED` |
| `git diff --check` | clean (exit 0) |
| Nothing staged | `SATISFIED` |
| No commit performed | `SATISFIED` |

## 15. Disposition

`BANPU-WP7 IDENTITY INGRESS CLARIFIED — CLI PORTFOLIO INPUT; WORKSPACE
DERIVED`

## 16. Exact next constitutional act

**A bounded BANPU-WP7 Work Package Plan revision**, incorporating this
clarification's determination (§10) to close §8 Open Item #1, and otherwise
correcting the defects identified by the independent WPP review. That
revision proceeds under the implementation authority already granted by the
Implementation Authorization Record and does not require re-allocation or
re-authorization. It is not performed by this record and is not performed in
this session.
