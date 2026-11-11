"""3-Layer Optimizer — L1 Strategist, L2 Challenger, L3 Risk Auditor.

See OPTIMIZER_PHILOSOPHY.md §5 (pipeline stages) and §6 (Belief Engine
boundary) — these layers answer belief questions only; trade selection and
funding arithmetic happen downstream, deterministically.
"""
import json
import logging
from copy import deepcopy
from math import floor
from typing import Callable
from services.ai_client import MujiLayer1Response, call_ai
from services.json_utils import safe_parse_json
from services.optimizer.sector_policy import (
    OPTIMIZER_POLICY_MUJI_V2, SECTOR_POLICY_ADVISORY, UnsupportedOptimizerPolicyEvidence,
    attach_target_evaluation, current_values, evaluate_frozen_sectors,
    evaluate_sectors, freeze_concentration, freeze_positions, project_targets, sector_weights,
    optimizer_policy_mode as read_optimizer_policy_mode,
)
from services.optimizer.risk_flags import investment_risk_flags
from services.optimizer.auditor_claims import build_claim_evidence, validate_auditor_claims
from services.optimizer import strategic_candidates
from services.optimizer.strategic_candidates import (
    SELECTION_VERSION, validate_candidate_reviews, decide_selection,
)
from services.optimizer.strategy_profiles import build_persona_context, get_profile  # noqa: F401
from services.optimizer.policy_engine import (  # noqa: F401
    compute_policy_alignment_score,
    compute_concentration_breach_severity,
    get_relaxed_turnover_cap,
    envelope_to_dict as _envelope_to_dict,
    HardConstraints as _HardConstraints,
    PolicyEnvelope as _PolicyEnvelope,
)
from services.optimizer.constraint_resolver import (  # noqa: F401
    EffectiveEnvelope as _EffectiveEnvelope,
    envelope_to_dict as _eff_env_to_dict,
)
from services.advisory_intent_context import (
    ATTEMPT_FALLBACK as _ATTEMPT_FALLBACK,
    ATTEMPT_PRIMARY as _ATTEMPT_PRIMARY,
    EFFECT_ORIGINATE as _ORIGINATE,
    EFFECT_RELABEL as _RELABEL,
    EFFECT_REPLACE as _REPLACE,
    EFFECT_SCALE as _SCALE,
    EFFECT_SUPPRESS as _SUPPRESS,
    LAYER_FALLBACK as _LAYER_FALLBACK,
    LAYER_L1 as _LAYER_L1,
    LAYER_L1_RETRY as _LAYER_L1_RETRY,
    LAYER_L2 as _LAYER_L2,
    LAYER_L3 as _LAYER_L3,
    SOURCE_ADVISORY as _SRC_ADVISORY,
    SOURCE_POLICY_RISK as _SRC_POLICY,
    SOURCE_SYSTEM_RULE as _SRC_SYSTEM,
    STAGE_EXECUTION_CAP as _STAGE_EXEC_CAP,
    STAGE_FALLBACK as _STAGE_FALLBACK,
    STAGE_FORCED_SELL as _STAGE_FORCED_SELL,
    STAGE_HARD_POLICY as _STAGE_HARD_POLICY,
    STAGE_L1 as _STAGE_L1,
    STAGE_L2 as _STAGE_L2,
    STAGE_LEGACY_LOCK as _STAGE_LEGACY_LOCK,
    STAGE_NEUTRAL_SNAP as _STAGE_NEUTRAL_SNAP,
    STAGE_RECONCILIATION as _STAGE_RECONCILIATION,
)

logger = logging.getLogger(__name__)


# ─── Advisory Integration V1 (Slice 1) hooks ─────────────────────────────────
# `advisory` is an opaque run object (services.advisory_intent_context.
# AdvisoryIntentRun) passed only when the default-OFF advisory-intent flag is
# on. It carries a FROZEN prompt context and records proposal transitions at
# the mutation sites below. With advisory=None every hook is a no-op and every
# prompt is byte-identical to the legacy one. It never changes an allocation.

def _alloc_basis(a: dict | None) -> dict | None:
    if a is None:
        return None
    return {"action": (a.get("action") or "HOLD").upper(), "target_weight": a.get("target_weight"),
            "current_weight": a.get("current_weight")}


def _observe(advisory, symbol: str, before: dict | None, after_row: dict | None, *, stage: str,
             source: str, effect: str, reason_code: str, reason_text: str = "") -> None:
    if advisory is None:
        return
    advisory.observe(symbol, stage=stage, source=source, effect=effect, reason_code=reason_code,
                     reason_text=reason_text, before=before, after=_alloc_basis(after_row))


def _intent_block(advisory, layer: str) -> str:
    return advisory.prompt_block(layer) if advisory is not None else ""


def _goal_decision_block(context: dict | None) -> str:
    if context is None:
        return ""
    goals = [{key: goal.get(key) for key in ("id", "goal_type", "priority", "target_amount",
              "target_date", "designated_total", "funding_gap")}
             for goal in context.get("goals", [])]
    return ("[OBSERVED SELECTED GOALS — decision context, not trade instructions]\n"
            + json.dumps({"version": context["contract_version"], "goals": goals}, sort_keys=True)
            + "\nFunding gap is not an immediate cash requirement; no success probability is available.\n")


def _note_prompt(advisory, layer: str, outcome: str) -> None:
    if advisory is not None:
        advisory.note_prompt(layer, advisory.ledger.attempt, outcome)


def _note_l1_proposals(advisory, swaps: list[dict], locked: list[str]) -> None:
    """Accepted L1 swap legs on held symbols; legs dropped by the legacy lock are SUPPRESSED."""
    if advisory is None:
        return
    locked_set = set(locked)
    for swap in swaps:
        blocked = swap.get("sell_symbol") in locked_set or swap.get("buy_symbol") in locked_set
        legs = ((swap.get("sell_symbol"), "SELL" if swap.get("type") == "SELL" else "REDUCE"),
                (swap.get("buy_symbol"), "ACCUMULATE"))
        for symbol, action in legs:
            if not symbol:
                continue
            leg = {"action": action, "target_weight": 0.0 if action == "SELL" else None, "current_weight": None}
            advisory.observe(symbol, stage=_STAGE_L1, source=_SRC_ADVISORY, effect=_ORIGINATE,
                             reason_code="L1_PROPOSAL", reason_text=str(swap.get("reason") or ""),
                             after=leg, direction_only=action != "SELL")
            if blocked:
                advisory.observe(symbol, stage=_STAGE_LEGACY_LOCK, source=_SRC_SYSTEM, effect=_SUPPRESS,
                                 reason_code="LEGACY_ALLOW_SWAP_FALSE",
                                 reason_text="Swap dropped: a leg is a legacy-locked position.",
                                 before=leg, after={"action": "HOLD", "target_weight": None, "current_weight": None})


def _apply_forced_and_locked(
    alloc_map: dict[str, dict], sell_forced: list[str], locked_set: set, pc_map: dict[str, float],
    advisory,
) -> None:
    """Forced exits then legacy locks (shared by the primary and fallback paths)."""
    for sym in sell_forced:
        if sym in alloc_map:
            before = _alloc_basis(alloc_map[sym])
            alloc_map[sym]["action"] = "SELL"
            alloc_map[sym]["target_weight"] = 0.0
            if alloc_map[sym].get("decision_basis") in _CONCENTRATION_ADVISORY_BASES:
                alloc_map[sym].pop("decision_basis")
                alloc_map[sym]["reason"] = "Forced exit: SELL signal."
            if (before["action"], before["target_weight"]) != ("SELL", 0.0):
                _observe(advisory, sym, before, alloc_map[sym], stage=_STAGE_FORCED_SELL, source=_SRC_SYSTEM,
                         effect=_REPLACE, reason_code="FORCED_EXIT_SELL_SIGNAL",
                         reason_text="Forced exit: SELL signal.")
        else:
            cur_w = pc_map.get(sym, 0.0)
            alloc_map[sym] = {
                "symbol": sym, "current_weight": cur_w, "target_weight": 0.0,
                "action": "SELL", "allocation_change_percent": round(-cur_w, 2),
                "estimated_amount": 0, "reason": "Forced exit: SELL signal.",
            }
            _observe(advisory, sym, None, alloc_map[sym], stage=_STAGE_FORCED_SELL, source=_SRC_SYSTEM,
                     effect=_ORIGINATE, reason_code="FORCED_EXIT_SELL_SIGNAL",
                     reason_text="Forced exit: SELL signal.")
    for sym in locked_set:
        if sym in alloc_map and alloc_map[sym].get("action") not in ("HOLD", "WATCH"):
            before = _alloc_basis(alloc_map[sym])
            alloc_map[sym]["action"] = "HOLD"
            alloc_map[sym]["target_weight"] = alloc_map[sym].get("current_weight", 0.0)
            alloc_map[sym]["allocation_change_percent"] = 0.0
            _observe(advisory, sym, before, alloc_map[sym], stage=_STAGE_LEGACY_LOCK, source=_SRC_SYSTEM,
                     effect=_SUPPRESS, reason_code="LEGACY_ALLOW_SWAP_FALSE",
                     reason_text="Legacy lock (allow_swap=false) holds this position unchanged.")


class HardPolicyEnforcementError(RuntimeError):
    """Deterministic hard-policy enforcement could not be proven safe."""


def _emit_stage(on_stage: Callable[[str], None] | None, stage: str) -> None:
    """Fire the optional progress callback; never let it break the run."""
    if on_stage is None:
        return
    try:
        on_stage(stage)
    except Exception:  # pragma: no cover — presentation-only plumbing
        pass


def _make_envelope_from_dict(d: dict) -> _PolicyEnvelope:
    """Reconstruct a PolicyEnvelope from its serialized dict form (for scoring)."""
    hc = d.get("hard_constraints", {})
    return _PolicyEnvelope(
        hard_constraints=_HardConstraints(
            min_cash_pct            = float(hc.get("min_cash_pct", 5.0)),
            max_single_position_pct = float(hc.get("max_single_position_pct", 22.0)),
            max_sector_pct          = float(hc.get("max_sector_pct", 40.0)),
            max_turnover_pct        = float(hc.get("max_turnover_pct", 40.0)),
            suppress_speculative    = bool(hc.get("suppress_speculative", False)),
            beta_ceiling            = hc.get("beta_ceiling"),
            max_new_positions       = int(hc.get("max_new_positions", 3)),
        ),
        soft_factor_tilts       = d.get("soft_factor_tilts", {}),
        deployment_bias         = d.get("deployment_bias", "SELECTIVE"),
        risk_budget             = float(d.get("risk_budget", 55.0)),
        rebalance_aggressiveness= float(d.get("rebalance_aggressiveness", 0.5)),
        strictness_level        = d.get("strictness_level", "NORMAL"),
        emergency_override      = bool(d.get("emergency_override", False)),
        emergency_reason        = d.get("emergency_reason"),
        policy_narrative        = d.get("policy_narrative", ""),
        confidence_discount     = float(d.get("confidence_discount", 0.0)),
        violations              = list(d.get("violations", [])),
        resolved_sector_limits  = d.get("resolved_sector_limits", {}),
        sector_limit_sources    = d.get("sector_limit_sources", {}),
        position_limit_source   = d.get("position_limit_source", "POLICY_ENGINE"),
        sector_policy_mode      = d.get("sector_policy_mode"),
        optimizer_policy_mode   = d.get("optimizer_policy_mode"),
    )


_DEFAULT_LAYERS: dict = {
    "layer1": {
        "name": "Strategist",
        "role": "Capital allocation strategist",
        "provider": "anthropic",
        "model": "claude-sonnet-4-6",
    },
    "layer2": {
        "name": "Challenger",
        "role": "Independent risk-aware reviewer",
        "provider": "anthropic",
        "model": "claude-sonnet-4-6",
    },
    "layer3": {
        "name": "Risk Auditor",
        "role": "Concentration risk and assumption validator",
        "provider": "anthropic",
        "model": "claude-sonnet-4-6",
    },
}


# ─── Data helpers ─────────────────────────────────────────────────────────────

def _compute_portfolio_weights(portfolio_items: list[dict], cash_balance: float = 0.0) -> list[dict]:
    """Add market_value and NAV-basis weight_pct to each portfolio item.

    ``weight_pct`` is value / NAV x 100 at full precision (NAV = positions +
    ``cash_balance``); see services/optimizer/nav_basis.py. The legacy
    equity-only weight is kept as ``equity_weight_pct`` for audit only.
    """
    from services.optimizer.nav_basis import BASIS_NAV, compute_nav_basis, item_value

    basis = compute_nav_basis(portfolio_items, cash_balance)
    result = []
    for item in portfolio_items:
        value = item_value(item)
        result.append({
            **item,
            "market_value": round(value, 2),
            "value_exact": value,
            "weight_pct": (value / basis.nav * 100.0) if basis.usable else 0.0,
            "equity_weight_pct": round(value / basis.equity * 100, 1) if basis.equity > 0 else 0.0,
            "weight_basis": BASIS_NAV,
            "nav_value": basis.nav,
            "nav_cash": basis.cash,
        })
    return result


def _compact_p(items: list[dict]) -> list[dict]:
    return [
        {
            "symbol": i["symbol"],
            "sector": i.get("sector") or "Other",
            "sector_classification": i.get("sector_classification"),
            "signal": i.get("signal", "HOLD"),
            "combined_score": i.get("combined_score", 0),
            "ta_score": i.get("ta_score", 0),
            "fa_score": i.get("fa_score", 0),
            "trend": i.get("trend", "sideways"),
            "pe_ratio": i.get("pe_ratio"),
            "roe": round(i["roe"] * 100, 1) if i.get("roe") else None,
            "allow_swap": i.get("allow_swap", True),
            "weight_pct": round(i.get("weight_pct", 0.0), 2),
            "market_value": i.get("market_value", 0.0),
            "current_price": i.get("current_price"),
            # Phase 4C.6H.3 — timing fields
            "timing_score": i.get("timing_score"),
            "timing_data_available": i.get("timing_data_available", False),
            "execution_priority": i.get("execution_priority"),
            "momentum": i.get("momentum"),
        }
        for i in items
    ]


def _compact_w(items: list[dict]) -> list[dict]:
    return [
        {
            "symbol": i["symbol"],
            "current_price": i.get("current_price"),
            "sector": i.get("sector") or "Other",
            "sector_classification": i.get("sector_classification"),
            "signal": i.get("signal", "HOLD"),
            "combined_score": i.get("combined_score", 0),
            "ta_score": i.get("ta_score", 0),
            "fa_score": i.get("fa_score", 0),
            "trend": i.get("trend", "sideways"),
            "pe_ratio": i.get("pe_ratio"),
            "roe": round(i["roe"] * 100, 1) if i.get("roe") else None,
            # Phase 4C.6H.3 — timing fields
            "timing_score": i.get("timing_score"),
            "timing_data_available": i.get("timing_data_available", False),
            "execution_priority": i.get("execution_priority"),
            "momentum": i.get("momentum"),
        }
        for i in items
    ]


def _build_score_context_map(pc: list[dict], wc: list[dict]) -> dict[str, dict]:
    """symbol -> compact score dict, for attaching deterministic context to AI rows.

    Portfolio holdings take priority over watchlist entries for symbols present in both
    (fresher weight/price data). No new calculations — pc/wc are already computed by
    _compact_p/_compact_w before this is called.
    """
    score_map: dict[str, dict] = {w["symbol"]: w for w in wc}
    score_map.update({p["symbol"]: p for p in pc})
    return score_map


# Reason UX (progressive disclosure) — deterministic fields attached to swap/allocation
# rows by symbol lookup, mirroring the existing per_sym_exec execution-metadata join.
_SCORE_CONTEXT_FIELDS = ("ta_score", "fa_score", "pe_ratio", "roe", "sector", "sector_classification", "combined_score", "timing_score")


def _apply_score_context(row: dict, score_map: dict[str, dict] | None, symbol: str | None) -> None:
    if not score_map or not symbol:
        return
    ctx = score_map.get(symbol)
    if not ctx:
        return
    for field in _SCORE_CONTEXT_FIELDS:
        if field in row:
            continue
        value = ctx.get(field)
        if value is not None:
            row[field] = value


_L1_BUY_SIGNALS = {"BUY", "ACCUMULATE", "WATCH"}


def _compress_for_layer1(pc: list[dict], wc: list[dict]) -> tuple[list[dict], list[dict]]:
    """Strip data to minimum Layer 1 needs — shortened keys reduce prompt tokens."""
    c_pc = [
        {
            "s": i["symbol"],
            "sec": i.get("sector", "Other"),
            "sector_status": (i.get("sector_classification") or {}).get("classification_status"),
            "w": round(i.get("weight_pct", 0), 1),
            "mv": round(i.get("market_value", 0)),
            "fa": i.get("fa_score", 0),
            "ta": i.get("ta_score", 0),
            "sig": i.get("signal", "HOLD"),
            "swap": i.get("allow_swap", True),
            "ts": i.get("timing_score"),        # Phase 4C.6H.3 — timing score
            "pr": i.get("execution_priority"),  # Phase 4C.6H.3 — execution priority
        }
        for i in pc
    ]
    actionable = [w for w in wc if w.get("signal", "HOLD") in _L1_BUY_SIGNALS]
    actionable.sort(key=lambda x: -(x.get("fa_score", 0) + x.get("ta_score", 0)))
    c_wc = [
        {
            "s": w["symbol"],
            "sec": w.get("sector", "Other"),
            "sector_status": (w.get("sector_classification") or {}).get("classification_status"),
            "fa": w.get("fa_score", 0),
            "ta": w.get("ta_score", 0),
            "sig": w.get("signal", "WATCH"),
            "ts": w.get("timing_score"),        # Phase 4C.6H.3 — timing score
            "pr": w.get("execution_priority"),  # Phase 4C.6H.3 — execution priority
        }
        for w in actionable[:10]
    ]
    return c_pc, c_wc


def _postprocess_swaps(swaps: list[dict], sell_forced: list[str], locked: list[str]) -> list[dict]:
    """Ensure forced SELLs appear in swap list and remove locked symbols."""
    locked_set = set(locked)
    result = [s for s in swaps if s.get("sell_symbol") not in locked_set and s.get("buy_symbol") not in locked_set]
    covered = {s["sell_symbol"] for s in result if s.get("type") == "SELL"}
    for sym in sell_forced:
        if sym not in covered:
            result.insert(0, {"sell_symbol": sym, "buy_symbol": None, "reason": "Forced exit: SELL signal.", "score_improvement": 0, "sector": "Other", "type": "SELL"})
    return result


def _normalize_l1_swaps(swaps: list, score_map: dict[str, dict] | None = None) -> list[dict]:
    """Normalise L1 compact swap objects into the full swap format used downstream."""
    result = []
    for s in (swaps or []):
        sell = s.get("sell") or s.get("sell_symbol")
        buy = s.get("buy") or s.get("buy_symbol")
        row = {
            "sell_symbol": sell,
            "buy_symbol":  buy,
            "reason": str(s.get("reason") or s.get("r") or ""),
            "score_improvement": float(
                s.get("score_delta") or s.get("delta") or s.get("score_improvement") or 0
            ),
            "sector": s.get("sector", "Other"),
            "type": s.get("type", "SWAP"),
        }
        # Reason UX — deterministic context for the expanded detail panel (subject = buy
        # side when present, since that's the opportunity being evaluated; else sell side).
        _apply_score_context(row, score_map, buy or sell)
        result.append(row)
    return result


def _normalize_allocations(
    allocs: list,
    pc_map: dict[str, float] | None = None,
    score_map: dict[str, dict] | None = None,
    *, muji_v2: bool = False,
) -> list[dict]:
    """Normalise L2 allocation objects to the internal TargetAllocation schema.

    pc_map: symbol → actual weight_pct from portfolio data (authoritative source for current_weight).
    allocation_change_percent and estimated_amount are computed in Python — never trusted from AI.
    score_map: symbol → compact score dict (see _build_score_context_map), attached for Reason UX.
    """
    result = []
    for a in (allocs or []):
        sym = str(a.get("symbol") or a.get("s") or "")
        target_w = float(a.get("target_weight") or a.get("tw") or 0)
        # Use real portfolio weight if available; AI's reported current_weight is a fallback only
        current_w = (pc_map or {}).get(sym, float(a.get("current_weight") or a.get("w") or 0))
        change_pct = round(target_w - current_w, 2)
        row = {
            "symbol": sym,
            "current_weight": round(current_w, 2),
            "target_weight": round(target_w, 2),
            "action": str(a.get("action") or a.get("sig") or "HOLD").upper(),
            "allocation_change_percent": change_pct,
            "estimated_amount": 0,  # filled in by caller once total_value is known
            "reason": str(a.get("reason") or a.get("r") or ""),
        }
        if a.get("decision_basis") in ("SECTOR_ADVISORY", "INVESTMENT_THESIS") or (
            muji_v2 and a.get("decision_basis") == "CONCENTRATION_ADVISORY"
        ):
            row["decision_basis"] = a["decision_basis"]
        _apply_score_context(row, score_map, sym)
        result.append(row)
    return [a for a in result if a["symbol"]]


def _complete_candidate_input(rows) -> bool:
    """A Phase 3 candidate must explicitly provide direction and target for every row."""
    return isinstance(rows, list) and bool(rows) and all(
        isinstance(row, dict)
        and ("symbol" in row or "s" in row)
        and ("action" in row or "sig" in row)
        and ("target_weight" in row or "tw" in row)
        for row in rows
    )


def _separate_sector_alternatives(model_result, allocations, holdings, nav, concentration, *, muji_v2=False,
                                 sell_forced=()):
    """Keep concentration-only ideas out of investment decisions and funding."""
    nav_repairs = {
        row["symbol"] for row in concentration["current_breaches"] if row["basis"] == "NAV"
    } if concentration and not concentration["current"]["estimated_symbols"] else set()
    optional = []
    raw_alternatives = model_result.get("sector_alternatives")
    if isinstance(raw_alternatives, list):
        for idea in raw_alternatives[:5]:
            if not isinstance(idea, dict):
                continue
            try:
                optional.extend(_normalize_allocations([idea], holdings))
            except (TypeError, ValueError):
                continue
    for row in allocations:
        if muji_v2 and row.get("decision_basis") in _CONCENTRATION_ADVISORY_BASES:
            row["original_recommendation"] = {key: row[key] for key in ("action", "target_weight", "reason")}
            if row["action"] in ("SELL", "REDUCE"):
                optional.append(dict(row))
            row.update(action="HOLD", target_weight=row["current_weight"], allocation_change_percent=0,
                       reason="Concentration observation recorded for review.")
            continue
        if muji_v2 and row["action"] in ("SELL", "REDUCE") and row["symbol"] not in sell_forced:
            row["thesis_evidence_status"] = "UNVERIFIED"
        if row["action"] in ("SELL", "REDUCE") and row.get("decision_basis") == "SECTOR_ADVISORY":
            # The scheduler needs the proposed sale to verify and reserve any
            # independent NAV repair. Its sector-tagged remainder cannot fund buys.
            if row["symbol"] in nav_repairs:
                continue
            optional.append(dict(row))
            row.update(action="HOLD", target_weight=row["current_weight"], allocation_change_percent=0,
                       reason="Sector concentration alternative available for review.")
    advisory_blocks = ("sector_limit_exceeded",)
    if muji_v2:
        advisory_blocks += ("position_limit_exceeded", "allocation_drift", "drift_below_threshold")
    model_result["blocked_opportunities"] = [
        item for item in model_result.get("blocked_opportunities", []) or []
        if not isinstance(item, dict) or (
            item.get("reason") not in advisory_blocks
            and (not muji_v2 or item.get("decision_basis") not in _CONCENTRATION_ADVISORY_BASES)
        )
    ]
    alternatives = {}
    for row in optional:
        symbol = row["symbol"]
        target = 0 if row["action"] == "SELL" else row["target_weight"]
        if row["action"] in ("SELL", "REDUCE") and 0 <= target < holdings.get(symbol, 0):
            alternatives[symbol] = {
                "symbol": symbol, "action": row["action"], "reason": row["reason"],
                "estimated_amount": round(nav * (holdings[symbol] - target) / 100),
            }
    return list(alternatives.values())


def _degraded_sector_policy(limits, default_cap, effective_envelope):
    if effective_envelope is not None:
        return {
            "sector_policy_mode": SECTOR_POLICY_ADVISORY,
            "resolved_sector_limits": effective_envelope.effective_sector_limits,
            "sector_limit_sources": {
                **{sector: cap.binding_source for sector, cap in effective_envelope.sector_limits.items()},
                "default": effective_envelope.global_sector_cap.binding_source,
            },
            "hard_constraints": {"max_sector_pct": effective_envelope.global_sector_cap.effective},
            "hard_policy_unavailable": True,
        }
    limits = limits or {}
    return {
        "sector_policy_mode": SECTOR_POLICY_ADVISORY,
        "resolved_sector_limits": limits,
        "sector_limit_sources": dict.fromkeys([*limits, "default"], "WORKSPACE_THRESHOLD_FALLBACK"),
        "hard_constraints": {"max_sector_pct": limits.get("default", default_cap)},
        "hard_policy_unavailable": True,
    }


def _capture_sector_policy(output, policy, mode, portfolio, candidates, nav, degraded_policy, alternatives,
                           optimizer_policy_mode=None):
    if mode == SECTOR_POLICY_ADVISORY:
        if policy is None:
            # Exposure remains measurable when hard-policy evidence is unavailable.
            policy = degraded_policy
        policy["sector_policy_mode"] = mode
        policy["sector_alternatives"] = alternatives
    if policy is not None:
        if optimizer_policy_mode is not None:
            policy["optimizer_policy_mode"] = optimizer_policy_mode
        output["active_policy"] = policy
        policy["concentration"] = freeze_concentration(portfolio, candidates, policy, nav)
        attach_target_evaluation(output)


def _snap_neutral_actions(allocations: list[dict], observer=None) -> None:
    """HOLD/WATCH are investment-conviction signals, not capital-movement instructions.
    Pin target_weight back to current_weight so no downstream consumer (Cash Impact
    column, action_summary, sector-weight projection) can show a nonzero trade for a
    row the AI didn't intend as an execution instruction. Mutates in place.
    """
    for a in allocations:
        if (a.get("action") or "").upper() in ("HOLD", "WATCH"):
            before = _alloc_basis(a)
            a["target_weight"] = a.get("current_weight", 0.0)
            a["allocation_change_percent"] = 0.0
            a["estimated_amount"] = 0
            if observer is not None and before["target_weight"] != a["target_weight"]:
                _observe(observer, a.get("symbol", ""), before, a, stage=_STAGE_NEUTRAL_SNAP,
                         source=_SRC_SYSTEM, effect=_SCALE, reason_code="NEUTRAL_SNAP",
                         reason_text="HOLD/WATCH pinned to the current weight.")


def _rebuild_watchlist_ranking(buy_symbols: list, wc: list[dict]) -> list[dict]:
    """Rebuild watchlist_ranking from BUY/ACCUMULATE targets + watchlist data."""
    wc_map = {w["symbol"]: w for w in wc}
    seen: set[str] = set()
    ranked: list[str] = []
    for sym in (buy_symbols or []):
        if sym in wc_map and sym not in seen:
            ranked.append(sym)
            seen.add(sym)
    for w in sorted(wc, key=lambda x: -(x.get("fa_score", 0) + x.get("ta_score", 0))):
        if w["symbol"] not in seen:
            ranked.append(w["symbol"])
            seen.add(w["symbol"])
    return [
        {
            "symbol": sym,
            "rank": i + 1,
            "signal": wc_map.get(sym, {}).get("signal", "WATCH"),
            "combined_score": wc_map.get(sym, {}).get("combined_score", 0),
            "sector": wc_map.get(sym, {}).get("sector", "Other"),
            "suggested_allocation_pct": 0.0,
            "reasoning": "",
        }
        for i, sym in enumerate(ranked)
    ]


# ─── Sector normalization ─────────────────────────────────────────────────────

_CANONICAL_SECTORS = frozenset({
    "Technology", "Financial", "Energy", "Healthcare",
    "Consumer", "Industrial", "Real Estate", "Utilities", "Other",
})


def normalize_sector(raw: str | None) -> str:
    """Map raw yfinance/FA sector strings to canonical frontend sector keys."""
    s = (raw or "").strip()
    if s in _CANONICAL_SECTORS:
        return s
    if "Financial" in s:
        return "Financial"
    if "Consumer" in s:
        return "Consumer"
    if "Industrial" in s:
        return "Industrial"
    return "Other"


# ─── Sector weight helpers ────────────────────────────────────────────────────

def calculate_current_sector_weights(portfolio_items: list[dict]) -> dict:
    positions = freeze_positions(portfolio_items)
    return sector_weights(evaluate_sectors(positions, current_values(positions), {}, 100, "CURRENT"))


def calculate_projected_sector_weights(portfolio_items: list[dict], swaps: list[dict]) -> dict:
    """Simulate portfolio after swaps and recompute sector weights (legacy path)."""
    holdings: dict[str, dict] = {}
    for item in portfolio_items:
        sector = normalize_sector(item.get("sector"))
        price = item.get("current_price") or item.get("avg_cost") or 0
        mv = (item.get("shares") or 0) * price
        holdings[item["symbol"]] = {"sector": sector, "value": mv}

    for swap in swaps:
        sell_sym = swap.get("sell_symbol")
        buy_sym = swap.get("buy_symbol")
        sector = normalize_sector(swap.get("sector"))
        sell_val = holdings.pop(sell_sym, {"value": 0})["value"] if sell_sym else 0
        if buy_sym and sell_val > 0:
            holdings[buy_sym] = {"sector": sector, "value": sell_val}

    sector_values: dict[str, float] = {}
    for h in holdings.values():
        sector_values[h["sector"]] = sector_values.get(h["sector"], 0.0) + h["value"]
    total = sum(sector_values.values())
    if total == 0:
        return {}
    return {
        s: {"value": round(v, 2), "weight_pct": round(v / total * 100, 1)}
        for s, v in sorted(sector_values.items(), key=lambda x: -x[1])
    }


def calculate_projected_sector_weights_from_allocations(
    portfolio_items: list[dict],
    allocations: list[dict],
    total_value: float,
) -> dict:
    positions = freeze_positions(portfolio_items)
    values = project_targets(positions, allocations, total_value)
    return sector_weights(evaluate_sectors(positions, values, {}, 100, "PROJECTED_TARGET"))


def _compute_sector_warnings(
    current: dict,
    projected: dict,
    sector_limits: dict | None,
    max_sector_pct: int,
) -> list[dict]:
    """Return per-sector status vs allocation limits for current and projected weights."""
    all_sectors = set(current) | set(projected)
    result = []
    for sector in sorted(all_sectors):
        cur_pct = current.get(sector, {}).get("weight_pct", 0.0)
        proj_pct = projected.get(sector, {}).get("weight_pct", 0.0)
        if cur_pct == 0 and proj_pct == 0:
            continue
        limits = sector_limits or {}
        limit = limits.get(sector) or limits.get("default") or max_sector_pct
        if proj_pct > limit:
            status = "EXCEEDS"
        elif proj_pct > limit * 0.8:
            status = "WARNING"
        else:
            status = "OK"
        result.append({
            "sector": sector,
            "current_pct": cur_pct,
            "projected_pct": proj_pct,
            "limit_pct": int(limit),
            "status": status,
        })
    return result


# ─── Derived swap suggestions (backward compat) ───────────────────────────────

def _derive_swap_suggestions(
    allocations: list[dict],
    sell_forced: list[str],
    locked: list[str],
) -> list[dict]:
    """Derive legacy swap_suggestions format from target_allocations."""
    suggestions: list[dict] = []
    locked_set = set(locked)

    covered_forced = {a["symbol"] for a in allocations if a.get("action") == "SELL"}
    for sym in sell_forced:
        if sym not in covered_forced:
            suggestions.append({
                "sell_symbol": sym, "buy_symbol": None,
                "reason": "Forced exit: SELL signal.", "score_improvement": 0,
                "sector": "Other", "type": "SELL",
            })

    reduces = [a for a in allocations if a.get("action") in ("SELL", "REDUCE") and a.get("allocation_change_percent", 0) < -1]
    buys    = [a for a in allocations if a.get("action") in ("BUY", "ACCUMULATE") and a.get("allocation_change_percent", 0) > 1]

    for a in allocations:
        if a.get("action") == "SELL":
            suggestions.append({
                "sell_symbol": a["symbol"], "buy_symbol": None,
                "reason": a.get("reason", ""), "score_improvement": 0,
                "sector": "Other", "type": "SELL",
            })

    buy_idx = 0
    for red in reduces:
        if red.get("action") == "SELL":
            continue
        buy = buys[buy_idx] if buy_idx < len(buys) else None
        if buy_idx < len(buys):
            buy_idx += 1
        suggestions.append({
            "sell_symbol": red["symbol"],
            "buy_symbol": buy["symbol"] if buy else None,
            "reason": red.get("reason", "") + (" → " + buy.get("reason", "") if buy else ""),
            "score_improvement": round(abs(red.get("allocation_change_percent", 0)), 1),
            "sector": "Other",
            "type": "SWAP" if buy else "REDUCE",
        })

    for i, buy in enumerate(buys):
        if i >= buy_idx:
            suggestions.append({
                "sell_symbol": None,
                "buy_symbol": buy["symbol"],
                "reason": buy.get("reason", ""),
                "score_improvement": round(buy.get("allocation_change_percent", 0), 1),
                "sector": "Other",
                "type": "SWAP",
            })

    return [s for s in suggestions if not (s.get("sell_symbol") in locked_set and s.get("type") == "SWAP")]


# ─── Consensus Engine ─────────────────────────────────────────────────────────

_CONSENSUS_LEGACY_AGREES: dict[str, bool] = {
    "STRONG_CONSENSUS":        True,
    "REFINED_CONSENSUS":       True,
    "PARTIAL_CONSENSUS":       True,
    "WEAK_CONSENSUS":          False,
    "RISK_CONFLICT":           True,
    "STRATEGIC_CONFLICT":      False,
    "NO_ACTION_CONSENSUS":     True,
    "NO_REBALANCE_CONSENSUS":  True,  # stabilization-layer injected state
}


def _consensus_engine(l1: dict, l2: dict, l3: dict, *, sector_advisory: bool = False, muji_v2: bool = False,
                      sell_forced=()) -> dict:
    """Classify optimizer output into one of 7 consensus types with alignment scoring."""

    # ── L2 inputs ─────────────────────────────────────────────────────────────
    agrees            = bool(l2.get("agrees_with_layer1", True))
    disagreements     = list(l2.get("disagreements", []) or [])
    advisory_comments = []
    if sector_advisory:
        actionable = []
        for item in disagreements:
            issue = item.get("issue") if isinstance(item, dict) else item
            if not isinstance(issue, str) or not issue.strip():
                continue
            if isinstance(item, dict) and item.get("basis") in ("ACTION", "SIZING", "INVESTMENT_THESIS", "HARD_POLICY"):
                actionable.append(issue)
            else:
                advisory_comments.append(issue)
        disagreements = actionable
        if l2.get("strategist_parse_failed"):
            disagreements.insert(0, "L1_PARSE_FAILURE: Strategist output could not be parsed.")
        if l2.get("error"):
            disagreements.insert(0, "L2_PARSE_FAILURE: Challenger output could not be parsed.")
    xai_status        = l2.get("status", "REBALANCE")
    xai_score         = int(l2.get("rebalance_opportunity_score") or 50)
    no_action_reason  = l2.get("no_action_reason")
    no_action_summary = l2.get("no_action_summary")
    l2_allocs         = list(l2.get("target_allocations", []) or [])
    if muji_v2:
        l2_allocs = [a for a in l2_allocs if a.get("decision_basis") not in _CONCENTRATION_ADVISORY_BASES
                     and a.get("thesis_evidence_status") != "UNVERIFIED"]

    # ── L3 inputs ─────────────────────────────────────────────────────────────
    # Preserve all flags in layer3_result; only investment evidence is scored.
    risk_flags   = investment_risk_flags(list(l3.get("risk_flags", []) or []))
    safer_choice = l3.get("safer_choice", "layer1")
    final_risk   = l3.get("final_risk_level", "medium")
    if final_risk not in ("low", "medium", "high"):
        final_risk = "high"
    critical_flags = [f for f in risk_flags if f.get("severity", "").upper() == "CRITICAL"]
    high_flags     = [f for f in risk_flags if f.get("severity", "").upper() in ("HIGH", "CRITICAL")]

    # ── Buy / sell overlap (L1 vs L2) ────────────────────────────────────────
    l1_buys  = set(l1.get("top_buys", []) or [])
    l1_swaps = list(l1.get("swap_suggestions", []) or [])
    l1_sells = {s["sell_symbol"] for s in l1_swaps if s.get("sell_symbol")}
    if muji_v2:
        l1_sells.intersection_update(sell_forced)

    l2_buy_syms  = {a["symbol"] for a in l2_allocs if a.get("action") in ("BUY", "ACCUMULATE")}
    l2_sell_syms = {a["symbol"] for a in l2_allocs if a.get("action") in ("SELL", "REDUCE")}
    if sector_advisory:
        l2_symbols = {a["symbol"] for a in l2_allocs}
        action_conflict = (l1_buys & (l2_symbols - l2_buy_syms)) or (l1_sells & (l2_symbols - l2_sell_syms))
        agrees = not (disagreements or action_conflict)

    buy_union    = l1_buys | l2_buy_syms
    sell_union   = l1_sells | l2_sell_syms
    buy_overlap  = len(l1_buys & l2_buy_syms)  / len(buy_union)  if buy_union  else 1.0
    sell_overlap = len(l1_sells & l2_sell_syms) / len(sell_union) if sell_union else 1.0

    # ── Alignment scores (0–100) ──────────────────────────────────────────────
    base             = 80 if agrees else 30
    disagree_penalty = min(35, len(disagreements) * 12)
    overlap_bonus    = round((buy_overlap * 0.6 + sell_overlap * 0.4) * 20 - 10)  # –10 … +10
    strategist_alignment_score = int(max(5, min(95, base - disagree_penalty + overlap_bonus)))

    # When L1 parsing failed entirely, strategist alignment is unknowable — hard-cap
    # it so the consensus type reflects the degraded signal quality.
    l1_parse_failure = any("L1_PARSE_FAILURE" in (d or "") for d in disagreements)
    if l1_parse_failure or l1.get("error"):
        strategist_alignment_score = min(strategist_alignment_score, 28)

    if not risk_flags:
        risk_alignment_score = 92
    elif critical_flags:
        risk_alignment_score = 12
    elif high_flags:
        risk_alignment_score = max(30, 55 - len(high_flags) * 8)
    else:
        medium_flags = [f for f in risk_flags if f.get("severity", "").upper() == "MEDIUM"]
        risk_alignment_score = max(50, 80 - len(medium_flags) * 8)

    consensus_strength_score = round(strategist_alignment_score * 0.65 + risk_alignment_score * 0.35)

    # ── Consensus type classification ─────────────────────────────────────────
    is_no_action = (
        xai_status == "NO_ACTION"
        and xai_score < 40
        and not critical_flags
        and not (final_risk == "high" and high_flags)
    )

    if is_no_action:
        consensus_type     = "NO_ACTION_CONSENSUS"
        confidence         = "high" if xai_score < 20 else "medium"
        recommended        = "no_action"
        consensus_decision = "NO_ACTION"

    elif critical_flags or (final_risk == "high" and len(high_flags) >= 2):
        consensus_type     = "RISK_CONFLICT"
        confidence         = "low"
        recommended        = "neither"
        consensus_decision = "REVIEW"

    elif not agrees and strategist_alignment_score < 40:
        consensus_type     = "STRATEGIC_CONFLICT"
        confidence         = "low"
        recommended        = "layer2" if safer_choice == "layer2" else "neither"
        consensus_decision = "REBALANCE"

    elif final_risk == "high" and high_flags:
        consensus_type     = "RISK_CONFLICT"
        confidence         = "medium" if agrees else "low"
        recommended        = "layer1" if agrees and safer_choice != "layer2" else "layer2"
        consensus_decision = "REBALANCE"

    elif strategist_alignment_score >= 70 and risk_alignment_score >= 65:
        consensus_type     = "STRONG_CONSENSUS"
        confidence         = "high"
        recommended        = "layer1"
        consensus_decision = "REBALANCE"

    elif agrees and strategist_alignment_score >= 50:
        consensus_type     = "REFINED_CONSENSUS"
        confidence         = "medium"
        recommended        = "layer2"
        consensus_decision = "REBALANCE"

    elif strategist_alignment_score >= 35:
        consensus_type     = "PARTIAL_CONSENSUS"
        confidence         = "medium"
        recommended        = "layer2" if safer_choice == "layer2" else "layer1"
        consensus_decision = "REBALANCE"

    else:
        consensus_type     = "WEAK_CONSENSUS"
        confidence         = "low"
        recommended        = safer_choice if safer_choice in ("layer1", "layer2") else "neither"
        consensus_decision = "REBALANCE"

    # ── Refinement summary (explainability) ───────────────────────────────────
    if consensus_type in ("NO_ACTION_CONSENSUS", "NO_REBALANCE_CONSENSUS"):
        refinement_summary = (
            no_action_summary
            or ("The committee found insufficient investment rationale for rebalancing."
                if sector_advisory else
                "All layers independently concluded the portfolio is well-balanced with insufficient edge for rebalancing.")
        )
    elif consensus_type == "STRONG_CONSENSUS":
        refinement_summary = (
            "The layers agree on the investment decision. Sector exposure is reviewed separately."
            if sector_advisory else "All layers agree on a clear rebalancing path with strong conviction and acceptable risk."
        )
    elif consensus_type == "REFINED_CONSENSUS":
        if disagreements:
            d_text = "; ".join(disagreements[:2])
            refinement_summary = f"Challenger agrees with the Strategist's core thesis but refines: {d_text}"
        else:
            refinement_summary = "Challenger confirms the Strategist's allocation direction with expanded positioning detail."
    elif consensus_type == "PARTIAL_CONSENSUS":
        n = len(disagreements)
        refinement_summary = (
            f"Challenger partially validates the Strategist's proposal "
            f"with {n} material difference{'s' if n != 1 else ''}."
        )
    elif consensus_type == "RISK_CONFLICT":
        if critical_flags:
            syms = ", ".join(f.get("symbol", "?") for f in critical_flags[:3])
            refinement_summary = (
                f"Risk Auditor identified CRITICAL investment or constraint concerns in {syms} — "
                "review the evidence before deciding whether to execute."
            )
        else:
            syms = ", ".join(f.get("symbol", "?") for f in high_flags[:3])
            refinement_summary = (
                f"Risk Auditor flagged high-severity risks in {syms} "
                "despite strategic alignment between layers."
            )
    elif consensus_type == "STRATEGIC_CONFLICT":
        refinement_summary = (
            "Challenger fundamentally rejects the Strategist's proposed allocation direction — "
            "review both plans manually before acting."
        )
    else:  # WEAK_CONSENSUS
        refinement_summary = (
            "Low confidence across layers — recommendations are inconsistent. "
            "Consider re-running after refreshing analysis data."
        )

    # ── Recommended action text ───────────────────────────────────────────────
    parts: list[str] = []
    if consensus_type in ("NO_ACTION_CONSENSUS", "NO_REBALANCE_CONSENSUS"):
        parts.append("No rebalancing action recommended at this time.")
        if no_action_summary:
            parts.append(no_action_summary)
        elif no_action_reason:
            parts.append(f"Reason: {no_action_reason.replace('_', ' ').lower()}.")
        if high_flags:
            syms = ", ".join(f.get("symbol", "?") for f in high_flags[:3])
            parts.append(f"Continue monitoring: {syms}.")
    elif consensus_type == "STRONG_CONSENSUS":
        parts.append("Follow Strategist allocation plan — high conviction across all layers.")
    elif consensus_type == "REFINED_CONSENSUS":
        parts.append("Follow Challenger's refined allocation plan — improves on Strategist's core direction.")
    elif consensus_type == "PARTIAL_CONSENSUS":
        if recommended == "layer2":
            parts.append("Consider Challenger's allocation — it addresses key gaps in the Strategist's plan.")
        else:
            parts.append("Follow Strategist plan with caution — Challenger has material reservations.")
    elif consensus_type == "RISK_CONFLICT":
        parts.append("Address Risk Auditor's flags before executing any rebalancing.")
        if high_flags:
            syms = ", ".join(f.get("symbol", "?") for f in high_flags[:3])
            parts.append(f"High-risk positions: {syms}.")
    elif consensus_type == "STRATEGIC_CONFLICT":
        parts.append("Significant strategic disagreement — review both Strategist and Challenger plans manually.")
        if disagreements:
            parts.append(f"Key conflict: {disagreements[0]}")
    else:  # WEAK_CONSENSUS
        parts.append("Low conviction — neither proposal is strongly supported. Review manually.")

    if l3.get("auditor_notes"):
        parts.append(l3["auditor_notes"])

    return {
        # New fields
        "consensus_type":             consensus_type,
        "consensus_strength_score":   consensus_strength_score,
        "strategist_alignment_score": strategist_alignment_score,
        "risk_alignment_score":       risk_alignment_score,
        "disagreement_reasons":       disagreements,
        **({"challenger_agrees": agrees, "unscored_challenger_comments": advisory_comments} if sector_advisory else {}),
        "refinement_summary":         refinement_summary,
        # Legacy fields (backward compat)
        "agrees":             _CONSENSUS_LEGACY_AGREES.get(consensus_type, agrees),
        "consensus_decision": consensus_decision,
        "confidence":         confidence,
        "recommended":        recommended,
        "final_risk_level":   final_risk,
        "risk_flag_count":    len(risk_flags),
        "recommended_action": " ".join(parts),
    }


_CONCENTRATION_ADVISORY_BASES = ("SECTOR_ADVISORY", "CONCENTRATION_ADVISORY")
_MUJI_THESIS_GUIDANCE = (
    "Position NAV concentration, sector concentration and allocation drift are advisory diagnostics. "
    "They cannot by themselves justify or veto a trade, change its score, or rule out HOLD or NO_ACTION. "
    "Use available market, downside, valuation, portfolio and investor-goal evidence to justify "
    "each BUY, ACCUMULATE, REDUCE or SELL. A concentrated winner can remain a HOLD."
)


# ─── Prompt builders ──────────────────────────────────────────────────────────

def _layer1_prompt(
    c_pc: list[dict],
    c_wc: list[dict],
    sell_forced: list[str],
    swap_eligible: list[str],
    max_sector_pct: int = 40,
    sector_limits: dict | None = None,
    max_stocks: int = 12,
    current_count: int = 0,
    persona_context: dict | None = None,
    regime_context: dict | None = None,
    policy_context: dict | None = None,
    effective_envelope: "_EffectiveEnvelope | None" = None,
    t1_breach_note: str = "",
    execution_context: dict | None = None,
    intent_block: str = "",
    sector_advisory: bool = False,
    muji_v2: bool = False,
    goal_decision_input: dict | None = None,
) -> str:
    # Phase 3B.5: use resolved per-sector limits when available; fall back to raw sector_limits
    if effective_envelope is not None:
        sl = dict(effective_envelope.effective_sector_limits)
        sl.setdefault("default", effective_envelope.global_sector_cap.effective)
    else:
        sl = sector_limits or {"default": max_sector_pct}

    # Policy block (3B.4) — overrides / supplements regime + strategy blocks
    policy_block = ""
    if policy_context and policy_context.get("prompt_block"):
        policy_block = policy_context["prompt_block"] + "\n"

    regime_block = ""
    if regime_context and not policy_context:
        # Only inject standalone regime block when no unified policy block is present
        from services.analytics.regime_detector import build_regime_prompt_block
        regime_block = build_regime_prompt_block(regime_context, concentration_advisory=muji_v2) + "\n"

    strategy_block = ""
    if persona_context:
        p_label      = persona_context.get("persona_label", "Balanced").upper()
        p_dna        = persona_context.get("dna_display", "")
        p_drift_sev  = persona_context.get("drift_severity", "LOW")
        p_drift_sc   = persona_context.get("drift_score", 0)
        p_dominant   = persona_context.get("dominant_factor_label", "")
        p_top        = persona_context.get("top_target_factor", "")
        p_priority   = persona_context.get("priority_order", "")
        p_turn_lbl   = persona_context.get("turnover_label", "MODERATE")
        p_urgency    = persona_context.get("rebalance_urgency", "MODERATE")
        p_misaligned = persona_context.get("misaligned_display", "none")
        p_turn       = persona_context.get("turnover_tolerance", 0.5)

        low_turn_note  = "PREFER incremental DCA; avoid large single-step replacements." if p_turn < 0.30 else ""
        high_turn_note = "High turnover is ACCEPTABLE — act decisively on factor misalignment." if p_turn > 0.70 else ""

        strategy_block = f"""[STRATEGY CONTEXT — MANDATORY]
Target Persona: {p_label}
Current Portfolio DNA: {p_dna}
Dominant Style: {p_dominant} → target dominant is {p_top}
Style Drift: {p_drift_sev} ({p_drift_sc}/100) | {"Diagnostic context" if muji_v2 else f"Rebalance Urgency: {p_urgency}"}
Factor Priority: {p_priority}
Most Misaligned: {p_misaligned}
Turnover Tolerance: {p_turn_lbl} ({int(p_turn * 100)}%)

[STRATEGY MANDATE]
{"Use factor alignment as one input to the investment thesis." if muji_v2 else f"All swap proposals MUST increase {p_top} factor alignment."}
{low_turn_note}{high_turn_note}
Stocks selected for BUY/ACCUMULATE must support the {p_label} factor profile.
Stocks proposed for REDUCE/SELL must {"have an independent investment or risk rationale" if muji_v2 else f"be misaligned with {p_label} or overweight"}.

"""

    # Build a note when the policy envelope already shows hard-constraint violations.
    # This prevents L1 from freezing when historical positions breach the limits —
    # it must actively propose REDUCE actions to resolve the breach step-by-step.
    violation_note = ""
    if policy_context and not muji_v2:
        hc = policy_context.get("hard_constraints", {})
        max_pos = float(hc.get("max_single_position_pct", 22.0))
        policy_violations = policy_context.get("violations", [])
        if policy_violations:
            violation_note = (
                f"\nPOLICY VIOLATIONS ACTIVE: {', '.join(policy_violations)}\n"
                f"Max single position is {max_pos:.0f}%. Every position currently over this limit "
                "MUST be targeted for REDUCE in your swaps (sell=SYM, buy=null). "
                "Step-by-step trimming is preferred over full exits. "
                "Do NOT output no_action — a REDUCE is always the right response to a breach.\n"
            )
        else:
            # Even without flagged violations, remind about the position cap
            violation_note = (
                f"\nPolicy max single position: {max_pos:.0f}%. "
                "If any holding currently exceeds this, propose an incremental REDUCE swap.\n"
            )

    execution_block = ""
    if execution_context:
        from services.optimizer.execution_penalty import build_execution_prompt_block
        execution_block = build_execution_prompt_block(execution_context)

    timing_block = """[TIMING INTELLIGENCE — Phase 4C.6H]
Each symbol carries ts= (timing score 0-100) and pr= (execution priority: HIGH/MEDIUM/LOW/DEFER).
Timing Score = entry quality: trend + momentum + relative strength + volume.
  ts≥80 / HIGH  : strong entry → increase conviction for BUY/ACCUMULATE ranking
  ts 60-79 / MED: acceptable  → proceed normally
  ts 40-59 / LOW : weak entry → reduce urgency; rank watchlist candidates lower
  ts<40 / DEFER  : poor entry → note in sector_flags; still eligible as lower-ranked top_buy
Timing informs urgency — it does not block. A DEFER symbol with strong fundamentals is still top_buys material at lower rank.

"""

    strategist_guidance = f"""{_MUJI_THESIS_GUIDANCE}
Prefer high-conviction changes after transaction costs. Evaluate buying opportunities,
independently justified exits or reductions, and holding the current portfolio.
Return priority="no_action" when no investment case warrants a change.
Put concentration observations in sector_flags and keep them out of swaps and top_buys.""" if muji_v2 else """- MINIMUM DRIFT: only propose allocation changes ≥ 3%. Smaller shifts create noise with no economic value.
- HIGH CONVICTION: only propose swaps with strong, defensible signal quality improvement.
- TURNOVER PENALTY: fewer trades are better. Each trade incurs real friction cost (~0.15% per 1% NAV).
- PREFER holding well-positioned assets over constant micro-rotation.

EVALUATE ALL FIVE — but only act if improvement is material:
1. Flag sector exposure above advisory thresholds on invested equity excluding cash. Keep it separate from swaps, buys and the investment decision.
2. Watchlist opportunities: BUY/ACCUMULATE candidate with clear edge over current holdings? → rank in top_buys
3. Overweight positions: swap-eligible stock >25%? → consider REDUCE, but only if drift ≥ 3%
4. Low-score holdings: weak fa+ta vs watchlist with 10+ score advantage? → consider swap
5. Policy violations: active hard single-position CONCENTRATION_BREACH? → propose remediation (mandatory)

priority="no_action" when ALL of the following are true:
- No hard position limit breach. A sector warning alone permits no_action.
- No watchlist candidate has a clearly superior score (10+ advantage) over current holdings
- All current positions are within 3% of their ideal weight
- No urgent regime or policy signal"""

    summary_guidance = """summary: exactly 2 sentences. Explain the portfolio outlook and the evidence supporting action or HOLD.
"r" = one independent investment reason for each swap, under 12 words.""" if muji_v2 else """summary: exactly 2 sentences, written the way a strategist briefs a client — natural
  investment language, not a status log. Sentence 1: what you reviewed and the
  overall read (e.g. "Sector weights are balanced and no position has drifted far
  from target." / "The portfolio still carries a sound risk posture heading into
  this cycle."). Sentence 2: name what, if anything, cleared today's conviction bar
  and why the rest did not (e.g. "KBANK's concentration has crossed a line worth
  trimming, but ADVANC and CENTEL don't yet show enough edge to displace what's
  already held."). Vary phrasing and sentence structure run to run — do not reuse
  the same template every time. Never restate the full allocation plan, that is
  Layer 2's job. Avoid mechanical phrases like "system", "threshold triggered", or
  "no action detected" — write as an analyst, not a machine.
"r" = one reason for the swap, under 12 words (e.g. "Technology at 45% > 30% limit")."""

    swap_basis = ',"decision_basis":"INVESTMENT_THESIS"' if muji_v2 else ""
    return f"""{policy_block}{regime_block}{strategy_block}{t1_breach_note}{execution_block}{timing_block}{intent_block}{_goal_decision_block(goal_decision_input) if muji_v2 else ''}You are a STRATEGIST. Output swap targets in JSON only.
No explanation. No prose. Only valid JSON output.
{violation_note}
Portfolio: {json.dumps(c_pc)}
Watchlist: {json.dumps(c_wc)}
{"" if sector_advisory else f"Sector limits: {json.dumps(sl)}"}
Swap eligible: {swap_eligible or "none"}
Forced sells: {sell_forced or "none"}

STOCK COUNT: {current_count}/{max_stocks} max unique stocks after rebalancing.
SIGNALS: BUY=add aggressively, ACCUMULATE=add gradually, HOLD=keep, WATCH=monitor, REDUCE=trim, SELL=exit

STABILIZATION MANDATE — quality over quantity. Every proposed change must clear a high bar:
{strategist_guidance}

Output schema — nothing else. Max 550 tokens.
swaps: max 3 (sell or buy may be null for one-sided REDUCE or ACCUMULATE from cash)
top_buys: max 5 watchlist symbols ranked by signal quality
sector_flags: max 3 short strings
priority: one word only
{summary_guidance}

If running low on output budget, prioritize in this order: (1) swaps, (2) priority,
(3) summary, (4) top_buys, (5) sector_flags.

{{"swaps":[{{"sell":"SYM|null","buy":"SYM|null","score_delta":0.0,"sector":"S","type":"SELL|SWAP|REDUCE","r":"<12 words"{swap_basis}}}],"top_buys":["S"],"sector_flags":["S 45%>30%"],"priority":"growth","summary":"<2 natural-language sentences>"}}"""


def _layer2_prompt(
    pc: list[dict],
    wc: list[dict],
    l1: dict,
    role: str = "",
    cash_balance: float = 0.0,
    total_value: float = 0.0,
    persona_context: dict | None = None,
    regime_context: dict | None = None,
    policy_context: dict | None = None,
    t1_breach_note: str = "",
    execution_context: dict | None = None,
    intent_block: str = "",
    sector_advisory: bool = False,
    muji_v2: bool = False,
    goal_decision_input: dict | None = None,
) -> str:
    role_line = f"Your role: {role}\n\n" if role else ""

    policy_block = ""
    if policy_context and policy_context.get("prompt_block"):
        policy_block = policy_context["prompt_block"] + "\n"

    regime_block = ""
    if regime_context and not policy_context:
        from services.analytics.regime_detector import build_regime_prompt_block
        regime_block = build_regime_prompt_block(regime_context, concentration_advisory=muji_v2) + "\n"
    l1_swaps    = l1.get("swap_suggestions", l1.get("swaps", []))
    l1_top_buys = l1.get("top_buys", [])
    l1_flags    = [] if sector_advisory else l1.get("sector_flags", [])
    l1_priority = l1.get("priority", "balanced")

    strategy_block = ""
    if persona_context:
        p_label     = persona_context.get("persona_label", "Balanced")
        p_dna       = persona_context.get("dna_display", "")
        p_drift_sev = persona_context.get("drift_severity", "LOW")
        p_drift_sc  = persona_context.get("drift_score", 0)
        p_priority  = persona_context.get("priority_order", "")
        p_turn_lbl  = persona_context.get("turnover_label", "MODERATE")
        p_urgency   = persona_context.get("rebalance_urgency", "MODERATE")
        p_desc      = persona_context.get("persona_description", "")
        p_turn      = persona_context.get("turnover_tolerance", 0.5)
        p_max_cash  = persona_context.get("max_cash_preference", 0.05)
        p_vol       = persona_context.get("volatility_tolerance", 0.5)

        strategy_block = f"""[STRATEGY CONTEXT — MANDATORY INVESTMENT POLICY]
Target Persona: {p_label.upper()} — {p_desc}
Current Portfolio DNA: {p_dna}
Style Drift: {p_drift_sev} ({p_drift_sc}/100) | {"Diagnostic context" if muji_v2 else f"Urgency: {p_urgency}"}
Factor Priority: {p_priority}
Turnover Tolerance: {p_turn_lbl} ({int(p_turn * 100)}%)
Max Cash Preference: {int(p_max_cash * 100)}% of portfolio
Volatility Tolerance: {int(p_vol * 100)}% (0%=very defensive, 100%=aggressive)

[ALLOCATION POLICY]
Your allocation plan MUST align with the {p_label.upper()} investment philosophy.
Factor weighting, position sizing, and stock selection must all reflect this persona.
{"Prefer gradual position changes; high turnover is discouraged for this persona." if p_turn < 0.30 else ""}
{"Active rebalancing is consistent with this persona; larger position changes are appropriate." if p_turn > 0.70 else ""}

"""

    execution_block = ""
    if execution_context:
        from services.optimizer.execution_penalty import build_execution_prompt_block
        execution_block = build_execution_prompt_block(execution_context)

    timing_disagreement = (
        "Record material timing disagreements with basis=INVESTMENT_THESIS and include the symbol and timing evidence."
        if sector_advisory else
        'Add to disagreements[]: "TIMING_CONCERN: [SYM] poor entry timing (ts=[N], priority=DEFER) — waiting 2-4 weeks may improve entry."'
    )
    advisory_basis = "CONCENTRATION_ADVISORY" if muji_v2 else "SECTOR_ADVISORY"
    disagreement_example = (
        f'{{"basis":"ACTION|SIZING|INVESTMENT_THESIS|HARD_POLICY|{advisory_basis}","issue":"<20 words>"}}'
        if sector_advisory else '"<20 words each>"'
    )
    timing_challenge_block = f"""[TIMING AWARENESS — CHALLENGER]
Each symbol carries timing_score and execution_priority.
Challenge BUY/ACCUMULATE recommendations where execution_priority=DEFER or timing_score<40.
{timing_disagreement}
Timing does not invalidate a fundamentally attractive stock — document the concern, do not block.

"""

    # TEMP DEBUG — cash data-flow trace (2026-07-03), remove after cash_pct bug confirmed
    _invested_value = sum(i.get("market_value", 0) for i in pc)
    logger.info(
        "[CASH_TRACE stage=3_L2_PROMPT] portfolio_value=%.2f invested_value=%.2f "
        "available_cash=%.2f cash_pct=%.4f%% policy_context_present=%s",
        total_value, _invested_value, cash_balance,
        (cash_balance / total_value * 100) if total_value else 0.0,
        bool(policy_context),
    )

    challenge_guidance = f"""{_MUJI_THESIS_GUIDANCE}
Challenge the Strategist with an independently supported alternative or confirm the proposal.
Compare the expected benefit and trading costs against keeping the existing portfolio.
Use NO_ACTION when the available evidence supports keeping the portfolio.
Keep concentration observations separate from actionable allocations and opportunity scoring.""" if muji_v2 else """BEFORE proposing any rebalancing, apply this 3-step discipline:
1. DRIFT TEST: Is any allocation change < 3%? If yes, suppress it — noise, not signal.
2. CONVICTION TEST: Does the proposed change have a clear, measurable benefit (10+ score advantage or hard-policy breach repair)?
3. COST TEST: Will the expected portfolio improvement exceed the ~0.15% trading cost per 1% NAV traded?

status="NO_ACTION" with rebalance_opportunity_score below 25 is STRONGLY ENCOURAGED when:
- All positions are within 3% of their natural weight (drift tolerance band)
- No watchlist candidate has a compelling 10+ score advantage over existing holdings
- No hard-policy violations exist. A sector warning can coexist with NO_ACTION.
- Market conditions are uncertain or data is insufficient to justify rebalancing

PREFER large, high-conviction changes over many small adjustments.
A portfolio with 2 targeted swaps beats one with 6 micro-adjustments."""

    allocation_basis = ',"decision_basis":"INVESTMENT_THESIS|CONCENTRATION_ADVISORY"' if muji_v2 else ""
    return f"""You are an independent portfolio reviewer.
{policy_block}{regime_block}{strategy_block}{t1_breach_note}{execution_block}{timing_challenge_block}{intent_block}{_goal_decision_block(goal_decision_input) if muji_v2 else ''}{role_line}The Strategist (Layer 1) proposed:
- Priority: {l1_priority}
- Swaps: {json.dumps(l1_swaps, indent=2)}
- Top watchlist picks: {l1_top_buys}
{"" if sector_advisory else f"- Sector observations: {l1_flags}"}

Full portfolio data for your analysis:
{json.dumps(pc, indent=2)}

Full watchlist for your analysis:
{json.dumps(wc, indent=2)}

Total portfolio value: {total_value:.0f}, Cash balance: {cash_balance:.0f}
Thai stocks end in .BK.

STABILIZATION PHILOSOPHY:
Unnecessary portfolio churn destroys value through transaction costs, tax drag, and operational complexity.

{challenge_guidance}

score guide: 0-25=no action needed, 26-45=minor optimization, 46-70=moderate opportunity, 71-100=strong opportunity.
no_action_reason enum (use null if status=REBALANCE):
  WELL_BALANCED | LOW_CONFIDENCE | HIGH_DISAGREEMENT | CONSTRAINT_BLOCKED | MARKET_UNCERTAINTY | INSUFFICIENT_EDGE

Build a complete capital allocation plan. Challenge or confirm the Strategist's swaps.

OUTPUT CONTRACT — this JSON is read by software, not a person; a separate step writes the human-readable
report later. Do not spend output tokens on prose. Follow this priority order if you are running low on
output budget: (1) allocations for existing holdings and BUY/ACCUMULATE/REDUCE/SELL decisions, (2) risk/
constraint-violation notes, (3) portfolio_assessment, (4) blocked_opportunities, (5) watchlist WATCH rows,
(6) any optional explanation. Never drop an allocation row to make room for longer text.

ALLOCATIONS ARRAY:
- Include every existing portfolio holding exactly once, with its action (ACCUMULATE|BUY|HOLD|REDUCE|SELL|WATCH).
- Include a watchlist symbol only if you assign it BUY or ACCUMULATE, OR it is one of your top few WATCH-worthy
  candidates with a specific reason (max 5 WATCH rows total). Do not add a row for every watchlist symbol —
  omit ones with no actionable signal completely.
- Weights are FLAT PERCENTAGES (10.0 = 10% of portfolio), not monetary amounts.
- Omit current weight — the backend already has it; send only the target.
- "r" = one reason, under 20 words. State each idea once — do not repeat it in "r", disagreements, and
  portfolio_assessment.

If a watchlist symbol with BUY/ACCUMULATE signal was evaluated but rejected (cash constraint,
portfolio count cap), list it in blocked_opportunities — but only the highest-priority rejections, max 5.
Keep each "reason" under 10 words (e.g. "insufficient_cash").
Sector thresholds alone cannot block BUY/ACCUMULATE or justify a SELL/REDUCE.
Put optional sector-only reductions in sector_alternatives, using the same allocation row format.
Keep the actionable allocation HOLD unless independently justified. Mark thesis-driven SELL/REDUCE
with decision_basis=INVESTMENT_THESIS. Judge agreement and opportunity only on actionable decisions.
 If the complete allocation forms a coherent optional strategy, label strategy_family as
 RAISE_CASH, DEFENSIVE_ROTATION or GROWTH_ROTATION; otherwise use null. Evidence refs may
 cite only observed fields: symbol:SYM:signal, symbol:SYM:fa_score, symbol:SYM:ta_score,
 symbol:SYM:pe_ratio, symbol:SYM:roe, symbol:SYM:timing_score, regime:regime,
 goal:ID:target_date, goal:ID:funding_gap or goal:ID:priority. A cited fact does not
 by itself prove the strategy is superior. Never cite a concentration threshold as support.

disagreements[]: only material disagreements with Layer 1 (wrong signal, missed breach, constraint conflict).
{f"Use {advisory_basis} for concentration-only comments. Other bases must identify the actionable disagreement." if sector_advisory else "Skip informational observations."}
Max 5 entries, each under 20 words.

portfolio_assessment: 2-3 sentences max — a decision summary, not an essay.

Return JSON only. No markdown fences, no prose outside the JSON.

{{
  "status": "REBALANCE|NO_ACTION",
  "rebalance_opportunity_score": 50,
  "no_action_reason": "WELL_BALANCED|LOW_CONFIDENCE|HIGH_DISAGREEMENT|CONSTRAINT_BLOCKED|MARKET_UNCERTAINTY|INSUFFICIENT_EDGE|null",
  "no_action_summary": "<20 words, null if REBALANCE",
  "blocked_opportunities": [{{"symbol":"X","signal":"BUY","reason":"insufficient_cash|portfolio_count_cap"}}],
  "agrees_with_layer1": true,
  "disagreements": [{disagreement_example}],
  "portfolio_assessment": "2-3 sentences",
  "cash_balance_target": 0.0,
{('  "strategy_family": "RAISE_CASH|DEFENSIVE_ROTATION|GROWTH_ROTATION|null", "observed_evidence_refs": ["symbol:SYM:signal"],\n') if muji_v2 else ''}  "allocations": [
    {{"s":"X","tw":0.0,"sig":"BUY|ACCUMULATE|HOLD|REDUCE|SELL|WATCH","r":"<20 words"{allocation_basis}}}
  ]
}}"""


_CANDIDATE_REVIEW_SCHEMA_LINE = (
    '  "candidate_reviews": [{"candidate_id":"exact candidate_id","supporting_refs":["exact cited_refs key"],'
    '"opposing_refs":["exact relevant_evidence key"],"material_conflicts":["unresolved material conflict"],'
    '"assessment":"<30 words"}],\n'
)

# Opt-in Auditor output budget. Each of up to four candidate reviews (HOLD,
# primary plan, two additional plans) can carry ~10-20 exact refs plus a short
# assessment (~250-350 tokens each) on top of up to 8 risk_flags (~500 tokens);
# 2048 tokens risks truncating the JSON and failing the whole review closed.
_LAYER3_SELECTION_MAX_TOKENS = 4096


def _candidate_review_block(envelope: dict) -> str:
    """Opt-in Auditor instructions plus the compact frozen candidate evidence view."""
    view = strategic_candidates.candidate_review_view(envelope)
    return (
        "[STRATEGIC CANDIDATE REVIEW — REQUIRED FOR THIS RUN]\n"
        "Review every candidate below, including hold-current. Return candidate_reviews with exactly\n"
        "one row per candidate_id; omit none and repeat none. A missing or incomplete review set\n"
        "invalidates the whole review.\n"
        "- supporting_refs: only keys from that candidate's cited_refs that genuinely support it.\n"
        "- opposing_refs: keys from relevant_evidence that contradict or weaken that candidate.\n"
        "  Report material contradictory facts, not only supporting ones.\n"
        "- material_conflicts: short descriptions of unresolved material conflicts; [] if none.\n"
        "- assessment: one sentence under 30 words. Model opinions are unscored.\n"
        "Use exact keys only. Never invent a reference or a value; missing information stays missing.\n"
        "A review is not a selection. Do not use safer_choice as a selection vote.\n"
        f"CANDIDATES_FOR_REVIEW={json.dumps(view, sort_keys=True, default=str)}\n\n"
    )


def _layer3_prompt(
    l1: dict,
    l2: dict,
    role: str = "",
    max_sector_pct: int = 40,
    persona_context: dict | None = None,
    policy_context: dict | None = None,
    effective_envelope: "_EffectiveEnvelope | None" = None,
    t1_breach_note: str = "",
    intent_block: str = "",
    execution_context: dict | None = None,
    claim_contract: dict | None = None,
    muji_v2: bool = False,
    goal_decision_input: dict | None = None,
    candidate_review_block: str = "",
) -> str:
    from services.optimizer.execution_penalty import build_execution_prompt_block
    execution_block = build_execution_prompt_block(execution_context or {})
    role_line = f"Your role: {role}\n\n" if role else ""
    # Committee opt-in only; empty fragments keep every other prompt byte-identical.
    candidate_review_schema = _CANDIDATE_REVIEW_SCHEMA_LINE if candidate_review_block else ""
    l1_swaps    = l1.get("swap_suggestions", l1.get("swaps", []))[:4]
    l1_priority = l1.get("priority", "balanced")
    l2_allocs   = l2.get("allocations", l2.get("target_allocations", []))

    # Use resolved position cap for CRITICAL threshold — eliminates hardcoded 30% magic number
    if effective_envelope is not None:
        resolved_max_pos    = effective_envelope.effective_single_position_pct
    elif policy_context:
        hc = policy_context.get("hard_constraints", {})
        resolved_max_pos    = float(hc.get("max_single_position_pct", 22.0))
    else:
        resolved_max_pos    = 30.0   # legacy: was hardcoded

    # CRITICAL threshold: any position > resolved max + 8pp buffer, or resolved position cap + 8pp
    critical_pos_threshold = min(30.0, resolved_max_pos + max(5.0, resolved_max_pos * 0.25))

    persona_note = ""
    if persona_context:
        p_label = persona_context.get("persona_label", "Balanced")
        p_turn  = persona_context.get("turnover_tolerance", 0.5)
        p_vol   = persona_context.get("volatility_tolerance", 0.5)
        persona_note = (
            f"\nPersona Policy: {p_label.upper()} "
            f"(turnover tolerance: {int(p_turn*100)}%, volatility tolerance: {int(p_vol*100)}%)\n"
            "Flag any risk that conflicts with this persona's policy constraints.\n"
        )

    policy_note = ""
    if policy_context and not muji_v2:
        hc = policy_context.get("hard_constraints", {})
        bias = policy_context.get("deployment_bias", "SELECTIVE")
        policy_note = (
            f"\nActive Policy Governance ({bias} mode — strictness: {policy_context.get('strictness_level','NORMAL')}):\n"
            f"  Cash mandate: ≥{hc.get('min_cash_pct', 5):.0f}%  "
            f"  Max position: {hc.get('max_single_position_pct', 22):.0f}%  "
            f"  Default sector cap: {hc.get('max_sector_pct', 40):g}% of invested equity, excluding cash\n"
            "Flag POLICY_VIOLATION for cash < mandate, CONCENTRATION_BREACH for position > cap,\n"
            "OVER_AGGRESSION for excessive buys in defensive mode, REGIME_MISMATCH for emergency violations.\n"
        )

    high_pos_threshold = round(resolved_max_pos * 0.85, 1)  # HIGH = 85–100% of cap

    timing_risk_block = """[TIMING RISK ASSESSMENT — Phase 4C.6H]
Flag MEDIUM severity when a new BUY or ACCUMULATE position has execution_priority=DEFER or timing_score<40.
Use: {"symbol":"X","issue":"Poor entry timing (ts=[N], priority=DEFER) for new position","severity":"MEDIUM"}
Do NOT escalate to HIGH or CRITICAL for timing alone — timing cautions, it does not block.

"""

    severity_guidance = """Report position concentration and drift as ADVISORY_CONCERN. Flag genuine instrument restrictions,
investor restrictions and evidence-quality concerns with the relevant contract evidence.
Assess independent investment risks using the evidence contract and its severity guidance.""" if muji_v2 else f"""Check for (use exact resolved severity thresholds — derived from active policy, not hardcoded):
- CRITICAL : single stock > {critical_pos_threshold:.0f}% of NAV
- HIGH     : single stock {high_pos_threshold:.0f}–{critical_pos_threshold:.0f}% OR weak fundamentals on large position
- MEDIUM   : conflicting allocation math
- LOW      : minor concentration risk, suboptimal but acceptable"""

    return f"""{t1_breach_note}{_goal_decision_block(goal_decision_input) if muji_v2 else ''}You are a portfolio risk auditor.
{execution_block}{timing_risk_block}{policy_note}{persona_note}{intent_block}{role_line}Evaluate both allocation proposals for concentration risk and soundness.

[AUTHORITATIVE POLICY CLAIM CONTRACT]
{json.dumps(claim_contract or {}, sort_keys=True)}
Sector advisories in the contract are informational and excluded from risk_flags and safer_choice.
An optional sector comment can use SECTOR_ADVISORY with its exact evidence_ref.
Every risk flag must include claim_kind. POLICY_BREACH and EXECUTION_RESTRICTION must
reference an exact evidence_ref from this contract, with the same symbol (PORTFOLIO for
portfolio-wide evidence). Missing or mismatched evidence is unscored, unsupported model output.
General portfolio policy is separate from per-instrument execution caps. An execution cap
is applicable only to proposed BUY/ACCUMULATE targets, never a universal holding limit.
EXISTING_EXPOSURE above an execution cap requires no automatic liquidation; it is unscored context.
ADVISORY_CONCERN includes the prompt-only 40% DR basket guidance; it is not a governance breach.
Use INVESTMENT_JUDGMENT for independent business, valuation, volatility or timing risk opinions
only, never assertions that a deterministic limit is breached. Model-only opinions are visible but
unscored. Investment observations require a matching independently produced evidence_ref;
the model label alone never authorizes a risk penalty. Only existing contract evidence is scoreable.
Severity thresholds below guide opinions, not proof of a policy violation. Do not invent limits.

Layer 1 (Strategist):
Priority: {l1_priority}
Proposed swaps: {json.dumps(l1_swaps, indent=2)}

Layer 2 (Challenger):
Agrees: {l2.get("agrees_with_layer1", True)}
Disagreements: {json.dumps(l2.get("disagreements", []))}
Allocations: {json.dumps(l2_allocs, indent=2)}

{severity_guidance}

{"" if muji_v2 else "Only flag positions that actually cross a threshold above — do not add a LOW-severity row for every position that\nis merely fine. "}Max 8 risk_flags, "issue" under 15 words each. "auditor_notes" is a 1-2 sentence verdict — do not
restate the risk_flags issue text there.

Every flag must have category INVESTMENT_RISK or OWNER_INTENT_REVIEW.
Use OWNER_INTENT_REVIEW only for disagreement with owner Intent. Such disagreement is
allowed: preserve it for owner review, but exclude it from final_risk_level, safer_choice
and investment/governance/quality judgments. A real investment risk in the same symbol
must be a separate INVESTMENT_RISK flag. Never disguise investment risk as Intent review.

{candidate_review_block}Return JSON only. No markdown fences.

{{
{candidate_review_schema}  "risk_flags": [{{"symbol":"...","issue":"...","severity":"LOW|MEDIUM|HIGH|CRITICAL","category":"INVESTMENT_RISK|OWNER_INTENT_REVIEW","claim_kind":"POLICY_BREACH|EXECUTION_RESTRICTION|EXISTING_EXPOSURE|ADVISORY_CONCERN|SECTOR_ADVISORY|INVESTMENT_JUDGMENT","evidence_ref":"exact contract key or null"}}],
  "safer_choice": "layer1|layer2|neither",
  "final_risk_level": "low|medium|high",
  "auditor_notes": "1-2 sentences."
}}"""


def _enforce_hard_policy(
    allocations: list[dict],
    *,
    total_value: float,
    policy_context: dict | None,
    regime_context: dict | None,
    observer=None,
    muji_v2: bool = False,
) -> None:
    """Apply the existing Goal-agnostic deterministic hard-policy sequence.

    observer: optional Advisory Integration V1 run; records each mutation.
    """
    if policy_context:
        pc_hard = policy_context.get("hard_constraints", {})
        min_cash_pct = float(pc_hard.get("min_cash_pct", 5.0))
        max_pos_pct = float(pc_hard.get("max_single_position_pct", 22.0))
        emergency = bool(policy_context.get("emergency_override", False))

        if emergency:
            for allocation in allocations:
                if allocation.get("action") in ("BUY", "ACCUMULATE"):
                    logger.info(
                        "[POLICY_EMERGENCY] freezing %s BUY→HOLD (emergency override)",
                        allocation["symbol"],
                    )
                    before = _alloc_basis(allocation)
                    allocation["action"] = "HOLD"
                    allocation["target_weight"] = allocation.get("current_weight", 0.0)
                    allocation["allocation_change_percent"] = 0.0
                    allocation["estimated_amount"] = 0
                    _observe(observer, allocation["symbol"], before, allocation, stage=_STAGE_HARD_POLICY,
                             source=_SRC_POLICY, effect=_SUPPRESS, reason_code="EMERGENCY_BUY_FREEZE",
                             reason_text="Emergency policy override freezes new buying.")

        for allocation in allocations:
            if (
                not muji_v2 and allocation.get("action") in ("BUY", "ACCUMULATE")
                and allocation.get("target_weight", 0) > max_pos_pct
            ):
                logger.info(
                    "[POLICY] capping %s target_weight %.1f→%.1f (bias=%s)",
                    allocation["symbol"], allocation["target_weight"], max_pos_pct,
                    policy_context.get("deployment_bias"),
                )
                before = _alloc_basis(allocation)
                allocation["target_weight"] = max_pos_pct
                allocation["allocation_change_percent"] = round(
                    allocation["target_weight"] - allocation["current_weight"], 2,
                )
                allocation["estimated_amount"] = round(
                    (allocation["allocation_change_percent"] / 100) * total_value,
                )
                _observe(observer, allocation["symbol"], before, allocation, stage=_STAGE_HARD_POLICY,
                         source=_SRC_POLICY, effect=_SCALE, reason_code="POSITION_CAP",
                         reason_text=f"Capped at the {max_pos_pct:.1f}% single-position limit.")

        total_target = sum(
            allocation.get("target_weight", 0)
            for allocation in allocations
            if allocation.get("action") not in ("SELL",)
        )
        cash_headroom = 100.0 - total_target
        if cash_headroom < min_cash_pct:
            deficit = min_cash_pct - cash_headroom
            buy_allocations = sorted(
                [a for a in allocations if a.get("action") in ("BUY", "ACCUMULATE")],
                key=lambda item: -item.get("target_weight", 0),
            )
            for allocation in buy_allocations:
                if deficit <= 0:
                    break
                trim = min(allocation["target_weight"], deficit)
                before = _alloc_basis(allocation)
                allocation["target_weight"] = round(allocation["target_weight"] - trim, 2)
                allocation["allocation_change_percent"] = round(
                    allocation["target_weight"] - allocation["current_weight"], 2,
                )
                allocation["estimated_amount"] = round(
                    (allocation["allocation_change_percent"] / 100) * total_value,
                )
                _observe(observer, allocation["symbol"], before, allocation, stage=_STAGE_HARD_POLICY,
                         source=_SRC_POLICY, effect=_SCALE, reason_code="CASH_FLOOR_TRIM",
                         reason_text=f"Trimmed to keep the {min_cash_pct:.0f}% minimum cash.")
                deficit -= trim
            logger.info(
                "[POLICY] enforced min_cash=%.0f%% deployment=%s",
                min_cash_pct, policy_context.get("deployment_bias"),
            )
    elif regime_context:
        from services.analytics.regime_detector import get_regime_constraints
        regime_constraints = get_regime_constraints(regime_context.get("regime", "SIDEWAYS"))
        min_cash_pct = regime_constraints["min_cash_pct"]
        max_pos_pct = regime_constraints["max_single_position_pct"]
        for allocation in allocations:
            if (
                not muji_v2 and allocation.get("action") in ("BUY", "ACCUMULATE")
                and allocation.get("target_weight", 0) > max_pos_pct
            ):
                before = _alloc_basis(allocation)
                allocation["target_weight"] = max_pos_pct
                allocation["allocation_change_percent"] = round(
                    allocation["target_weight"] - allocation["current_weight"], 2,
                )
                allocation["estimated_amount"] = round(
                    (allocation["allocation_change_percent"] / 100) * total_value,
                )
                _observe(observer, allocation["symbol"], before, allocation, stage=_STAGE_HARD_POLICY,
                         source=_SRC_POLICY, effect=_SCALE, reason_code="REGIME_POSITION_CAP",
                         reason_text=f"Capped at the {max_pos_pct:.1f}% regime position limit.")
        total_target = sum(
            allocation.get("target_weight", 0)
            for allocation in allocations
            if allocation.get("action") not in ("SELL",)
        )
        cash_headroom = 100.0 - total_target
        if cash_headroom < min_cash_pct:
            deficit = min_cash_pct - cash_headroom
            buy_allocations = sorted(
                [a for a in allocations if a.get("action") in ("BUY", "ACCUMULATE")],
                key=lambda item: -item.get("target_weight", 0),
            )
            for allocation in buy_allocations:
                if deficit <= 0:
                    break
                trim = min(allocation["target_weight"], deficit)
                before = _alloc_basis(allocation)
                allocation["target_weight"] = round(allocation["target_weight"] - trim, 2)
                allocation["allocation_change_percent"] = round(
                    allocation["target_weight"] - allocation["current_weight"], 2,
                )
                allocation["estimated_amount"] = round(
                    (allocation["allocation_change_percent"] / 100) * total_value,
                )
                _observe(observer, allocation["symbol"], before, allocation, stage=_STAGE_HARD_POLICY,
                         source=_SRC_POLICY, effect=_SCALE, reason_code="REGIME_CASH_FLOOR_TRIM",
                         reason_text=f"Trimmed to keep the {min_cash_pct:.0f}% minimum cash.")
                deficit -= trim
            logger.info(
                "[REGIME] enforced min_cash=%.0f%% regime=%s",
                min_cash_pct, regime_context.get("regime"),
            )



def _limit_sector_buys(allocations, total_value, policy_context, positions, observer=None):
    """Reduce only proposed increases. Re-evaluate after each one-way trim."""
    if total_value <= 0:
        return
    envelope = _make_envelope_from_dict(policy_context)
    for row in sorted(allocations, key=lambda row: (-row.get("target_weight", 0), row["symbol"])):
        if row["action"] not in ("BUY", "ACCUMULATE"):
            continue
        symbol = row["symbol"]
        sector = positions.get(symbol, {}).get("sector", "Other")
        values = project_targets(positions, allocations, total_value)
        evaluation = evaluate_sectors(
            positions, values, envelope.resolved_sector_limits,
            envelope.hard_constraints.max_sector_pct, "PROJECTED_TARGET",
        )
        breach = next((item for item in evaluation["sectors"]
                       if item["sector"] == sector and item["breach_pp"]), None)
        if breach is None:
            continue
        current = positions.get(symbol, {}).get("value", 0.0)
        cap_fraction = breach["limit_pct"] / 100
        removable = breach["breach_amount"] / (1 - cap_fraction)
        target = max(current, values[symbol] - removable)
        before = _alloc_basis(row)
        row["target_weight"] = max(row["current_weight"], floor(target / total_value * 10000) / 100)
        row["allocation_change_percent"] = round(row["target_weight"] - row["current_weight"], 2)
        row["estimated_amount"] = round(row["allocation_change_percent"] / 100 * total_value)
        _observe(observer, symbol, before, row, stage=_STAGE_HARD_POLICY,
                 source=_SRC_POLICY, effect=_SCALE, reason_code="SECTOR_CAP_TRIM",
                 reason_text=f"Reduced proposed buying under the {breach['limit_pct']:g}% invested-equity cap for {sector}.")


def _reconcile_allocation_actions(allocations: list[dict], observer=None, *, muji_v2=False) -> None:
    """Reconcile action labels after deterministic target-weight changes."""
    for allocation in allocations:
        delta = allocation.get("allocation_change_percent", 0)
        action = (allocation.get("action") or "HOLD").upper()
        before = _alloc_basis(allocation)
        if muji_v2 and action in ("BUY", "ACCUMULATE") and delta <= 0:
            allocation.setdefault("original_action", action)
            allocation["action"] = "HOLD"
            allocation["allocation_change_percent"] = 0
            allocation["estimated_amount"] = 0
            allocation["target_weight"] = allocation["current_weight"]
        elif muji_v2 and action in ("SELL", "REDUCE") and delta >= 0:
            allocation.setdefault("original_action", action)
            allocation["action"] = "HOLD"
            allocation["allocation_change_percent"] = 0
            allocation["estimated_amount"] = 0
            allocation["target_weight"] = allocation["current_weight"]
        elif action in ("BUY", "ACCUMULATE") and delta < -1.0:
            allocation["action"] = "REDUCE"
            logger.info(
                "[ACTION_RECONCILE] %s %s→REDUCE (delta=%.1f%% after constraint enforcement)",
                allocation.get("symbol"), action, delta,
            )
        elif action in ("BUY", "ACCUMULATE") and delta <= 0:
            allocation["action"] = "HOLD"
            logger.info(
                "[ACTION_RECONCILE] %s %s→HOLD (delta=%.1f%% suppressed to zero by constraints)",
                allocation.get("symbol"), action, delta,
            )
        elif action == "REDUCE" and delta > 1.0:
            allocation["action"] = "ACCUMULATE"
            logger.info(
                "[ACTION_RECONCILE] %s REDUCE→ACCUMULATE (delta=%.1f%% after constraint enforcement)",
                allocation.get("symbol"), delta,
            )
        if observer is not None and _alloc_basis(allocation)["action"] != before["action"]:
            _observe(observer, allocation.get("symbol", ""), before, allocation,
                     stage=_STAGE_RECONCILIATION, source=_SRC_SYSTEM, effect=_RELABEL,
                     reason_code="ACTION_RECONCILE",
                     reason_text=f"Relabelled {before['action']} to {allocation['action']} "
                                 f"after constraint enforcement (delta {delta:.1f}%).")


def _fallback_prompt(
    pc: list[dict],
    wc: list[dict],
    sell_forced: list[str],
    locked: list[str],
    max_stocks: int,
    max_sector_pct: int,
    total_value: float,
    cash_balance: float,
    effective_policy_rules: str = "",
    intent_block: str = "",
    sector_advisory: bool = False,
    muji_v2: bool = False,
) -> str:
    allocation_basis = ',"decision_basis":"INVESTMENT_THESIS|CONCENTRATION_ADVISORY"' if muji_v2 else ""
    return f"""You are an emergency portfolio analyst. The multi-layer optimizer pipeline failed.
Produce a complete, compliant capital allocation plan in a single response.

Portfolio holdings (current): {json.dumps(pc, indent=2)}
Watchlist candidates: {json.dumps(wc, indent=2)}
Forced exits (SELL signal): {sell_forced or "none"}
Locked positions (no swap): {locked or "none"}
Max portfolio stocks: {max_stocks}
{"" if sector_advisory else f"Default sector threshold: {max_sector_pct}% of invested equity, excluding cash"}
Total portfolio value: {total_value:.0f}, Cash balance: {cash_balance:.0f}

{intent_block}HARD RULES — you MUST follow all of these:
1. Forced exit symbols MUST appear with action=SELL and target_weight=0.0
2. Locked symbols MUST appear with action=HOLD and unchanged target_weight
3. Total unique stocks after rebalancing (HOLD/BUY/ACCUMULATE/REDUCE combined) MUST NOT exceed {max_stocks}
5. target_weight values are FLAT PERCENTAGES (10.0 = 10% of portfolio), NOT monetary amounts
6. Every existing portfolio holding must appear in allocations with an explicit action
{effective_policy_rules}

{_MUJI_THESIS_GUIDANCE + "\n" if muji_v2 else ""}Sector caps are advisory. Allow HOLD and NO_ACTION with a concentration warning.
Never block a buy or propose an actionable sale solely because of sector exposure.
Put optional sector-only SELL/REDUCE ideas in sector_alternatives using the same allocation row format.
Keep the actionable allocation HOLD unless independently justified. Mark thesis-driven reductions
with decision_basis=INVESTMENT_THESIS.{('\n If this is a coherent optional strategy, return strategy_family as RAISE_CASH, DEFENSIVE_ROTATION or GROWTH_ROTATION and observed_evidence_refs using only frozen symbol:SYM:signal, symbol:SYM:fa_score, symbol:SYM:ta_score, regime:regime or goal:ID:target_date facts. Otherwise use null and an empty evidence list.') if muji_v2 else ''}

OUTPUT CONTRACT — this JSON is read by software; do not spend output tokens on prose. Watchlist symbols you are
not recommending (no BUY/ACCUMULATE) do NOT need an allocations row — omit them, except up to 5 WATCH rows for
your top-ranked candidates. "r"/"reason" is one line, under 20 words. blocked_opportunities and risk_flags: only
the highest-priority items, max 5 each. Never drop an existing-holding allocation row to make room for text.

Every risk flag must have category INVESTMENT_RISK or OWNER_INTENT_REVIEW.
Owner Intent disagreement is allowed and belongs to OWNER_INTENT_REVIEW; preserve it
for review but exclude it from investment risk, final_risk_level and governance judgments.
Any actual investment risk in the same symbol must remain a separate INVESTMENT_RISK flag.
Include claim_kind=INVESTMENT_JUDGMENT for independent risk opinions, ADVISORY_CONCERN
for concentration guidance. Do not assert a deterministic breach without evidence_ref.
Model-only opinions are visible but unscored; a model label never authorizes a penalty.
Fallback execution has no deterministic DR target clamp; holding size does not mandate liquidation.

Return ONLY valid JSON without markdown fences:
{{
  "status": "REBALANCE|NO_ACTION",
  "rebalance_opportunity_score": 50,
  "no_action_reason": "WELL_BALANCED|LOW_CONFIDENCE|HIGH_DISAGREEMENT|CONSTRAINT_BLOCKED|MARKET_UNCERTAINTY|INSUFFICIENT_EDGE|null",
  "no_action_summary": "<20 words, null if REBALANCE",
  "blocked_opportunities": [{{"symbol":"X","signal":"BUY","reason":"insufficient_cash|portfolio_count_cap"}}],
  "portfolio_assessment": "1-2 sentence summary of the plan",
  "cash_balance_target": 5.0,
{('  "strategy_family": "RAISE_CASH|DEFENSIVE_ROTATION|GROWTH_ROTATION|null", "observed_evidence_refs": ["symbol:SYM:signal"],\n') if muji_v2 else ''}  "allocations": [
    {{"s":"X","tw":0.0,"sig":"BUY|ACCUMULATE|HOLD|REDUCE|SELL|WATCH","r":"<20 words"{allocation_basis}}}
  ],
  "risk_flags": [{{"symbol":"...","issue":"<15 words","severity":"LOW|MEDIUM|HIGH|CRITICAL","category":"INVESTMENT_RISK|OWNER_INTENT_REVIEW","claim_kind":"INVESTMENT_JUDGMENT|ADVISORY_CONCERN","evidence_ref":null}}],
  "final_risk_level": "low|medium|high|critical",
  "auditor_notes": "brief compliance note"
}}"""


def _run_single_shot_fallback(
    pc: list[dict],
    wc: list[dict],
    sell_forced: list[str],
    locked: list[str],
    portfolio_data: list[dict],
    current_sector_weights: dict,
    pc_map: dict[str, float],
    max_stocks: int,
    max_sector_pct: int,
    sector_limits: dict | None,
    total_value: float,
    cash_balance: float,
    fallback_provider: str,
    fallback_model: str,
    portfolio_name: str,
    portfolio_count: int,
    max_reached: bool,
    policy_context: dict | None = None,
    effective_envelope: "_EffectiveEnvelope | None" = None,
    enforce_effective_policy: bool = False,
    advisory=None,
    execution_context: dict | None = None,
    sector_policy_mode: str | None = None,
    optimizer_policy_mode: str | None = None,
    muji_policy_block: str = "",
    goal_decision_input: dict | None = None,
    regime_context: dict | None = None,
    strategy_selection_mode: str | None = None,
) -> dict:
    """Single-shot emergency fallback when the 3-layer pipeline fails completely.

    advisory: the SAME frozen Advisory Integration V1 run as the primary path
    (substitutes for L2, so it receives hard + soft context).
    """
    muji_v2 = (sector_policy_mode == SECTOR_POLICY_ADVISORY
               and optimizer_policy_mode == OPTIMIZER_POLICY_MUJI_V2)
    selection_enabled = strategy_selection_mode == SELECTION_VERSION and muji_v2
    sector_advisory = sector_policy_mode == SECTOR_POLICY_ADVISORY
    degraded_policy = _degraded_sector_policy(sector_limits, max_sector_pct, effective_envelope) if sector_advisory else None
    score_map = _build_score_context_map(pc, wc)
    effective_policy_rules = ""
    if muji_v2:
        effective_policy_rules = muji_policy_block or (policy_context or {}).get("prompt_block", "")
    elif enforce_effective_policy:
        hard = (policy_context or {}).get("hard_constraints", {})
        max_position = float(hard.get(
            "max_single_position_pct",
            effective_envelope.effective_single_position_pct if effective_envelope else 22.0,
        ))
        min_cash = float(hard.get(
            "min_cash_pct",
            effective_envelope.effective_cash_min_pct if effective_envelope else 5.0,
        ))
        emergency = bool((policy_context or {}).get("emergency_override", False))
        effective_policy_rules = (
            f"7. Effective maximum single-position weight is {max_position:.1f}%\n"
            f"8. Effective minimum cash weight is {min_cash:.1f}%\n"
            + ("10. Emergency policy prohibits BUY and ACCUMULATE\n" if emergency else "")
        )
    prompt = _fallback_prompt(
        pc, wc, sell_forced, locked, max_stocks, max_sector_pct,
        total_value, cash_balance, effective_policy_rules, sector_advisory=sector_advisory, muji_v2=muji_v2,
        **({"intent_block": _intent_block(advisory, _LAYER_FALLBACK)} if advisory is not None else {}),
    )
    from services.optimizer.execution_penalty import build_execution_prompt_block
    prompt = build_execution_prompt_block(execution_context or {}) + (
        _goal_decision_block(goal_decision_input) if muji_v2 else ""
    ) + prompt
    try:
        raw = call_ai(
            prompt, fallback_provider, fallback_model, max_tokens=4096,
            usage_operation="optimize", usage_layer="fallback",
        )
    except Exception:
        _note_prompt(advisory, _LAYER_FALLBACK, "FAILED")
        raise
    _note_prompt(advisory, _LAYER_FALLBACK, "SUCCESS")
    fb_latency_ms = raw["latency_ms"]
    result = safe_parse_json(raw["text"])

    raw_allocs = result.pop("allocations", None) or []
    allocations = _normalize_allocations(raw_allocs, pc_map, score_map, muji_v2=muji_v2)
    sector_alternatives = []
    if sector_advisory:
        concentration = freeze_concentration(portfolio_data, wc, policy_context, total_value) if policy_context else None
        sector_alternatives = _separate_sector_alternatives(
            result, allocations, pc_map, total_value, concentration, muji_v2=muji_v2, sell_forced=sell_forced,
        )
    for a in allocations:
        a["estimated_amount"] = round((a["allocation_change_percent"] / 100) * total_value)
        _observe(advisory, a["symbol"], None, a, stage=_STAGE_FALLBACK, source=_SRC_ADVISORY,
                 effect=_ORIGINATE, reason_code="FALLBACK_ALLOCATION", reason_text=a.get("reason", ""))

    fallback_candidates = None
    fallback_selection = None
    if selection_enabled:
        try:
            fallback_candidates = strategic_candidates.prepare_candidates(
                portfolio_data, wc, cash_balance,
                {**result, "target_allocations": allocations,
                 "target_cash_weight": result.get("cash_balance_target")},
                regime=regime_context, goals=goal_decision_input,
                source_layer="SINGLE_SHOT_FALLBACK")
            hold = fallback_candidates["candidates"][0]
            hold_safe = hold["eligibility_status"] == "ELIGIBLE"
            if hold_safe:
                trial = deepcopy(hold["proposed_allocations"])
                _enforce_hard_policy(trial, total_value=total_value,
                                     policy_context=policy_context,
                                     regime_context=regime_context, muji_v2=True)
                hold_safe = trial == hold["proposed_allocations"]
                floor_pct = (policy_context or {}).get("hard_constraints", {}).get("min_cash_pct")
                if floor_pct is not None and total_value > 0 and cash_balance / total_value * 100 < floor_pct:
                    hold_safe = False
            fallback_selection = decide_selection(
                fallback_candidates, {"status": "UNAVAILABLE", "reason": "AUDITOR_UNAVAILABLE_IN_FALLBACK"},
                None, hold_safe=hold_safe)
            allocations = (deepcopy(hold["proposed_allocations"])
                           if fallback_selection["selected_candidate_id"] == "hold-current" else [])
        except Exception as exc:
            fallback_candidates = {"version": "wealth.strategic-candidates.v1",
                                   "status": "UNAVAILABLE", "candidates": [],
                                   "reason": "CANDIDATE_PREPARATION_FAILED"}
            fallback_selection = decide_selection(fallback_candidates,
                {"status": "UNAVAILABLE", "reason": type(exc).__name__}, None, hold_safe=False)
            allocations = []

    locked_set = set(locked)
    alloc_map: dict[str, dict] = {a["symbol"]: a for a in allocations}
    _apply_forced_and_locked(alloc_map, [] if selection_enabled else sell_forced,
                             locked_set, pc_map, advisory)

    final_allocations = list(alloc_map.values())
    for a in final_allocations:
        _apply_score_context(a, score_map, a["symbol"])
        a["allocation_change_percent"] = round(a["target_weight"] - a["current_weight"], 2)
        a["estimated_amount"] = round((a["allocation_change_percent"] / 100) * total_value)
    _observer_kw = {"observer": advisory} if advisory is not None else {}
    if enforce_effective_policy or policy_context:
        try:
            _enforce_hard_policy(
                final_allocations,
                total_value=total_value,
                policy_context=policy_context,
                regime_context=None,
                muji_v2=muji_v2,
                **_observer_kw,
            )
            if policy_context and not sector_advisory:
                _limit_sector_buys(final_allocations, total_value, policy_context,
                                   freeze_positions(portfolio_data, wc), advisory)
            _reconcile_allocation_actions(final_allocations, **_observer_kw)
        except Exception as exc:
            raise HardPolicyEnforcementError("fallback hard-policy enforcement failed") from exc
    _snap_neutral_actions(final_allocations, **_observer_kw)

    swap_suggestions = _derive_swap_suggestions(final_allocations,
                                                [] if selection_enabled else sell_forced, locked)
    projected_sector_weights = calculate_projected_sector_weights_from_allocations(
        portfolio_data, final_allocations, total_value
    )
    sector_warnings = _compute_sector_warnings(
        current_sector_weights, projected_sector_weights, sector_limits, max_sector_pct
    )

    buy_symbols = [a["symbol"] for a in final_allocations if a.get("action") in ("BUY", "ACCUMULATE")]
    watchlist_ranking = _rebuild_watchlist_ranking(buy_symbols, wc)

    portfolio_assessment = result.get("portfolio_assessment", "Emergency fallback analysis.")
    # Fallback has no execution-cap clamp. Do not imply primary-only enforcement.
    fallback_details = []
    if policy_context:
        from services.optimizer.policy_engine import compute_policy_alignment_score
        fallback_details = compute_policy_alignment_score(final_allocations,
            _make_envelope_from_dict(policy_context), total_value,
            effective_turnover_cap=policy_context.get("relaxed_turnover_cap"),
            frozen_positions=freeze_positions(portfolio_data, wc))[4]
    claim_contract = build_claim_evidence(final_allocations, fallback_details, {},
        risk_inputs={p["symbol"]: p for p in [*pc, *wc]})
    if sector_advisory:
        claim_contract["sector_advisories"] = {}
    result = validate_auditor_claims(result, claim_contract)
    risk_flags = result.get("risk_flags", [])
    final_risk_level = result.get("final_risk_level", "medium")
    auditor_notes = result.get("auditor_notes", "Fallback mode — single-shot analysis.")
    fb_tag = f"[FALLBACK:{fallback_provider}/{fallback_model}]"

    xai_status            = result.get("status", "REBALANCE")
    xai_score             = int(result.get("rebalance_opportunity_score") or 50)
    xai_no_action_reason  = result.get("no_action_reason")
    xai_no_action_summary = result.get("no_action_summary")
    xai_blocked           = result.get("blocked_opportunities", [])

    consensus = {
        "consensus_type":             "WEAK_CONSENSUS",
        "consensus_strength_score":   20,
        "strategist_alignment_score": 20,
        "risk_alignment_score":       50,
        "disagreement_reasons":       [],
        "refinement_summary":         "Emergency fallback mode — single-shot analysis, review allocations manually.",
        "agrees":             True,
        "consensus_decision": "REBALANCE",
        "confidence":         "low",
        "recommended":        "fallback",
        "final_risk_level":   "medium",
        "risk_flag_count":    len(investment_risk_flags(risk_flags)),
        "recommended_action": (
            f"{fb_tag} Pipeline recovered via emergency single-shot analysis. "
            "Review allocations manually before acting."
        ),
    }

    output = {
        "portfolio_name": portfolio_name,
        "status": xai_status,
        "rebalance_opportunity_score": xai_score,
        "no_action_reason": xai_no_action_reason,
        "no_action_summary": xai_no_action_summary,
        "blocked_opportunities": xai_blocked,
        "portfolio_assessment": f"{fb_tag} {portfolio_assessment}",
        "optimization_notes": consensus["recommended_action"],
        "target_allocations": final_allocations,
        "target_cash_weight": float(result.get("cash_balance_target", 0.0)),
        "portfolio_turnover_percent": sum(abs(a["allocation_change_percent"]) for a in final_allocations),
        "swap_suggestions": swap_suggestions,
        "watchlist_ranking": watchlist_ranking,
        "portfolio_count": portfolio_count,
        "max_reached": max_reached,
        "max_stocks": max_stocks,
        "cash_balance": cash_balance,
        "total_value": round(total_value, 2),
        "ai_provider": fallback_provider,
        "ai_model": fallback_model,
        "current_sector_weights": current_sector_weights,
        "projected_sector_weights": projected_sector_weights,
        "sector_warnings": sector_warnings,
        "layer1_latency_ms": 0,
        "layer2_latency_ms": 0,
        "layer3_latency_ms": fb_latency_ms,
        "total_latency_ms": fb_latency_ms,
        "layer1_result": {
            "provider": fallback_provider, "model": fallback_model, "name": "Fallback",
            "error": "Pipeline failed — emergency fallback activated",
            "swap_suggestions": [], "top_buys": [], "sector_flags": [], "priority": "",
        },
        "layer2_result": {
            "provider": fallback_provider, "model": fallback_model, "name": "Fallback",
            "target_allocations": final_allocations, "portfolio_assessment": portfolio_assessment,
            "agrees_with_layer1": True, "disagreements": [],
        },
        "layer3_result": {
            **{k: result[k] for k in ("claim_reviews", "claim_validation_version", "raw_model_output", "policy_claim_contract")},
            "provider": fallback_provider, "model": fallback_model, "name": "Fallback",
            "risk_flags": risk_flags, "safer_choice": "fallback",
            "final_risk_level": final_risk_level, "auditor_notes": auditor_notes,
        },
        "consensus": consensus,
        "fallback_mode": True,
    }
    policy_output = ({**{k: v for k, v in policy_context.items() if k != "prompt_block"},
                      "violation_details": fallback_details} if policy_context else None)
    _capture_sector_policy(output, policy_output, sector_policy_mode, portfolio_data, wc,
                           total_value, degraded_policy, sector_alternatives, optimizer_policy_mode)
    if selection_enabled:
        output["strategic_candidates"] = fallback_candidates
        output["strategy_selection"] = fallback_selection
        output["candidate_audit"] = {"status": "UNAVAILABLE",
                                     "reason": "AUDITOR_UNAVAILABLE_IN_FALLBACK", "reviews": {}}
        output["active_policy"]["strategy_selection_mode"] = strategy_selection_mode
        output["target_allocations"] = final_allocations
        output["status"] = "NO_ACTION" if fallback_selection["selected_candidate_id"] else "REVIEW"
        output["target_cash_weight"] = cash_balance / total_value * 100 if total_value else 0.0
        output["portfolio_assessment"] = fallback_selection.get("decision_rationale") or "Human review required."
        output["consensus"]["strategy_selection_state"] = fallback_selection["state"]
        output["consensus"]["recommended"] = fallback_selection["selected_candidate_id"] or "human_review"
        output["consensus"]["recommended_action"] = output["portfolio_assessment"]
        output["optimization_notes"] = output["portfolio_assessment"]
    elif muji_v2:
        from services.optimizer.strategic_candidates import VERSION
        try:
            output["strategic_candidates"] = strategic_candidates.prepare_candidates(
                portfolio_data, wc, cash_balance,
                {**result, "target_allocations": final_allocations,
                 "target_cash_weight": output["target_cash_weight"]},
                regime=regime_context, goals=goal_decision_input,
                source_layer="SINGLE_SHOT_FALLBACK",
            )
        except Exception as exc:
            logger.exception("MUJI fallback candidate preparation unavailable: %s", exc)
            output["strategic_candidates"] = {
                "version": VERSION, "status": "UNAVAILABLE", "goal_context_version":
                (goal_decision_input or {}).get("contract_version"), "candidates": [],
                "reason": "CANDIDATE_PREPARATION_FAILED",
            }
    return output


# ─── L1 minimal-prompt retry helper ──────────────────────────────────────────

def _retry_l1_with_schema(
    c_pc: list[dict],
    c_wc: list[dict],
    sell_forced: list[str],
    swap_eligible: list[str],
    l1_cfg: dict,
    intent_block: str = "",
    execution_context: dict | None = None,
    muji_v2: bool = False,
    policy_block: str = "",
    goal_decision_input: dict | None = None,
) -> dict:
    """Single-shot L1 retry with a stripped-down prompt after an initial parse failure.

    Called only when the full L1 prompt produced unparseable output.  The goal is
    to get *something* structurally valid so L2/L3 can still run with real signal.
    """
    from services.optimizer.execution_penalty import build_execution_prompt_block
    guidance = (
        _MUJI_THESIS_GUIDANCE + "\nUse empty swaps and priority=no_action when appropriate.\n"
        if muji_v2 else "Sector concentration is advisory and cannot by itself justify a trade.\n"
    )
    minimal_prompt = build_execution_prompt_block(execution_context or {}) + intent_block + policy_block + (
        _goal_decision_block(goal_decision_input) if muji_v2 else ""
    ) + (
        "You are a portfolio strategist. Return ONLY a valid JSON object — "
        "no markdown, no prose, just the JSON.\n\n"
        f"Current holdings: {json.dumps(c_pc)}\n"
        f"Watchlist candidates: {json.dumps(c_wc)}\n"
        f"Swap-eligible: {swap_eligible or 'none'}\n"
        f"Forced exits: {sell_forced or 'none'}\n\n"
        "Propose up to 3 independently justified swap / reduce actions and rank the top watchlist buys.\n"
        f"{guidance}"
        "Required output (fill in real values, \"r\" = reason under 12 words):\n"
        '{"swaps":[{"sell":"SYM_OR_NULL","buy":"SYM_OR_NULL","score_delta":0.0,'
        '"sector":"Other","type":"SWAP","r":"<12 words"}],"top_buys":["SYM"],'
        '"sector_flags":[],"priority":"balanced"}'
    )
    raw = call_ai(
        minimal_prompt,
        l1_cfg["provider"],
        l1_cfg["model"],
        max_tokens=2048,
        use_schema=MujiLayer1Response if muji_v2 else True,
        usage_operation="optimize",
        usage_layer="layer1_retry",
    )
    return safe_parse_json(raw["text"])


# ─── Public API ───────────────────────────────────────────────────────────────

def run_optimizer(
    portfolio_data: list[dict],
    watchlist_data: list[dict],
    portfolio_name: str,
    portfolio_count: int = 0,
    max_reached: bool = False,
    provider: str = "anthropic",
    model: str = "claude-sonnet-4-6",
    max_stocks: int = 12,
    max_sector_pct: int = 40,
    cash_balance: float = 0.0,
) -> dict:
    """Single-model optimizer (legacy path)."""
    portfolio_data = _compute_portfolio_weights(portfolio_data, cash_balance)

    sell_forced   = [p["symbol"] for p in portfolio_data if p.get("signal") == "SELL"]
    locked        = [p["symbol"] for p in portfolio_data if not p.get("allow_swap", True)]
    swap_eligible = [p["symbol"] for p in portfolio_data if p.get("allow_swap", True) and p.get("signal") != "SELL"]
    pc = _compact_p(portfolio_data)
    wc = _compact_w(watchlist_data)
    score_map = _build_score_context_map(pc, wc)
    c_pc, c_wc = _compress_for_layer1(pc, wc)
    prompt = _layer1_prompt(
        c_pc, c_wc, sell_forced, swap_eligible,
        max_sector_pct=max_sector_pct, max_stocks=max_stocks, current_count=portfolio_count,
    )
    logger.info(f"L1 prompt chars: {len(prompt)}")
    ai_result = call_ai(
        prompt, provider, model, max_tokens=2048,
        use_schema=True,
        usage_operation="optimize", usage_layer="layer1",
    )
    result = safe_parse_json(ai_result["text"])
    result["portfolio_name"] = portfolio_name
    result["portfolio_count"] = portfolio_count
    result["max_reached"] = max_reached
    result["max_stocks"] = max_stocks
    result["swap_suggestions"] = _postprocess_swaps(
        _normalize_l1_swaps(result.get("swaps", []), score_map), sell_forced, locked
    )
    result["watchlist_ranking"] = _rebuild_watchlist_ranking(result.get("top_buys", []), wc)
    return result


def run_layered_optimizer(
    portfolio_data: list[dict],
    watchlist_data: list[dict],
    portfolio_name: str,
    portfolio_count: int = 0,
    max_reached: bool = False,
    layers: dict | None = None,
    max_stocks: int = 12,
    max_sector_pct: int = 40,
    sector_limits: dict | None = None,
    cash_balance: float = 0.0,
    fallback_provider: str = "anthropic",
    fallback_model: str = "claude-sonnet-4-6",
    persona_context: dict | None = None,
    regime_context: dict | None = None,
    policy_context: dict | None = None,
    effective_envelope: "_EffectiveEnvelope | None" = None,
    execution_context: dict | None = None,
    on_stage: Callable[[str], None] | None = None,
    enforce_effective_policy_in_fallback: bool = False,
    advisory=None,
    sector_policy_mode: str | None = None,
    optimizer_policy_mode: str | None = None,
    goal_decision_input: dict | None = None,
    strategy_selection_mode: str | None = None,
) -> dict:
    """3-layer Dynamic Capital Allocation Engine with global single-shot fallback.

    on_stage: optional presentation-only progress callback (Phase 4C.1) invoked
    with a stage key before each AI layer call. Failures inside the callback are
    swallowed — it can never affect optimizer behavior.

    advisory: Advisory Integration V1 run (default-OFF flag), else None. When
    present: frozen Intent prompt context for L1/L2/L3 (+ retry/fallback),
    common-NAV current weights for held positions when that basis resolves,
    and proposal-transition capture. It never changes an allocation decision.
    """
    # Keep one identity for all layer attempts, including the schema retry.
    policy_identity = dict(policy_context or {})
    for field, mode in (("sector_policy_mode", sector_policy_mode),
                        ("optimizer_policy_mode", optimizer_policy_mode)):
        if mode is not None and policy_identity.setdefault(field, mode) != mode:
            raise UnsupportedOptimizerPolicyEvidence(f"Conflicting {field}")
    resolver_mode = getattr(effective_envelope, "optimizer_policy_mode", None)
    muji_v2 = read_optimizer_policy_mode(
        policy_identity, effective_envelope={"optimizer_policy_mode": resolver_mode} if resolver_mode is not None else None,
    ) == OPTIMIZER_POLICY_MUJI_V2
    if strategy_selection_mode not in (None, SELECTION_VERSION) or (strategy_selection_mode and not muji_v2):
        raise UnsupportedOptimizerPolicyEvidence("Unsupported strategy_selection_mode")
    selection_enabled = strategy_selection_mode == SELECTION_VERSION
    muji_policy_block = ""
    if muji_v2 and policy_context:
        from services.optimizer.policy_engine import build_policy_prompt_block
        if policy_context.get("optimizer_policy_mode") != OPTIMIZER_POLICY_MUJI_V2 or not policy_context.get("prompt_block"):
            policy_identity["prompt_block"] = build_policy_prompt_block(_make_envelope_from_dict(policy_identity))
        policy_context = policy_identity
        muji_policy_block = policy_context["prompt_block"]
    elif muji_v2 and regime_context:
        from services.analytics.regime_detector import build_regime_prompt_block
        muji_policy_block = build_regime_prompt_block(regime_context, concentration_advisory=True)
    sector_policy_mode = policy_identity.get("sector_policy_mode")
    optimizer_policy_mode = policy_identity.get("optimizer_policy_mode")
    sector_advisory = sector_policy_mode == SECTOR_POLICY_ADVISORY
    advisory_bases = _CONCENTRATION_ADVISORY_BASES if muji_v2 else ("SECTOR_ADVISORY",) if sector_advisory else ()
    degraded_policy = _degraded_sector_policy(sector_limits, max_sector_pct, effective_envelope) if sector_advisory else None
    sector_alternatives = []
    if layers is None:
        layers = _DEFAULT_LAYERS

    l1_cfg = {**_DEFAULT_LAYERS["layer1"], **layers.get("layer1", {})}
    l2_cfg = {**_DEFAULT_LAYERS["layer2"], **layers.get("layer2", {})}
    l3_cfg = {**_DEFAULT_LAYERS["layer3"], **layers.get("layer3", {})}

    sell_forced   = [p["symbol"] for p in portfolio_data if p.get("signal") == "SELL"]
    locked        = [p["symbol"] for p in portfolio_data if not p.get("allow_swap", True)]

    portfolio_data = _compute_portfolio_weights(portfolio_data, cash_balance)
    total_equity = sum(i.get("market_value", 0) for i in portfolio_data)
    total_value = total_equity + cash_balance

    # TEMP DEBUG — cash data-flow trace (2026-07-03), remove after cash_pct bug confirmed
    logger.info(
        "[CASH_TRACE stage=2_OPTIMIZER_CONTEXT] portfolio_value=%.2f invested_value=%.2f "
        "available_cash=%.2f cash_pct=%.4f%%",
        total_value, total_equity, cash_balance,
        (cash_balance / total_value * 100) if total_value else 0.0,
    )

    # Authoritative current weights from real portfolio data (not AI-reported)
    pc_map: dict[str, float] = {p["symbol"]: p.get("weight_pct", 0.0) for p in portfolio_data}
    # Advisory Integration V1: held current weights on the common NAV basis
    # (equity + cash, frozen quotes), matching L2's "% of portfolio" targets.
    # None when that basis cannot be established — legacy weights then stand.
    _canonical_weights = advisory.canonical_current_weights() if advisory is not None else None
    if _canonical_weights:
        pc_map.update(_canonical_weights)

    swap_eligible = [p["symbol"] for p in portfolio_data if p.get("allow_swap", True) and p.get("signal") != "SELL"]
    pc = _compact_p(portfolio_data)
    if _canonical_weights:
        for p in pc:
            if p["symbol"] in _canonical_weights:
                p["weight_pct"] = _canonical_weights[p["symbol"]]
    wc = _compact_w(watchlist_data)
    score_map = _build_score_context_map(pc, wc)
    c_pc, c_wc = _compress_for_layer1(pc, wc)

    frozen_positions = freeze_positions(portfolio_data, watchlist_data)
    current_sector_weights = calculate_current_sector_weights(portfolio_data)

    # ── Phase 3B.6 — Tier 1 breach detection for dynamic turnover relaxation ──
    # Detect concentration breaches in the CURRENT portfolio before AI layers run.
    # When breaches exist, Tier 3 turnover constraints are relaxed so they cannot
    # block the remediation that Tier 1 demands.
    _t1_severity: str = "NONE"
    _t1_reason:   str = ""
    _base_turn_cap:    float = 0.0
    _relaxed_turn_cap: float | None = None

    if policy_context and not muji_v2:
        _pe_for_t1 = _make_envelope_from_dict(policy_context)
        _base_turn_cap = _pe_for_t1.hard_constraints.max_turnover_pct
        _t1_severity, _t1_reason = compute_concentration_breach_severity(
            portfolio_data,
            _pe_for_t1.hard_constraints.max_single_position_pct,
            _pe_for_t1.hard_constraints.max_sector_pct,
            dict(policy_context.get("resolved_sector_limits") or {}),
            include_sectors=not sector_advisory,
        )
        _relaxed_turn_cap = get_relaxed_turnover_cap(_base_turn_cap, _t1_severity)
        if _t1_severity != "NONE":
            logger.info(
                "[TIER1_RELAX] severity=%s base_turn=%.0f%% relaxed=%.0f%% reason=%s",
                _t1_severity, _base_turn_cap, _relaxed_turn_cap, _t1_reason,
            )

    # Prompt note injected into all 3 layers when Tier 1 breaches are present
    _t1_note = ""
    if _t1_severity != "NONE" and _relaxed_turn_cap is not None and _base_turn_cap > 0:
        _mult_pct = round((_relaxed_turn_cap / _base_turn_cap - 1) * 100)
        _t1_note = (
            f"[CONSTRAINT HIERARCHY — CONCENTRATION PRIORITY ACTIVE]\n"
            f"TIER 1 BREACH DETECTED ({_t1_severity}): {_t1_reason}\n"
            f"PRIORITY RULE: Eliminating dangerous concentration risk takes absolute precedence "
            f"over Tier 3 turnover efficiency constraints.\n"
            f"Effective turnover ceiling this run: {_relaxed_turn_cap:g}% "
            f"(base {_base_turn_cap:.0f}% + {_mult_pct}% relaxation for Tier 1 remediation).\n"
            f"concentration reduction > turnover efficiency | "
            f"safety remediation > optimization friction\n"
            f"\n"
            f"AUTHORIZED EXCEPTION SEMANTICS — MANDATORY FOR ALL AGENTS:\n"
            f"'Turnover Relaxation Active' is a SAFE AUTHORIZED STATE, NOT a failure condition.\n"
            f"The system has mathematically pre-approved this temporary turnover overshoot to eliminate\n"
            f"a more dangerous Tier 1 concentration risk. This is controlled, policy-compliant behavior.\n"
            f"\n"
            f"SAFE AUTHORIZED STATES (do NOT escalate to REVIEW / flag HIGH or CRITICAL):\n"
            f"  • Turnover Relaxation Active    — controlled Tier 3 flex for Tier 1 remediation\n"
            f"  • Temporary Cash Deployment Override — transient, for forced exits\n"
            f"  • Sector Exposure Advisory     — review concentration separately from the trade decision\n"
            f"\n"
            f"DANGEROUS FAILURE STATES (flag HIGH/CRITICAL, warrant REVIEW or REJECT):\n"
            f"  • Concentration breach UNRESOLVED after proposed rebalancing\n"
            f"  • Contradictory allocation logic (same stock BUY + SELL simultaneously)\n"
            f"  • Unauthorized leverage or risk escalation beyond policy envelope\n"
            f"  • Policy envelope violations WITHOUT documented system authorization\n"
            f"\n"
            f"MANDATORY DECISION RULE:\n"
            f"  IF (a) concentration violations are materially reduced by the proposed plan, AND\n"
            f"     (b) portfolio diversification improves (fewer or smaller overweight positions), AND\n"
            f"     (c) the ONLY remaining concern is an authorized turnover relaxation buffer:\n"
            f"  THEN → L2 MUST output status=REBALANCE (not NO_ACTION, not REVIEW).\n"
            f"          L3 MUST output final_risk_level=low or medium (not high).\n"
            f"  Authorized operational relaxations confirm the system is working correctly.\n\n"
        )

    try:
        sector_context = (freeze_concentration(
            portfolio_data, watchlist_data, policy_context or degraded_policy, total_value,
        ) if sector_advisory else None)
        # Layer 1 — Strategist
        _emit_stage(on_stage, "LAYER1_PROPOSAL")
        l1_parse_failed = False
        try:
            l1_prompt = _layer1_prompt(
                c_pc, c_wc, sell_forced, swap_eligible,
                max_sector_pct=max_sector_pct, sector_limits=sector_limits, sector_advisory=sector_advisory,
                max_stocks=max_stocks, current_count=portfolio_count,
                persona_context=persona_context,
                regime_context=regime_context,
                policy_context=policy_context,
                effective_envelope=effective_envelope,
                t1_breach_note=_t1_note,
                muji_v2=muji_v2,
                goal_decision_input=goal_decision_input if muji_v2 else None,
                execution_context=execution_context,
                **({"intent_block": _intent_block(advisory, _LAYER_L1)} if advisory is not None else {}),
            )
            logger.info(f"L1 prompt chars: {len(l1_prompt)}")
            l1_raw = call_ai(
                l1_prompt, l1_cfg["provider"], l1_cfg["model"], max_tokens=4096,
                use_schema=MujiLayer1Response if muji_v2 else True,
                usage_operation="optimize", usage_layer="layer1",
            )
            l1_latency_ms = l1_raw["latency_ms"]
            raw_l1_text = l1_raw.get("text", "")
            logger.info(
                "[L1_DEBUG] provider=%s model=%s raw_text_len=%d latency_ms=%d",
                l1_cfg["provider"], l1_cfg["model"], len(raw_l1_text), l1_latency_ms,
            )
            l1_result = safe_parse_json(raw_l1_text)
            _l1_swaps = _normalize_l1_swaps(
                [s for s in l1_result.get("swaps", [])
                 if s.get("decision_basis") not in advisory_bases], score_map,
            )
            l1_result["swap_suggestions"] = _postprocess_swaps(_l1_swaps, sell_forced, locked)
            _note_prompt(advisory, _LAYER_L1, "SUCCESS")
            _note_l1_proposals(advisory, _l1_swaps, locked)
            logger.info(
                "[L1_DEBUG] parsed: swaps_count=%d swap_suggestions_count=%d top_buys=%s priority=%s",
                len(l1_result.get("swaps", [])),
                len(l1_result.get("swap_suggestions", [])),
                l1_result.get("top_buys", []),
                l1_result.get("priority"),
            )
        except Exception as e:
            logger.error("[L1_DEBUG] parse_error=%s", e)
            _note_prompt(advisory, _LAYER_L1, "FAILED")
            # Single quiet retry with a minimal stripped-down prompt before giving up
            try:
                l1_result = _retry_l1_with_schema(
                    c_pc, c_wc, sell_forced, swap_eligible, l1_cfg,
                    execution_context=execution_context, muji_v2=muji_v2,
                    goal_decision_input=goal_decision_input if muji_v2 else None,
                    policy_block=(muji_policy_block + "\n" if muji_policy_block else ""),
                    **({"intent_block": _intent_block(advisory, _LAYER_L1_RETRY)} if advisory is not None else {}),
                )
                if selection_enabled:
                    # The successful retry has no latency field in the legacy helper.
                    l1_latency_ms = 0
                _l1_swaps = _normalize_l1_swaps(
                    [s for s in l1_result.get("swaps", [])
                     if s.get("decision_basis") not in advisory_bases], score_map,
                )
                l1_result["swap_suggestions"] = _postprocess_swaps(_l1_swaps, sell_forced, locked)
                l1_parse_failed = False
                _note_prompt(advisory, _LAYER_L1_RETRY, "SUCCESS")
                _note_l1_proposals(advisory, _l1_swaps, locked)
                logger.info("[L1_RETRY] recovered successfully after minimal-prompt retry")
            except Exception as retry_err:
                _note_prompt(advisory, _LAYER_L1_RETRY, "FAILED")
                logger.error("[L1_RETRY] also failed: %s", retry_err)
                l1_parse_failed = True
                l1_result = {
                    "error": str(e), "swap_suggestions": [],
                    "top_buys": [], "sector_flags": [], "priority": "",
                }
                l1_latency_ms = 0

        # Layer 2 — Challenger
        _emit_stage(on_stage, "LAYER2_CHALLENGE")
        try:
            l2_prompt = _layer2_prompt(pc, wc, l1_result, l2_cfg.get("role", ""),
                               cash_balance=cash_balance, total_value=total_value, sector_advisory=sector_advisory,
                               persona_context=persona_context,
                               regime_context=regime_context,
                               policy_context=policy_context,
                               t1_breach_note=_t1_note, muji_v2=muji_v2,
                                goal_decision_input=goal_decision_input if muji_v2 else None,
                               execution_context=execution_context,
                               **({"intent_block": _intent_block(advisory, _LAYER_L2)}
                                  if advisory is not None else {}))
            if selection_enabled:
                l2_prompt += ("\nOptional additional_plans: up to two complete portfolio plans, each with "
                              "strategy_family, observed_evidence_refs, cash_balance_target, "
                              "portfolio_assessment, and allocations in the same format as the primary plan. "
                              "Omit when evidence is insufficient. These are candidates, not selected trades.\n")
            l2_raw = call_ai(
                l2_prompt,
                l2_cfg["provider"], l2_cfg["model"], max_tokens=8192,
                usage_operation="optimize", usage_layer="layer2",
            )
            l2_latency_ms = l2_raw["latency_ms"]
            raw_l2_text = l2_raw.get("text", "")
            logger.info(
                "[L2_DEBUG] provider=%s model=%s raw_text_len=%d latency_ms=%d",
                l2_cfg["provider"], l2_cfg["model"], len(raw_l2_text), l2_latency_ms,
            )
            l2_result = safe_parse_json(raw_l2_text)
            if selection_enabled:
                extra_plans = []
                for plan in (l2_result.get("additional_plans") or [])[:2]:
                    if not isinstance(plan, dict):
                        continue
                    raw_extra = plan.get("allocations", plan.get("target_allocations", []))
                    normalized = _normalize_allocations(raw_extra, pc_map, score_map, muji_v2=True)
                    extra_plans.append({**plan, "target_allocations": normalized,
                                        "candidate_input_invalid": not _complete_candidate_input(raw_extra),
                                        "target_cash_weight": plan.get("target_cash_weight", plan.get("cash_balance_target"))})
                l2_result["additional_plans"] = extra_plans
            # Fix: use None check so an explicitly-empty allocations:[] isn't dropped
            raw_allocs = l2_result.pop("allocations", None)
            if raw_allocs is None:
                raw_allocs = l2_result.pop("target_allocations", [])
            if selection_enabled:
                l2_result["candidate_input_invalid"] = not _complete_candidate_input(raw_allocs)
            l2_allocs = _normalize_allocations(raw_allocs, pc_map, score_map, muji_v2=muji_v2)
            if sector_advisory:
                sector_alternatives = _separate_sector_alternatives(
                    l2_result, l2_allocs, pc_map, total_value, sector_context if policy_context else None,
                    muji_v2=muji_v2, sell_forced=sell_forced,
                )
            for a in l2_allocs:
                a["estimated_amount"] = round((a["allocation_change_percent"] / 100) * total_value)
            _note_prompt(advisory, _LAYER_L2, "SUCCESS")
            for a in l2_allocs:
                _observe(advisory, a["symbol"], None, a, stage=_STAGE_L2, source=_SRC_ADVISORY,
                         effect=_ORIGINATE, reason_code="L2_ALLOCATION", reason_text=a.get("reason", ""))
            l2_result["target_allocations"] = l2_allocs
            if "portfolio_assessment" in l2_result and "summary" not in l2_result:
                l2_result["summary"] = l2_result["portfolio_assessment"]
            if "cash_balance_target" in l2_result and "target_cash_weight" not in l2_result:
                l2_result["target_cash_weight"] = l2_result["cash_balance_target"]
            # If L1 failed, L2 cannot meaningfully agree with it — mark disagreement
            if l1_parse_failed:
                l2_result["agrees_with_layer1"] = False
                if not sector_advisory:
                    l2_result.setdefault("disagreements", []).insert(
                        0, "L1_PARSE_FAILURE: Strategist output could not be parsed — treating as disagreement."
                    )
                l2_result["strategist_parse_failed"] = True
            logger.info(
                "[L2_DEBUG] status=%s allocs_count=%d agrees_with_layer1=%s strategist_parse_failed=%s",
                l2_result.get("status"),
                len(l2_allocs),
                l2_result.get("agrees_with_layer1"),
                l2_result.get("strategist_parse_failed", False),
            )
        except Exception as e:
            logger.error("[L2_DEBUG] parse_error=%s", e)
            _note_prompt(advisory, _LAYER_L2, "FAILED")
            l2_result = {
                "error": str(e), "agrees_with_layer1": False,
                "disagreements": [] if sector_advisory else ["L2_PARSE_FAILURE: Challenger output could not be parsed."],
                "target_allocations": [],
            }
            l2_latency_ms = 0

        candidate_envelope = None
        if selection_enabled:
            try:
                candidate_envelope = strategic_candidates.prepare_candidates(
                    portfolio_data, watchlist_data, cash_balance, l2_result,
                    regime=regime_context, goals=goal_decision_input,
                    source_layer="CHALLENGER_DEGRADED" if l1_parse_failed or "error" in l2_result else "CHALLENGER",
                )
                for candidate in candidate_envelope["candidates"]:
                    if candidate["eligibility_status"] != "ELIGIBLE":
                        continue
                    trial = deepcopy(candidate["proposed_allocations"])
                    _enforce_hard_policy(trial, total_value=total_value,
                                         policy_context=policy_context,
                                         regime_context=regime_context, muji_v2=True)
                    if any((a.get("action"), a.get("target_weight")) !=
                           (b.get("action"), b.get("target_weight"))
                           for a, b in zip(candidate["proposed_allocations"], trial)):
                        candidate["eligibility_status"] = "INELIGIBLE"
                        candidate["eligibility_reasons"].append("HARD_SAFEGUARD_CONFLICT")
                    if candidate["family"] != "HOLD" and any(
                        row.get("symbol") in locked and row.get("action") not in ("HOLD", "WATCH")
                        for row in candidate["proposed_allocations"]
                    ):
                        candidate["eligibility_status"] = "INELIGIBLE"
                        candidate["eligibility_reasons"].append("MANDATORY_LOCK_CONFLICT")
            except Exception as exc:
                candidate_envelope = {"version": "wealth.strategic-candidates.v1",
                                      "status": "UNAVAILABLE", "candidates": [],
                                      "reason": "CANDIDATE_PREPARATION_FAILED",
                                      "error_type": type(exc).__name__}

        # Layer 3 — Risk Auditor
        _emit_stage(on_stage, "LAYER3_ARBITRATION")
        # Evaluate the proposal with the existing policy calculator; do not enforce
        # or change allocations here. This evidence is distinct from final governance.
        proposal_details = []
        if policy_context:
            from services.optimizer.policy_engine import compute_policy_alignment_score
            proposal_details = compute_policy_alignment_score(
                l2_result.get("target_allocations", []), _make_envelope_from_dict(policy_context),
                total_value, frozen_positions=frozen_positions,
                effective_turnover_cap=_relaxed_turn_cap,
            )[4]
        claim_contract = build_claim_evidence(l2_result.get("target_allocations", []),
                                              proposal_details, execution_context,
                                              risk_inputs={p["symbol"]: p for p in [*portfolio_data, *watchlist_data]})
        claim_contract["general_policy_limits"] = dict((policy_context or {}).get("hard_constraints", {}))
        if muji_v2:
            claim_contract["general_policy_limits"].pop("max_single_position_pct", None)
        if sector_advisory:
            claim_contract["general_policy_limits"].pop("max_sector_pct", None)
            projected = project_targets(frozen_positions, l2_result.get("target_allocations", []), total_value)
            target = evaluate_frozen_sectors(sector_context, projected, "PROJECTED_TARGET")
            claim_contract["sector_advisories"] = {
                row["evidence_id"]: row
                for evaluation in (sector_context["current"], target)
                for row in evaluation["sectors"] if row["breach_pp"]
            }
        # Only a prepared envelope can be reviewed; any other state fails closed below.
        review_candidates = bool(selection_enabled and candidate_envelope
                                 and candidate_envelope.get("status") == "PREPARED_NOT_SELECTED")
        try:
            l3_prompt = _layer3_prompt(l1_result, l2_result, l3_cfg.get("role", ""), max_sector_pct=max_sector_pct,
                               execution_context=execution_context,
                               claim_contract=claim_contract,
                               persona_context=persona_context,
                               policy_context=policy_context,
                               effective_envelope=effective_envelope,
                               t1_breach_note=_t1_note, muji_v2=muji_v2,
                                goal_decision_input=goal_decision_input if muji_v2 else None,
                               **({"intent_block": _intent_block(advisory, _LAYER_L3)}
                                  if advisory is not None else {}),
                               **({"candidate_review_block": _candidate_review_block(candidate_envelope)}
                                  if review_candidates else {}))
            l3_raw = call_ai(
                l3_prompt,
                l3_cfg["provider"], l3_cfg["model"],
                max_tokens=_LAYER3_SELECTION_MAX_TOKENS if review_candidates else 2048,
                usage_operation="optimize", usage_layer="layer3",
            )
            l3_latency_ms = l3_raw["latency_ms"]
            l3_result = safe_parse_json(l3_raw["text"])
            _note_prompt(advisory, _LAYER_L3, "SUCCESS")
        except Exception as e:
            _note_prompt(advisory, _LAYER_L3, "FAILED")
            l3_result = {
                "error": str(e), "risk_flags": [],
                "safer_choice": "layer1", "final_risk_level": "medium", "auditor_notes": "",
            }
            l3_latency_ms = 0

        l3_result = validate_auditor_claims(l3_result, claim_contract)
        candidate_audit = (validate_candidate_reviews(l3_result.get("raw_model_output"), candidate_envelope)
                           if selection_enabled and candidate_envelope.get("status") == "PREPARED_NOT_SELECTED"
                           else {"status": "UNAVAILABLE", "reason": "CANDIDATE_ENVELOPE_UNAVAILABLE", "reviews": {}})

        # If L2 produced no allocations all three layers failed — trigger global fallback
        if "error" in l2_result and not l2_result.get("target_allocations"):
            raise RuntimeError(
                f"L2 allocation plan empty after all layers attempted. L2 error: {l2_result.get('error')}"
            )

        consensus = _consensus_engine(
            l1_result, l2_result, l3_result, sector_advisory=sector_advisory, muji_v2=muji_v2,
            sell_forced=sell_forced,
        )
        strategy_selection = None
        if selection_enabled:
            hold_candidate = next((c for c in candidate_envelope.get("candidates", [])
                                   if c.get("id") == "hold-current"), None)
            hold_safe = bool(hold_candidate and hold_candidate.get("eligibility_status") == "ELIGIBLE")
            floor_pct = (policy_context or {}).get("hard_constraints", {}).get("min_cash_pct")
            if floor_pct is not None and total_value > 0 and cash_balance / total_value * 100 < floor_pct:
                hold_safe = False
            committee_result = None
            failure_reason = None
            actionable = [c for c in candidate_envelope.get("candidates", [])
                          if c.get("family") != "HOLD" and c.get("eligibility_status") == "ELIGIBLE"]
            if not actionable:
                failure_reason = "NO_ELIGIBLE_ACTION"
            if candidate_audit["status"] == "AVAILABLE" and hold_safe and actionable:
                try:
                    committee_prompt = (
                        "You are the existing portfolio Committee. Compare the frozen candidates "
                        "qualitatively against HOLD. Consider supported thesis, risk and exposure, "
                        "liquidity, selected goals, trading friction, opposing evidence, and uncertainty. "
                        "Only cite references verified by the Auditor. An actionable choice must explain "
                        "why it is preferable to HOLD; scores are not return forecasts. "
                        "Return JSON with selected_candidate_id, supporting_evidence_refs, "
                        "opposing_evidence_refs, comparison_against_hold, decision_rationale, "
                        "material_uncertainty.\nCANDIDATES=" + json.dumps(candidate_envelope, default=str)
                        + "\nAUDITOR=" + json.dumps(candidate_audit, default=str)
                    )
                    committee_raw = call_ai(committee_prompt, l3_cfg["provider"], l3_cfg["model"],
                                            max_tokens=2048, usage_operation="optimize",
                                            usage_layer="committee")
                    committee_result = safe_parse_json(committee_raw["text"])
                except Exception as exc:
                    failure_reason = "COMMITTEE_UNAVAILABLE:" + type(exc).__name__
            strategy_selection = decide_selection(candidate_envelope, candidate_audit,
                                                  committee_result, hold_safe=hold_safe,
                                                  failure_reason=failure_reason)
            consensus["strategy_selection_state"] = strategy_selection["state"]
            consensus["recommended"] = strategy_selection["selected_candidate_id"] or "human_review"
            consensus["recommended_action"] = (strategy_selection.get("decision_rationale")
                                               or "Human review required; no candidate selected.")
        if sector_advisory:
            l2_result["agrees_with_layer1"] = consensus.pop("challenger_agrees")
            l2_result["disagreements"] = consensus["disagreement_reasons"]
            l2_result["unscored_comments"] = consensus.pop("unscored_challenger_comments")

        # ── Policy governance scoring (3B.4) ───────────────────────────────────
        # Populated after final_allocations are known; policy_context may be None.
        # We store placeholders now and fill them in below after constraint enforcement.
        _policy_scores_pending = bool(policy_context)

        # XAI metadata — extracted from L2 with safe defaults
        xai_status              = l2_result.get("status", "REBALANCE")
        xai_score               = int(l2_result.get("rebalance_opportunity_score") or 50)
        xai_no_action_reason    = l2_result.get("no_action_reason")
        xai_no_action_summary   = l2_result.get("no_action_summary")
        xai_blocked             = l2_result.get("blocked_opportunities", [])

        # Older runs retain Challenger ownership. Only explicit Phase 3 selection transfers it.
        final_allocations = l2_result.get("target_allocations", [])
        final_cash_weight = l2_result.get("target_cash_weight", 0.0)
        final_summary = l2_result.get("summary", l2_result.get("portfolio_assessment", ""))
        if selection_enabled:
            selected_id = strategy_selection["selected_candidate_id"]
            selected = next((c for c in candidate_envelope.get("candidates", [])
                             if c.get("id") == selected_id), None)
            final_allocations = deepcopy(selected["proposed_allocations"]) if selected else []
            final_cash_weight = ((selected or {}).get("cash_intent") or {}).get(
                "value", (cash_balance / total_value * 100 if total_value else 0.0))
            final_summary = strategy_selection.get("decision_rationale") or "Human review required; no actionable allocation selected."
            xai_status = "NO_ACTION" if selected_id == "hold-current" else "REBALANCE" if selected else "REVIEW"
            xai_no_action_reason = "INSUFFICIENT_EDGE" if selected_id == "hold-current" else None
            xai_no_action_summary = final_summary if selected_id == "hold-current" else None

        # Enforce constraints regardless of AI output
        locked_set = set(locked)
        alloc_map: dict[str, dict] = {a["symbol"]: a for a in final_allocations}
        _apply_forced_and_locked(alloc_map, [] if selection_enabled else sell_forced,
                                 locked_set, pc_map, advisory)

        final_allocations = list(alloc_map.values())

        # Recompute change% and THB amounts in Python — never trust AI-reported monetary values
        for a in final_allocations:
            _apply_score_context(a, score_map, a["symbol"])
            a["allocation_change_percent"] = round(a["target_weight"] - a["current_weight"], 2)
            a["estimated_amount"] = round((a["allocation_change_percent"] / 100) * total_value)

        # ── Policy and regime hard constraints ────────────────
        _observer_kw = {"observer": advisory} if advisory is not None else {}
        try:
            _enforce_hard_policy(
                final_allocations,
                total_value=total_value,
                policy_context=policy_context,
                regime_context=regime_context,
                muji_v2=muji_v2,
                **_observer_kw,
            )
        except Exception as exc:
            if enforce_effective_policy_in_fallback:
                raise HardPolicyEnforcementError("primary hard-policy enforcement failed") from exc
            raise

        # ── Phase 3B.10 — Execution quality cap enforcement ──────────────────
        # Applies per-asset position caps for DR and illiquid assets.
        # This is a SOFT enforcement: reduces target_weight to the cap but never
        # hard-rejects the asset. Runs after all other constraint enforcement.
        if execution_context:
            per_sym_exec = execution_context.get("per_symbol", {})
            for a in final_allocations:
                if a.get("action") not in ("BUY", "ACCUMULATE"):
                    continue
                sym = a.get("symbol", "")
                sym_exec = per_sym_exec.get(sym, {})
                cap = sym_exec.get("position_cap_pct")   # None = no reduced cap
                if cap is not None and a.get("target_weight", 0) > cap:
                    logger.info(
                        "[EXEC_CAP] %s target_weight %.1f%% → %.1f%% (DR/illiquid cap)",
                        sym, a["target_weight"], cap,
                    )
                    _before = _alloc_basis(a)
                    a["target_weight"]             = round(cap, 2)
                    a["allocation_change_percent"] = round(a["target_weight"] - a["current_weight"], 2)
                    a["estimated_amount"]          = round((a["allocation_change_percent"] / 100) * total_value)
                    a["execution_capped"]          = True
                    _observe(advisory, sym, _before, a, stage=_STAGE_EXEC_CAP, source=_SRC_POLICY,
                             effect=_SCALE, reason_code="EXECUTION_QUALITY_CAP",
                             reason_text=f"Capped at the {cap:.1f}% DR/illiquid position limit.")

        # Attach per-symbol execution metadata to allocations for frontend badge rendering
        if execution_context:
            per_sym_exec = execution_context.get("per_symbol", {})
            for a in final_allocations:
                sym = a.get("symbol", "")
                if sym in per_sym_exec:
                    a["execution_risk"]     = per_sym_exec[sym].get("execution_risk", "LOW")
                    a["execution_warnings"] = per_sym_exec[sym].get("execution_warnings", [])
                    a["asset_type"]         = per_sym_exec[sym].get("asset_type", "EQUITY")
                    a["slippage_est_pct"]   = per_sym_exec[sym].get("slippage_cost_est_pct")

        # ── Post-enforcement action label reconciliation ──────────────────────
        # Constraint passes (policy cap, cash floor, DR exec cap and legacy sector cap) all
        # update target_weight + allocation_change_percent but never touch action.
        # A BUY/ACCUMULATE whose delta went negative is now a net REDUCE; fix it.
        if policy_context and not sector_advisory:
            _limit_sector_buys(final_allocations, total_value, policy_context, frozen_positions, advisory)
        _reconcile_allocation_actions(final_allocations, muji_v2=muji_v2, **_observer_kw)

        _snap_neutral_actions(final_allocations, **_observer_kw)

        if selection_enabled and strategy_selection["selected_candidate_id"]:
            original = next(c for c in candidate_envelope["candidates"]
                            if c["id"] == strategy_selection["selected_candidate_id"])
            before = {a["symbol"]: (a["action"], a["target_weight"])
                      for a in original["proposed_allocations"]}
            after = {a["symbol"]: (a["action"], a["target_weight"])
                     for a in final_allocations}
            if before != after:
                strategy_selection["downstream_outcome"] = {
                    "status": "ALTERED_BY_SAFEGUARDS", "original": before, "result": after,
                }
                if strategy_selection["selected_candidate_id"] == "hold-current" or any(
                    a["action"] in ("BUY", "ACCUMULATE") and a["allocation_change_percent"] < 0
                    or a["action"] in ("SELL", "REDUCE") and a["allocation_change_percent"] > 0
                    for a in final_allocations
                ):
                    strategy_selection["state"] = "HUMAN_REVIEW_REQUIRED"
                    strategy_selection["reason_codes"].append("DOWNSTREAM_PLAN_INCOHERENT")
                    final_allocations = []
                    xai_status = "REVIEW"
                    consensus["strategy_selection_state"] = "HUMAN_REVIEW_REQUIRED"
                    consensus["recommended"] = "human_review"
                    consensus["recommended_action"] = "Selected plan altered incoherently; human review required."
                    final_summary = consensus["recommended_action"]
            else:
                strategy_selection["downstream_outcome"] = {"status": "UNCHANGED"}

        # Defensive: auto-correct NO_ACTION when allocations contain real changes
        if xai_status == "NO_ACTION" and any(
            a.get("action") not in ("HOLD", "WATCH") or abs(a.get("allocation_change_percent", 0)) >= 1.0
            for a in final_allocations
        ):
            logger.warning(
                "[DEFENSIVE] status=NO_ACTION but %d allocations with changes — auto-correcting to REBALANCE",
                len(final_allocations),
            )
            xai_status = "REBALANCE"
            xai_no_action_reason = None
            xai_no_action_summary = None

        # ── Policy governance scores (fill in now that allocations are finalized) ─
        if _policy_scores_pending and policy_context:
            from services.optimizer.policy_engine import compute_policy_alignment_score, PolicyEnvelope
            pa_score, rc_score, rg_score, gov_flags, violation_details = compute_policy_alignment_score(
                final_allocations,
                _make_envelope_from_dict(policy_context),
                total_value,
                frozen_positions=frozen_positions,
                effective_turnover_cap=_relaxed_turn_cap,
            )
            consensus["policy_alignment_score"]  = pa_score
            consensus["regime_compliance_score"] = rc_score
            consensus["risk_governance_score"]   = rg_score
            consensus["governance_flags"]        = gov_flags
            consensus["violation_details"]       = violation_details
            # Downgrade consensus strength when genuine governance flags are raised.
            # Authorized turnover expansions (Tier 1 relaxation active) are controlled
            # policy-compliant events — exclude them so authorized behavior isn't penalized.
            if gov_flags:
                penalizable = gov_flags if _t1_severity == "NONE" else [
                    f for f in gov_flags
                    if not any(kw in f.lower() for kw in ("turnover", "tier3_efficiency"))
                ]
                penalty = min(20, len(penalizable) * 6)
                if penalty > 0:
                    consensus["consensus_strength_score"] = max(
                        5, consensus.get("consensus_strength_score", 50) - penalty
                    )
                logger.info(
                    "[POLICY_GOV] flags=%d penalizable=%d strength_penalty=-%d t1_severity=%s",
                    len(gov_flags), len(penalizable), penalty, _t1_severity,
                )

        # Auto-generate summary when empty but allocations exist
        if not final_summary and final_allocations:
            action_counts: dict[str, int] = {}
            for a in final_allocations:
                act = a.get("action", "HOLD")
                action_counts[act] = action_counts.get(act, 0) + 1
            summary_parts = [f"{act}×{cnt}" for act, cnt in sorted(action_counts.items()) if act not in ("HOLD", "WATCH")]
            if summary_parts:
                final_summary = f"Proposed changes: {', '.join(summary_parts)} across {len(final_allocations)} positions."

        logger.info(
            "[PIPELINE_FINAL] status=%s allocs_count=%d summary_len=%d swap_suggestions_count_pre=%d",
            xai_status, len(final_allocations), len(final_summary or ""),
            len(l1_result.get("swap_suggestions", [])),
        )

        swap_suggestions = _derive_swap_suggestions(final_allocations,
                                                    [] if selection_enabled else sell_forced, locked)
        projected_sector_weights = calculate_projected_sector_weights_from_allocations(
            portfolio_data, final_allocations, total_value
        )
        sector_warnings = _compute_sector_warnings(
            current_sector_weights, projected_sector_weights, sector_limits, max_sector_pct
        )

        total_latency_ms = l1_latency_ms + l2_latency_ms + l3_latency_ms
        buy_symbols = [a["symbol"] for a in final_allocations if a.get("action") in ("BUY", "ACCUMULATE")]
        watchlist_ranking = _rebuild_watchlist_ranking(buy_symbols, wc)

        persona_fields: dict = {}
        if persona_context:
            persona_fields = {
                "target_persona":         persona_context.get("persona"),
                "persona_label":          persona_context.get("persona_label"),
                "current_portfolio_dna":  persona_context.get("portfolio_dna"),
                "style_drift_score":      persona_context.get("drift_score"),
                "style_drift_severity":   persona_context.get("drift_severity"),
                "factor_alignment_score": persona_context.get("factor_alignment_score"),
                "factor_drift":           persona_context.get("factor_drift"),
                "rebalance_urgency":      persona_context.get("rebalance_urgency"),
            }

        # Strip prompt_block from policy_context before surfacing to API (it's large)
        active_policy_out: dict | None = None
        if policy_context:
            active_policy_out = {k: v for k, v in policy_context.items() if k != "prompt_block"}
            active_policy_out["policy_alignment_score"]  = consensus.get("policy_alignment_score")
            active_policy_out["regime_compliance_score"] = consensus.get("regime_compliance_score")
            active_policy_out["risk_governance_score"]   = consensus.get("risk_governance_score")
            active_policy_out["governance_flags"]        = consensus.get("governance_flags", [])
            active_policy_out["violation_details"]       = consensus.get("violation_details", [])
            # Phase 3B.6 — Tier 1 turnover relaxation metadata
            active_policy_out["turnover_relaxation_active"] = _t1_severity != "NONE"
            active_policy_out["turnover_relaxation_reason"] = _t1_reason if _t1_severity != "NONE" else None
            active_policy_out["relaxed_turnover_cap"]       = _relaxed_turn_cap if _t1_severity != "NONE" else None

        output = {
            "portfolio_name": portfolio_name,
            "status": xai_status,
            "rebalance_opportunity_score": xai_score,
            "no_action_reason": xai_no_action_reason,
            "no_action_summary": xai_no_action_summary,
            "blocked_opportunities": xai_blocked,
            "portfolio_assessment": final_summary,
            "optimization_notes": consensus["recommended_action"],
            "target_allocations": final_allocations,
            "target_cash_weight": final_cash_weight,
            "portfolio_turnover_percent": sum(
                abs(a["allocation_change_percent"]) for a in final_allocations
            ),
            "swap_suggestions": swap_suggestions,
            "watchlist_ranking": watchlist_ranking,
            "portfolio_count": portfolio_count,
            "max_reached": max_reached,
            "max_stocks": max_stocks,
            "cash_balance": cash_balance,
            "total_value": round(total_value, 2),
            "ai_provider": l1_cfg["provider"],
            "ai_model": l1_cfg["model"],
            "current_sector_weights": current_sector_weights,
            "projected_sector_weights": projected_sector_weights,
            "sector_warnings": sector_warnings,
            "layer1_latency_ms": l1_latency_ms,
            "layer2_latency_ms": l2_latency_ms,
            "layer3_latency_ms": l3_latency_ms,
            "total_latency_ms": total_latency_ms,
            "layer1_result": {
                **l1_result,
                "provider": l1_cfg["provider"], "model": l1_cfg["model"], "name": l1_cfg.get("name", "Strategist"),
            },
            "layer2_result": {
                **l2_result,
                "provider": l2_cfg["provider"], "model": l2_cfg["model"], "name": l2_cfg.get("name", "Challenger"),
            },
            "layer3_result": {
                **l3_result,
                "provider": l3_cfg["provider"], "model": l3_cfg["model"], "name": l3_cfg.get("name", "Risk Auditor"),
            },
            "consensus": consensus,
            "active_policy": active_policy_out,
            # Phase 3B.5 — resolved constraint breakdown (None when resolver not run)
            "effective_envelope": _eff_env_to_dict(effective_envelope) if effective_envelope else None,
            **persona_fields,
        }
        _capture_sector_policy(output, active_policy_out, sector_policy_mode, portfolio_data, watchlist_data,
                               total_value, degraded_policy, sector_alternatives, optimizer_policy_mode)
        if selection_enabled:
            output["strategic_candidates"] = candidate_envelope
            output["strategy_selection"] = strategy_selection
            output["candidate_audit"] = candidate_audit
            output["active_policy"]["strategy_selection_mode"] = strategy_selection_mode
        elif muji_v2:
            from services.optimizer.strategic_candidates import VERSION
            try:
                output["strategic_candidates"] = strategic_candidates.prepare_candidates(
                    portfolio_data, watchlist_data, cash_balance, l2_result,
                    regime=regime_context, goals=goal_decision_input,
                    source_layer="CHALLENGER_DEGRADED" if l1_parse_failed or "error" in l3_result else "CHALLENGER",
                )
            except Exception as exc:
                logger.exception("MUJI candidate preparation unavailable: %s", exc)
                output["strategic_candidates"] = {
                    "version": VERSION, "status": "UNAVAILABLE", "goal_context_version":
                    (goal_decision_input or {}).get("contract_version"), "candidates": [],
                    "reason": "CANDIDATE_PREPARATION_FAILED",
                }
        return output

    except HardPolicyEnforcementError:
        raise
    except Exception as exc:
        logger.critical(
            f"Multi-layer pipeline failed. Initiating Global Fallback Model: "
            f"{fallback_provider}/{fallback_model}. Error: {exc}"
        )
        if advisory is not None:
            # Primary-attempt proposals are abandoned: never active, never a conflict.
            advisory.abandon_attempt(_ATTEMPT_PRIMARY)
            advisory.begin_attempt(_ATTEMPT_FALLBACK)
        return _run_single_shot_fallback(
            pc, wc, sell_forced, locked, portfolio_data, current_sector_weights,
            pc_map, max_stocks, max_sector_pct, sector_limits,
            total_value, cash_balance, fallback_provider, fallback_model,
            portfolio_name, portfolio_count, max_reached,
            policy_context=({**policy_context, "relaxed_turnover_cap": _relaxed_turn_cap}
                            if policy_context else None),
            effective_envelope=effective_envelope,
            enforce_effective_policy=enforce_effective_policy_in_fallback,
            sector_policy_mode=sector_policy_mode,
            optimizer_policy_mode=optimizer_policy_mode,
            execution_context=execution_context,
            muji_policy_block=muji_policy_block,
            goal_decision_input=goal_decision_input if muji_v2 else None,
            regime_context=regime_context if muji_v2 else None,
            strategy_selection_mode=strategy_selection_mode,
            **({"advisory": advisory} if advisory is not None else {}),
        )
