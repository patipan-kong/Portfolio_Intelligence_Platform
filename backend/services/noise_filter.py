"""Presentation-layer noise filter for optimizer recommendations.

Converts micro-rebalance BUY/SELL/ACCUMULATE/REDUCE actions to HOLD when the
recommended change is too small to be meaningful for a real investor.

Applied to the HTTP response only — DB records (history, signal history,
recommendation snapshots) retain the unfiltered optimizer output.
"""
from __future__ import annotations

from services.optimizer.sector_policy import OPTIMIZER_POLICY_MUJI_V2, optimizer_policy_mode

DRIFT_THRESHOLD_PCT = 1.0   # Rule A: abs(target_weight - current_weight) < 1.0%
MIN_TRADE_VALUE_THB = 5000  # Rule B: abs(estimated_amount) < 5,000 THB
DRIFT_NOISE_REASON = "สัดส่วนปัจจุบันใกล้เคียงเป้าหมายแล้ว"

_SUPPRESSIBLE = {"BUY", "SELL", "ACCUMULATE", "REDUCE"}


def apply_noise_filter(result: dict, *, replay: bool = False) -> dict:
    """Suppress micro-rebalance actions in target_allocations in-place.

    Rule A — drift < DRIFT_THRESHOLD_PCT: position already close enough to target (legacy only).
    Rule B — trade value < MIN_TRADE_VALUE_THB: trade too small to execute.
    If either rule fires, action is set to HOLD with a Thai explanation.

    Returns the same dict (mutated) for convenience.
    """
    muji_v2 = optimizer_policy_mode(
        result.get("active_policy") or {}, effective_envelope=result.get("effective_envelope"),
    ) == OPTIMIZER_POLICY_MUJI_V2
    # Slice 1 already used the MUJI marker but still applied the drift veto.
    if replay and not (result.get("stabilization") or {}).get("drift_advisory"):
        muji_v2 = False
    for alloc in result.get("target_allocations") or []:
        action = (alloc.get("action") or "").upper()
        if action not in _SUPPRESSIBLE:
            continue

        drift = abs(alloc.get("allocation_change_percent") or 0)
        trade_val = abs(alloc.get("estimated_amount") or 0)

        if not muji_v2 and drift < DRIFT_THRESHOLD_PCT:
            alloc["action"] = "HOLD"
            alloc["noise_suppressed"] = True
            alloc["noise_reason"] = DRIFT_NOISE_REASON
        elif trade_val < MIN_TRADE_VALUE_THB:
            alloc["action"] = "HOLD"
            alloc["noise_suppressed"] = True
            alloc["noise_reason"] = "มูลค่าที่ต้องปรับมีขนาดเล็กมาก"

    return result
