"""Structured L3 evidence boundary; unclassified legacy flags remain risk flags."""

OWNER_INTENT_REVIEW = "OWNER_INTENT_REVIEW"


def investment_risk_flags(flags: list[dict]) -> list[dict]:
    """Keep investment risk separate from reviewable owner disagreement.

    Never classify from prose or from a symbol also having an Intent conflict:
    the same position may independently have real investment risk.
    """
    return [flag for flag in flags if flag.get("category") != OWNER_INTENT_REVIEW]
