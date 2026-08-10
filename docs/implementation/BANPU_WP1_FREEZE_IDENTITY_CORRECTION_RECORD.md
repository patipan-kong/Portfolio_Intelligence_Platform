# BANPU-WP1 — Freeze Identity Correction Record

**Artifact class:** Additive lifecycle evidence — freeze identity metadata correction only
**Correction date:** 2026-08-07
**Disposition:** `FREEZE IDENTITY CORRECTED — READY FOR INDEPENDENT GOVERNANCE REVIEW`
**Corrects:** Three erroneous per-file identity rows in [BANPU-WP1 Freeze Record](BANPU_WP1_FREEZE_RECORD.md) §4
**Authority:** Freeze Identity Correction Authority, acting on the completed BANPU-WP1 Freeze Identity Forensics investigation

## 1. Artifact classification

This record is:

- **additive lifecycle evidence** — it introduces new, independently verifiable identity metadata; it does not alter any existing artifact;
- **a correction to freeze identity metadata only** — it corrects three SHA-256/byte-count values recorded in error; it changes no implementation content, no test, no migration, no design document, and no accounting or business rule;
- **NOT an amendment to WP1 implementation** — no capability, constraint, schema element, parser behavior, or vocabulary correction described in the Freeze Record §3 candidate scope is touched, reopened, or reinterpreted;
- **NOT a reopening of the WP1 freeze** — the freeze disposition (`FROZEN WITH RECORDED RESIDUALS`), the four recorded residuals in §7, and the freeze scope/exclusions in §8–§9 of the Freeze Record remain in force unchanged;
- **NOT a replacement for `BANPU_WP1_FREEZE_RECORD.md`** — that record remains the sole constitutional freeze act for WP1 and is not edited, superseded in substance, or invalidated by this record. This record supersedes only the three erroneous identity-metadata cells identified below, for future verification purposes.

## 2. Original freeze reference

- **Original freeze artifact:** [BANPU_WP1_FREEZE_RECORD.md](BANPU_WP1_FREEZE_RECORD.md)
- **Original frozen-corpus cardinality:** 12 files (§4)
- **Original aggregate identity:** `56478CB0A4312314724DD81D90A9FAE852434C2156BD47B5FED141296E0578A9`
- **Original baseline HEAD/branch:** `451ab8529567076eb8836e20e6c632956b2de675` on `feature/m46-banpu-remediation` (§10)
- **Original three erroneous rows, exactly as recorded in §4:**

  | # | Frozen artifact | Bytes | Physical lines | SHA-256 |
  |---|---|---:|---:|---|
  | 1 | `backend/models/database.py` | 72,515 | 1,222 | `377D008E68B973F5DA2F56CE12EF890719746AB2BEFBB9B44926BA467839F6C3` |
  | 6 | `docs/architecture/ARCHITECTURE.md` | 25,328 | 525 | `DFFE081EDF166CAE9DA3B585725A22B40BABCD3E5F5D15003B7EE1627F8FEA2F` |
  | 7 | `docs/investment/PORTFOLIO_CALCULATION_RULES.md` | 45,125 | 392 | `9BF323803F618CB210E1CE97E104B13CBB329F29672D1984570939E701E3718D` |

## 3. Forensic basis

This correction is based on the completed BANPU-WP1 Freeze Identity Forensics investigation (governance/evidentiary review, no file modified during that investigation). Summary of method and findings:

- **Working-tree hashing.** Raw SHA-256 was computed for all 12 corpus files directly from current working-tree bytes.
- **LF normalization.** Each file was independently re-hashed after stripping trailing `\r` from every line (`sed 's/\r$//' file | sha256sum`), producing a canonical LF-content SHA-256 and byte count per file.
- **Index and HEAD comparison.** For all 12 files, `git ls-files -s` and `git rev-parse HEAD:<path>` were compared; for the 3 files under investigation, index blob SHA-1 equals HEAD blob SHA-1 exactly (confirmed via empty `git diff --cached --stat` for those paths), meaning their WP1-era edits exist only as unstaged working-tree modifications and were never separately staged.
- **Reachable and unreachable Git-object search.** Every blob object in the repository — 2,207 total, enumerated via `git cat-file --batch-all-objects --batch-check`, including reachable and dangling/unreachable objects from `git fsck --unreachable --no-reflogs` — was searched for content markers unique to each of the 3 files' WP1 addition. Exactly one matching blob was found per file, in each case byte-identical to the current working-tree content. No alternate, historical, dangling, or stashed byte-state for these three files exists anywhere in the object store.
- **Lifecycle-document comparison.** [BANPU_WP1_CONFIRMATION.md](BANPU_WP1_CONFIRMATION.md) and [BANPU_WP1_FREEZE_READINESS_ASSESSMENT.md](BANPU_WP1_FREEZE_READINESS_ASSESSMENT.md) were read in full. Neither contains a per-file hash table; the Freeze Readiness Assessment §3 explicitly defers hash computation to the freeze act itself. The Freeze Record is therefore the sole source of any per-file byte-identity claim for the WP1 corpus, and no independent lifecycle checkpoint exists to corroborate or contradict its recorded values.
- **Semantic diff inspection.** `git diff HEAD` for all 3 files shows content limited exactly to the narrow additive scope the Confirmation, Freeze Readiness, and Freeze Record narrative all describe: the `conversion_payload` schema/constraint/index/migration block in `database.py`, and the one vocabulary passage in each of the two documentation files. No unexplained or unexpected content exists in any of the three diffs.

**Explicit distinction between the 9 reconcilable files and the 3 corrected files:**

- **9 CRLF-reconcilable files** (`transaction_canonicalizer.py`, the migration file, `test_transaction_canonicalizer.py`, `test_position_conversion_migration.py`, `BANPU_POSITION_CONVERSION_IMPLEMENTATION_DESIGN.md`, `BANPU_REMEDIATION_WORK_PACKAGE_ROADMAP.md`, `BANPU_IMPLEMENTATION_SEQUENCE.md`, `BANPU_WP1_CONFIRMATION.md`, `BANPU_WP1_FREEZE_READINESS_ASSESSMENT.md`): each file's LF-normalized SHA-256 and LF byte count reproduce the Freeze Record's recorded values exactly, with no residual discrepancy of any kind. (For two of these — `transaction_canonicalizer.py` and `test_transaction_canonicalizer.py` — the working tree currently carries no CRLF at all, so the raw hash already equals the recorded value; LF normalization is a no-op for those two and still reproduces the recorded identity under the same single convention.)
- **3 genuine recorded-metadata errors** (`database.py`, `ARCHITECTURE.md`, `PORTFOLIO_CALCULATION_RULES.md`): for each, neither the raw working-tree hash, nor the LF-normalized hash, nor the index/HEAD blob, nor any object found in the exhaustive blob search reproduces the Freeze Record's recorded SHA-256 or byte count. The exact provenance of the original erroneous values is not reconstructable. This record does not claim that no ephemeral, never-recorded byte sequence could ever have existed prior to the freeze; it states only that no repository-reconstructable evidence supports any alternative candidate to the content verified here.

## 4. Corrected identity convention

**Canonical convention: Git-canonical LF content — SHA-256 computed over file bytes with trailing `\r` stripped from every line (equivalent to the repository's own Git blob byte representation under its checkout normalization).**

This convention is adopted because:

- it is the **only single, uniform rule** that reproduces the Freeze Record's own recorded values for all 9 unaffected files, with zero exceptions and zero residual byte deltas;
- it is independently corroborated by Git's own object model: `git hash-object`/blob storage for this repository normalizes CRLF to LF on write, so a file's Git blob content and its LF-normalized SHA-256 are the same evidence expressed two ways;
- the raw working-tree byte count is a function of the platform/editor checkout state (CRLF vs LF), not of file content — using raw bytes as the canonical identity would make future verification depend on checkout configuration rather than on content, which is the actual drift this investigation diagnosed for 9 of the 12 files.

This convention is stated once, explicitly, and is not silently varied elsewhere in this record. Every corrected value in §5 and §6 below is computed under this exact convention.

## 5. Corrected identity table

| Path | Original Freeze Record SHA-256 | Original recorded bytes | Corrected canonical SHA-256 (LF-normalized) | Corrected canonical bytes (LF) | Evidence source |
|---|---|---:|---|---:|---|
| `backend/models/database.py` | `377D008E68B973F5DA2F56CE12EF890719746AB2BEFBB9B44926BA467839F6C3` | 72,515 | `F10F7FEE23392DC6C0953D255BA52A173D18F5C7DF217DD48AC03BB0DC5A6E6E` | 71,374 | Recomputed directly from current working-tree bytes (`sed 's/\r$//' backend/models/database.py \| sha256sum`); corroborated by exhaustive Git blob search (blob `c59ab1d8200af2e33ae082c827d28df23cbe94c9`, the sole matching object in the repository's object database) |
| `docs/architecture/ARCHITECTURE.md` | `DFFE081EDF166CAE9DA3B585725A22B40BABCD3E5F5D15003B7EE1627F8FEA2F` | 25,328 | `D9CD713828A1BD082E5464D3BF79AFF88D08760AB8B387F78B1ED47A22D3A449` | 24,804 | Recomputed directly from current working-tree bytes; corroborated by exhaustive Git blob search (blob `74f2d07c0f91c96471bb82a0d8f6082b21682904`, the sole matching object) |
| `docs/investment/PORTFOLIO_CALCULATION_RULES.md` | `9BF323803F618CB210E1CE97E104B13CBB329F29672D1984570939E701E3718D` | 45,125 | `D1719C49E23882113A8B5C100A5B5F900DC91995384EC6D11AD92A512D0190FD` | 44,736 | Recomputed directly from current working-tree bytes; corroborated by exhaustive Git blob search (blob `6a2cdbad4287b2c19a193a30a78ebdc40632ede0`, the sole matching object) |

All three corrected values were recomputed directly against verified repository content during this correction task; none is transcribed from the earlier forensic investigation without re-derivation.

## 6. Corrected aggregate identity

**Yes — an additive corrected aggregate manifest identity can be computed**, because the original aggregate algorithm was successfully reconstructed and independently verified byte-for-byte against the recorded value in Freeze Record §4:

> Manifest = for each of the 12 corpus rows, in the Freeze Record's §4 table order, the line `<repo-relative-path>\t<SHA-256, uppercase hex>\t<byte count>`, lines joined by `\n`, with one trailing `\n`, the whole manifest encoded UTF-8, then hashed with SHA-256.

Applying this exact algorithm to the original 12 recorded rows reproduces `56478CB0A4312314724DD81D90A9FAE852434C2156BD47B5FED141296E0578A9` exactly, confirming the algorithm is correctly reconstructed and not invented.

Recomputing the same algorithm with the 3 corrected rows from §5 substituted (all 9 unaffected rows unchanged, since their LF-canonical values are identical to the original recorded values) produces the corrected aggregate identity:

```text
DF0AF823EFEACA38171F4DACAC0B19975BAE07EE1BA09A040B549B06ACD443E1
```

This corrected aggregate identity **supersedes the original aggregate identity for future identity verification only.** The original aggregate identity remains recorded, unedited, in Freeze Record §4 as part of the immutable freeze act; it is not accurate for byte-level reverification against canonical LF content and should not be used for that purpose going forward. Any future automated or manual WP1 corpus-identity check should use the corrected aggregate identity above, computed under the canonical LF convention defined in §4 of this record.

## 7. Constitutional effect

- WP1 semantic content is unchanged.
- WP1 implementation remains frozen.
- WP1 acceptance and accounting semantics are unchanged.
- No source file is modified by this correction.
- No migration is modified.
- No test is modified.
- The original Freeze Record remains immutable and is not edited by this correction.
- This record supersedes only the erroneous identity metadata identified in §5–§6, for future verification purposes; it supersedes no other content, decision, residual, or disposition in the Freeze Record.

## 8. WP2 effect

- WP2 implementation remains technically unchanged by this correction.
- BANPU-WP2 Implementation Step 8's frozen-hash blocker is the direct reason this correction record exists.
- This correction alone does **not** authorize WP2 Step 9.
- Step 9 may proceed only after independent governance review accepts this correction and the corrected identity is reverified against the then-current repository state.

## 9. Future verification rule

Future WP1 frozen-corpus identity checks must use:

- the original [BANPU_WP1_FREEZE_RECORD.md](BANPU_WP1_FREEZE_RECORD.md) for all unaffected constitutional content, decisions, and residuals;
- this additive correction record for the corrected per-file and aggregate identity metadata for the three affected files;
- the canonical LF-normalized hashing convention defined in §4 of this record for all future WP1 corpus identity verification.

No future process may rewrite the original freeze artifact merely to make hashes line up with a particular checkout's line-ending state.

## 10. Verification

Recomputed from disk/repository evidence during preparation of this record:

- all 12 canonical WP1 identities (raw and LF-normalized) — see §3 and §5;
- the corrected identities for the three affected files — see §5, freshly recomputed, not transcribed;
- CRLF reconciliation for the remaining 9 files — confirmed exact under the single LF-normalized convention, no exceptions;
- the corrected aggregate manifest — computed in §6 using the reconstructed-and-verified original algorithm.

Repository verification commands run as part of this task:

| Command | Result |
|---|---|
| `git diff --check` | Clean — no whitespace-error findings introduced by this task |
| `git diff --cached --check` | Clean |
| `git status --short` | Only this new file (`docs/implementation/BANPU_WP1_FREEZE_IDENTITY_CORRECTION_RECORD.md`) added to the working tree as untracked/new during this task; all other entries pre-date this task and are unchanged by it |
| `graphify update .` | To be run after this record is saved, per standard practice; not required to change any code-graph node since no source file changed |

## 11. Final disposition

**FREEZE IDENTITY CORRECTED — READY FOR INDEPENDENT GOVERNANCE REVIEW**

This record does not itself clear BANPU-WP2 Step 8, and does not authorize BANPU-WP2 Step 9. WP2 Step 9 remains blocked pending independent governance acceptance of this correction.
