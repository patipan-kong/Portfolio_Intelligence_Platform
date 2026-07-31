# M44-WP5 — RC4 Independent Constitutional Review

**Milestone:** M44 — Portfolio Analytics Gate Closure and Normative Semantics

**Work package:** M44-WP5 only

**Record class:** Non-normative constitutional review-chain governance record

**Review candidate:** `RC4`

**Review target:**
`docs/implementation/M44_WP5_ANNUALIZATION_BASIS_OWNERSHIP_DETERMINATION_AND_REQUIREMENT_SPECIFICATION.md`

**Reviewed candidate commit:** `6b2ab48f9c4f6eb2d018b586db56631c6dc9b200`

**Reviewed candidate blob:** `0eb18aab774da881c8071ddf0962485deb64a532`

**Reviewed candidate extent:** 1012 lines

**Review-time repository HEAD:** `6cb7e1a461d70e9cc7c7a762640f5585e3248777`

**Working tree at review time:** Clean

**Reviewer posture:** Author-independent; read-only; the candidate is assumed
defective until proved conforming against frozen text

**Determination:** `NOT APPROVED`

**RC3 finding dispositions:** 8 `RESOLVED`; 1 `NOT RESOLVED`; 0 `REGRESSED`;
0 `SUPERSEDED BY A NEW FINDING`

**Active findings after RC4:** 1 `CRITICAL`; 1 `MAJOR`; 1 `MINOR`;
0 `EDITORIAL` — total 3

**Approval granted by this record:** `NONE`

**Ownership determined by this record:** `NONE`

**G-3 disposition authority:** `NONE`

**G-4 disposition authority:** `NONE`

**§12.1.1 checkpoint disposition authority:** `NONE`

**M44-WP6 authorization:** `NONE`

**M44-WP7 authorization:** `NONE`

**Implementation authority:** `NONE`

**Runtime authority:** `NONE`

**Source-code authority:** `NONE`

**Persistence authority:** `NONE`

**Schema and migration authority:** `NONE`

**API and transport authority:** `NONE`

**UI and presentation authority:** `NONE`

**Provider authority:** `NONE`

**Production-method authority:** `NONE`

**Executable-validation authority:** `NONE`

**Contract-authoring, registration, extension, versioning, and serialization
authority:** `NONE`

**Vocabulary-admission authority:** `NONE`

**Frozen-artifact-amendment authority:** `NONE`

**Capability-completion authority:** `NONE`

---

## 1. Executive summary

This is the filed repository record for the historical RC4 independent
constitutional review of the M44-WP5 ownership determination and requirement
specification. It is not a new review. It files a review that was performed
read-only and author-independently against candidate blob
`0eb18aab774da881c8071ddf0962485deb64a532` at commit
`6b2ab48f9c4f6eb2d018b586db56631c6dc9b200`, with repository HEAD at
`6cb7e1a461d70e9cc7c7a762640f5585e3248777` and a clean working tree, and that
was not written to a repository path at the time it was performed.

RC4 reviewed the corrected candidate authored in response to RC3. RC4 performed
the per-finding verification of the RC3 disposition that frozen M44 Architecture
§12.4 requires of a corrected candidate, and found eight of RC3's nine findings
`RESOLVED`. One — RC3 `MINOR-4` — was found `NOT RESOLVED`. No RC3 finding
regressed, and no RC3 finding was superseded by a new finding.

RC4 nevertheless returned `NOT APPROVED` on three active findings: one
`CRITICAL`, one `MAJOR`, and one `MINOR`.

The `CRITICAL` finding was not against the candidate's substance. At the
review-time repository state the required RC2 and RC3 corrections-response
artifacts did not exist at any repository path, so the dispositions the RC3 and
RC4 candidates rest on were not inspectable from filed records. Frozen §12.4
fixes the lifecycle as "independent constitutional review → required-corrections
response if findings exist → independent confirmation → freeze," and frozen
§13.1 allocates the corrections-response artifact as part of the review chain.
The candidate's own §2.2 quotes both provisions and enumerates the chain, but
records only the unfiled RC3 review — it does not record that no
corrections-response artifact exists for either RC2 or RC3.

The `MAJOR` finding was a consequence of the RC3 correction itself. The RC3
`MAJOR-1` correction supplied §10.1 with a branch-local correction and
re-attempt mechanism that does not invoke §10.3. §10.2 is the other branch that
never enters review, confirmation, or freeze, and §10.3 expressly declares
itself inapplicable to it. §10.2 received no equivalent mechanism, so the
repository-proof-incomplete branch has no stated lawful correction and
re-attempt route.

The `MINOR` finding is the surviving remainder of RC3 `MINOR-4`. The correction
marked the branch applicability of §9 items 10 and 11 for the §10.1 branch
only. On the §10.2 branch an owner is proved, so §10.1's "no owner is proved"
reasoning does not transfer, and whether §8.6 was lawfully reached depends on
which §10.2 trigger fired. Early §10.2 applicability is therefore left
unresolved.

RC4 granted no approval, determined no owner, dispositioned no gate or
checkpoint, and authorized no downstream work. Filing this record grants nothing
that RC4 did not grant.

## 2. Reviewed repository state

Verified at review-time HEAD
`6cb7e1a461d70e9cc7c7a762640f5585e3248777`:

| Item | State at RC4 |
| --- | --- |
| Working tree | Clean |
| Reviewed candidate path | `docs/implementation/M44_WP5_ANNUALIZATION_BASIS_OWNERSHIP_DETERMINATION_AND_REQUIREMENT_SPECIFICATION.md` |
| Reviewed candidate commit | `6b2ab48f9c4f6eb2d018b586db56631c6dc9b200` |
| Reviewed candidate blob | `0eb18aab774da881c8071ddf0962485deb64a532` |
| Reviewed candidate extent | 1012 lines |
| M44-WP5 planning governance | `COMPLETE AND FROZEN` at planning candidate `RC3` |
| RC1 specification review record | Filed |
| RC1 formal corrections response | Filed |
| RC2 specification review record | Filed |
| RC2 formal corrections response | **Did not exist** |
| RC3 specification review record | Filed at `6cb7e1a` |
| RC3 formal corrections response | **Did not exist** |
| Frozen artifacts touched by `66b5b8b..6b2ab48` | None |
| M44-WP5 | `OPEN` |
| `G-3` | `OPEN — PARTIAL` |
| `G-4` | `NOT DETERMINED` |
| §12.1.1 checkpoint | `NOT DISPOSITIONED` |
| M44-WP6 | `NOT AUTHORIZED` |
| M44-WP7 | `NOT AUTHORIZED` |
| Implementation authority | `NONE` |
| Frozen M1–M44-WP4 artifacts | Unchanged |

The reviewed blob was the blob at the specification path at review-time HEAD:
`git ls-tree -r 6cb7e1a` returns
`0eb18aab774da881c8071ddf0962485deb64a532` for that path. The candidate commit
`6b2ab48` therefore remained the current state of the deliverable throughout the
review, and the only change between the candidate commit and review-time HEAD
was the filing of the RC3 review record.

The three filed `M44_WP5_RC1`, `RC2`, and `RC3` **architecture review** records
present at that commit target the M44-WP5 planning document. None of them
reviewed a specification candidate, and none is this record.

The absence of the RC2 and RC3 corrections-response artifacts at the review-time
state is the subject of `RC4-CRITICAL-1` at §6.1. It is a fact of the repository
at the time of review, not a later characterisation.

## 3. Review methodology

RC4 was conducted read-only, author-independent, and against frozen repository
text rather than against the candidate's own characterisations. Every asserted
authority was required to trace to an exact citation; every consumed frozen
provision was read at its frozen meaning; paraphrase of frozen normative text
was treated as a defect rather than a stylistic matter. RC4 was a full review of
the corrected candidate, not a delta review of the RC3 corrections, and it
additionally performed the per-finding verification of the RC3 disposition that
frozen M44 Architecture §12.4 requires of a corrected candidate.

RC4 evaluated authority; repository allocation; extension-basis usage;
normative correctness; the evidence model; the workflow; stopping conditions;
the failure model; stage correspondence; planning fidelity; frozen-text
fidelity; governance-chain consistency; authority ceilings; and internal
consistency.

Excluded from scope: the merits of any ownership hypothesis, the substance of
`G-4`, the §12.1.1 checkpoint, and any downstream work package.

### 3.1 Record provenance and its limits

The RC4 review was performed in an earlier session and was not filed at a
repository path when it was performed. This record is the filed governance
artifact for that review. It is documentary.

**The provenance of this record is weaker than that of the RC3 record, and the
difference is recorded here so that no reader assumes the two rest on the same
evidence.** The RC3 record at §3.1 was able to state that the original RC3
review narrative survived in full and had been recovered verbatim from an
authoring session transcript. **No equivalent claim can be made here. The
original RC4 review narrative does not survive in any retrievable session
output.**

A search of every session transcript for this project at
`~/.claude/projects/d--Works-TA-work-Portfolio-Intelligence-Platform/` was
performed for the RC4 finding identifiers, the RC4 finding titles, the reviewed
commit and blob abbreviations, the review-time HEAD, and the disposition
vocabulary. Every match returned lies in the authoring instructions that
directed the corrections-response work and this filing, or in the tool calls
made in the course of that work. No reviewer output was found. The RC4 reviewer's
own prose is not available to be reproduced.

What survives, and what is therefore carried through this record without
reconstruction, is the review's **result**: the determination `NOT APPROVED`;
the RC3 disposition totals; the identifier, classification, and stated condition
of each of the three active findings; and the active finding counts. These were
carried forward in the authoring instruction that directed this filing, and
`RC4-CRITICAL-1` was additionally carried forward — at the same identifier and
in the same terms — in the earlier instruction that directed the RC2 and RC3
corrections responses, before this filing was contemplated. That earlier
carry-forward is a contemporaneous, independent attestation of at least that
finding.

What does **not** survive, and is therefore **reconstruction**, is the
reviewer's reasoning: the per-finding constitutional rationale, the per-finding
exact-correction wording, the per-axis assessment at §5, and the wording of the
confirmation-readiness statement. Those are reconstructed in this record from
the surviving finding statements and from the reviewed blob itself. They are
marked as reconstruction at each place they appear. **They are not presented as
the reviewer's words, because they are not.**

Independent corroboration of the surviving result was performed against the
repository, and every element of it is mechanically re-derivable by a reader
with no access to any session output:

| Element | Corroboration in the repository |
| --- | --- |
| Reviewed commit and blob | `6b2ab48` exists; blob `0eb18aa` exists and is the blob that commit places at the specification path |
| Review-time HEAD and candidate identity | `6cb7e1a` exists and places blob `0eb18aa` at the same path; the tree is otherwise unchanged from `6b2ab48` |
| `RC4-CRITICAL-1` | Verified — `git ls-tree -r 6cb7e1a` returns no `RC2_FORMAL` or `RC3_FORMAL` corrections-response path (zero matches); candidate §2.2 quotes the frozen §13.1 corrections-response allocation at lines 229–231 and enumerates the chain at lines 234–252 without recording either absence |
| `RC4-MAJOR-1` | Verified in blob `0eb18aa` — §10.1's correction and re-attempt mechanism at lines 747–756; §10.2 at lines 813–849 carrying no equivalent; §10.3's inapplicability sentence at lines 853–855 |
| `RC3-MINOR-4` not resolved | Verified in blob `0eb18aa` — item 10's positive-vector condition at line 673 and its §10.1-only carve-out at lines 677–680; item 10's every-branch sentence at lines 691–694; item 11's §10.1-only carve-out at lines 698–701; no §10.2 applicability stated for either |
| RC3 dispositions `RESOLVED` | Each corroborated in blob `0eb18aa` or in the repository record set, as tabulated at §4 |
| Frozen artifacts unmodified | `git diff --name-only 66b5b8b 6b2ab48` returns only the specification and the RC2 review record; `INV-C1` held |

Three limits are recorded so that no reader mistakes this record for more than
it is.

First, and most importantly, **the reasoning in this record is reconstructed,
not reproduced.** A reader must treat §5 and the *constitutional rationale* and
*exact correction required* fields at §6 as this record's reconstruction of why
the recorded findings hold, not as the historical reviewer's text. The
identifiers, classifications, conditions, counts, dispositions, and
determination are the review's own.

Second, the surviving result reached this record through authoring instruction
rather than through a repository artifact or git history. A reader inspecting
only the repository cannot re-derive the fact that a review was performed on a
particular date by a particular independent reviewer. What such a reader can
independently verify is every finding's factual predicate, every count, the
reviewed commit and blob, and the review-time repository state, as tabulated
above.

Third, this filing is performed by the same party that authored the reviewed
candidate. The filing act is therefore not author-independent, even though the
review being filed was. This does not alter the review's recorded result, which
is carried through without modification, but it is why the review's own
determination — and not this filing — remains the operative governance fact, and
it is a further reason the reconstructed reasoning at §5 and §6 must not be read
as independent review output.

This record performs no re-review. It alters no finding, revises no
classification, upgrades and downgrades no severity, and applies no later
knowledge to any RC4 conclusion.

## 4. RC3 finding-disposition verification

RC4 verified the disposition of each of the nine findings recorded in
[M44_WP5_RC3_INDEPENDENT_CONSTITUTIONAL_REVIEW.md](M44_WP5_RC3_INDEPENDENT_CONSTITUTIONAL_REVIEW.md).
Each RC3 finding appears exactly once below, at its original RC3 classification.

| RC3 finding | RC3 class | RC4 disposition | Corroboration |
| --- | --- | --- | --- |
| `CRITICAL-1` — RC2 review not filed | `CRITICAL` | `RESOLVED` | The RC2 independent constitutional review record exists at the review-time state; `git diff --name-only 66b5b8b 6b2ab48` shows it filed within the candidate commit range |
| `MAJOR-1` — §10.1 routes to §10.3, which declares itself inapplicable | `MAJOR` | `RESOLVED` | In blob `0eb18aa`, "corrected within M44-WP5 under §10.3" is absent; the branch-local mechanism is at lines 747–756 with express bars on §10.3, §13, and WP5.6; §10.3's scoping sentence survives unchanged at lines 853–855 |
| `MINOR-1` — WP5.3–WP5.4 stage row omits caller-override rejection | `MINOR` | `RESOLVED` | In blob `0eb18aa`, the completed correspondence row at line 484; §8.6 caller-override item at line 578 and version non-substitutability at line 584; the conjunctive statement at line 588; the §10.2 stop trigger at lines 824–825 |
| `MINOR-2` — §2.1 misroutes an extension-basis defect to §10.1 | `MINOR` | `RESOLVED` | In blob `0eb18aa`, "§10.1 states the only route for such a defect" is absent; the Freeze Record §9 quotation and §1.6 rule 3 citation at lines 189–191; the documenting-not-exercising qualification at lines 192–196 |
| `MINOR-3` — checkpoint consequence unqualified as to agent | `MINOR` | `RESOLVED` | In blob `0eb18aa`, the agent-qualified consequence bullet at lines 742–743; the extended two-reading paragraph at lines 799–811 |
| `MINOR-4` — §9 items 10–12 unconditional in form | `MINOR` | **`NOT RESOLVED`** | Partially corrected for the §10.1 branch only; the residual condition is recorded as an active finding at §6.3 |
| `EDITORIAL-1` — truncated `INV-D2` quotation | `EDITORIAL` | `RESOLVED` | In blob `0eb18aa`, the restored clause "including the same rounding, ordering, and tie-break outcome" at lines 456–458 |
| `EDITORIAL-2` — "a later revision of this file" | `EDITORIAL` | `RESOLVED` | In blob `0eb18aa`, the phrase "a later revision of this file" is absent |
| `EDITORIAL-3` — §10.2 omits the two-reading qualifier | `EDITORIAL` | `RESOLVED` | In blob `0eb18aa`, the qualified §10.2 bullet at lines 836–837, matching the §10.1 bullet at lines 742–743 apart from its trailing referent |

**Disposition totals:**

| Disposition | Count |
| --- | ---: |
| `RESOLVED` | 8 |
| `NOT RESOLVED` | 1 |
| `REGRESSED` | 0 |
| `SUPERSEDED BY A NEW FINDING` | 0 |
| **Total** | **9** |

`RC4-MAJOR-1` at §6.2 concerns §10.2's want of the mechanism that the RC3
`MAJOR-1` correction supplied to §10.1. RC4 did not record it as a regression of
RC3 `MAJOR-1`, and did not record RC3 `MAJOR-1` as superseded: the RC3 finding
was against §10.1 and the correction to §10.1 holds. `RC4-MAJOR-1` is a distinct
active finding against a distinct subsection. Both counts above are therefore
zero, and the distinction is preserved here rather than harmonised away.

## 5. Constitutional assessment by review axis

> **Reconstruction notice.** The historical RC4 per-axis narrative does not
> survive. The table below is this record's reconstruction, built from the three
> surviving active findings, the surviving RC3 dispositions, and inspection of
> blob `0eb18aa`. For every axis marked conforming, what survives from RC4 is
> only that RC4 recorded no active finding on that axis — **not** the reviewer's
> reasoning for so concluding. The reasoning shown is this record's, and carries
> no independent review authority. See §3.1.

| Axis | Recorded RC4 result | Basis |
| --- | --- | --- |
| Authority | No active finding | Full `INV-A1` block present in blob `0eb18aa`, every declaration `NONE`; authority derived from frozen §§1.5, 8.4, 11, 13.1 |
| Repository allocation | No active finding | Sole deliverable at the exact frozen §13.1 path; §2.2 lines 254–258 correctly exclude review-chain records from the §1 and §12 bar on additional artifacts |
| Extension-basis usage | No active finding | Exactly one basis named under `INV-C2`; RC3 `MINOR-2` resolved at §2.1 lines 189–196 |
| Evidence model | No active finding | RC3 raised none and RC4 recorded none |
| Workflow | No active finding | RC3 `MINOR-1` resolved at §8.6 lines 578–588 and the correspondence row at line 484 |
| Stopping conditions | **Defective** | `RC4-MAJOR-1`; §10.2 lines 813–849 carry no correction and re-attempt mechanism while §10.3 lines 853–855 exclude the branch |
| Required repository evidence | **Defective** | `RC3-MINOR-4` not resolved; §9 items 10 and 11 state branch applicability for §10.1 only |
| Stage correspondence | No active finding | RC3 `MINOR-1` resolved |
| Planning fidelity | No active finding | RC3 raised none against the corrected text and RC4 recorded none |
| Frozen-text fidelity | No active finding | RC3 `EDITORIAL-1` resolved at lines 456–458 |
| Governance-chain consistency | **Defective** | `RC4-CRITICAL-1`; no RC2 or RC3 corrections-response artifact existed at the review-time state |
| Authority ceilings | No active finding | RC3 `EDITORIAL-2` resolved; §14 exclusions intact |
| Internal consistency | **Defective** | `RC4-MAJOR-1` and `RC3-MINOR-4` |

The candidate was assessed as constitutionally sound in posture and
substantially corrected in execution — eight of nine RC3 findings resolved, with
no regression — but not approvable while its stopping-condition set left one
branch without a correction route, while the branch applicability of its
required-evidence items remained partly unstated, and while the corrections
responses the review chain requires remained unfiled.

## 6. Complete active findings

Three active findings. Each appears exactly once, at its original
classification. Identifiers and classifications are carried through from the
historical review without modification.

> **Reconstruction notice.** For each finding below, the *identifier*,
> *classification*, and *exact condition* are carried through from the surviving
> RC4 result. The *affected sections*, *constitutional rationale*, and *exact
> correction required* are this record's reconstruction against blob `0eb18aa`,
> because the reviewer's own wording for those fields does not survive. See
> §3.1.

### 6.1 CRITICAL

#### `RC4-CRITICAL-1` — Required RC2 and RC3 corrections-response artifacts are absent

*Classification:* `CRITICAL`

*Exact condition (carried through from RC4):* Required RC2 and RC3
corrections-response artifacts are absent.

*Affected sections (reconstructed):* the review chain as a whole; candidate
§2.2, lines 225–258, which discloses the chain's state but records neither
absence.

*Constitutional rationale (reconstructed):* Frozen M44 Architecture §12.4 fixes
the lifecycle as "independent constitutional review → required-corrections
response if findings exist → independent confirmation → freeze." Frozen §13.1
allocates "[p]er-work-package independent review, corrections-response, and
confirmation artifacts" to the review chain. RC1 `NOT APPROVED`, RC2
`NOT APPROVED`, and RC3 `NOT APPROVED` each carried findings, so a
corrections-response artifact was required for each. Only the RC1 response was
filed. At the review-time state `git ls-tree -r 6cb7e1a` returns no
corrections-response path for RC2 or for RC3, so the dispositions on which the
RC3 and RC4 candidates rest are inspectable only from the author's commit
messages and from the candidate's own characterisations — not from filed
records. The candidate quotes both frozen provisions at §2.2 lines 227–231 and
then enumerates the chain at lines 234–252, recording the unfiled RC3 review at
lines 249–252 while recording neither missing corrections response. Correct
disclosure of one gap does not cure the two undisclosed ones, and the candidate
cannot be treated as reviewed to conclusion while the chain's mandated links are
absent.

*Exact correction required (reconstructed):* File the RC2 and RC3
corrections-response artifacts at repository paths, so that the disposition of
every RC2 and every RC3 finding becomes inspectable from filed records, and
update candidate §2.2 to state the chain's actual state. This is not corrected
by editing the specification's substance.

*Status note.* The required correction was performed later, at commit
`e02a50bfe929c3a2ccfbce8455f47d812595ba67`. That is recorded at §11 as
chronology. It does not alter this finding, which is preserved as RC4 recorded
it, and this record does not mark the finding resolved.

### 6.2 MAJOR

#### `RC4-MAJOR-1` — §10.2 has no lawful correction and re-attempt mechanism

*Classification:* `MAJOR`

*Exact condition (carried through from RC4):* §10.2 has no lawful correction and
re-attempt mechanism.

*Affected sections (reconstructed):* §10.2, lines 813–849; §10.1, lines
747–756; §10.3, lines 853–855.

*Constitutional rationale (reconstructed):* The RC3 `MAJOR-1` correction
supplied §10.1 with a branch-local route: the determination record "is corrected
within M44-WP5 by correcting the determination record and re-attempting the
determination from §8.1 under this same specification," expressly not entering
or invoking §10.3 or §13 and not beginning WP5.6, with a re-attempt that again
fails §7 stopping "again under this subsection." §10.2 is the other stopping
branch. §10.3 states at lines 853–855 that it "is inapplicable to the §10.1 and
§10.2 branches, which never enter review, confirmation, or freeze," so §10.2
cannot route a defect there. §10.2's own text states the branch's consequences
at lines 829–839 and bars §8.7 and §13 at lines 845–849, but states no means by
which a record that stopped under §10.2 may be corrected and the determination
re-attempted. The branch is therefore terminal in form without being terminal in
substance: a repository-proof defect is a work-package defect of the same class
§10.1 now provides for, and the specification supplies the route for one branch
and not the other. This is the same defect class RC3 recorded at `MAJOR-1`,
surviving at the subsection the correction did not reach.

*Exact correction required (reconstructed):* State in §10.2 a branch-local
correction and re-attempt mechanism on the same terms §10.1 now carries —
correction of the determination record and re-attempt from the stage the branch
permits, under this same specification, expressly as an authoring act within
M44-WP5 that is not a review, confirmation, or freeze stage, that does not enter
or invoke §10.3 or §13, and that does not begin WP5.6 — together with the
consequence of a re-attempt that again fails. §10.3 must remain unchanged.

### 6.3 MINOR

#### `RC3-MINOR-4` — Early §10.2 applicability remains ambiguous

*Classification:* `MINOR`

*Exact condition (carried through from RC4):* Early §10.2 applicability remains
ambiguous.

*Identifier note.* This finding is carried at its RC3 identifier and RC3
classification because it is the unresolved remainder of RC3 `MINOR-4`, not a
new finding — which is why RC4's `NOT RESOLVED` count is 1 and its
`SUPERSEDED BY A NEW FINDING` count is 0. The heading above states the residual
condition as RC4 recorded it. It is not a rename of the RC3 finding. The filed
RC3 record's heading for `MINOR-4` reads: "§9 items 10–12 are unconditional in
form, and item 10's positive vector is in tension with §10.1's bar on
§§8.5–8.7." Both wordings are recorded here so that neither displaces the other.

*Affected sections (reconstructed):* §9 item 10, lines 670–694; §9 item 11,
lines 695–701; §10.2, lines 815–827.

*Constitutional rationale (reconstructed):* RC3 `MINOR-4` required items 10–12
to be marked with their branch applicability in the same form as items 7–9. The
correction did so for the §10.1 branch. Item 12 was made branch-general at lines
702–708 and is not in issue. Items 10 and 11 remain incomplete for §10.2. Item
10 conditions the positive vector on "**If §8.6 is lawfully reached**" at line
673 and then resolves only one branch — "[o]n the §10.1 branch no owner is
proved and §§8.5–8.7 MUST NOT begin, so no positive vector is produced" at lines
677–680 — while stating at lines 691–694 that the negative and rejection vectors
"are required on every branch, including the §10.1 and §10.2 stopping branches;
only the positive vector is branch-conditioned." The branch-conditioned element
is thus the one element whose §10.2 treatment is never stated. Item 11 has the
same shape: it carves out "[o]n the §10.1 branch, where no owner is proved" at
lines 698–701 and says nothing of §10.2. The §10.1 reasoning cannot be
transferred, because §10.2 opens "[a]fter ownership is proved" at line 815. On
§10.2 the answer therefore turns on whether §8.6 was lawfully reached, and the
branch's triggers are not uniform in that respect: the corpus-boundary and
searchability triggers at lines 818–821 arise at §8.5, before §8.6, while the
caller-override and canonical-bytes triggers at lines 822–827 arise within it. A
reader cannot determine from the text whether an early §10.2 stop requires
item 10's positive vector or item 11's owner-published side. The ambiguity RC3
identified therefore survives for the early §10.2 case.

*Exact correction required (reconstructed):* Mark items 10 and 11 with their
§10.2 applicability in the same form already used for §10.1, distinguishing a
§10.2 stop that occurs before §8.6 is lawfully reached from one that occurs
within it, and stating for each whether the positive vector and the
owner-published side of the boundary example are produced.

## 7. Findings count

| Classification | Count | Identifiers |
| --- | ---: | --- |
| `CRITICAL` | 1 | `RC4-CRITICAL-1` |
| `MAJOR` | 1 | `RC4-MAJOR-1` |
| `MINOR` | 1 | `RC3-MINOR-4` |
| `EDITORIAL` | 0 | — |
| **Total** | **3** | |

Two of the three are correctable within the candidate. `RC4-CRITICAL-1` is
corrected by filing governance records, not by editing the specification.

## 8. Overall determination

`NOT APPROVED`

## 9. Confirmation-readiness statement

> The wording of the historical RC4 confirmation-readiness statement does not
> survive. What survives is the determination and the active finding set. This
> section states the position those entail; see §3.1.

The specification is **NOT READY** for Independent Constitutional Confirmation.

Under frozen M44 Architecture §12.4, confirmation follows an independent review
and, where findings exist, a required-corrections response. Three active
findings exist, one of them `CRITICAL`. A corrected candidate is required, and
under §12.4 that corrected candidate requires a renewed full author-independent
constitutional review before confirmation is reachable.

Four constraints govern the correction:

1. No correction may amend, reinterpret, or supersede any frozen artifact.
   `INV-C1` holds throughout.
2. No correction may name or imply an owner, disposition `G-3`, `G-4`, or the
   §12.1.1 checkpoint, or authorize M44-WP6, M44-WP7, or any implementation
   work.
3. No correction may re-scope M44-WP5 or alter its frozen authority ceiling.
   Every `INV-A1` declaration remains `NONE`.
4. The corrected candidate is a new candidate of the same allocated deliverable,
   at the same frozen §13.1 path. It is not an edit of a confirmed artifact and
   it creates no second deliverable.

Nothing in this record constitutes a claim that the review chain is closed, that
confirmation is available, or that any remaining step may be shortened.

## 10. Explicit status confirmation

Filing this record changes no governance status. As at this filing:

| Item | Status |
| --- | --- |
| M44-WP5 specification | `NOT APPROVED` at candidate `RC4` |
| Implementation authority | `NONE` |
| Ownership | `NOT DETERMINED` |
| `G-3` | `OPEN — PARTIAL` |
| `G-4` | `NOT DETERMINED` |
| §12.1.1 checkpoint | `NOT DISPOSITIONED` |
| M44-WP6 | `NOT AUTHORIZED` |
| M44-WP7 | `NOT AUTHORIZED` |
| Independent Constitutional Confirmation | `NOT ISSUED` |
| Frozen artifacts | Unchanged |

This record determines no owner, dispositions no gate, evaluates no checkpoint,
authorizes no work package, grants no implementation authority, and amends no
frozen artifact. It does not evaluate or disposition §12.1.1, and it does not
determine `G-4`. It creates one review-chain governance record under frozen
§13.1 and does nothing else.

## 11. Historical-integrity and provenance statement

This is the repository filing of the historical RC4 independent constitutional
review of the M44-WP5 specification. It is not a new review, and no part of it
constitutes a review act.

The following are disclosed expressly.

1. **This is a filing, not a review.** The RC4 review was conducted against blob
   `0eb18aa` at commit `6b2ab48`, with repository HEAD at `6cb7e1a` and a clean
   working tree, in an earlier session. It was **author-independent and
   read-only**. It was not written to a repository path at the time. This record
   creates the missing §13.1 review-chain artifact and does nothing else.

2. **The review's result is carried through; its reasoning is reconstructed.**
   The determination, the RC3 disposition totals, the active finding
   identifiers, classifications, conditions, and counts are the review's own.
   The per-finding rationale and correction wording at §6, the per-axis
   assessment at §5, and the confirmation-readiness wording at §9 are this
   record's reconstruction, because the RC4 reviewer's prose does not survive in
   any retrievable session output. §3.1 records the search performed and its
   result. **This reconstruction limit is disclosed rather than concealed, and
   no provenance stronger than the evidence is claimed.**

3. **The later corrections-response filing does not retroactively alter this
   review.** The RC2 and RC3 formal constitutional corrections responses were
   filed at commit `e02a50bfe929c3a2ccfbce8455f47d812595ba67`, after RC4 was
   performed. RC4 reviewed the repository as it stood at `6cb7e1a`, where those
   artifacts did not exist. Nothing filed after the review changes what the
   review found, and no later artifact is treated here as having been available
   to the reviewer.

4. **`RC4-CRITICAL-1` remains part of the historical review even though its
   required correction was later performed.** The finding is preserved at §6.1
   at its original classification and in its original terms. This record does
   **not** mark it resolved. Whether the later filing discharges it is a
   question for a subsequent author-independent review, not for this filing —
   and the responses filed at `e02a50b` disclose their own limits, including
   that the RC2 response inherits the RC2 record's reconstruction limit.

5. **No later work is incorporated.** No RC5 candidate, RC5 review, or any other
   later constitutional work has informed any finding, classification, condition,
   count, disposition, or the determination recorded here. No such work is known
   to this record, and none is referenced. Where later chronology is
   constitutionally relevant it appears only at §11.6, and only as chronology.

6. **Chronology.** In order: candidate `RC3` at `66b5b8b`; the RC2
   independent constitutional review record filed at `6ad7f3b`; candidate `RC4`
   at `6b2ab48`; the RC3 independent constitutional review record filed at
   `6cb7e1a`; **the RC4 independent constitutional review performed, read-only,
   against `0eb18aa` at HEAD `6cb7e1a`** — returning `NOT APPROVED`; the RC2 and
   RC3 formal constitutional corrections responses filed at `e02a50b`; this
   record filed. The review being filed here occurred before the last two
   entries, and is recorded as it stood at its own time.

7. **This filing is not author-independent.** It is performed by the same party
   that authored the reviewed candidate. The review being filed was independent;
   this filing is not. Filing grants nothing that RC4 did not grant, and the
   reconstructed material at §5, §6, and §9 carries no review authority
   whatsoever.

8. **This record is a review-chain artifact, not a WP5 deliverable.** It is a
   non-normative governance record under frozen §13.1. It is not an M44-WP5
   determination, requirement-specification, or constitutional-process artifact,
   and it is not an additional M44-WP5 normative deliverable. Candidate §1 and
   §12 continue to permit no additional artifact of those classes, and this
   record creates none.

The operative governance fact remains the review's own determination:
`NOT APPROVED`.
