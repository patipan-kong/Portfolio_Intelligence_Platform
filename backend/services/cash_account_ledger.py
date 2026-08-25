"""Small pure rules for the prospective CashAccount ledger."""
from __future__ import annotations


INCOME = "INCOME"
EXPENSE = "EXPENSE"
ADJUSTMENT = "ADJUSTMENT"
TRANSFER = "TRANSFER"


def signed_amount(transaction_type: str, amount: float) -> float:
    """Return the balance movement for a valid ledger transaction.

    INCOME and EXPENSE use positive stored magnitudes. ADJUSTMENT stores its
    signed difference so reconciliation can deterministically move either way.
    """
    if transaction_type == INCOME:
        return amount
    if transaction_type == EXPENSE:
        return -amount
    if transaction_type == ADJUSTMENT:
        return amount
    if transaction_type == TRANSFER:
        # Transfer legs store their signed balance effect directly: the source
        # leg is negative and the destination leg is positive.
        return amount
    raise ValueError(f"Unsupported cash transaction type: {transaction_type}")


def resulting_balance(current_balance: float, transaction_type: str, amount: float) -> float:
    return current_balance + signed_amount(transaction_type, amount)


def cash_balance_as_of(
    baseline_effective_on: str | None,
    baseline_observed_balance: float | None,
    events,
    as_of_date: str,
) -> float | None:
    """Reconstruct a CashAccount's historical balance as of a calendar date.

    Returns None ("unavailable") when there is no baseline, or when
    `as_of_date` predates `baseline_effective_on` — history before the
    explicit baseline observation does not exist and must never be reported
    as zero. `events` is an iterable of `(transaction_type, amount,
    occurred_on)` tuples for the account, in any order and unfiltered; this
    function alone owns the eligibility window
    (`baseline_effective_on <= occurred_on <= as_of_date`), so callers never
    duplicate that rule. Dates are plain ISO `YYYY-MM-DD` strings, which sort
    lexicographically identically to calendar order.

    Derives exclusively from dated evidence: never reads a CashAccount's
    current `balance`, `is_archived`, `created_at`, or `updated_at`.
    """
    if baseline_effective_on is None or baseline_observed_balance is None:
        return None
    if as_of_date < baseline_effective_on:
        return None
    total = baseline_observed_balance
    for transaction_type, amount, occurred_on in events:
        if baseline_effective_on <= occurred_on <= as_of_date:
            total += signed_amount(transaction_type, amount)
    return total
