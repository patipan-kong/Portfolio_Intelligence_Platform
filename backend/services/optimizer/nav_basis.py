"""Single source of truth for optimizer position weights on the NAV basis.

NAV = sum(shares x price) + cash. A position weight is value / NAV x 100,
carried at full precision. Callers round only for display or for an
established output contract (allocation rows keep 2 dp).

Why this exists: weights were once equity-only (value / sum of position
values) while L2 targets, ``total_value`` and every amount are NAV based.
That mixed denominators in ``target - current`` and let a cash-heavy
portfolio report a concentration breach that did not exist on NAV
(history 219: MICRON01.BK 22.2% equity-only, 15.73% of NAV).

Sector weights deliberately stay on their existing equity-only basis for this
hotfix (see docs/implementation/NAV_BASIS_HOTFIX.md).
"""
from __future__ import annotations

from dataclasses import dataclass, field

BASIS_NAV = "NAV"


def item_price(item: dict) -> float:
    """Price rule shared with the legacy weight helper: live quote, else cost."""
    return float(item.get("current_price") or item.get("avg_cost") or 0)


def item_value(item: dict) -> float:
    return float(item.get("shares") or 0) * item_price(item)


@dataclass(frozen=True)
class NavBasis:
    nav: float
    equity: float
    cash: float
    values: dict[str, float] = field(default_factory=dict)

    @property
    def usable(self) -> bool:
        return self.nav > 0

    def weight_pct(self, symbol: str) -> float:
        """Unrounded percent of NAV (0.0 when the basis is unusable)."""
        if not self.usable:
            return 0.0
        return self.values.get(symbol, 0.0) / self.nav * 100.0


def compute_nav_basis(items: list[dict], cash_balance: float | None) -> NavBasis:
    cash = float(cash_balance or 0.0)
    values: dict[str, float] = {}
    for item in items:
        sym = item.get("symbol")
        values[sym] = values.get(sym, 0.0) + item_value(item)
    equity = sum(values.values())
    return NavBasis(nav=equity + cash, equity=equity, cash=cash, values=values)
