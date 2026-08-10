# BANPU-WP1 — Residual Identity Record

**Artifact class:** Residual carry-forward record (BANPU-WP1 governance
corpus)
**Date:** 2026-08-07
**Issuing authority:** Freeze Authority (residual carry-forward authority)
**Disposition:** RESIDUAL RECORDED — WP1 remains FROZEN WITH RECORDED
RESIDUALS; WP2 Step 8 REMAINS BLOCKED

---

## 1. Artifact classification

This record is:

- **Additive constitutional evidence.** It adds a new, standalone artifact to
  the BANPU-WP1 governance corpus; it introduces no change to any existing
  artifact.
- **A residual carry-forward artifact.** It records one unresolved
  identity-verification item alongside the frozen corpus, in the same manner
  as the residuals already carried forward in `BANPU_WP1_FREEZE_RECORD.md`
  §7 (MINOR-1, MINOR-2, MINOR-5, NEW-MINOR-A).
- **Non-amending.** It does not alter any text, value, or statement in
  `BANPU_WP1_FREEZE_RECORD.md`.
- **Non-corrective.** It does not assert that any recorded identity is wrong,
  and it replaces no SHA-256, byte count, or aggregate value.
- **Non-reopening.** It does not reopen BANPU-WP1 implementation, and it does
  not admit any new implementation, execution, or behavioral change into the
  frozen corpus.

## 2. Authority

This record is issued under the Freeze Authority's existing **residual
carry-forward authority** — the same authority under which
`BANPU_WP1_FREEZE_RECORD.md` §7 already carries forward unresolved items
without amending the frozen corpus identity. No amendment authority is
claimed or exercised. No authority beyond recording an already-completed
governance determination is exercised here.

## 3. Background

- **Forensic Round 1** investigated an apparent 3-file mismatch between the
  Freeze Record's recorded SHA-256/byte-count values and the current
  repository state, and produced a Freeze Identity Correction candidate
  proposing LF-normalized values for `backend/models/database.py`,
  `docs/architecture/ARCHITECTURE.md`, and
  `docs/investment/PORTFOLIO_CALCULATION_RULES.md`. That correction candidate
  was **not approved**.
- **Independent Review** subsequently introduced new repository evidence
  showing that `docs/architecture/ARCHITECTURE.md` and
  `docs/investment/PORTFOLIO_CALCULATION_RULES.md` can each be reconstructed
  exactly from a mixed-EOL working-tree state, removing both files from
  further investigation. Only `backend/models/database.py` remained
  unresolved.
- **Forensic Round 2** conducted a first-principles investigation limited to
  `backend/models/database.py`: comparison of raw, LF-normalized, index, and
  HEAD states; an exhaustive search of the local git object database
  (reachable, unreachable, dangling, stashed, and tooling-checkpoint blobs);
  and systematic testing of every technically plausible mixed-EOL
  reconstruction (uniform, context/insertion split in both directions, and
  full hunk-boundary subset combinations). No reconstruction reproduced the
  recorded identity.
- **The governance determination**, treated as authoritative for this
  record, classified `backend/models/database.py` as **IDENTITY NOT
  RECONSTRUCTABLE** and directed that the correct constitutional path is a
  Residual Identity Record — not a correction, not an amendment — leaving
  the Freeze Record fully intact.

## 4. Positive corroboration

Of the 12 files in the frozen WP1 corpus, **11 are now positively
corroborated** against the identities recorded in
`BANPU_WP1_FREEZE_RECORD.md` §4.

Positive corroboration was established through multiple independent
repository-supported reconstruction mechanisms. These mechanisms are
intentionally recorded separately. No single universal newline-normalization
rule is asserted by this record.

- **Seven files** corroborated through repository-supported newline
  normalization (CRLF → LF) of the current working-tree bytes, which
  reproduces the recorded SHA-256 and byte count exactly:
  - `backend/migrations/versions/b7d9f1a3c5e7_add_position_conversion_payload.py`
  - `backend/tests/test_position_conversion_migration.py`
  - `docs/implementation/BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`
  - `docs/implementation/BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`
  - `docs/implementation/BANPU_IMPLEMENTATION_SEQUENCE.md`
  - `docs/implementation/BANPU_WP1_CONFIRMATION.md`
  - `docs/implementation/BANPU_WP1_FREEZE_READINESS_ASSESSMENT.md`

- **Two files** corroborated through repository-supported mixed-EOL
  reconstruction (established during Independent Review), a distinct
  mechanism from simple newline normalization:
  - `docs/architecture/ARCHITECTURE.md`
  - `docs/investment/PORTFOLIO_CALCULATION_RULES.md`

- **Two files** — both belonging to the `transaction_canonicalizer` family —
  already matched the recorded identity on raw working-tree bytes, because
  their working-tree bytes are unchanged since the freeze instant and
  therefore still satisfy the Freeze Record's declared raw-working-tree-bytes
  convention directly, with no normalization step required:
  - `backend/services/transaction_canonicalizer.py`
  - `backend/tests/test_transaction_canonicalizer.py`

These three paths are recorded separately and are not collapsed into a
single universal normalization rule; each reflects a distinct evidentiary
basis specific to the file(s) it covers.

## 5. Residual identity

**File:** `backend/models/database.py`

**Classification:** `IDENTITY NOT RECONSTRUCTABLE`

**Exact constitutional meaning:** No repository-reconstructable evidence
presently reproduces the recorded Freeze Record identity.

This record explicitly does **not** conclude:

- that the Freeze Record is wrong;
- that implementation drift occurred;
- that another implementation candidate exists.

## 6. Freeze effect

WP1 remains:

**FROZEN WITH RECORDED RESIDUALS**

This record records one additional residual (`backend/models/database.py`
identity verification) alongside the existing residual register already
carried forward in `BANPU_WP1_FREEZE_RECORD.md` §7. The existing Freeze
Record remains unchanged. Nothing else about the freeze changes.

## 7. WP2 effect

WP2 implementation is technically unchanged.

WP2 Step 8 remains blocked.

This record does **not** unblock Step 8.

This record does **not** authorize Step 9.

## 8. Terminal condition

This residual closes only by one of the following:

**A.** Successful future reconstruction of the recorded identity for
`backend/models/database.py` from evidence outside the repository — for
example, editor/IDE local history, OS volume shadow copies or backups dated
2026-08-06, build or test artifacts embedding the file, or a terminal record
of the original freeze-time hashing run. Round 2 exhaustively searched all
repository-internal evidence (reachable, unreachable, dangling, stashed, and
tooling-checkpoint objects) and found none; any surviving evidence for this
path exists, if at all, only outside the repository and may be perishable.
Preservation of any such evidence should not be delayed; or

**B.** An explicit Architecture Owner decision accepting the reduced
assurance and formally closing the residual on that basis. Such a decision
must record, at minimum: that the Step 8 gate is being closed on a
scope-limited basis (11 of 12 frozen identities corroborated;
`backend/models/database.py` named as the twelfth); the substitute
instrument of admittedly lower strength being relied on in its place; an
explicit statement, in those words, that WP2 proceeds without byte-level
identity verification of `backend/models/database.py`; the identity of the
accepting authority; and the carry-forward of this residual alongside that
decision.

No other closure mechanism is recognized by this record.

## 9. Excluded effects

This record explicitly does **not** effect any of the following:

- Freeze Record amendment
- SHA-256 replacement
- Aggregate manifest replacement
- Frozen corpus modification
- Implementation modification
- Governance reinterpretation

## 10. Repository verification

The following were verified after creating this record:

- Only `docs/implementation/BANPU_WP1_RESIDUAL_IDENTITY_RECORD.md` was
  created; no existing file was modified.
- No production file changed.
- No frozen WP1 file changed.
- No WP2 implementation file changed.
- `git diff --check` — clean.
- `git diff --cached --check` — one pre-existing, out-of-scope finding
  (`BANPU_WP2_ALLOCATION_RECORD.md:170`, blank line at EOF), already known
  from prior verification, not part of this task's scope and left untouched.
- `git status --short` — confirms only this new file was added; all
  previously-modified files retain their pre-existing state.
- `graphify update .` — executed successfully.

---

## Final disposition

**RESIDUAL RECORDED**

WP1 remains:

**FROZEN WITH RECORDED RESIDUALS**

WP2 Step 8:

**REMAINS BLOCKED**

Exact next constitutional act: Architecture Owner determination regarding
Step 8 gate scope or future identity reconstruction. This record itself
performs no part of that act.
