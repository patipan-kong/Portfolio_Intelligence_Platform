# Review Handbook

> Status: `DRAFT`

This handbook is explanatory repository documentation. It describes how review
is practised in this repository and what makes a review trustworthy. It is not
a constitutional artifact, governance record, review record, allocation,
authorization, implementation specification, or runtime permission.

## Contents

1. [Purpose](#1-purpose)
2. [Review philosophy](#2-review-philosophy)
3. [Types of review](#3-types-of-review)
4. [Review boundary](#4-review-boundary)
5. [Source hierarchy during review](#5-source-hierarchy-during-review)
6. [Findings](#6-findings)
7. [Independent review](#7-independent-review)
8. [Focused re-review](#8-focused-re-review)
9. [Confirmation](#9-confirmation)
10. [Common review mistakes](#10-common-review-mistakes)
11. [Review reports](#11-review-reports)
12. [Relationship to other handbooks](#12-relationship-to-other-handbooks)
13. [Related canonical sources](#13-related-canonical-sources)

## 1. Purpose

This handbook explains repository review methodology: how a reviewer decides
what to examine, how to reason from sources, how to express findings, and how
to stop at the edge of the review role.

It creates no authority. Reading it does not make anyone a reviewer, does not
constitute a review, does not produce review evidence, and does not change what
any governing source requires of a review. When a real review happens, its
subject, scope, competence, and disposition are set by the sources that
actually apply to it — which, for a review inside a governed lifecycle, means
the governing corpus and the applicable allocation, authorization, and
lifecycle records, and, for ordinary repository work, means the repository
instructions and the relevant technical source of truth. Determining which of
those applies is the first thing a reviewer does; see
[Review boundary](#4-review-boundary). This handbook only helps a reviewer do
that work well.

Two companion documents carry most of the load that this one deliberately does
not:

- [AI_RULES.md](AI_RULES.md) states the operating rules an AI must follow in
  this repository, including source tracing, evidence discipline, identity
  boundaries, scope control, stop conditions, and reporting. Section 7 of that
  handbook states the review-role boundaries in their operational form.
- [GOVERNANCE_HANDBOOK.md](GOVERNANCE_HANDBOOK.md) explains the governance
  model: which acts exist, what each act does and does not establish, and why
  authority and evidence are different things.

This handbook uses the same vocabulary those documents use, and it keeps the
same four labels distinct throughout:

- **Constitutional requirement** — a requirement stated by the applicable
  governing or frozen source. A reviewer discovers these; a handbook never
  creates one.
- **Repository convention** — an established way of organizing or performing
  repository work. Useful and often expected, but not constitutional authority.
- **Recommended practice** — explanatory guidance in this handbook. Following it
  tends to produce better reviews; departing from it is not a violation of
  anything unless a canonical source separately says so.
- **Reviewer judgment** — the space a competent reviewer is expected to
  exercise, where no source dictates an answer and reasonable reviewers may
  differ.

Where a passage in this handbook is recommended practice rather than a
requirement, it says so. Where it describes something a governing source
imposes, it points at the source rather than restating the source's words.

## 2. Review philosophy

Review exists because an author cannot be a reliable judge of their own work.
That is not a comment on anyone's integrity; it is a structural fact. The
author knows what they meant, so they read intent into text that a stranger
would read differently. Review supplies the stranger.

Everything below follows from that purpose.

### Independent judgment

A reviewer's value is their independence. The moment a reviewer helps design
the thing, negotiates the outcome, or adopts the author's framing wholesale,
the review stops being a second perspective and becomes an echo.

Independence is practical, not ceremonial. It means reading the artifact
against its sources rather than against the author's explanation of it; it
means being willing to record a finding that is inconvenient; and it means not
having a stake in the disposition. A reviewer who wants the artifact to pass is
no longer reviewing it.

Independence also has a role dimension: the reviewer role is distinct from the
author, confirmer, validator, freeze, release, and closeout roles. Those
boundaries are stated operationally in
[AI_RULES.md §7](AI_RULES.md#7-review-role-boundaries) and explained in the
[Governance Handbook](GOVERNANCE_HANDBOOK.md). A reviewer does not acquire a
neighboring role by being nearby when the next act becomes due.

### Bounded review

A review has a subject. It is not "an opinion about the repository." Reviewing
outside the subject is not thoroughness — it is a different, unauthorized
review wearing the same record.

Boundedness protects three things. It protects the author, who prepared work
against a stated scope and should not be judged against an unstated one. It
protects the record, which must be reproducible: a later reader has to be able
to tell what was and was not examined. And it protects the reviewer, whose
disposition means something precise only because its subject was precise.

When a reviewer notices something real but out of scope, the answer is not to
review it silently. It is to note it as an observation, mark it out of scope,
and leave the disposition untouched. See
[Review boundary](#4-review-boundary).

### Evidence-first review

A finding is a claim about the artifact. Claims need evidence.

Evidence-first review means the reviewer can point to the exact text, path,
line, section, command output, or test result that establishes each finding.
"This section feels underspecified" is not evidence. "Section 4 states a
required predicate but never names the source that establishes it, and no other
section supplies it" is.

The same discipline applies in the other direction. A reviewer who concludes
that something is correct should be able to say what made it correct — which
source was consulted, what it required, and how the artifact satisfied it. An
unexamined pass and a verified pass look identical in a one-word disposition,
which is why the review record has to show its work.

### Source-first review

Read the governing source before reading the artifact's account of the source.

This ordering matters more than it sounds. An artifact that misdescribes its
own governing requirement is often internally consistent and entirely
persuasive — right up until the reviewer opens the actual source. A reviewer
who reads the artifact first will tend to confirm the artifact's framing; a
reviewer who reads the source first will notice the gap.

Source-first also means preferring the canonical artifact over any summary of
it. Indexes, navigation documents, decision logs, handbooks, and tooling output
help a reviewer find the source. They are not the source, and a finding that
rests on a summary rather than the artifact it summarizes is one indirection
away from being wrong.

### Fail-closed review

When a required predicate cannot be established, the honest result is
"unresolved" — not "probably fine."

Fail-closed review treats a missing prerequisite as a blocker rather than an
invitation to assume. If a record that should exist cannot be found, the review
says the record was not located and identifies what would resolve it. If an
identity comparison is ambiguous because the identity boundary was never named,
the review reports the ambiguity rather than picking a boundary and proceeding.
If the applicable source is genuinely silent, the review records silence rather
than reading permission into it.

This is the single most valuable habit a reviewer has, and the easiest to
abandon under time pressure. A review that resolves its own uncertainties by
assumption produces a clean record of an unexamined question, which is worse
than no record at all — the next reader will trust it.

### Review proportionality

Depth should match consequence. A reviewer has finite attention and should
spend it where an error would matter most.

Proportionality is *not* permission to skim high-consequence material because
the change looks small. A one-character change to a frozen identity predicate
deserves more scrutiny than a thousand words of new explanatory prose. The
question is never "how large is this?" but "what breaks if this is wrong, and
how would I detect that?"

Proportionality is reviewer judgment. Two competent reviewers may allocate
attention differently and both be right. What is not reviewer judgment is
whether the review states its own depth — see
[Review reports](#11-review-reports).

### Additive findings

Review evidence accumulates; it does not get tidied.

A finding, once recorded, stays recorded. A later correction responds to it, a
later re-review evaluates the correction, and a later act may supersede the
whole chain — but none of that erases the original finding. The point of an
additive history is that a future reader can reconstruct what was known at each
stage and why each act was or was not permitted.

This is why a repository keeps its failures visible. A history showing a
finding, a correction, and a passing re-review is far more trustworthy than a
history showing only a pass, because the first one can be audited and the
second one cannot. The
[Governance Handbook's evidence model](GOVERNANCE_HANDBOOK.md#6-evidence-model)
develops this further.

## 3. Types of review

The categories below describe what a review is *about*. They are descriptive
groupings, not a fixed repository taxonomy, and a single review often has
characteristics of more than one. What any particular review must examine is
determined by its applicable sources — the governing corpus where one applies,
and otherwise the requested scope and the repository's own instructions and
technical sources — not by this list.

### Documentation review

Subject: prose artifacts — handbooks, guides, indexes, explanatory documents,
READMEs.

A documentation reviewer asks whether the document is accurate against its
sources, whether it stays inside its declared scope, whether it links rather
than duplicates, whether it distinguishes requirement from convention from
recommendation, and whether it accidentally asserts authority it does not have.
That last question is the characteristic risk of documentation in a governed
repository: prose that describes a rule can drift into sounding like the rule.

Documentation review is usually the lightest in verification tooling and the
heaviest in careful reading.

### Implementation review

Subject: code, schemas, tests, migrations, configuration, or a documentary
implementation artifact produced under an implementation scope.

An implementation reviewer asks whether the artifact does what its scope
permitted, whether it stayed inside that scope, whether its behavior matches
the architecture and domain rules it must respect, whether it is verified, and
whether the verification actually demonstrates what it claims. Tests are
evidence here in a way they rarely are elsewhere: a passing test suite is
reproducible evidence, and a reviewer can and should run it.

Note that "implementation" in this repository includes normative documentary
artifacts produced under an implementation authorization. Those are reviewed as
implementation candidates even though they contain no code.

### Governance review

Subject: a governance record, or an artifact's position within a governance
lifecycle.

A governance reviewer asks whether the record states its act, scope, subject,
competence, disposition, and non-effects; whether its prerequisites are
actually recorded somewhere rather than assumed; whether it claims only the
effect its act produces; and whether it keeps distinct acts distinct. The
recurring failure mode is a record that quietly performs two acts, or that
describes a neighboring act in a way a later reader will mistake for having
performed it.

### Constitutional review

Subject: an artifact evaluated against a frozen or constitutional corpus.

Constitutional review is the narrowest and most source-bound. The reviewer
establishes the exact applicable corpus, reads its requirements and stated
limits, and evaluates the subject against those and nothing else. Preference,
better design, and repository convention are all out of bounds — a
constitutional review that records a convention as a constitutional finding has
misdescribed the corpus.

Constitutional review is also where corpus-boundedness bites hardest. An
interpretation adopted for one corpus does not transfer to a successor corpus
because the wording is similar or the work-package name is shared. See the
[Governance Handbook on corpus-bound interpretation](GOVERNANCE_HANDBOOK.md#8-constitutional-interpretation).

### Focused re-review

Subject: a specific correction or a specifically identified issue — not the
artifact as a whole.

Focused re-review is treated separately in [section 8](#8-focused-re-review)
because its most common failure is scope creep back into full review.

### Scope always comes from the applicable sources

None of these labels sets a review's scope. They describe families of concern.
The actual scope of any review comes from the sources that apply to the subject
— which depends on the operating lane, described in
[Determining the operating lane](#determining-the-operating-lane). For a
governed-lifecycle review that means the governing corpus together with the
allocation, authorization, and record that establish the review act. For an
ordinary documentation or implementation review it means the requested scope,
the repository instructions, and the technical source of truth for the material
under review.

In both lanes the same rule holds: when those sources and this handbook appear
to disagree about scope, the sources govern and this handbook is wrong.

## 4. Review boundary

Determining the boundary is the first real act of a review, and doing it badly
contaminates everything downstream. A reviewer should be able to state the
boundary before forming a single opinion about quality.

### Determining the operating lane

Before anything else, establish which lane the review is in. The distinction
mirrors the operating lanes in
[AI_RULES.md §3](AI_RULES.md#3-authority-before-action), and it determines
which inputs a reviewer is obliged to locate.

**Governed-lifecycle review.** The subject falls within a governing or frozen
corpus, or the review is itself a lifecycle act within one. Here the reviewer
locates the governing corpus, the applicable allocation and authorization, the
current lifecycle stage, and the record that establishes the review act, and
evaluates the subject against those. A missing prerequisite is a blocker.

**Ordinary-work review.** Routine documentation or implementation work outside
a governed lifecycle. Here there is normally no work-package allocation, no
lifecycle authorization, and no lifecycle stage to find, and their absence is
not a defect and not a blocker. The reviewer instead evaluates the subject
against the requested scope, the repository instructions, the applicable
repository conventions, and the technical source of truth — architecture and
domain rules for intended structure, code for current behavior, tests for
verification.

The lanes are not a spectrum, and the lane is a property of the subject rather
than of the reviewer's preference. A governing corpus applies when it actually
enumerates or governs the subject, not when it merely exists nearby or covers
similar-looking material; the discovery procedure for frozen paths in
[AI_RULES.md §4](AI_RULES.md#4-frozen-artifact-rules) is the reliable way to
settle the question rather than inferring from a filename or directory. If the
lane cannot be determined, that is itself an unresolved condition to report —
see [Fail-closed review](#fail-closed-review).

Everything else in this handbook applies in both lanes. Boundedness,
evidence-first and source-first reasoning, fail-closed handling of unresolved
questions, independence, and finding discipline do not relax because a review
is ordinary work. What changes is only which sources the reviewer must locate
and what counts as a missing prerequisite.

### Establishing the subject

Name the exact artifacts under review, by repository-relative path. Not "the
AF-WP4 work" — the specific files. If the subject is a pair or a set, say so
and treat the set as one bounded subject. If a file has a same-named twin
elsewhere in the tree, disambiguate by full path; this repository contains
same-basename artifacts in different directories with entirely different
artifact classes, and confusing them is a real and previously-encountered
hazard.

### Establishing the applicable sources

List the sources the subject will be evaluated against. Which sources those are
follows from the lane.

In the governed-lifecycle lane: the governing corpus, the allocation and
authorization defining the permitted scope, the architecture or domain rules
that apply, and any frozen predecessors the subject depends on.

In the ordinary-work lane: the requested scope, the repository instructions,
the applicable repository conventions and engineering principles, and the
technical sources that own the answer for the material under review. A
governing corpus enters this list only if it explicitly applies to the subject
— in which case the review is a governed-lifecycle review and should be treated
as one.

A source is *applicable* when it governs this subject. A source is merely
*present in the repository* when it does not. Reviewing against a source that
does not govern the subject produces findings the author had no way to
anticipate and no obligation to satisfy.

### Establishing authority boundaries

Two questions, both answered before reviewing:

1. What act is this review? Almost always: evaluate and record findings.
2. What acts is this review not? Everything else — correction, confirmation,
   identity validation, freeze, release attestation, closeout, implementation,
   allocation, authorization.

Writing the second list down is not bureaucratic. It is the thing a reviewer
consults at hour three, when the artifact has a small obvious defect and fixing
it would take ten seconds.

### Out-of-scope material

Material can be out of scope for several different reasons, and the reason
determines the right handling:

| Situation | Handling |
| --- | --- |
| Adjacent file, not part of the subject | Do not review. Note as an observation only if it affects the subject. |
| In the subject but governed by another owner domain | Note the boundary; do not evaluate against rules the domain does not own. |
| Real defect, outside the review's scope | Record as an explicitly out-of-scope observation; do not let it drive the disposition. |
| Preference or alternative design | Not a finding at all. See [Findings](#6-findings). |
| Already-settled question from an earlier act | Do not reopen. Note if the subject contradicts the settled state. |

An observation is not a finding. Keeping them typographically and structurally
separate in the report is recommended practice, because a later reader deciding
what must be corrected needs the line to be unambiguous.

### Historical evidence

Prior review records, correction responses, re-reviews, and confirmations are
context. They tell the reviewer what was already examined, what was found, and
what state the artifact was left in.

They are not conclusions the current review inherits. A prior `PASS` on an
earlier version does not carry to the current bytes. Equally, a prior finding
does not automatically remain open — the correction chain may have closed it,
and the reviewer should read the chain rather than assume either way.

The one thing historical evidence must never be is a target. A review does not
revise, reinterpret, or improve an earlier record. It reads it.

### Frozen artifacts

A frozen artifact within the review's field of view is read-only in the
strongest sense. It may be:

- read, cited, and relied upon as a boundary;
- compared against a recorded identity predicate.

It may not be edited, normalized, reformatted, reordered, re-encoded, or
"cleaned up" — not even to fix trailing whitespace, and not even when the fix
is obviously correct. The procedure for determining whether a path is actually
frozen, and the identity-boundary rules for comparing it, are stated in
[AI_RULES.md §4](AI_RULES.md#4-frozen-artifact-rules). A reviewer should follow
that procedure rather than infer frozen status from a filename or a directory.

### What reviewers must deliberately ignore

Some things a reviewer will notice and must consciously set aside:

- **The author's identity and reputation.** The artifact is the subject.
- **How much effort the work appeared to take.** Effort is not correctness.
- **How the reviewer would have written it.** A different valid approach is not
  a defect.
- **Downstream schedule pressure.** The next act being due is not evidence that
  this act should pass.
- **Convenience of the disposition.** A blocking finding is not less true
  because it is expensive.
- **Unrelated defects the reviewer happens to know about.** Real, but not this
  review's subject.

Setting these aside is a deliberate act, not an automatic one. Naming them is
the practical way to actually do it.

## 5. Source hierarchy during review

A reviewer constantly answers the question "which document settles this?" The
operating order for authority and governance questions is stated in
[AI_RULES.md §2](AI_RULES.md#2-source-of-truth-hierarchy) and is not repeated
here. What follows is how a reviewer *uses* it.

### Sorting sources by the question they answer

Before reaching for a hierarchy, ask what kind of question is being answered.
The hierarchy in AI_RULES orders authority and governance questions; it is
explicitly not a universal ranking of every engineering source. For a technical
question, the right source is the one that owns the answer:

| Question | Source that answers it |
| --- | --- |
| Was this act permitted? | In a governed lifecycle: the governing corpus, then the applicable allocation and authorization records. In ordinary work: the requested scope and the repository instructions. |
| Did this act occur, and within what limits? | The governance evidence record for that act. |
| What is the intended structure or ownership? | Architecture records and domain rules. |
| What does the system actually do today? | Source code. |
| What is verified, and how? | Tests and their results. |
| What is the current implementation state and sequence? | Implementation documents and the implementation index. |
| Why was a constraint chosen? | The decision log — context, not authority. |
| Where do I find the relevant record? | Navigation documents and indexes — pointers, not authority. |

Picking the wrong category is a common source of bad findings: evaluating a
governance record against engineering preference, or evaluating code against a
governance record that never addressed behavior.

The first two rows describe governed-lifecycle questions and simply do not
arise in most ordinary-work reviews. Their absence there is not a gap to
report; the remaining rows carry an ordinary review on their own.

### Governing sources versus supporting evidence

A **governing source** states what is required or permitted. A **supporting
evidence** record states what happened and within what limits. Findings about
compliance rest on governing sources; findings about lifecycle state rest on
evidence.

The distinction collapses in exactly one dangerous way: treating an evidence
record as though it granted the authority it describes. A record stating that
an act occurred is not permission for the next act. The
[Governance Handbook's authority model](GOVERNANCE_HANDBOOK.md#7-authority-model)
covers why.

### Repository conventions during review

Conventions — repository instructions, engineering principles, contribution
guidance, established file layouts — are legitimate review criteria for
ordinary repository work, and a reviewer may reasonably find that an artifact
departs from them.

What the reviewer must not do is record that departure as a constitutional
finding. The correct form is: "departs from repository convention X; convention,
not a constitutional requirement." That phrasing lets a later reader weigh it
correctly. The wrong form buries a preference-level issue inside a
requirement-level disposition.

### Implementation context

Code, tests, and implementation documents give a reviewer the ability to check
claims rather than accept them. Use them that way. When an artifact asserts
that behavior exists, look. When it asserts that a test covers something, read
the test.

Implementation context does not, however, override a governing source. "The
code already does it this way" answers a question about current behavior, not a
question about what was permitted.

## 6. Findings

### What constitutes a finding

A finding is a specific, evidenced defect in the subject, expressed against an
applicable source or an established repository criterion.

Three parts, all required:

1. **Specific** — locatable. A path, section, line, table row, or identified
   claim. If a reader cannot find what the finding is about, it is not yet a
   finding.
2. **Evidenced** — demonstrable from the artifact and its sources. The reviewer
   can show it, not merely assert it.
3. **Anchored** — traceable to something the subject was actually obliged to
   satisfy: a governing requirement, an authorization boundary, an architecture
   rule, a repository convention, or an internal contradiction within the
   subject itself.

An observation that fails the third test is not a finding, however true it is.
"This could be clearer" anchors to nothing.

### Material versus editorial

**Material** findings affect correctness, scope, authority, identity, safety, or
whether the artifact does what it was authorized to do. They are the ones that
should drive a disposition.

**Editorial** findings affect readability, formatting, consistency, or polish.
They are worth recording — a repository whose documents drift stylistically
becomes harder to review over time — but they should be visibly separated from
material findings and should not, on their own, block.

The practical test: if this were corrected, would the artifact *mean* something
different, or merely *read* better? Meaning is material. Reading is editorial.
A borderline case worth watching is ambiguity: prose that could be read two
ways is editorial when both readings are equivalent and material when they are
not.

### Required evidence

Each finding should carry enough for someone else to reach the same conclusion
without re-doing the review:

- the exact location in the subject;
- the exact source relied upon, by repository-relative path and section;
- what that source requires, permits, or leaves open;
- how the subject departs from it;
- if verification was run, the command and its actual result.

Where identity or Git state is involved, the evidence must name the identity
boundary used — working-tree bytes, Git-normalized content, staged index
content, or committed content — because a comparison at one boundary says
nothing definitive about another. The rules and reproducible commands are in
[AI_RULES.md §8](AI_RULES.md#8-repository-and-git-safety); a reviewer should
follow them rather than improvise a comparison.

### Supporting authority

Every material finding names the authority it rests on, and names it at the
right level. Three forms, in descending strength:

- "Requirement stated by *<source, section>*." — constitutional or governing.
- "Repository convention per *<source>*." — convention.
- "Internal inconsistency within the subject: *<A>* contradicts *<B>*." — needs
  no external source, since the subject cannot satisfy both.

If a reviewer cannot fill in one of these three, the item is an observation or a
preference, not a finding. Discovering this while drafting the finding is
normal and healthy — it is the mechanism that keeps preference out of the
record.

### Reproducibility

Another competent reviewer, given the same subject and sources, should reach
the same finding. That is the whole standard.

Reproducibility is why findings cite paths instead of describing documents, cite
sections instead of paraphrasing them, and record actual command output instead
of summarizing it as "checks passed." It is also why a reviewer states what was
*not* examined: an unstated gap is invisible to the next reader and silently
inherits the review's credibility.

### Finding identifiers

Stable identifiers let a correction response, a focused re-review, and a later
record refer to the same finding without ambiguity. This matters most in the
correction chain, where three separate records discuss one issue.

Recommended practice: a short prefix tied to the review subject plus a
sequential number — for example `AF-WP4-F1`, `AF-WP4-F2`. Repository practice
has not fixed a universal identifier format, so the working requirements are
simply that identifiers be unique within the review, stable once published, and
never reused for a different finding. If a finding is withdrawn, mark it
withdrawn rather than renumbering the rest.

### Severity classification

Severity communicates consequence, which is what a disposition-maker actually
needs. Repository governance records to date express review outcomes as
dispositions (`PASS`, material findings `NONE`, and similar) rather than as a
numbered severity scale. The `P1`/`P2`/`P3` scale below is therefore
**recommended practice for structuring a review's findings** — a working scale,
not a repository-wide taxonomy and not a constitutional classification. A
governing source that specifies its own scheme displaces it entirely.

| Level | Meaning | Effect on disposition |
| --- | --- | --- |
| `P1` | The subject is wrong, exceeds its authority, or violates a governing requirement. | Blocking. Correction required before the next act. |
| `P2` | The subject is defensible but materially deficient — incomplete, ambiguous in a way that changes meaning, or unevidenced. | Correction expected; may or may not block, and the review should say which. |
| `P3` | Editorial, stylistic, or consistency issue. | Non-blocking. Correct at convenience. |

**`P1` examples**

- A documentary artifact asserts a lifecycle act that no record establishes —
  for example, describing content as frozen when no freeze record enumerates
  that path.
- An implementation changes a file outside the paths its authorization named.
- A record combines two distinct lifecycle acts without a source that expressly
  permits the combination.
- An identity claim is stated without naming the identity boundary it was
  computed at, in a context where the boundaries would differ.

**`P2` examples**

- A record states a required predicate but never names the source establishing
  it; the predicate may well hold, but the record does not show it.
- A handbook describes a repository convention in language that reads as a
  requirement, without labelling which it is.
- Verification is claimed in summary form ("checks passed") without naming what
  was run, so the claim cannot be reproduced.
- A cross-reference points at a document that no longer contains the referenced
  section.

**`P3` examples**

- A relative link resolves but does not match the repository's prevailing link
  style.
- Heading levels skip a level, so the document outline is malformed.
- Trailing whitespace, inconsistent list markers, or an unwrapped long line in a
  file whose neighbours all wrap.
- Terminology drifts between two synonyms for the same defined concept.

The severity of a finding is reviewer judgment applied to consequence, not a
lookup. The same textual defect can be `P3` in an explanatory handbook and `P1`
in a frozen normative artifact, because the consequence differs.

## 7. Independent review

Independence is what the review role contributes. These are the specific ways
it gets lost.

### Avoiding solution design

A reviewer states what is wrong. Designing the fix is the author's work.

The reason is not territorial. A reviewer who supplies the solution has taken
partial authorship of the artifact, and can no longer evaluate the result
independently — the focused re-review would be reviewing the reviewer's own
design. It also narrows the author's options to whatever the reviewer happened
to think of first, which is often not the best available fix.

The line is not always sharp, and a little illustration usually helps rather
than hurts:

- Fine: "Section 4 asserts X but names no source. Either cite the establishing
  source or state the predicate as unresolved."
- Not fine: "Replace section 4 with the following four paragraphs."

The first identifies the defect and the shape of an acceptable resolution. The
second writes the artifact.

### Avoiding implementation

A reviewer does not edit the subject. Not to fix a typo, not to normalize
whitespace, not to correct an obviously wrong path.

This holds even when the fix is trivially correct and the reviewer's edit would
be strictly an improvement — because the review's disposition must describe the
bytes the author produced, and a reviewer who edits has silently changed the
subject of their own review. The correct move is always to record the finding
and let the correction act happen separately.

The one thing a reviewer does write is the review record itself.

### Avoiding authority creation

A review evaluates and records. It does not permit, approve, adopt, ratify,
confirm, validate, freeze, release, or close out — and it does not create a
requirement that no source imposes.

The subtle version of this is a review finding that invents its own criterion:
"the artifact should also have included a summary table." Should according to
what? If no source requires it, the reviewer has legislated. Findings must
trace to a source; that requirement exists precisely to prevent review from
becoming a channel for new rules.

The subtler version still is a review record whose language implies more than
its act — a review that reads as though it cleared the way for the next act.
State non-effects explicitly.

### Avoiding scope expansion

Scope expands quietly. A reviewer follows a reference into an adjacent file, the
adjacent file is interesting, and forty minutes later the review has a subject
it was never given.

Two habits contain it. First, write the boundary down before starting, and
re-read it whenever reaching for a new file — reading a neighbouring file for
context is fine; *evaluating* it is not. Second, when something out of scope
clearly matters, record it as an out-of-scope observation and finish the actual
review. Nothing is lost: the observation is on the record, and the next
reviewer or a properly scoped follow-up can take it up.

### Avoiding hidden assumptions

The most dangerous review defect is the assumption the reviewer never noticed
making. Common ones:

- assuming a record exists because the lifecycle implies it should;
- assuming a term means what it means elsewhere in the repository;
- assuming the corpus that governs a similar artifact governs this one;
- assuming a digest comparison used the boundary the reviewer had in mind;
- assuming that because no finding was found in an area, the area was examined.

The counter-habit is to make assumptions explicit and then check them. Any
assumption that survives into the report unverified should appear in the report
as an assumption, not as a conclusion. A review that says "I assumed X; I did
not verify it" is more useful than one that quietly relies on X and is right —
because the next reader can tell the difference.

## 8. Focused re-review

### Purpose

A focused re-review answers one narrow question: did the correction actually
address the finding, within the permitted correction scope, without collateral
change?

It exists so that a correction does not have to trigger a full re-review of an
artifact that was already examined. That efficiency is only legitimate if the
focus is real — which is why scope discipline matters more here than anywhere
else in the review lifecycle.

### Trigger

In current repository practice, a focused re-review follows a correction made
in response to a recorded finding: no finding, no correction, no re-review.
That is the pattern the existing review chains follow, and it is the one a
reviewer should expect by default.

It is repository practice rather than a universal rule. Another governing
corpus may define a different trigger — a re-review scoped to a specifically
identified issue without a preceding correction, a re-review triggered by a
changed dependency, or another bounded occasion of its own definition. When a
governing corpus applies, its trigger governs and this section describes only
what is customary elsewhere.

What does not become a trigger in either case is dissatisfaction. A focused
re-review is not a second opinion on a disposition someone disliked, and it is
not a periodic re-examination.

### Scope

On the correction-triggered path, the scope is the correction and the finding it
responds to — and additionally whether the correction stayed inside its
permitted bounds. That second part is substantive: a correction that fixes the
finding but also rewrites an unrelated section has a problem, and the focused
re-review is where it gets caught. Where a governing corpus defines a different
trigger, the scope is whatever that corpus identifies; the narrowness is the
point, not the particular occasion.

What is out of scope: everything the original review already covered and the
correction did not touch. A re-reviewer who finds a genuinely new material
defect in untouched material has found something real but out of the re-review's
scope; the honest handling is to record it as an out-of-scope observation and
let a properly scoped act address it, rather than silently widening this act.

### Expected outputs

- identification of the finding and the correction being examined;
- a determination on whether the correction resolves the finding;
- a determination on whether the correction stayed within permitted scope;
- any out-of-scope observations, marked as such;
- an explicit statement of what the re-review did not examine.

That last item is what keeps a focused re-review honest. Its disposition covers
its focus and nothing else, and the record should say so plainly.

### Difference from full review

| | Full review | Focused re-review |
| --- | --- | --- |
| Subject | The whole artifact within scope | One correction and its finding |
| Trigger | An implementation or artifact reaching review | A correction responding to a finding, or another occasion a governing corpus defines |
| Sources | All applicable governing sources | Those bearing on the finding and correction scope |
| Disposition covers | The reviewed subject | The examined correction only |

A focused re-review does not upgrade into a full review because the re-reviewer
had time, and a full review's disposition is not obtained by chaining focused
re-reviews.

### Difference from confirmation

They are different acts answering different questions. A focused re-review asks
whether a correction worked. Confirmation makes an independent determination
within its own stated boundary — it is not a third review pass, and it is not
performed by a re-reviewer simply finishing well. Repository practice records
them as separate acts by separate actors; a bounded combination would need a
governing corpus that expressly authorizes it, and even then each act keeps its
own scope, basis, and disposition. See [section 9](#9-confirmation).

## 9. Confirmation

### What confirmation verifies

Confirmation is an independent determination, within a stated boundary, that
the subject is in the state its record says it is in — typically that the exact
artifact under consideration is the one that was reviewed, that the recorded
lifecycle conditions are in place, and that the applicable boundaries were not
disturbed.

The essential word is *independent*. Confirmation is performed in the confirmer
role and carries its own disposition and its own stated limits. What
independence requires is that the determination rest on its own basis rather
than inherit the author's or the reviewer's — not, by itself, a particular
staffing arrangement.

Repository practice is that the confirmer is a different actor from the author
and the reviewer, and that confirmation is recorded as its own record. That is
the normal expectation, and a reviewer should treat a departure from it as
something to look for a source for rather than assume. It is not, however, an
absolute: an applicable governing corpus may expressly authorize a bounded
combination of acts, as the
[AF-WP3 combined allocation-and-authorization record](../governance/ASSET_FOUNDATION_AF_WP3_ALLOCATION_AND_AUTHORIZATION_RECORD.md)
shows for a different pair of acts. Where
that happens, the combination is legitimate only to the extent the corpus
states it, and each act still needs its own scope, its own basis, and its own
disposition — a combined record is not a merged act.

What no arrangement can supply is self-confirmation of one's own authorship. An
actor cannot make an independent determination about work whose correctness
they are the source of, because there is no second basis for the determination
to rest on. That constraint follows from what independence means, not from a
staffing convention, and it survives any permitted combination.

### Why confirmation is not another review

A review evaluates the substance of an artifact against its sources and
produces findings. Confirmation does not re-open that evaluation. It asks a
different question — whether the lifecycle state is what the record says, at the
boundary the confirmation defines.

Treating confirmation as a second review causes two distinct harms. It wastes
the independence that confirmation was supposed to supply, by re-litigating a
question already answered rather than answering the one assigned to it. And it
quietly makes the review's disposition provisional, since a substantive
disagreement at the confirmation stage has no defined channel — there is no
correction chain hanging off a confirmation the way there is off a review
finding.

If a confirmer discovers something that genuinely undermines the review, that is
a real and reportable condition. The handling is to report it and stop —
fail-closed — not to convert the confirmation record into a review record.

### How confirmation interacts with review findings

Confirmation reads the review chain as evidence of state:

```text
review finding -> correction response -> focused re-review -> confirmation
```

Each link is a separate record by a separate act. Confirmation observes that the
chain is complete and consistent; it does not re-adjudicate any link. An open
finding is a fact the confirmer reports, not a finding the confirmer resolves.

The governance semantics of confirmation — what the act establishes, what it
explicitly does not establish, and how it relates to identity validation and
freeze — belong to the
[Governance Handbook](GOVERNANCE_HANDBOOK.md#4-governance-lifecycle) and are not
restated here.

## 10. Common review mistakes

Each of these is common, understandable, and damaging in a specific way.

**Reviewing outside scope.** The reviewer evaluates material the review was
never given. *Why it harms:* the author had no notice of the criteria, and the
record now covers a subject nobody defined. *Instead:* record it as an
out-of-scope observation.

**Inventing authority.** A finding rests on a rule the reviewer believes should
exist. *Why it harms:* review becomes a channel for unlegislated requirements,
and a later reader cannot trace the rule to any source. *Instead:* if no source
requires it, it is a recommendation at most — label it that way.

**Rewriting requirements.** The reviewer restates a governing requirement in
their own words and then reviews against the restatement. *Why it harms:* the
paraphrase drifts, usually toward the reviewer's own reading, and the artifact
gets judged against text that does not exist. *Instead:* quote or cite the
source, and let the source's words carry the finding.

**Requesting redesign.** A finding effectively asks for a different solution to
a problem the artifact already solved acceptably. *Why it harms:* it converts
reviewer preference into a blocking condition and takes over authorship.
*Instead:* if the existing approach satisfies the applicable sources, there is
no finding — however much a different approach appeals.

**Confusing evidence with authority.** A record showing that an act occurred is
read as permission for the next act. *Why it harms:* this is the single failure
mode the whole governance model is built to prevent; it produces lifecycles that
appear complete and are not. *Instead:* trace each authority claim to the record
that states it, and read the record's non-effects.

**Conflating implementation with review.** The reviewer fixes what they found.
*Why it harms:* the reviewer becomes an author, the subject changes mid-review,
and independence is gone for every subsequent act. *Instead:* record the
finding; let correction be its own act.

**Raising preference as a finding.** "I would have structured this differently"
appears in the findings list. *Why it harms:* it inflates the disposition,
consumes correction effort on non-defects, and erodes the credibility of the
real findings around it. *Instead:* either anchor it to a source or drop it. If
it is genuinely valuable, say it as a non-blocking observation.

**Treating repository convention as constitutional rule.** A departure from
established practice is recorded as a governing-requirement violation. *Why it
harms:* it misrepresents the repository's authority structure and can block work
on grounds no source supports. *Instead:* name the convention as a convention.
The
[Governance Handbook](GOVERNANCE_HANDBOOK.md#8-constitutional-interpretation)
explains why this distinction is load-bearing.

## 11. Review reports

A review is only as useful as the record it leaves. These are the properties
that make a report worth reading later.

### Traceability

Every claim connects to something checkable: a path, a section, a command, a
result. A reader who doubts a conclusion should be able to reach the evidence
without asking the reviewer.

Traceability includes the review's own inputs — which sources were consulted,
which version or identity boundary of the subject was examined, and when. A
report that omits what it reviewed cannot be relied on once the artifact
changes.

### Clarity

Findings are stated in plain language, one defect per finding, with the
severity and the anchoring authority visible. Material and editorial findings
are separated. Observations are separated from findings.

Clarity is mostly a structural property, not a prose one. A reader should be
able to answer "what must be corrected?" by looking, not by reading the whole
document and inferring.

### Reproducibility

Enough detail that a second competent reviewer could arrive at the same
findings. Actual commands and actual results, not summaries of them. Identity
comparisons that name their boundary. Verification that names what ran.

"Verification performed" tells a reader nothing. "`git diff --check` — no
output; heading-level inspection of the changed file — no skipped levels;
relative-link inspection — 14 links, all resolve" tells them everything.

### Bounded conclusions

The disposition covers the stated subject and scope, and the report says so.
A report should make it easy for a reader to answer "what does this
*not* tell me?" — which requires stating what was not examined, which sources
were not consulted, and which questions were left to a later act.

This is not hedging. It is the difference between a conclusion a later act can
build on and one it cannot.

### Explicit uncertainty

Where the reviewer could not resolve something, say so, and say what would
resolve it. Fail-closed reasoning only works if the unresolved condition is
visible in the record.

An unresolved item should name: what was uncertain, why it could not be
resolved, what evidence or source would resolve it, and what the reviewer did
*not* conclude as a result. Assumptions that were made and not verified belong
here too.

### Recommended disposition

The reviewer records the outcome their findings support, within the review's
own act — which means recording a review disposition, not the next act's.

A useful disposition statement includes the outcome, the subject and scope it
covers, and its non-effects. Repository practice states non-effects explicitly
and at length, and the reason is worth internalizing: a disposition without
stated non-effects is routinely read as clearing the next gate. Saying what a
`PASS` does not establish is what keeps it from being over-read.

Where findings are open, the report says what state the subject is in and what
would move it forward — without performing that move or implying it is
authorized.

## 12. Relationship to other handbooks

Each handbook owns one concern. When a topic belongs to another handbook, this
one links rather than restates.

| Document | Relationship |
| --- | --- |
| [AI_RULES.md](AI_RULES.md) | Owns the operating rules: source-of-truth hierarchy, authority-before-action, frozen-artifact procedure, evidence discipline, Git and identity boundaries, stop conditions, reporting shape. A reviewer follows those rules while doing what this handbook describes. Where the two touch, AI_RULES states the rule and this handbook explains the practice. |
| [GOVERNANCE_HANDBOOK.md](GOVERNANCE_HANDBOOK.md) | Owns the governance model: what each lifecycle act establishes and does not establish, the authority model, the evidence model, constitutional interpretation. This handbook assumes that model and does not re-derive it. |
| [ARCHITECTURE_HANDBOOK.md](ARCHITECTURE_HANDBOOK.md) | Owns architectural navigation, ownership boundaries, and design records. An implementation or architecture reviewer uses it to locate the domain rules a subject must respect. |
| [AI_COLLABORATION_GUIDE.md](AI_COLLABORATION_GUIDE.md) | Owns human-AI working agreements, context preservation, and handoffs — including how review findings are communicated back to an author and how a review handoff is framed. |
| [CONTRIBUTING.md](../../CONTRIBUTING.md) | Owns contributor-facing repository conventions. A reviewer may cite it as convention, never as constitutional authority. |
| [Handbook entry point](README.md) | Describes the documentation system, its design philosophy, and its overall boundaries. |

## 13. Related canonical sources

These are pointers. The linked artifacts remain the sources of their own
content, scope, identity, and limitations; nothing here summarizes or extends
them.

### Repository conventions and navigation

- [Repository instructions](../../AGENTS.md)
- [Engineering Principles](../engineering/ENGINEERING_PRINCIPLES.md)
- [Decision Log](../engineering/DECISION_LOG.md)
- [Decision records](../decisions/README.md)
- [Implementation Index](../implementation/INDEX.md)
- [Repository Glossary](../GLOSSARY.md)

### Review and correction-chain precedents

The following governance records show a complete review chain as practised in
this repository. They are cited as examples of record structure and boundary
statement, not as universal requirements — each is bound to its own corpus and
scope.

- [AF-WP1 Independent Review](../governance/ASSET_FOUNDATION_AF_WP1_INDEPENDENT_REVIEW.md)
- [AF-WP1 Correction Response](../governance/ASSET_FOUNDATION_AF_WP1_CORRECTION_RESPONSE.md)
- [AF-WP1 Focused Re-review](../governance/ASSET_FOUNDATION_AF_WP1_FOCUSED_REREVIEW.md)
- [AF-WP1 Independent Confirmation](../governance/ASSET_FOUNDATION_AF_WP1_CONFIRMATION.md)
- [AF-WP4 Independent Review](../governance/ASSET_FOUNDATION_AF_WP4_INDEPENDENT_REVIEW.md)

### Constitutional navigation

- [Constitutional Precedent Index](../governance/CONSTITUTIONAL_PRECEDENT_INDEX.md) — non-authoritative navigation; follow its links to the source records.

## Status

`DRAFT`
