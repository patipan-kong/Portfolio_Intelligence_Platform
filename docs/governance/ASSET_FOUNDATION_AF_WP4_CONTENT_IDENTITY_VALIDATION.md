# Asset Foundation - AF-WP4 Content-Identity Validation

**Artifact class:** Independent AF-WP4 content-identity validation record
**Validation date:** 2026-08-04
**Validation authority:** Competent independent content-identity validation authority, acting solely in the content-identity validator role; no personal name asserted
**Validation scope:** Exact final bytes of the AF-WP4 documentary implementation candidate only
**Disposition:** `CONTENT IDENTITY VALIDATED`
**Authority granted by this record:** `NONE`

## 1. Validation boundary

This record validates the reproducible identity of the exact AF-WP4
implementation candidate bytes at the validation boundary. It does not
perform or establish exact-byte freeze, canonicalization, canonical supply,
release attestation, closeout, implementation, allocation, authorization,
review, confirmation, runtime, downstream, or Ledger authority.

The candidate was stabilized before identity calculation with the independent
review disposition `PASS`, independent confirmation `CONFIRMED`, and
content-identity validation in progress. The final pre-calculation changes
were limited to the permitted AF-WP4 lifecycle synchronization. No predecessor
payload, release predicate, terminal disposition, blocker outcome, scope
boundary, or authority boundary was changed for validation.

## 2. Freeze-candidate corpus determination

The exact AF-WP4 freeze-candidate corpus is the single normative documentary
implementation artifact below:

| Artifact class | Artifact | Corpus disposition | Reason |
|---|---|---|---|
| Normative implementation artifact | `docs/implementation/ASSET_FOUNDATION_AF_WP4_RELEASE_ATTESTATION.md` | INCLUDED | The frozen AF-WP4 scope defines one AF-4 release-attestation and owner-domain closeout implementation candidate. |
| Governance evidence | AF-WP4 allocation, authorization, and independent review records | EXCLUDED FROM CANDIDATE BYTES | These are separate lifecycle evidence records and do not form AF-4 implementation content. |
| Governance evidence | Prior independent confirmation determination | EXCLUDED FROM CANDIDATE BYTES | Confirmation is a separate lifecycle act; no confirmation artifact was created by that read-only act. |
| Frozen supporting evidence | Planning corpus, frozen roadmap and architecture plan, and AF-WP1 through AF-WP3 evidence | EXCLUDED FROM CANDIDATE BYTES | These are constitutional authority and predecessor evidence dependencies, not AF-WP4 implementation bytes. |
| Navigation artifact | `docs/implementation/INDEX.md` | EXCLUDED FROM CANDIDATE BYTES | The INDEX is navigation and lifecycle synchronization evidence only; it grants no authority. |
| Governance evidence | This validation record | EXCLUDED FROM CANDIDATE BYTES | It is additive evidence created to record the identity result. |

This corpus determination preserves the separate boundaries between normative
implementation content, governance evidence, frozen predecessor evidence, and
navigation. No supporting artifact is silently folded into the AF-WP4
freeze-candidate bytes.

## 3. Exact corpus inventory

| Repository-relative path | Tracking state | Git blob status | SHA-256 | Line count | Byte size |
|---|---|---|---|---:|---:|
| `docs/implementation/ASSET_FOUNDATION_AF_WP4_RELEASE_ATTESTATION.md` | Untracked working-tree file | Working-tree blob ID `372ebf8680c3a4654ae65d769723c0bb6bd2a8de`; no committed `HEAD` blob exists | `5a3b3ce7a4a8874cc78c2a98fd0a2d64b6b5624f1d04a16b2272b5ba02c825cb` | 350 | 30145 |

The current repository `HEAD` at calculation was
`0e8528bd95bf71f1c2c99649a1d5bd758d6f4856`. The candidate was not staged and
was not tracked by `HEAD`; the recorded Git blob identity is therefore a
working-tree content identity, not a committed-HEAD identity.

## 4. Validation method

The identity calculation began only after all permitted candidate lifecycle
synchronization edits were complete. The candidate was read as exact current
working-tree bytes and validated by:

1. calculating SHA-256 twice from the working-tree file and confirming
   identical results;
2. calculating the Git blob identity from the same working-tree bytes without
   writing or staging a repository object;
3. counting the exact current file lines; and
4. measuring the exact current byte length.

Both SHA-256 calculations returned
`5a3b3ce7a4a8874cc78c2a98fd0a2d64b6b5624f1d04a16b2272b5ba02c825cb`.
The candidate was readable and stable across both calculations.

## 5. Validation result

**Disposition: `CONTENT IDENTITY VALIDATED`**

The recorded SHA-256, working-tree Git blob identity, line count, and byte
size identify the exact AF-WP4 implementation candidate intended for a later
freeze act. This result validates identity only. It does not state that the
candidate is frozen, canonical, closed, released, or available as canonical
owner-domain supply.

## 6. Excluded evidence and post-validation restrictions

- The allocation, authorization, independent review, and prior independent
  confirmation acts remain separate lifecycle evidence and are outside the
  candidate bytes.
- The planning corpus, architecture plan, roadmap, and AF-WP1 through AF-WP3
  artifacts remain frozen supporting evidence and were not modified or
  revalidated as part of this act.
- The INDEX and this validation record are supporting governance/navigation
  artifacts outside the AF-WP4 freeze-candidate corpus.
- The validated candidate bytes must not be edited before exact-byte freeze.
  Any byte change requires a new identity-validation act.
- This record grants no implementation, runtime, downstream, Ledger, release,
  closeout, or successor authority.

## 7. Current constitutional state and exact next step

AF-WP4 is content-identity validated and remains not frozen, not released, and
not closed. No release predicate was evaluated, no terminal disposition was
selected, and no additional authority was created.

**Exact next step: Perform exact-byte freeze of the validated AF-WP4 corpus.**

Exact-byte freeze is not performed by this record.
