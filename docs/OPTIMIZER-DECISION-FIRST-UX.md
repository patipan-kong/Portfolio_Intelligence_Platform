# Optimizer decision-first UX (Phase 8A)

This presentation slice keeps the selected analysis and its recommendation visible before controls. It changes no allocation, scoring, policy, execution, Investor Intent, or history-writing semantics.

## Evidence mapping

| Display | Existing authoritative input | Missing/degraded handling |
| --- | --- | --- |
| Run identity | Selected history ID and response `analyzed_at` | Explicit unavailable identity/timestamp; history reads labeled historical, a newly completed response labeled just completed |
| Economic recommendation | `target_allocations[].action` and symbol | Unavailable for absent, invalid, duplicate, or already noise-suppressed recommendations; never inferred from `NO_ACTION` or trade count |
| Scheduled trade count | Complete `action_summary` arrays, existing execution-plan derivation, matching sell/reduce execution states | Unavailable for absent/partial/duplicate summaries or missing sell/reduce execution evidence; no assumed zero |
| Scheduling explanation | `stabilization.reason`, then `no_action_summary`, then existing `no_action_reason` labels | Explicit unavailable explanation |
| Owner Intent review | Frozen `advisory_intent_review` coverage and final/retained conflict outcomes | Unavailable without valid review evidence; conflict remains distinct from economic recommendation and scheduling |
| Consensus assessment | Stored consensus strength or stored final consensus score | Finite values only; unavailable is distinct from an assessed zero |
| Auditor observations | Existing flag validation status, scoring eligibility, category and provenance | Legacy claims neutral and explicitly unverified; structured opinions/advisory concerns remain unscored; missing risk level unavailable |
| Recorded owner decision | Existing decision lookup | Failed or potentially truncated lookup unavailable with retry; never treated as proof that no decision exists |

Scores are assessments, not return probabilities. Historical original scores and model text are retained, with presentation qualifications on summaries, consensus and each AI card. Raw structured flag provenance remains expandable. Recording an approval records a decision and virtual tracking; it does not place trades. Rebalance override starts a new analysis.

## History selection

Links include both `portfolio` and `history`. Explicit switching updates the URL, reload restores that run, and URL navigation hides the previous result synchronously while loading. Request guards ignore late responses. Missing/invalid requested history never substitutes a different run. Clearing a portfolio invalidates loaded history before restoring a selection.

The existing list endpoint is requested with a 30-run limit. A requested run outside the returned verified portfolio list is unavailable rather than fetched without confirmed portfolio ownership. Safe broader history navigation would require additional API support or pagination and is outside this slice.

## Fixture provenance and validation boundary

`frontend/tests/fixtures/optimizer-217.json` and `optimizer-218.json` are bounded copies of captured Dogfood #1 and #2 evidence (history 217/snapshot 173 and history 218/snapshot 174). Original layer text, target allocations, consensus scores, stabilization and frozen Intent evidence are copied unchanged. Unrelated watchlist details are omitted. The fixtures do not rewrite database records.

History 218 response-only action/execution summaries come from the captured response. For history 217, mocked action groups are constructed from captured actions; MICRON's deferred execution state comes from its frozen Advisory proposal's scheduled evidence. These are frontend test response fixtures, not a historical backend recomputation or counterfactual optimizer run.

Focused tests mock every API dependency and cover selection/reload, stale-response guards, shared portfolio selection, recommendation versus scheduling, missing evidence, historical qualification, decision lookup failure and provenance. Tests run sequentially with one Vitest worker and a 768 MB Node heap. Responsive inspection uses static HTML from the mocked rendered components and existing local CSS at 390×844 and 1440×900; it does not contact the application API. The full Next application shell and production end-to-end routing remain outside this visual check.

## Remaining boundaries

- Noise-suppressed responses do not expose the original economic recommendation sufficiently for this frontend to reconstruct it; show unavailable.
- Existing history reads may construct execution display fields from backend response logic. This slice does not add historical reconstruction or change frozen evidence.
- The existing owner-decision lookup returns at most 50 records. A full page without a match is uncertain and blocks duplicate recording until status can be established.
- Backend policy-scope inconsistencies identified by recon are outside this presentation slice.
- Unscored or unavailable evidence does not establish absence of risk. No offline replay score replaces a stored historical score.
- No live optimizer, provider, quote refresh, database write, backend restart, or source change outside the frontend/documentation is required for validation.
