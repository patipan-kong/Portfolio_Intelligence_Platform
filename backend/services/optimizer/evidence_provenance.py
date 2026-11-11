"""Evidence provenance for the Committee evidence catalog (MUJI V2 Slice 4.2).

Records, from data the optimizer already loads, whether each analysis value a
row carries was actually observed or is a default standing in for a missing,
failed or disabled analysis. Pure functions; no I/O, no decision authority.

Statuses: OBSERVED, MISSING (no analysis or no value), FAILED (the analysis
returned an error or an unusable label), DISABLED (the source is switched off).
"""

from __future__ import annotations

from math import isfinite

OBSERVED = "OBSERVED"
MISSING = "MISSING"
FAILED = "FAILED"
DISABLED = "DISABLED"

VALID_SIGNALS = frozenset({"ACCUMULATE", "BUY", "WATCH", "HOLD", "REDUCE", "SELL"})


def analysis_provenance(result, field: str, *, enabled: bool, source: str) -> dict:
    """Provenance of one score field from a technical/fundamental agent result.

    A genuine numeric value, including 0, is OBSERVED.
    """
    if not enabled:
        return {"status": DISABLED}
    if not result:
        return {"status": MISSING, "source": source}
    if "error" in result:
        return {"status": FAILED, "source": source}
    value = result.get(field)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        return {"status": MISSING, "source": source}
    return {"status": OBSERVED, "source": source}


def signal_provenance(cache_row) -> dict:
    """Provenance of a symbol's analysis signal from its AnalysisCache row (or None)."""
    if cache_row is None:
        return {"status": MISSING, "source": "ANALYSIS_CACHE"}
    if getattr(cache_row, "signal", None) not in VALID_SIGNALS:
        return {"status": FAILED, "source": "ANALYSIS_CACHE"}
    record = {"status": OBSERVED, "source": "ANALYSIS_CACHE"}
    analyzed_at = getattr(cache_row, "analyzed_at", None)
    if analyzed_at is not None:
        record["as_of"] = analyzed_at.isoformat()
    return record


def timing_provenance(timing_context) -> dict:
    """Provenance of a symbol's timing score; observed only when price data existed."""
    available = timing_context is not None and getattr(timing_context, "data_available", False) is True
    return {"status": OBSERVED if available else MISSING, "source": "TIMING_INTELLIGENCE"}
