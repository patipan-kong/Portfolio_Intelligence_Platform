"""Scoring projection; new runs validate claims before reaching this boundary.

Unknown/raw flags are unscored. Historical reads return frozen scores and do
not recompute them through this function.
"""

OWNER_INTENT_REVIEW = "OWNER_INTENT_REVIEW"


def investment_risk_flags(flags: list[dict]) -> list[dict]:
    """Keep investment risk separate from reviewable owner disagreement.

    Never classify from prose or from a symbol also having an Intent conflict:
    the same position may independently have real investment risk.
    """
    return [flag for flag in flags if flag.get("category") == "INVESTMENT_RISK"
            and flag.get("scoring_eligible") is True
            and flag.get("validation_status") == "VERIFIED"
            and isinstance(flag.get("provenance"), dict)
            and isinstance(flag.get("evidence_ref"), str)]
