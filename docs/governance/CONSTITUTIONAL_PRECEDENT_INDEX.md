# Constitutional Precedent Index

**Artifact class:** Repository-level constitutional precedent index

**Status:** Non-authoritative navigation only

**Authority granted:** `NONE`

## 1. Purpose and status

This index catalogs adopted constitutional interpretations and Architecture
Review Board adoption resolutions for future constitutional reference. It is a
repository navigation document only.

The index is non-authoritative. It does not interpret constitutional text,
adopt a holding, determine a classification, establish an applicable corpus,
or create any authority. The linked adopted records remain the sources of
their own stated content and limitations.

## 2. Record-type distinctions

| Record type | Meaning in this index | Authority boundary |
| --- | --- | --- |
| Constitutional Opinion | An independent constitutional interpretation that states holdings derived from an identified corpus. | Interpretive content comes from the opinion; the index adds none. |
| ARB Adoption Resolution | An Architecture Review Board record that states whether and within what limits an opinion is adopted. | Adoption effect comes from the resolution; the index does not extend it. |
| Governing Holdings | The holdings expressly adopted as the interpretive reference for the applicable corpus. | Holdings bind interpretation only within the adopted limits; they are not a source of operational or implementation authority. |
| Constitutional Classification | The classification the opinion assigns to an identified textual absence or express determination. | Classifications are recorded as stated and are not reclassified by the index. |
| Applicable corpus | The exact constitutional text to which an adopted interpretation applies. | A precedent is corpus-bound and does not automatically carry to a different or successor corpus. |
| Explicit limitations | The exclusions, non-effects, and boundaries stated by the opinion or adoption resolution. | Limitations are preserved; silence in the index is not permission. |

## 3. Additive entry schema

Each future entry should append the following fields without modifying an
existing entry:

1. **Index entry identifier** — a navigational identifier only; it creates no precedent or authority.
2. **Subject and short title** — copied or narrowly derived from the adopted records.
3. **Constitutional Opinion** — repository-relative link to the opinion record.
4. **ARB Adoption Resolution** — repository-relative link to the adoption record, if adoption exists.
5. **Governing Holdings** — the adopted holding headings or exact bounded statements, with section references to the source record.
6. **Constitutional Classification** — the source record's classification of the relevant absence, ambiguity, delegation, express determination, or other stated category.
7. **Applicable corpus** — the exact corpus name and immutable identities stated by the adopted records.
8. **Explicit limitations** — the source record's scope, exclusions, non-effects, and displacement rule.
9. **Adoption status** — the exact disposition stated by the ARB record, without inference.

An entry may add source links and exact section references, but may not convert
a navigational description into a new holding or expand the source record's
scope.

## 4. Adopted precedent entries

### CP-001 — LA-WP2 Constitutional Opinion on the CIV Framework

#### Constitutional Opinion

[Independent Constitutional Interpretation — Constitutional Completeness of the CIV Framework](CONSTITUTIONAL_OPINION_LA_WP2.md)

#### ARB Adoption Resolution

[Architecture Review Board Resolution — Adoption of the LA-WP2 Constitutional Opinion](ARB_RESOLUTION_ADOPTION_OF_CONSTITUTIONAL_OPINION.md)

#### Governing Holdings

The adopted records state the following bounded holdings:

- The corpus does not expressly require constitutional completeness of a mandatory lifecycle stage as a precondition to that stage's operation.
- The corpus distinguishes mandatory stage existence from constitutional specification of stage operation.
- The CIV framework is constitutionally existent and operationally unspecified; that condition is stated as lawful under the frozen corpus, not as a deficiency.
- An unestablished exact-confirmed-bytes predicate leaves Freeze unavailable and yields the expressly enumerated `BLOCKED — GOVERNANCE` consequence; this is not a defect finding or a breach finding.
- Later competent governance instruments may determine matters the frozen baseline leaves open, subject to the express prohibition on altering frozen content and on deriving authority from silence.
- Variation in evidentiary model is permitted within the opinion's three stated boundaries: sufficiency to the fixed conclusion, competence, and non-amendment. No model is recommended, preferred, ranked, or excluded.

These are navigational statements of the holdings recorded in the linked
opinion and adopted by the linked resolution. The index does not independently
adopt or extend them.

#### Constitutional Classification

The opinion classifies the identified matters as follows:

| Identified matter | Classification recorded in the opinion |
| --- | --- |
| No CIV actor named in the frozen corpus | Express delegation |
| No CIV role type in §4's enumeration | Constitutional ambiguity |
| No custody responsibility, burden of proof, or evidentiary sufficiency standard | Constitutional silence |
| No CIV operating procedure | Constitutional silence as to content; open as to method |
| No stage-completeness precondition | Constitutional silence |
| CIV absent from Roadmap §5's terminal-state triggers | Express omission within a closed enumeration |
| Whether Freeze may issue over bytes of undetermined identity | Not silence — expressly determined in the negative |
| Disposition when Freeze is unavailable | Not silence — expressly enumerated |
| Whether the framework's silences are defects | Not silence — foreclosed |

#### Applicable corpus

The adopted interpretation is confined to the two frozen Ledger & Accounting
planning artifacts:

- Architecture and Implementation Plan — Git identity `6e68ab3e3f152d105e72bef4f84cd7c4afae9e1a`.
- Work-Package Decomposition and Roadmap — Git identity `b812e31cb0473c16c324419e1efb6103af1e274a`.

The resolution states that the precedent carries no force over a different or
successor corpus.

#### Explicit limitations

- The precedent binds interpretation, not authority.
- It does not compel outcomes that the frozen text does not compel.
- It is displaceable only by a competent later interpretive act, not by practice, assumption, or downstream need.
- It does not alter planning, governance, implementation authority, implementation artifacts, LA-WP2 status, successor planning, frozen artifacts, terminal states, actors, roles, burdens, standards, or procedures.
- It does not verify underlying factual assertions or the adequacy, sufficiency, or correctness of any evidentiary model.
- It does not perform review, confirmation, Content Identity Validation, freeze, closeout, ratification, allocation, or authorization.

#### Adoption status

`ADOPTED AS INTERPRETIVE PRECEDENT, WITH FIXED PRECEDENTIAL LIMITS`

## 5. Governance boundaries

The index:

- creates no constitutional, planning, governance, implementation, runtime, or operational authority;
- does not amend or reopen Planning, Architecture, the Roadmap, LA-WP2, the Constitutional Opinion, the ARB Resolution, or any other constitutional record;
- does not perform review, confirmation, Content Identity Validation, freeze, closeout, ratification, allocation, or authorization;
- does not resolve factual disputes or select an evidentiary model;
- does not convert a prior opinion into authority over a different corpus; and
- must preserve each source record's scope, classifications, holdings, and limitations without reinterpretation.

## 6. Lifecycle positioning

This index is a documentary navigation layer adjacent to the repository's
governance records. It may be updated after an adopted constitutional opinion
and its adoption disposition exist, but its update does not constitute any
stage in an implementation, review, confirmation, Content Identity
Validation, freeze, closeout, planning, or successor-planning lifecycle.

An index entry records adoption as stated by the source resolution. It does
not create adoption, make a non-adopted opinion precedent, or change the
lifecycle status of any work package.

## 7. Future additive maintenance procedure

Future maintenance shall be additive:

1. Confirm that the proposed source opinion and, where applicable, ARB resolution are existing repository artifacts or are separately authorized for publication.
2. Add a new entry identifier at the end of §4; do not rewrite, reorder, merge, or delete an existing entry.
3. Link the source records using repository-relative paths.
4. Copy only the source-stated holding headings, classifications, applicable corpus, adoption status, and explicit limitations; keep section references where available.
5. Mark the entry as adopted only when the adoption resolution states that disposition.
6. Record any successor-corpus limitation exactly and never carry a precedent across corpora by implication.
7. Validate links and document cleanliness for the additive change.

If an adopted record is corrected or superseded, preserve the existing index
entry as a historical navigation record and append a new entry describing the
later competent act. The index itself remains non-authoritative throughout.
