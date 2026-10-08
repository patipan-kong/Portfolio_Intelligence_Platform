# Auditor policy claim integrity

## Root cause and evidence

History 218 / snapshot 174 captured two HIGH INVESTMENT_RISK flags with identical
issue text: "Position exceeds 15% max cap for single stock", for BH.BK and MICRON01.BK.
Its notes repeated the universal 15% premise. Raw final_risk_level was medium.
The canonical context was version wealth.optimizer-instrument-context.v1, SHA256
2e1e6713c2ee6614fbad3cf74d5d3853c6151e8f10cd38710b76bb643de3e46a.

The frozen active policy and effective envelope both specify 25% for a single
position. Final deterministic policy/regime/governance scores were 100, with no
violation_details or governance_flags. BH ordinary equity had no execution cap;
MICRON was HOLD at 16.03%, with a 15% BUY/ACCUMULATE execution target cap. Frozen
DR basket exposure 43.90% exceeded prompt-only 40% guidance, not an enforced rule.

The previous L3 producer already supplied the canonical block and active policy,
but offered only INVESTMENT_RISK versus OWNER_INTENT_REVIEW classification. JSON
parsing did not validate policy claims. investment_risk_flags included both HIGH
flags, and _consensus_engine computed max(30,55-2*8)=39. This was model inference
followed by an absent evidence-validation boundary, not a deterministic policy
calculator finding a breach. The nearby severity thresholds and execution caps
provide multiple numbers, but the exact frozen canonical block explicitly limits
execution caps to BUY/ACCUMULATE. A prompt-only fix is insufficient.

Full provider-request prompt payloads were not persisted. Frozen L1/L2 outputs,
canonical prompt_block, policy/envelope and L3 output are available; source tracing
proves construction/injection, not independently logged transport of the entire
L3 request. Do not call a reconstructed whole prompt an exact captured request.

## Structured contract and runtime path

wealth.auditor-policy-claims.v2 is built before L3 on the normalized L2 proposal.
The v1 model-opinion scoring gap is closed: no model label alone authorizes scoring.

Existing compute_policy_alignment_score -> structured violation_details ->
POLICY_BREACH evidence references -> L3 prompt -> validate_auditor_claims ->
eligible risk_flags -> consensus and stabilization. Its formulas are unchanged.
These results describe the L2 proposal; post-enforcement final governance remains
the existing separate policy calculation. No L3 observation creates a governance
flag. A proposal breach may be corrected before the final governance evaluation.

Execution metadata per_symbol.position_cap_pct + normalized action/weights ->
EXECUTION_RESTRICTION only for BUY/ACCUMULATE targets over the supplied cap;
otherwise existing exposure over the cap -> EXISTING_EXPOSURE, unscored and with
automatic_liquidation=false. Thresholds are consumed, never recreated: baseline
DR 15%, HIGH/CRITICAL DR 10% according to the existing execution producer.
No ticker heuristic is introduced. Ordinary equities receive only any cap actually
supplied by that producer; BH's absent cap is not replaced by a DR limit.

| Kind | Authority | Investment-risk scoring |
| --- | --- | --- |
| POLICY_BREACH | Exact policy evidence reference and matching symbol | Included; severity remains auditor judgment |
| EXECUTION_RESTRICTION | Exact applicable action/cap evidence reference | Included, explicitly scoped to proposal |
| EXISTING_EXPOSURE | Matching current exposure evidence | Excluded; no liquidation requirement |
| ADVISORY_CONCERN | Attributed model guidance, including DR basket | Excluded; never governance |
| INVESTMENT_OBSERVATION | Matching independently produced entry-timing evidence | Included at the existing MEDIUM timing severity |
| INVESTMENT_JUDGMENT without matching observation | Model-only opinion | Excluded; visible as unscored model opinion |
| OWNER_INTENT_REVIEW | Owner disagreement | Excluded; still visible |
| Unknown/missing/mismatched claim schema | Unsupported model output | Excluded; retained for review |

Validated deterministic issue text is generated from evidence, replacing model
prose even when a reference matches. Duplicate references cannot multiply scored
breaches. Malformed references fail closed. Raw output and the contract remain in
layer3_result, which the existing history writer freezes with the new run.
Free-form auditor_notes and raw safer_choice cannot carry rejected premises into
validated interpretations: summaries are derived from accepted observations; when
review items exist, the unsupported model choice is ignored in favor of the
existing L2 plan. Actual allocation selection already uses L2; no allocation or
execution-cap enforcement formula changed. Critical concerns invite review and
do not falsely promise a system trade block.

Fallback flags use the same validation boundary. Its prompt requests independent
opinions/advisory concerns, with no invented evidence reference. It has no
execution-cap clamp and receives no applicable execution-restriction evidence.
Fallback's existing degraded fixed consensus score is unchanged.

API/UI show VERIFIED restrictions, MODEL_OPINION investment assessments, ADVISORY,
UNSUPPORTED and OWNER_REVIEW separately. Unscored claims use neutral presentation;
raw notes are expandable and labeled unvalidated model opinion. Unscored flags
do not populate allocation risk badges. Historical records are labeled historical
model evidence and are not reinterpreted on read.

Independent investment observation path: timing_intelligence.compute_timing_score
-> score_timing_batch -> optimizer_timing.enrich_scores_with_timing ->
main.scores_map timing_score/execution_priority/timing_data_available ->
portfolio_data/watchlist_data -> pre-L3 risk:ENTRY_TIMING:<symbol> reference ->
L3 input contract -> matching validated claim -> consensus/stabilization.
No model allocation timing field is accepted as independent evidence. Only the
existing BUY/ACCUMULATE poor/deferred-entry rule is projected; no new risk taxonomy
or policy formula is created. Numeric score and data_available=true are required.

The existing timing adapter dropped the producer's data_available flag. It now
carries that boolean through the score context and fallback compact data, without
changing timing calculations or any write path. Missing price produces score zero
with data_available=false; it is not evidence of poor timing. Missing availability
also fails closed. The evidence freezes source, symbol, action, timing score,
priority, availability, rule source and MEDIUM severity. Model prose is replaced
by the factual observation; it cannot invent a holding cap or a long-term thesis.

The shared investment_risk_flags projection now requires explicit eligibility,
VERIFIED status, reference and structured provenance. Raw, missing-category flags
cannot penalize consensus or bypass minimum-benefit stabilization. Historical API
reads return stored scores, never recompute them through this new projection.
Model-only notes/risk levels/choices do not override the derived interpretation.
Owner-only output cannot promote an investment-risk penalty or choice.

## Offline replay and historical boundary

Read-only comparison against the previously captured complete database rows
confirmed history 218 and snapshot 174 unchanged. Replay used their frozen
outputs and metadata, without current Registry lookup, market refresh or AI.
Neither old flag contains claim_kind/evidence_ref: both become UNSUPPORTED review
items. This does not semantically classify their prose. Independently, frozen
policy evidence contradicts the universal-limit premise; MICRON has only an
unscored existing-exposure observation.

Offline interpretation: risk alignment 92, consensus strength 83. Stored historical
scores remain 39 and 64. This is a deterministic interpretation replay, not a new
optimizer result, allocation replay, or proof that a model recommendation changes.
Unchanged Intent/deferred execution is covered by the existing mocked endpoint
regression using an unscored model timing opinion alongside an owner
conflict, plus separate tests preserving independently evidenced entry risk. Real business records are never changed by this slice.

## Focused validation

Files changed in the scoring-authority follow-up:

- backend/services/optimizer/auditor_claims.py
- backend/services/optimizer/risk_flags.py
- backend/agents/optimizer.py
- backend/services/optimizer_timing.py
- backend/main.py (availability metadata projection only)
- frontend/components/optimizer/AuditorClaimFlag.tsx
- backend/tests/test_auditor_policy_claims.py
- backend/tests/test_advisory_dogfood_correctness.py
- backend/tests/test_advisory_intent_integration.py
- backend/tests/test_optimizer_pipeline.py
- frontend/tests/AuditorClaimFlag.test.tsx
- docs/AUDITOR-POLICY-CLAIM-INTEGRITY.md

The earlier uncommitted frontend/app/optimizer/page.tsx and frontend/lib/api.ts
changes remain present; this follow-up does not edit them. The complete working
diff therefore contains fourteen intended files, plus the owner's existing
ai-model.json modification and artifacts directory, both preserved.

Sequential bounded-memory tests, with all model/provider paths mocked:

- test_auditor_policy_claims.py: 32 passed (including mocked layered pipeline).
- test_optimizer_pipeline.py: 29 passed.
- test_advisory_dogfood_correctness.py: 10 passed.
- test_canonical_instrument_context.py: 6 passed (isolated SQLite history/fallback).
- test_advisory_intent_integration.py: 29 passed (Intent and deferred execution).
- test_optimizer_timing.py: 21 passed (existing enrichment and timing rules).
- AuditorClaimFlag.test.tsx: 4 passed, one worker, Node heap capped at 768 MB.

The new tests cover BH absent cap, MICRON HOLD/BUY/ACCUMULATE, supplied 15/10 caps,
real general-policy calculator breaches, basket advisory, missing/malformed/
duplicate evidence, independent risks, missing-data guards, forged model contracts,
offline immutable evidence and UI attribution. Total: 131 focused tests passed.
The false 15% claims score zero flags under DETERMINISTIC_POLICY,
INVESTMENT_JUDGMENT, ADVISORY_GUIDANCE, OWNER_INTENT_REVIEW, missing and unknown
labels. Tests exercise each as both category and claim_kind. All offline frozen
replays yield risk alignment 92 and consensus strength 83; no historical score changes.
Deprecation warnings predate this slice. No live optimizer/AI calls or builds.

## Normal endpoint write footprint (read-only audit)

| Producer/path | Expected production write | Future live-run authorization |
| --- | --- | --- |
| main.analyze_optimizer preparation / data_fetcher | agent_cache, market_data_cache updates, including missing TA/FA preparation | Explicitly permit cache/provider preparation; missing analyses may add AI calls |
| analytics.regime_detector.detect_regime -> _save_regime_snapshot | regime_snapshots | Permit regime capture |
| ai_client call_ai usage tracking | user_usage per actual provider call | Permit usage writes and specify retry/fallback policy |
| main history writer, snapshot_writer | optimizer_history, recommendation_snapshots | Permit one run's frozen evidence records |
| main background compute_calibration | confidence_calibration_records | Permit calibration, including background completion |
| main background grade_pending_plans | recommendation_grades | Permit grading; may process other pending plans for the portfolio |
| main background create_active_model_shadow/create_recommendation_shadow/value_shadow_portfolio | shadow_portfolios, shadow_portfolio_snapshots (virtual, not trades) | Explicitly permit virtual tracking and valuation |

Dogfood #2 observed exactly these ten changed tables. They are expected endpoint
behavior, but were broader than that run's narrow quote/history/snapshot write
allowance. The mismatch was authorization documentation, not evidence of real
holdings, transaction, Intent or Registry mutations. No write paths are changed.
Shadow code may refresh an existing ACTIVE_MODEL and create a recommendation-keyed
shadow; do not promise a fixed row count across runs. Calibration/grading/thread
failure handlers allow partial background results. Future audits must wait for
background completion and compare protected business data separately.

## Limits and review boundary

Verdict: READY TO COMMIT. The v1 adversarial case previously scored 39 when false
cap prose was labeled INVESTMENT_JUDGMENT. In v2 that label with no independent
reference yields MODEL_OPINION, scoring_eligible=false, and risk alignment 92.
Unsupported deterministic claims remain UNSUPPORTED; advisory and owner review
remain outside investment-risk scoring. The raw output remains visible for review.

No semantic text classifier, new policy engine, model-based evidence generation,
or live experiment is introduced. Opinions about valuation, earnings or business
risk remain visible but unscored where no existing independent producer/reference
is available. This is deliberate limited evidence coverage, not proof that such
risks are absent. A valid entry-timing reference supports only the generated entry
observation, never arbitrary accompanying model prose. Matching policy references
likewise support only their canonical calculated violation text.

Timing evidence inherits the existing producer's normalization, component defaults
and data-availability semantics. Its numeric result is frozen and independently
produced from market signals, but raw indicator histories and a separate quote-age
assessment are not added here. No timing fetch/refresh occurs in this slice.
Policy/execution severity remains the existing auditor severity convention once
evidence matches; entry timing retains the established MEDIUM ceiling. Existing
weights and score formulas are unchanged. Fallback retains its degraded fixed
consensus score; unavailable references produce unscored opinions.

Proposal evidence uses the existing policy evaluator and its existing meanings
(e.g. BETA_EXPOSURE is a count of aggressive buys, not measured portfolio beta).
This slice does not correct those policy semantics, resolve allocation math,
reconstruct historical relationships, or enforce DR basket guidance.

backend/ai-model.json and all 18 pre-existing artifact files were hash/inventory
verified against Dogfood #2 preservation evidence. No migrations, Registry/Intent/
holdings/transactions, market refresh, historical mutations, commit or push.
Read-only fingerprints of all 50 database tables matched the post-Dogfood #2
baseline. git diff --check passed; graphify update . refreshed the AST graph only.
