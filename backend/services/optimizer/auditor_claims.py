"""Evidence-linked auditor claims. No prose classifier or allocation enforcement.

Unknown/legacy claims are preserved for review, never inferred to be opinions.
Model labels/opinions never authorize scoring; matching producer evidence does.
"""
from copy import deepcopy

VERSION = "wealth.auditor-policy-claims.v2"


def build_claim_evidence(allocations, policy_details, execution_context, risk_inputs=None):
    evidence = {}
    for i, detail in enumerate(policy_details):
        ref = f"policy:{i}"
        evidence[ref] = {**deepcopy(detail), "kind": "POLICY_BREACH",
                         "source": "compute_policy_alignment_score", "scope": "L2_PROPOSAL"}
    for i, allocation in enumerate(allocations):
        symbol = allocation.get("symbol")
        meta = (execution_context or {}).get("per_symbol", {}).get(symbol, {})
        cap = meta.get("position_cap_pct")
        if cap is None:
            continue
        action = allocation.get("action", "HOLD")
        weight = float(allocation.get("target_weight") or 0)
        current = float(allocation.get("current_weight") or 0)
        if action in ("BUY", "ACCUMULATE") and weight > cap:
            kind, value = "EXECUTION_RESTRICTION", weight
        elif current > cap:
            kind, value = "EXISTING_EXPOSURE", current
        else:
            continue
        evidence[f"execution:{i}"] = {
            "kind": kind, "symbol": symbol, "proposed_pct": value, "allowed_pct": cap,
            "action": action, "source": "execution_context.per_symbol",
            "scope": "BUY_ACCUMULATE_TARGET_ONLY", "automatic_liquidation": False,
        }
    # Consume pre-L3 timing enrichment, never timing fields in model allocations.
    # Reuse the existing entry-timing rule, not a new investment-risk taxonomy.
    for allocation in allocations:
        symbol = allocation.get("symbol")
        observation = (risk_inputs or {}).get(symbol, {})
        score, priority = observation.get("timing_score"), observation.get("execution_priority")
        action = allocation.get("action", "HOLD")
        if observation.get("timing_data_available") is not True:
            continue
        if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 100:
            continue
        if action not in ("BUY", "ACCUMULATE") or not (priority == "DEFER" or score < 40):
            continue
        note = f"Poor current entry timing (score {score}, priority {priority})"
        evidence[f"risk:ENTRY_TIMING:{symbol}"] = {
            "kind": "INVESTMENT_OBSERVATION", "symbol": symbol, "source": "optimizer_timing.enrich_scores_with_timing",
            "scope": "L2_PROPOSAL_ENTRY_TIMING", "action": action, "timing_score": score,
            "execution_priority": priority, "issue": note, "severity": "MEDIUM",
            "data_available": True, "rule_source": "optimizer_timing.build_timing_note",
        }
    return {"version": VERSION, "evidence": evidence,
            "basket_guidance": {"kind": "ADVISORY_CONCERN", "threshold_pct":
                (execution_context or {}).get("dr_portfolio_cap", 40), "enforced": False}}


def validate_auditor_claims(result, contract):
    """Return a new interpretation; never mutate frozen input or model evidence."""
    output = deepcopy(result)
    accepted, review, seen = [], [], set()
    for raw in result.get("risk_flags", []) or []:
        if not isinstance(raw, dict):
            review.append({"symbol": "UNKNOWN", "issue": "Malformed model flag", "severity": "LOW",
                           "validation_status": "UNSUPPORTED", "scoring_eligible": False})
            continue
        flag = deepcopy(raw)
        kind = flag.get("claim_kind")
        if flag.get("category") == "OWNER_INTENT_REVIEW":
            flag.update(validation_status="OWNER_REVIEW", scoring_eligible=False)
            accepted.append(flag)
            continue
        flag["severity"] = str(flag.get("severity", "")).upper()
        valid_schema = flag.get("category") == "INVESTMENT_RISK" and flag["severity"] in ("LOW", "MEDIUM", "HIGH", "CRITICAL")
        ref = flag.get("evidence_ref")
        evidence = contract.get("evidence", {}).get(ref) if isinstance(ref, str) else None
        matching_kind = evidence and (evidence["kind"] == kind or
            (kind == "INVESTMENT_JUDGMENT" and evidence["kind"] == "INVESTMENT_OBSERVATION"))
        if valid_schema and kind in ("POLICY_BREACH", "EXECUTION_RESTRICTION", "EXISTING_EXPOSURE", "INVESTMENT_JUDGMENT", "INVESTMENT_OBSERVATION") \
                and matching_kind and flag.get("symbol") == evidence.get("symbol", "PORTFOLIO"):
            if ref in seen:
                flag.update(validation_status="UNSUPPORTED", scoring_eligible=False,
                            provenance="Duplicate evidence reference; no additional scored breach")
                review.append(flag)
                continue
            seen.add(ref)
            # Model text is not authoritative even with a valid reference.
            unit = " allocations" if evidence.get("violation_type") == "BETA_EXPOSURE" else "%"
            flag["issue"] = evidence.get("issue") or f"{evidence.get('violation_type', kind)}: {evidence.get('proposed_pct')}{unit} / {evidence.get('allowed_pct')}{unit}"
            if evidence["kind"] == "INVESTMENT_OBSERVATION":
                flag["severity"] = evidence["severity"]
                flag["claim_kind"] = "INVESTMENT_OBSERVATION"
            if kind == "EXISTING_EXPOSURE":
                flag["issue"] += "; execution cap does not require liquidation"
            flag.update(validation_status="VERIFIED" if kind != "EXISTING_EXPOSURE" else "ADVISORY",
                        scoring_eligible=kind != "EXISTING_EXPOSURE", provenance=deepcopy(evidence))
            (accepted if flag["scoring_eligible"] else review).append(flag)
        else:
            status = "MODEL_OPINION" if kind in ("INVESTMENT_JUDGMENT", "INVESTMENT_OBSERVATION") else \
                "ADVISORY" if kind in ("ADVISORY_CONCERN", "ADVISORY_GUIDANCE") else "UNSUPPORTED"
            flag.update(validation_status=status, scoring_eligible=False,
                        provenance="No matching independently produced evidence; unscored model claim")
            review.append(flag)
    output.update(risk_flags=accepted, claim_reviews=review, raw_model_output=deepcopy(result),
                  policy_claim_contract=deepcopy(contract), claim_validation_version=VERSION)
    scored = [f for f in accepted if f.get("scoring_eligible")]
    output["final_risk_level"] = ("high" if any(f.get("severity") in ("HIGH", "CRITICAL") for f in scored)
                                  else "medium" if scored else "low")
    # Free-form notes/choice may restate rejected premises; retain only as raw evidence.
    output["auditor_notes"] = f"{len(scored)} scored observations; {len(review)} unscored claims for review."
    if review or not scored:
        output["safer_choice"] = "layer2"
    return output
