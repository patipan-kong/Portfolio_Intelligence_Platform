"""Small pure rules for the prospective CashAccount ledger."""
from __future__ import annotations


INCOME = "INCOME"
EXPENSE = "EXPENSE"
ADJUSTMENT = "ADJUSTMENT"


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
    raise ValueError(f"Unsupported cash transaction type: {transaction_type}")


def resulting_balance(current_balance: float, transaction_type: str, amount: float) -> float:
    return current_balance + signed_amount(transaction_type, amount)
