"""Pure Liability historical-balance rules (Phase 5 — no ORM, no DB session)."""


def liability_balance_as_of(observations, as_of_date: str) -> float | None:
    """Effective-state lookup: the latest observation with observed_on <= as_of_date.

    `observations` is an iterable of `(observed_on, balance)` tuples for one
    Liability, in any order and unfiltered; this function alone owns the
    eligibility rule. Dates are plain ISO `YYYY-MM-DD` strings, which sort
    lexicographically identically to calendar order.

    Returns None ("unavailable") when no observation exists on or before
    as_of_date — history before the first observation does not exist and must
    never be reported as zero or forward-filled from a later value. Derives
    exclusively from dated observations: never reads a Liability's current
    `balance`, `created_at`, or `updated_at`.
    """
    eligible = [(observed_on, balance) for observed_on, balance in observations if observed_on <= as_of_date]
    if not eligible:
        return None
    return max(eligible, key=lambda pair: pair[0])[1]
