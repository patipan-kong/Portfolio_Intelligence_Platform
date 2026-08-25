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
