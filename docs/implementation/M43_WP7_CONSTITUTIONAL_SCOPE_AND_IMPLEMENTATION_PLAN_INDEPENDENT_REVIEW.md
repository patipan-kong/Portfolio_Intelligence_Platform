Independent Constitutional Review — M43-WP7
Artifact reviewed: M43_WP7_Constitutional_Scope_Implementation_Plan.md (660 lines)
Reviewer role: Independent constitutional reviewer — read-only
Authorities consulted: frozen M43 Architecture §9, frozen WP1 register §§7.3–7.4, frozen WP4 plan §§6.6–6.7, frozen WP6 plan §§0/3.2/12, repository state

1. Executive assessment
The artifact is constitutionally sound in its central determination and in every ownership, authority, and no-default instrument it declares.

Its most important act is correct: it refuses the requested relabeling of WP7 as "Core Performance and Rolling Method Specification." Frozen M43 §9 allocates Core Performance and Rolling Method Specifications to WP6 and Risk and Benchmark-Relative Method Specifications to WP7. §0 preserves both allocations without amending either, and §18 restates the boundary permanently. This is the correct fail-closed response to a request that would have produced a constitutional allocation collision, an ownership merger, and a redesign of a completed package.

All ten frozen WP7 methods are allocated and only those methods. All authority classes that must be NONE are NONE. The M42-WP5 Benchmark Declaration remains the sole benchmark-selection authority with no fallback path. Risk-free and annualization dependencies remain fail-closed against exactly the defaults frozen WP4 prohibits, and §9 correctly prohibits hidden 252/365 rather than the values themselves — preserving frozen WP4 §6.7's allowance for an explicitly governed, version-bound derived session count.

Three defects require correction before confirmation: one omitted inherited gate, one unallocated frozen validation criterion, and one self-inconsistent placement declaration. None is a redesign; all are documentary corrections internal to WP7.

One premise correction the review must record. The task brief states M43-WP1 through WP6 are "COMPLETE AND FROZEN / Independent Constitutional Confirmation: CONFIRMED." The repository does not evidence this. docs/implementation/ contains ten M43 files; WP4, WP5, and WP6 exist only as _CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md planning artifacts, and no M43 independent-review or independent-confirmation artifact exists at all (M40 and M41 have them; M43 has none). The three normative specifications named as binding sources — M43_WP4_TEMPORAL_CURRENCY_CALENDAR_BENCHMARK_AND_ARITHMETIC_SEMANTICS_CONTRACT_SPECIFICATION.md, M43_WP5_PORTFOLIO_MEASURE_RESULT_CONTRACT_SPECIFICATION.md, M43_WP6_CORE_PERFORMANCE_AND_ROLLING_METHOD_SPECIFICATION.md — are absent.

WP7 is therefore right, not wrong, to hold the WP4, WP5, and WP6 gates open and to state Normative method-work status: BLOCKED PENDING INHERITED GATE CLOSURE. Had WP7 adopted the brief's status premise and treated those gates as closed, that would have been a MAJOR constitutional defect. It did not. No finding is raised against WP7 on this point; it is recorded so the discrepancy is resolved against the repository rather than silently against the artifact.

2. Resolution of constitutional findings
MAJOR
MAJOR-1 — The frozen WP1 §7.4 standing governance block on WP6 is absent from the inherited-gate inventory

Issue. Frozen WP1 §7.3 rejected the proposition "Ledger & Accounting owns the canonical period-return rule," splitting the concern into Portfolio-performance measure meaning (Portfolio Intelligence, frozen) and accounting semantics determining what enters the return (Ledger & Accounting, frozen). Frozen WP1 §7.4 records the resulting fail-closed consequence verbatim:

M43-WP6 BLOCKED — GOVERNANCE CORRECTION REQUIRED BEFORE WP6

Closure requires an independently reviewed M43 constitutional correction carried as a standing M43 governance item — owned by the M43 governance sequence, not by WP6 and not by WP7. Frozen WP6 §§0, 3.2(1–3), 13(2–3), and 15.2(1) preserve this block as its first entry gate.

WP7 §3.2 states a "WP6 completion gate" covering only the absence of a confirmed WP6 normative specification. The antecedent governance-correction block — which prevents WP6 method work from beginning at all — appears nowhere in the artifact. §13 step 3 requires verifying "frozen WP1–WP6 artifacts remain unchanged" and step 4 requires inventorying "every inherited gate," but no step names it. §15.1 then asserts External gates complete — PASS — Section 3.2 records all inherited gates.

Constitutional impact. WP7's entire method corpus depends on WP6-confirmed Portfolio-return dependencies (§3.1, §3.3, §6, §8.1–§8.6). A gate that blocks WP6 transitively blocks WP7. Omitting it produces an incomplete gate inventory, an unsupported PASS, and a latent path by which a future WP7 execution could read "WP6 normative specification confirmed" as sufficient without confirming that the specification was itself authorized by a closed governance correction. It also leaves the frozen WP1 §7.3 ownership split unrecorded in the artifact that consumes its output.

Required correction. Add an explicit inherited gate to §3.2 — M43 governance-correction gate — reciting the frozen WP1 §7.4 block by its exact citation, stating that it is owned by the M43 governance sequence and closable neither by WP6 nor by WP7, and stating that no WP7 dependency row may bind a WP6 Portfolio-return method until the correction is independently confirmed and the resulting WP6 normative specification is independently confirmed. Add the corresponding step to §13 before current step 7, add the corresponding row to §15.2, and restate the frozen WP1 §7.3 split in §6 alongside the existing Portfolio-return methods row. Correct the §15.1 External gates complete evidence cell accordingly.

MAJOR-2 — The frozen "missing benchmark" validation criterion is unallocated, and §12 does not map the frozen WP7 validation list

Issue. Frozen M43 §9 WP7 fixes eight validation criteria: zero variance, insufficient sample, missing benchmark, Explicitly None, unimplemented Composite/Category evidence, asynchronous calendars, zero tracking error, and negative-return vectors.

WP7 §11.1 and §11.2 cover seven of the eight. Missing benchmark has no coverage. §11.1 provides "Single benchmark evidence with exact identity," "Explicitly None," "unimplemented Composite," and "unimplemented Category" — none of which is the missing-benchmark case, which is the distinct condition where the M42 Benchmark Declaration coordinate is absent, or a Single declaration exists but its governed evidence is absent from the manifest. Frozen M43 §14 requires that missing M42 coordinates produce explicit unavailability rather than inferred values, making this case constitutionally load-bearing and non-substitutable by Explicitly None (a declared choice, not an absence).

Separately, §12 maps methods, applicability, sufficiency, vectors, vocabulary, and WP9 handoff — but does not map the frozen eight-item validation list to normative homes and entry gates. Frozen WP6 §12 established the governing precedent by mapping each frozen validation criterion as its own traceability row ("Cash-flow neutrality validation," "Missing-period handling validation," and four others). §15.1 nonetheless asserts Traceability — PASS — Section 12 maps every frozen WP7 allocation.

Constitutional impact. A frozen allocation item is unassigned, so §12 is not exhaustive and the §15.1 PASS is unsupported. Under WP7's own §13 closing rule — "WP7 cannot be declared complete by omitting a frozen allocated method" — an omitted frozen validation criterion is the same class of defect. Left uncorrected, a future WP7 corpus could satisfy every stated obligation while never specifying what happens when a declared benchmark's evidence is absent, which is precisely where a silent fallback would otherwise be introduced.

Required correction. Add missing-benchmark coverage to §11.1 as a distinct boundary case — declaration coordinate absent, and Single declaration present with absent or non-conforming governed evidence — with the corresponding fail-closed expectation, and add the matching rejection to §11.2 (no substitution, no fallback, no inference of a declaration). Extend §12 with one row per frozen M43 §9 WP7 validation criterion, each mapped to its normative home, required evidence, and entry gate. Correct the §15.1 Traceability evidence cell.

MAJOR-3 — The artifact does not occupy the singular normative home it declares for itself

Issue. §16.1 authorizes exactly one artifact: docs/implementation/M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md. The file under review is docs/implementation/M43_WP7_Constitutional_Scope_Implementation_Plan.md — a different path, differing in both casing and the omission of AND_. The declared path does not exist in the repository; the existing path is not authorized by §16.1. §16.1's three named review-chain artifacts are all keyed to the non-existent path, as are the eleven §10 deliverables and the §16.2 gate-conditional set by naming convention.

Constitutional impact. §7 requires exactly one normative home per concern and forbids a semantic rule having two. The artifact's own constitutional allocation currently resides at a path its §16 disclaims, so its placement declaration is self-inconsistent and the repository contains a path outside the authorized effect. Every downstream citation of this plan by exact path — required by WP7 §3.2's own "cited by exact path" discipline and by frozen WP6 §3.2's precedent — would resolve to nothing. All nine other M43 artifacts use the SCREAMING_SNAKE_CASE convention; this is the sole deviation.

Required correction. Rename the file to docs/implementation/M43_WP7_CONSTITUTIONAL_SCOPE_AND_IMPLEMENTATION_PLAN.md, matching §16.1 and the frozen corpus convention. Do not amend §16.1 to match the current filename — the declared path is the one consistent with WP1–WP6 and with the review-chain and deliverable names already written into §10 and §16.

MINOR
MINOR-1 — Inherited gates are recited without exact section or path anchors

Issue. §3.2 describes eight gates substantively correctly but cites none by exact anchor. The underlying gates have precise homes: the Portfolio Composition canonical-byte gap at frozen WP3 Subject Contract §7.1 and Input Manifest Contract §§6.3 and 10.3 against M42-WP7 §5; the risk-free authority-class proof at frozen WP4 §6.6; the annualization representability gap at frozen WP4 §6.7. Frozen WP6 §§0, 3.1, 3.2, and 12 cite each of these by exact section throughout.

Constitutional impact. Gate verifiability is weakened. A reviewer cannot confirm that WP7's paraphrase matches the frozen gate without independently locating it, and paraphrase drift across packages is how a gate is silently narrowed. No gate is presently weakened in substance — this is a citation-precision defect, not a regression.

Required correction. Add exact section citations to each §3.2 gate and to the corresponding §3.1 dependency rows, and name the two required binding-source paths (M43_WP4_TEMPORAL_CURRENCY_CALENDAR_BENCHMARK_AND_ARITHMETIC_SEMANTICS_CONTRACT_SPECIFICATION.md, M43_WP5_PORTFOLIO_MEASURE_RESULT_CONTRACT_SPECIFICATION.md) explicitly, with the frozen WP6 §3.2 proviso that a different independently confirmed path must be cited instead if one is confirmed.

MINOR-2 — "Active return" and "excess return" are relied upon without disposition

Issue. §5.1 closes inherited vocabulary and carves out only "the method-family labels listed in frozen M43" as allocation labels. §262 concludes "no new constitutional noun is required by this plan." But §8.6 requires "exact aligned active-return observations," §12 lists "Active return" in a required-evidence column, and §11.1 requires "negative excess returns." Neither term appears in the frozen M43 §9 WP7 allocation, so neither is covered by the allocation-label carve-out, and §5.2 forbids a "fixture field, method identity, or acceptance criterion" from implicitly admitting a noun.

Constitutional impact. Low. Both read as ordinary structural language rather than contract types, and no Glossary change is proposed. But their appearance in a traceability required-evidence column sits at the edge of §5.2's own prohibition, and the §262 conclusion is stated more absolutely than the text supports.

Required correction. Either extend the §5.1 allocation-label statement to cover ordinary descriptive quantity terms introduced by this plan — stating expressly that they are not admitted as constitutional nouns or contract types — or route both terms through §5.2 before the future corpus relies on them.

MINOR-3 — §2.2 omits governance-correction and frozen-artifact-amendment authority classes

Issue. Frozen WP6 §2.2 declares Governance correction — NONE, Frozen-artifact amendment — NONE, and Future-WP design — NONE. WP7 §2.2 declares neither of the first two. The prohibitions exist in prose (§4.2 final bullet, §16.3), but not as declared authority classes.

Constitutional impact. §15 requires that the artifact "declares every authority class" and §15.1 marks Authority declarations — PASS. With MAJOR-1 outstanding, the absence of an explicit Governance correction — NONE declaration is the specific omission that would matter most.

Required correction. Add Governance correction — NONE and Frozen-artifact amendment — NONE to the §2.2 declarations.

MINOR-4 — ADR range inconsistency and omission of Portfolio Calculation Rules from the authority order

Issue. §2.1 lists "ADR-001 through ADR-005"; the §3.1 dependency row lists "ADR-001–ADR-004." Frozen M43 §6 names ADR-001 through ADR-005 as a hard dependency. Separately, §2.1 omits docs/investment/PORTFOLIO_CALCULATION_RULES.md, which frozen M43 §6 names as a hard dependency and frozen WP6 §2.1 includes at position 4; the §3.1 Ledger & Accounting row cites no governing instrument.

Constitutional impact. Low. WP7 consumes accounting semantics indirectly through WP6 returns rather than directly, so no rule is displaced. The internal inconsistency and the unattributed Ledger & Accounting row are documentary defects.

Required correction. Reconcile the ADR range to ADR-001 through ADR-005 in both places, and cite Portfolio Calculation Rules in §2.1 and in the §3.1 Ledger & Accounting row.

MINOR-5 — §5.1 lists inherited terms without dispositions, owners, or normative homes

Issue. §5.1 enumerates fifteen inherited terms as a flat list. Frozen WP6 §5.1 records each with its frozen WP1 disposition, owner/grammar authority, and exact permitted use — including that Portfolio Degraded State is REUSE, that Degraded State is the term to use, and that the prefixed noun is never admitted.

Constitutional impact. None substantive. WP7 uses Degraded State correctly throughout and correctly preserves UNAVAILABLE as a Degraded State that never becomes a Portfolio Computation Outcome. The omission is documentary completeness, not a disposition regression.

Required correction. Record disposition, owner, and permitted-use for each §5.1 term, matching the frozen WP6 §5.1 form, including the explicit Portfolio Degraded State → REUSE → never admit the prefixed noun row.

MINOR-6 — Markdown structure is degraded relative to the entire frozen M43 corpus

Issue. The artifact contains zero ATX headings (#), two pipe characters, and 19 list markers across 660 lines. All eight declared matrices — §2.2, §3.1, §6, §7, §8.7, §9, §12, §15.1 — are tab-delimited plain text with no pipe delimiters and no header separator rows. Frozen WP6, by comparison, contains 55 headings, 135 pipes, and 302 list markers. Column boundaries remain recoverable via the tab characters, but no markdown renderer will present these as tables, and no section is addressable as a heading.

Constitutional impact. Low but non-zero. §1 sets the two-independent-readers standard as WP7's constitutional objective; ownership and no-default matrices that collapse into unstructured prose on render work against it, and unaddressable sections impede the exact-section citation discipline that MINOR-1 requires of WP7 itself.

Required correction. Restore ATX headings and pipe-delimited markdown tables with header separators, matching the frozen WP1–WP6 convention. This is a formatting correction only; no wording, row, or disposition changes.

3. Regression assessment
Dimension	Result	Basis
Constitutional regression	NONE	§0 preserves both frozen allocations and rejects the requested relabel. §18 makes the WP6 boundary permanent. §4.2 excludes core performance, period return, cumulative, annualized, rolling, and normalized performance. No frozen allocation is reinterpreted.
Ownership regression	NONE	§6 assigns exactly one owner per concern across twenty rows. Benchmark selection stays with M42-WP5 (No replacement or default); Portfolio-return methods stay with frozen WP6 (No recomputation); benchmark and risk-free evidence stay with Market Intelligence; calendar meaning stays with Market Intelligence; Provenance stays with Connectivity & Ingestion; attribution stays with WP8; runtime placement stays with WP9. §285 correctly treats an unresolved owner as a blocking condition rather than a claim. No laundering path found. (MAJOR-1 asks that the frozen WP1 §7.3 split be recorded, not that any owner be changed.)
Placement regression	ONE DEFECT — MAJOR-3	§7 assigns one normative home per concern with no duplicates, and §298 states the rule. The defect is that the artifact does not occupy the home §16.1 declares for it. No semantic rule is given two homes.
Authority regression	NONE	Header declares ten authority classes NONE; §2.2 adds registry activation, persistence/serialization implementation, API/UI adoption, provider selection, and capability-completion as NONE. No prose grants indirect authority to any NONE class. (MINOR-3 concerns two undeclared classes, not an expansion.)
Capability expansion	NONE	§70 expressly disclaims deploying Advanced Risk Metrics or activating benchmark-relative analytics. §16.3 prohibits touching ROADMAP capability status. §17 requires an explicit no-capability-declared statement and the M43-WP7 INCOMPLETE — BLOCKED form when a gate is open.
Executable semantics	NONE	§8.1–§8.6 state only what a future specification must close — no formula, algorithm, operation order, threshold, or convention is fixed. §3.3's dependency flow is explicitly annotated "No arrow represents executable flow or production behavior." §11.3 marks gate-touching material ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING and forbids reverse-authoring a rule from an expected value.
Production authority	NONE	Production-method authority: NONE in the header and §2.2; §4.2 prohibits admitting production methods; §10 requires every future artifact to state documentary/non-executable/non-production; §11.2 requires direct negative coverage of production-method claims.
Redesign	NONE	§4.2 and §16.3 prohibit modifying frozen M43 Architecture, WP1–WP6, and any M1–M42 artifact. §509 routes upstream defects to their owners rather than repairing them locally. §3.2 states that gate failure "never authorizes a fallback, weakened dependency, alternate formula, or ownership transfer." No frozen work package is redesigned.
Benchmark applicability (§8.7) — verified separately. The four Declaration forms remain constitutionally separated with no fallback introduced: Explicitly None → not applicable, no fallback; Single → applicable only with exact matching governed evidence; Composite and Category → blocked absent exact governed construction/matching evidence. §376 forbids collapsing Composite or Category into an arbitrary Single. §9 forbids global and asset-class fallback from Explicitly None. Consistent with frozen M43 §9 WP7 and frozen M42-WP5. (MAJOR-2 adds the missing-benchmark case; it does not disturb this separation.)

Method-family boundaries (§8.1–§8.6) — verified separately. All ten frozen methods are present and documentary only. §8.1 correctly consumes rather than recreates the WP6 return or normalized-performance series. §8.3 correctly prohibits a literal 0, 2.5%, environment value, caller value, or "current risk-free rate." §8.4 correctly requires a non-Explicitly-None declaration and rejects request- and provider-selected symbols. §9 correctly prohibits hidden 252/365/365.25 rather than the values as such, preserving frozen WP4 §6.7's allowance for an explicitly governed, version-bound derived session count — a distinction that would have been a regression if collapsed.

4. Overall assessment
APPROVED WITH REQUIRED CORRECTIONS

Three MAJOR and six MINOR findings must be resolved. All are documentary corrections confined to WP7's own artifact: one omitted inherited gate to add, one frozen validation criterion to allocate, one filename to align with the artifact's own §16.1, and six precision and completeness items. None requires redesigning WP7, none touches a frozen work package, and none alters the plan's central determination — which is correct and should be preserved unchanged.

Per §14.5, the corrected artifact requires renewed independent review, and confirmation requires unresolved findings NONE.

5. Repository modifications
NONE

This review was read-only. No file was created, modified, renamed, or deleted. The corrections identified above — including the MAJOR-3 rename — are stated as requirements for the authoring workflow and were not applied.
