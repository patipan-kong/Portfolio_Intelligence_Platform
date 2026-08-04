# Asset Foundation — AF-WP3 Content-Identity Validation

**Artifact class:** Independent AF-WP3 content-identity validation record
**Validation date:** 2026-08-04
**Validation scope:** Exact current bytes of the AF-WP3 implementation candidate only
**Disposition:** `CONTENT IDENTITY VALIDATED`
**Authority granted by this record:** `NONE`

## 1. Validation boundary

This record validates the exact current bytes of the AF-3 Owner Evidence
Manifest and Conformance-Annex Index candidate at the validation boundary. It
does not perform or establish freeze, canonicalization, canonical supply,
closeout, release, implementation, allocation, authorization, or downstream
authority.

The candidate was stabilized before identity calculation with the historical
initial review `FAIL`, additive correction, focused re-review `PASS`,
independent confirmation `CONFIRMED`, and content-identity validation in
progress. No substantive AF-WP3 scope, architecture, authority, or predecessor
content was changed for validation.

## 2. Freeze-candidate corpus determination

The exact AF-WP3 freeze-candidate corpus is the single AF-3 implementation
artifact below:

| Corpus item | Inclusion | Rationale |
|---|---|---|
| AF-WP3 implementation candidate | INCLUDED | The frozen roadmap defines AF-WP3 as the AF-3 Owner Evidence Manifest and Conformance-Annex Index; the manifest and annex index are the exact implementation package intended for AF-WP3 freeze. |
| AF-WP3 allocation and authorization record | EXCLUDED FROM CANDIDATE BYTES | Separate governance evidence for prerequisite allocation and authorization; it is not AF-3 implementation content. |
| AF-WP3 independent confirmation record | EXCLUDED FROM CANDIDATE BYTES | Separate later governance evidence documenting confirmation; confirmation is distinct from the implementation bytes. |
| `docs/implementation/INDEX.md` | EXCLUDED FROM CANDIDATE BYTES | Navigation and synchronization evidence; the INDEX is expressly non-normative and grants no authority. |
| This validation record | EXCLUDED FROM CANDIDATE BYTES | Additive evidence created to record the result after the candidate bytes were calculated. |

This determination follows the frozen rule that “AF-WP3 freezes only `AF-3`”
and that the manifest and annex index are frozen as one exact evidence package.
The excluded records remain required lifecycle evidence and are linked by the
candidate and INDEX, but their bytes are not silently folded into the AF-3
freeze candidate.

## 3. Exact corpus inventory

| Repository-relative path | Tracking state | Git blob status | Working-tree SHA-256 | Line count | Byte size |
|---|---|---|---|---:|---:|
| `docs/implementation/ASSET_FOUNDATION_AF_WP3_OWNER_EVIDENCE_MANIFEST_AND_CONFORMANCE_ANNEX_INDEX.md` | Untracked working-tree file | Working-tree blob ID `4f8cae8e17be4f8e743a6d0a43b5c43a6dec851a`; no committed `HEAD` blob exists | `095c081746fcf00fce27c8b9bcfd2e6e37482e28028b93943a3b3a9a938fe67f` | 332 | 25735 |

The current repository `HEAD` at calculation was
`4d475f5ef3674b058047be3c6632e6ae8d13e4ad`. The candidate was not staged and
was not tracked by `HEAD`; the recorded Git blob identity is therefore a
working-tree content identity, not a committed-HEAD identity.

At calculation time, the relevant working-tree state was:

- candidate: untracked, unstaged;
- allocation and authorization record: untracked, excluded from candidate
  bytes;
- independent confirmation record: untracked, excluded from candidate bytes;
- `docs/implementation/INDEX.md`: modified, unstaged, excluded from candidate
  bytes; and
- no staged candidate-corpus changes.

The frozen planning, AF-WP1, and AF-WP2 predecessor paths had no working-tree
diff and their cited Git identities were unchanged.

## 4. Validation method

Identity calculation began only after all candidate pre-validation edits were
complete. The candidate was read as exact current file bytes and validated by:

1. calculating SHA-256 twice from the working-tree file and confirming identical
   results;
2. calculating the Git blob identity from the same working-tree bytes without
   representing it as a committed object;
3. counting the file's current lines; and
4. measuring the exact current byte length.

The two SHA-256 calculations both returned
`095c081746fcf00fce27c8b9bcfd2e6e37482e28028b93943a3b3a9a938fe67f`.
The candidate was readable and stable across both calculations.

## 5. Validation result

**Disposition: `CONTENT IDENTITY VALIDATED`**

The recorded SHA-256, working-tree Git blob identity, line count, and byte size
match the exact AF-3 candidate bytes intended for the subsequent freeze stage.
This result validates identity only. It does not state that the candidate is
frozen, canonical, closed, released, or available as canonical supply.
The candidate's `CONTENT-IDENTITY VALIDATION IN PROGRESS` wording is the
pre-validation lifecycle state intentionally captured in those validated bytes;
this record and the navigation INDEX carry the post-validation result without
editing the validated candidate.

## 6. Limitations and post-validation restrictions

- No committed `HEAD` identity exists for the untracked candidate.
- The allocation/authorization record, independent confirmation record, INDEX,
  and this validation record are supporting evidence outside the AF-3 candidate
  bytes and were not validated as part of this freeze-candidate identity.
- The validated candidate bytes must not be edited before exact-byte freeze. Any
  byte change requires this validation result to be discarded and recalculated
  from the corrected bytes.
- This record does not authorize freeze, canonicalization, closeout, release,
  downstream intake, runtime work, or any successor allocation.

AF-WP3 is content-identity validated but remains not frozen, not closed, and
not released. The exact next act is AF-WP3 exact-byte freeze authorization and
freeze-record creation.
