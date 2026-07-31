# M45 Architecture Candidate — Second Focused Independent Re-Review

**Artifact class:** Additive independent review record
**Review round:** Second focused re-review (targeted to N-1, N-2, N-3)
**Reviewed candidate status:** `PLANNING CANDIDATE — NOT RATIFIED`
**Final disposition:** `CORRECTIONS REQUIRED`
**N-1:** `RESOLVED`  **N-2:** `RESOLVED`  **N-3:** `RESOLVED`
**F-1 … F-10 regression:** no regression; all ten remain resolved
**New findings:** `BLOCKING` 0 · `MAJOR` 0 · `MINOR` 1 (N-4) · `ADVISORY` 1 (A-8)
**Advisories A-6, A-7:** both `ADOPTED` and accurately implemented
**Ratification performed:** `NO`
**Independent confirmation performed:** `NO`
**Freeze performed:** `NO`
**Work-package authorization performed:** `NO`

---

## 1. Review scope

This is a second focused re-review only. It is bounded to:

1. whether findings `N-1`, `N-2`, and `N-3` from
   [M45 Architecture Focused Re-Review](M45_ARCHITECTURE_FOCUSED_REREVIEW.md)
   are resolved at the root of the defect, not merely in wording;
2. whether advisories `A-6` and `A-7` were accurately adopted;
3. a regression scan confirming that `F-1` through `F-10` from
   [M45 Architecture Independent Review](M45_ARCHITECTURE_INDEPENDENT_REVIEW.md)
   remain resolved; and
4. whether the targeted corrections themselves introduce a new constitutional
   defect.

This review does not restart the original architecture review, does not
redesign the milestone, and introduces no review scope beyond defects created
by the corrections themselves. No resolved finding is reopened under a new
identifier for wording preference.

This review performs no ratification, confirmation, freeze, gate change, or
work-package authorization, and modifies no candidate, frozen, navigation, or
non-documentary file.

---

## 2. Evidence examined

Read in full:

- [M45 Architecture Focused Re-Review](M45_ARCHITECTURE_FOCUSED_REREVIEW.md)
- [M45 Architecture Review — Corrections Response](M45_ARCHITECTURE_REVIEW_CORRECTIONS_RESPONSE.md)
- corrected [M45 Architecture and Implementation Plan](M45_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md)
- corrected [M45 Work-Package Decomposition and Roadmap](M45_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md)

Frozen sources verified directly, at the exact sections cited by the
corrections, rather than through the correction author's summary:

| Frozen source | Sections verified | Purpose |
| --- | --- | --- |
| [Platform Architecture](../architecture/platform_architecture.md) | §4 Laws 1–15; §11 G1–G6; §12 V1–V4 | `N-2` title, numbering, and meaning verification |
| [M44 G-3 Closure and WP6-Entry Roadmap](M44_G3_CLOSURE_AND_WP6_ENTRY_ROADMAP.md) | §9 five-condition WP6-0 boundary; §13 ordered permission conditions | `N-1` mapping and ordering verification |
| [M44 Architecture](M44_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) | §4.1 (`I-7`, `I-8`) | `F-8` regression |
| [M43-WP7 Plan](M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) | §3.1; §3.2 items 5–6; §3.3 | `A-7` anchor verification |
| [M43-WP4 Plan](M43_WP4_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) | §§6.1–6.11 | `F-7` regression |
| [M44-WP4 Contract](M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md) | `WP4-NR-032` | `F-2` regression |
| [M42-WP3 Stage B](M42_WP3_STAGE_B_INVESTMENT_UNIVERSE_DECLARATION_CONTRACT_SPECIFICATION.md) | §9.2 | `F-2` regression |
| [M44-WP1 Reconciliation](M44_WP1_ROADMAP_AND_CURRENT_STATE_RECONCILIATION.md) | §6.6 | `F-2` regression |

---

## 3. Reviewer independence statement

This record is issued by the same independent reviewer who authored the
original independent review and the first focused re-review. The reviewer:

- did not author, co-author, edit, or advise on either planning candidate or
  on the corrections response;
- did not modify any candidate artifact in this round;
- verified the constitutional and frozen sources directly rather than
  accepting any correction summary; and
- holds no ratification, confirmation, freeze, gate, or authorization power,
  and exercised none.

Independence from the candidate author is preserved. Continuity of reviewer
identity across rounds is a review-quality property; it does not merge the
reviewer role with the author role or with the later independent confirmer,
who must be distinct from both.

---

## 4. N-1 determination

**Original finding (MAJOR):** M45-WP5 had no authorization act distinct from
M45-WP4's own checkpoint disposition. The candidate bound itself to the frozen
WP6-0 boundary while collapsing frozen condition 1 (a *separately authorized*
governance act) into frozen condition 3 (a distinct confirmed authorizing
checkpoint), thereby weakening the boundary it adopted.

**Status: `RESOLVED`.**

### 4.1 A substantive, genuinely distinct authorization act now exists

Architecture §4.4 introduces a **Substantive M45-WP5 authorization lifecycle
stage**, declared expressly as "an external governance stage in the M45
execution dependency model, not an eighth M45 work package and not an act
performed by WP4." Its terminal dispositions are exactly
`WP5 SUBSTANTIVE WORK AUTHORIZED` and `WP5 SUBSTANTIVE WORK NOT AUTHORIZED`.

Distinctness was tested against each act the finding named:

| Act it must not be | Where distinctness is stated | Verified |
| --- | --- | --- |
| Architecture ratification | Architecture §4.4 closing paragraph; §4.2 stage 7; roadmap §1 | Yes |
| Architecture freeze | Architecture §4.4 closing paragraph; §4.2 stage 8; roadmap §1 | Yes |
| WP1 authorization | Architecture §4.4 closing paragraph; §4.2 stage 9; roadmap §1 | Yes |
| `G-3` closure | Roadmap §1; roadmap §5 (authorization is verified *before* any G-3 act) | Yes |
| WP4 checkpoint disposition | Architecture §4.4 prohibited actions ("issue the prospective checkpoint"); roadmap §5 | Yes |
| WP4 entry verification | Architecture §4.4 prohibited actions ("perform WP4 entry verification"); roadmap §5 | Yes |

Architecture §4.4 additionally forbids inferring the authority from
"architecture ratification or freeze, WP1 authorization, `G-3 CLOSED`, review
approval, frozen WP3 evidence, the M45 label, or WP4." This closes the exact
inference paths the finding identified.

### 4.2 The required properties

- **Competent actor may remain unidentified.** Architecture §4.4 names the
  actor only as "Separately competent substantive-work governance authority;
  not identified by the frozen sources or this candidate." Roadmap §1 repeats
  "Separately competent authority not identified by this candidate." This is
  correct: the absence is recorded as a present blocker, consistent with
  architecture §4.1.
- **No authority is invented.** Architecture §4.4 states "no M45 artifact may
  invent the unidentified competent authority." Nothing in either artifact
  confers, delegates, or constructs the authority.
- **The authorization record is external.** It appears in architecture §5.2
  ("External predecessor conditions"; M45 power: "Verify only; never infer,
  issue, or widen") and roadmap §1 ("External predecessor conditions — not M45
  work packages"; "receive no M45 identifiers"). It is carried in no M45 work
  package.
- **WP4 neither issues nor infers it.** Roadmap §5: "WP4 does not authorize
  substantive WP5 work. It verifies a separately issued authorization record."
  Roadmap §5 freeze boundary: WP4 "neither issues substantive WP5 authority,
  alters M44, nor makes WP5 output exist."
- **WP5 cannot begin without it.** Roadmap §6 Dependencies enumerates five
  non-substitutable dependency classes and closes with "WP4's disposition
  alone cannot release WP5." Roadmap §6 exit criteria require the separate
  `WP5 SUBSTANTIVE WORK AUTHORIZED` record to be cited by exact identity
  before authoring began. Architecture §7 mirrors this in the WP5 release
  condition.
- **Refusal routes truthfully to WP7.** An absent or negative record produces
  `WP5 ENTRY BLOCKED — SUBSTANTIVE AUTHORIZATION ABSENT OR NOT AUTHORIZED`
  and routes `TB-4` to WP7 "without changing G-3 or checkpoint truth"
  (roadmap §5). Architecture §10 and roadmap §10 record it as a valid
  operational outcome, not an architecture failure. See `N-4` below for a
  residual routing-locus inconsistency; it does not affect the distinctness
  holding.

### 4.3 Complete five-condition mapping

Roadmap §5 reproduces the frozen
[M44 G-3 Roadmap](M44_G3_CLOSURE_AND_WP6_ENTRY_ROADMAP.md) §9 boundary and
assigns a distinct satisfier to each condition. Verified against the frozen
text condition by condition:

| Frozen §9 condition (verified verbatim) | Candidate satisfier | Distinct record | Assessment |
| --- | --- | --- | --- |
| 1. a separately authorized future governance act explicitly authorizes substantive work | External substantive M45-WP5 authorization stage | Content-identified `WP5 SUBSTANTIVE WORK AUTHORIZED` record | Correct; no longer shared with condition 3 |
| 2. `G-3 CLOSED` evidence is valid, complete, independently confirmed, and traceable to frozen owner-domain forms | Frozen WP3 evidence/formability package plus WP4's separate G-3 determination | Frozen WP3 manifest, formability and two-reader records; confirmed WP4 G-3 determination | Correct; evidence and determination are separate artifacts |
| 3. a distinct independently confirmed authorizing checkpoint disposition exists | WP4 prospective-checkpoint phase | Independently confirmed authorizing checkpoint disposition | Correct; expressly "distinct from its G-3 determination and entry verification" |
| 4. M44-WP4 and M44-WP5 remain frozen and their cited outputs resolve at exact canonical paths | WP1 exact predecessor-path and identity verification | Frozen WP1 baseline/content-identity register | Correct |
| 5. the historic `STOP` is not bypassed by implication | WP1 historic-`STOP` preservation determination | Frozen WP1 gate/checkpoint entry-state and historic-`STOP` preservation record | Correct; expressly "distinct from exact-path verification and the prospective checkpoint" |

No single M45 act satisfies more than one condition. Conditions 2 and 3 both
involve WP4 but are assigned to two separate, separately confirmed acts, which
is what frozen §9 requires. Roadmap §5 states the controlling rule directly:
"The WP4 entry-verification act only verifies those five pre-existing facts;
it satisfies none of them and cannot create a missing authorization, gate
closure, checkpoint, frozen path, or non-bypass fact." Each condition also
carries an explicit fail-closed outcome.

### 4.4 Ordering conforms to the frozen permission boundary

Frozen [M44 G-3 Roadmap](M44_G3_CLOSURE_AND_WP6_ENTRY_ROADMAP.md) §13 requires
its four conditions "in order": substantive authorization, then valid
`G-3 CLOSED`, then a distinct confirmed authorizing checkpoint, then entry
verification. Roadmap §5 scope and §5 expected sequence apply exactly that
order prospectively, verifying the authorization record "before any G-3 or
checkpoint act." Architecture §9 items 7–10 and roadmap §9 stages 4–6B follow
the same order. This is a refinement in the direction of the frozen boundary,
consistent with G2, and no circularity is created: the authorization stage's
declared inputs are the frozen WP3 evidence and the frozen M44 prerequisites,
and its permitted action is expressly "subject to the later G-3 determination,
prospective checkpoint, and five-condition entry verification."

The correction resolves the constitutional defect at its root: frozen
condition 1 now has an owner outside M45 that no M45 act can supply.

---

## 5. N-2 determination

**Original finding (MAJOR):** Architecture §6.1 and §6.2 claimed compliance
with the Platform Laws and governance rules while restating them under invented
titles — eleven of fifteen law titles did not match the constitution, G2/G4/G6
were substituted, and G3 was rendered as frozen `WP4-NR-001`. Law 1, Laws 3–12,
G2, G4, and G6 were therefore never actually assessed, and the section
constituted the private dialect that frozen risk `R-10` and V2 warn against.

**Status: `RESOLVED`.**

### 5.1 Platform Laws 1–15 — title-by-title verification

Verified against [Platform Architecture](../architecture/platform_architecture.md)
§4, which is the constitution's own binding section ("The constitutional laws
… this section is binding"). Architecture §6.1 now states the source section
explicitly and quotes each title.

| Law | Constitutional title (§4) | Candidate §6.1 title | Match |
| --- | --- | --- | --- |
| 1 | The ledger is the single source of truth | identical | Yes |
| 2 | Recorded history is immutable | identical | Yes |
| 3 | Holdings are derived | identical | Yes |
| 4 | Replay is deterministic and reproducible | identical | Yes |
| 5 | Asset identity is permanent | identical | Yes |
| 6 | Identity is resolved decisively or not at all | identical | Yes |
| 7 | AI never performs accounting | identical | Yes |
| 8 | Evaluation observes; it never touches | identical | Yes |
| 9 | Every business rule has exactly one implementation | identical | Yes |
| 10 | The core never knows the edge | identical | Yes |
| 11 | Everything enters through the hallway | identical | Yes |
| 12 | The human owns the ledger and the decision point | identical | Yes |
| 13 | Failure is loud | identical | Yes |
| 14 | Explainability is a fiduciary duty | identical | Yes |
| 15 | Correctness outranks everything | identical | Yes |

All fifteen laws are now present, correctly numbered, exactly titled, and each
carries a substantive engagement classification and compliance statement. The
previously unassessed laws are assessed. Spot-checking the substance: Law 3's
entry correctly reports that M45 introduces no derived runtime state rather
than asserting a false operational engagement; Law 9's entry correctly ties
"one normative home" to WP5 and WP6 without claiming an implementation
property; Law 11's entry correctly distinguishes documentary evidence intake
from the ingestion hallway. No compliance claim overstates what a documentary
planning candidate can do, and none weakens a law.

### 5.2 Governance Rules G1–G6 — verification

Verified against [Platform Architecture](../architecture/platform_architecture.md)
§11, correctly cited by the candidate.

| Rule | Constitutional title (§11) | Candidate §6.2 title | Match |
| --- | --- | --- | --- |
| G1 | Higher states intent; lower states reality | identical | Yes |
| G2 | Lower may refine, never weaken | identical | Yes |
| G3 | Silence delegates | identical | Yes |
| G4 | Conflict is a defect, resolved upward | identical | Yes |
| G5 | Each level amends by its own mechanism | identical | Yes |
| G6 | Code is never precedent | identical | Yes |

The substituted rules are gone. Meaning was checked, not only titles:

- **G3** now reads as the constitution does — "Where a higher source is
  silent, M45 records the decision at the proper level only under competent
  authority" — and adds "silence does not identify that authority or settle an
  existing explicit prohibition." That addition constrains rather than
  relaxes, which G2 permits, and it no longer misattributes frozen
  `WP4-NR-001` as a constitutional rule.
- **G4** correctly forbids resolution "by recency, authorship, or
  implementation evidence," matching §11's prohibition on recency, seniority,
  and running code.
- **G6** correctly restricts code to evidence of current reality.

### 5.3 Vocabulary Rules V1–V4 — verification

Verified against [Platform Architecture](../architecture/platform_architecture.md)
§12, correctly cited.

| Rule | Constitutional title (§12) | Candidate §6.3 title | Match |
| --- | --- | --- | --- |
| V1 | One term, one meaning, one home | identical | Yes |
| V2 | New nouns are registered before they are relied upon | identical | Yes |
| V3 | Constitutional terms carry constitutional weight | identical | Yes |
| V4 | The vocabulary serves every level | identical | Yes |

V3's compliance entry correctly names reserved constitutional terms rather
than redefining them.

### 5.4 Separation of engineering constraints from constitutional rules

Architecture §6.4 is now titled "M45-derived architectural constraints" and
opens with "These are not constitutional Laws or Governance Rules." Each row
carries an explicit basis column that distinguishes a direct consequence of a
frozen record from a candidate-specific planning constraint. The candidate's
own commitments are therefore no longer presented as constitutional text. This
is the structural fix the finding required.

### 5.5 Corpus-wide scan

Both planning artifacts were scanned for any remaining constitutional
restatement. The roadmap contains no laws or governance-rules table and cites
constitutional rules only by exact number where needed. No invented
constitutional title, substituted governance rule, renumbering, or private
constitutional dialect remains in either artifact. Frozen non-constitutional
rules such as `WP4-NR-032` are cited by their own identifiers and are not
presented as constitutional rules.

---

## 6. N-3 determination

**Original finding (MINOR):** WP7's terminal-branch enumeration omitted a
frozen WP3 blocked/non-formable outcome, contradicting the roadmap's own
fail-closed path list and stage table.

**Status: `RESOLVED`.**

A single canonical inventory now exists. Roadmap §12.1 is designated
"Canonical post-WP1 terminal-branch inventory" and states that it "is
exhaustive and is reused by WP7 Dependencies and the consolidated stage
table."

| Location | Content | Consistent with §12.1 |
| --- | --- | --- |
| Roadmap §12.1 (canonical) | TB-1 … TB-6 | — |
| Roadmap §8 WP7 Dependencies | TB-1 … TB-6, identical text | Yes |
| Roadmap §12 "Valid fail-closed M45 paths after WP1" | TB-1, TB-2, TB-3, TB-4, TB-6; TB-5 identified as the intended path | Yes |
| Roadmap §9 stage table | 5A: TB-1, TB-2, TB-4; 6A: TB-3, TB-6; stage 8: exactly one of TB-1 … TB-6 | Yes |
| Architecture §12.3 | TB-1 … TB-6, identical text, citing roadmap §12.1 | Yes |
| Architecture §12.1 item 9 | closeout names exactly one TB-1 … TB-6 branch | Yes |
| Architecture §5.5 dependency diagram | TB-1 … TB-6 all present | Yes as to inventory; see `N-4` as to the TB-4 locus |

The omitted WP3 outcome is now `TB-2` in every location. Branch
non-substitutability is stated identically in roadmap §12.1, roadmap §8, and
architecture §12.3: "TB-2 does not pass through WP4, and TB-4 is not a
checkpoint `STOP`."

**Can WP7 close truthfully from every lawful branch?** Yes for all six
branches. Each branch is defined by an existing frozen predecessor
determination, so WP7's exit criteria ("every started WP has an exact terminal
lifecycle state"; "no unperformed WP is reported complete or frozen") can be
satisfied without WP7 creating or completing another package. The one
qualification is `TB-4`, whose producing act is described inconsistently
across the corpus; that is recorded as `N-4` and is a locus defect, not an
inventory defect.

---

## 7. Regression scan

Regression only. Each item was re-verified against the corrected text.

| Finding | Regression check | Verified location | Status |
| --- | --- | --- | --- |
| F-1 | Cross-domain work packages remain absent | Seven WPs only, all Portfolio Intelligence-owned (architecture §7; roadmap §§2–8). External domains appear only in architecture §5.2 and roadmap §1, with no M45 identifiers and "M45 cannot request, commission, schedule, govern, review, confirm, correct, or freeze these external acts." Architecture §2.4 non-goal retained. | No regression |
| F-2 | No nested-form authoring returns | Architecture §5.3 retains "Therefore `WP4-NR-032` remains controlling. M45 performs no form authoring," with the five external-act requirements. Roadmap §1 retains "M45 authors none of those forms" and the M42-WP3 §9.2 / M44-WP1 §6.6 / `WP4-NR-032` / G-3 Roadmap §4 reconciliation. Architecture §2.4 non-goal retained. | No regression |
| F-3 | WP1 still cannot self-authorize | Roadmap §2: "WP1 does not settle `OQ-5`, determine its own competence, write the Decision Log, or close G-2"; exit criteria bar any Decision Log write; risks name self-authorization. Architecture §12.1 item 8 confines Decision Log/INDEX change to explicit competent synchronization authority. | No regression |
| F-4 | Allocation / confirmation / ratification / freeze / WP1 authorization remain distinct | Architecture §4.2 nine-stage table intact with distinct actors, outputs, and terminal dispositions, closing "Review approval is not confirmation. Confirmation is not ratification. Ratification is not WP1 authorization." The new §4.4 stage is declared external and additional, not a renumbering of the nine stages. Roadmap §0 restates the separation. | No regression; strengthened |
| F-5 | Review-before-freeze lifecycle preserved | Architecture §8.1 `DRAFT → … → FROZEN` chain and §8.2 additive `RCn` rule intact; roadmap §0 universal lifecycle intact; every WP (§§2–8) retains its own review, confirmation, identity-validation, and freeze boundary; WP3 still reviews before freeze. | No regression |
| F-6 | Procedural neutrality preserved | Architecture §1.1 ("M45 does not define success as `G-3 CLOSED`"), §2.2 "Conditions examined, not predetermined outcomes," §12.3 fail-closed completion; roadmap §5 "A confirmed `STOP` is a successful procedural WP4 result." The new refusal outcome is likewise recorded as valid, "not an architecture failure." | No regression |
| F-7 | A–K attribution preserved | Roadmap §6: allocation "originates in frozen M43-WP4 §§6.1–6.11"; M44-WP6 credited only with carried-forward entry, atomicity, and no-result-leakage discipline. Component G remains "Named annualization-basis unavailability only"; Component H retains the frozen title "Missing data, density, and partial windows." | No regression |
| F-8 | `I-7` / `I-8` discharge preserved | Roadmap §6 and §7 and architecture §12.2 record both obligations as held in frozen M44 Architecture §4.1, grounded in M43-WP4 / M43-WP5 and the M43-WP7 dependency model, "by content, not predecessor path." Verified against M44 Architecture §4.1. | No regression |
| F-9 | Authority headers preserved | Both headers carry all sixteen authority classes, every one `NONE`, including cross-domain, gate-disposition, ownership-determination, vocabulary-admission, contract-lifecycle, executable-validation, and production-method. Milestone label remains "prospective; allocation not yet evidenced." | No regression |
| F-10 | Joint planning corpus preserved | Architecture header and §4.3 and roadmap header declare one corpus subject to the same review, confirmation, ratification, identity-validation, and freeze acts. | No regression as to the declaration; `N-4` records a coherence defect *within* the corpus that this rule governs |

No previously resolved finding has regressed.

---

## 8. Advisory verification

| Advisory | Original observation | Implementation | Determination |
| --- | --- | --- | --- |
| A-6 | WP4 was silent on whether `G-4` blocks WP5 entry, although frozen [M44 G-3 Roadmap](M44_G3_CLOSURE_AND_WP6_ENTRY_ROADMAP.md) §13 settles it | Roadmap §5 now states: "`G-4 OPEN — EFFECTIVE AND FROZEN` does not block WP5 entry once all G-3, substantive-authorization, checkpoint, and entry-verification conditions are satisfied. WP4 does not close, cure, replace, reinterpret, or weaken `G-4`; Component G later binds only the named annualization unavailability." | `ADOPTED` — accurate. Verified against frozen §13, which states `G-4` "does not block WP6 entry once the `G-3` and checkpoint conditions above are satisfied, and it does not authorize a value, factor, alias, placeholder, or synthetic dependency." The candidate restates the frozen position without weakening it and correctly ties it to the additional M45 conditions. Consistent with architecture §2.1 item 7 and §6.5. |
| A-7 | [M43-WP7](M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md) was cited for the dependency model without a section anchor | Architecture §12.2, roadmap §6, and roadmap §7 now cite "§3.1, §3.2 items 5–6, and §3.3" | `ADOPTED` — accurate. Verified at source: §3.1 is the hard-dependency table including the M43-WP4 and M43-WP5 required-normative-specification rows; §3.2 item 5 is the WP4 normative-specification gate and item 6 the WP5 normative-result gate; §3.3 is the dependency flow. The anchors resolve and support the claims made. |

Both advisories were adopted accurately. Advisory `A-2` from the original
review remains `NOT ADOPTED` for the stated scope reason and continues to
create no ratification blocker; nothing in this correction round changes that
disposition.

---

## 9. Validation

| Validation | Method | Result |
| --- | --- | --- |
| Repository-relative links in this artifact | Every link target resolved on disk | `PASS` — all resolve |
| `git diff --check` | Executed at repository root | `PASS` — no whitespace or conflict-marker errors |
| Candidate artifacts unmodified | No write performed against either candidate or the corrections response | `PASS` |
| Frozen artifacts unmodified | No write performed against any M1–M44 artifact | `PASS` |
| Decision Log / Implementation INDEX | Not opened for write | `PASS` — unchanged |
| Source, runtime, schema, API, provider, migration, deployment, configuration, production files | None touched | `PASS` — unchanged |

Reported file states appear in §12.

---

## 10. New findings

Introduced only where the targeted corrections themselves create a defect.
No resolved finding is reopened.

### N-4 — `MINOR` — The corpus contradicts itself about which act produces the frozen `TB-4` record

**Affected sections.** Architecture §5.5 (dependency diagram), architecture §9
item 8, and roadmap §9 stage 5A, in conflict with roadmap §5 (scope,
deliverable 5, exit criteria, dependencies, expected sequence), roadmap §12.1,
roadmap §8, and architecture §7 and §12.3.

**Remaining defect.** `TB-4` is defined in the canonical inventory as a
"frozen WP5-entry blocked/not-authorized determination." Roadmap §5 assigns
that determination to M45-WP4: WP4 verifies the external authorization record
first, and if it is absent or negative WP4 "produce[s] the bounded WP5-entry
blocked determination and route[s] TB-4 to WP7," issuing it as WP4 deliverable
5 under WP4's own review, confirmation, identity-validation, and freeze
lifecycle. Architecture §7 is consistent with this: WP4's release condition is
that the external stage "has a content-identified terminal determination,"
which is satisfied by either polarity.

Three other passages say the opposite. Architecture §9 item 8 reads: "If it is
absent or `NOT AUTHORIZED`, leave WP5 unstarted and execute truthful WP7
closeout; otherwise execute WP4" — WP4 is not executed on the refusal path.
Architecture §5.5 draws the `TB-4` edge from the external authorization stage
directly to WP7, bypassing WP4. Roadmap §9 places stage 5A ("Fail-closed
closeout | TB-1, TB-2, or TB-4") before stage 5B ("Execute WP4 …"), implying
the same bypass.

On the bypass reading, no competent act produces or freezes the `TB-4`
artifact. WP4 never runs, so it cannot freeze the entry-status record; and
WP7's own boundary forbids the substitute — roadmap §8 requires that "no
unperformed WP is reported complete or frozen," and WP7 "cannot retroactively
authorize, complete, or freeze another WP or external artifact." A terminal
branch defined as a *frozen determination* would then have no producer, and
WP7 could not close truthfully on it. This defect did not exist before this
round: both the external authorization stage and `TB-4` are products of the
`N-1` correction.

**Controlling authority.** Architecture §4.3 and both headers make the two
files one corpus subject to a single ratification and freeze, so an
intra-corpus contradiction is a corpus defect; G4 ("Conflict is a defect,
resolved upward") forbids resolving it by recency or authorship; Law 13
("Failure is loud") requires the refusal path to terminate in an explicit,
recorded, attributable fact rather than an unattributed one; roadmap §8 WP7
exit criteria and freeze boundary supply the concrete impossibility on the
bypass reading.

**Required correction.** State in exactly one place which act produces,
reviews, confirms, and freezes the `TB-4` record, and conform the other
passages to it. The recommended resolution is roadmap §5's bounded-WP4 model,
because it is the reading under which `TB-4` has a competent producer and
under which architecture §7's WP4 release condition already reads correctly:
amend architecture §9 item 8 so that WP4 executes in bounded
verification-only mode on the refusal path; redraw the architecture §5.5
`TB-4` edge so it originates at WP4; and reorder or re-label roadmap §9 stage
5A so `TB-4` is emitted after the bounded WP4 act rather than in place of it.
If instead the bypass reading is intended, the corpus must name the competent
act that freezes the `TB-4` determination without WP4, and reconcile that with
roadmap §8's prohibition on WP7 freezing another package's output.

**Focused re-review scope after correction.** Architecture §5.5, §7, §9, and
§12.3; roadmap §5, §8, §9, and §12.1 — verifying one consistent `TB-4`
producer, an unchanged canonical inventory, and no new authority created for
WP4 or WP7 by the fix. No re-examination of `N-1` distinctness, `N-2`, or
`F-1` … `F-10` is required.

### 10.1 Advisory

**A-8 — `ADVISORY` — the correction round has no corresponding corrections
response.** Architecture §4.2 stage 4 defines the correction stage's output as
"Revised pair and response." The existing
[corrections response](M45_ARCHITECTURE_REVIEW_CORRECTIONS_RESPONSE.md) still
records "Review disposition received: `NOT APPROVED`" and a matrix covering
only `F-1` … `F-10`; it contains no `N-1` … `N-3` rows and no `A-6` / `A-7`
disposition. The corrected architecture header does record the round
("`CORRECTIONS REQUIRED`; N-1 through N-3 corrections prepared for second
focused re-review"), but the roadmap header carries no equivalent review-state
line. This did not impede the present review — every determination above was
made directly against the corrected text and the frozen sources — and it is
therefore recorded as an advisory on lifecycle-record completeness, not as a
defect. Adding an additive response for this round, and a matching roadmap
review-state line, would keep the corpus self-documenting under its own §4.2.

---

## 11. Final disposition

**`CORRECTIONS REQUIRED`**

Determination counts:

- `N-1`: `RESOLVED`
- `N-2`: `RESOLVED`
- `N-3`: `RESOLVED`
- `F-1` … `F-10`: all remain resolved; no regression
- Advisories `A-6`, `A-7`: both accurately `ADOPTED`
- New findings: `BLOCKING` 0; `MAJOR` 0; `MINOR` 1 (`N-4`); `ADVISORY` 1 (`A-8`)

`APPROVED FOR INDEPENDENT CONFIRMATION` is not available. The three targeted
findings are resolved and no regression exists, but the approval precondition
also requires no unresolved `MINOR` finding, and `N-4` is unresolved.

The residual defect is narrow and localized. It concerns the internal
consistency of one fail-closed routing path created by the `N-1` correction,
not the constitutional soundness of the correction itself. No authority is
invented, no frozen boundary is weakened, and no gate is affected by it.

This disposition does not ratify M45, does not confirm the planning corpus,
does not freeze the architecture, and does not authorize any work package.

---

## 12. Required next action

1. The candidate author may publish an additive corrected revision resolving
   `N-4`, with `A-8` expressly dispositioned, together with a corrections
   response covering this round in the form required by architecture §4.2
   stage 4. The response must not declare the finding resolved.
2. A third focused independent re-review, bounded to the `N-4` scope stated in
   §10, determines resolution.
3. Only on `APPROVED FOR INDEPENDENT CONFIRMATION` may an independent
   confirmer, distinct from both the author and this reviewer, act.
4. Ratification, joint content-identified freeze of both planning artifacts,
   and a separate M45-WP1 authorization remain distinct later acts, each
   requiring its own competent authority. None is performed or implied here.

### 12.1 Repository state at the time of this review

| File | State | Changed by this review |
| --- | --- | --- |
| `docs/implementation/M45_ARCHITECTURE_SECOND_FOCUSED_REREVIEW.md` | Added (this artifact) | Yes — created |
| `docs/implementation/M45_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` | Staged addition, pre-existing | No |
| `docs/implementation/M45_ARCHITECTURE_FOCUSED_REREVIEW.md` | Staged addition, pre-existing | No |
| `docs/implementation/M45_ARCHITECTURE_INDEPENDENT_REVIEW.md` | Staged addition, pre-existing | No |
| `docs/implementation/M45_ARCHITECTURE_REVIEW_CORRECTIONS_RESPONSE.md` | Staged addition, pre-existing | No |
| `docs/implementation/M45_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md` | Staged addition, pre-existing | No |

No tracked file was modified. No frozen artifact, Decision Log entry,
Implementation INDEX entry, source file, schema, migration, API, provider,
configuration, deployment, or production file was changed.

### 12.2 Present governance state

`G-2` remains `RELEASED — FINAL RECORDING PENDING AUTHORIZED VEHICLE`.
`G-3` remains `OPEN — PARTIAL`. `G-4` remains `OPEN`. `G-5` remains `OPEN`.
The historic M44 checkpoint remains `STOP`. M44 remains complete and frozen
and is unmodified by this review.

M45 remains NOT RATIFIED.
M45-WP1 remains NOT AUTHORIZED.
Independent Confirmation has not been performed.
