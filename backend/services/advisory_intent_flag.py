"""Advisory Integration V1 (Slice 1): the single feature flag and contract names.

One default-OFF flag covers the whole integration as a unit: frozen Intent
context, the common-NAV projection basis, prompt context, proposal
provenance, deterministic Intent review, the frozen review envelope and the
response review fields. There is deliberately no finer-grained switch, so AI
Intent context can never run without the deterministic review.

Scope: /analyze/optimizer, existing positive held positions only. Position
sizing, risk budget, idea review and Decision Workspace are not Intent-aware.
"""
from __future__ import annotations

import os

FLAG_ENV = "FEATURE_ADVISORY_INTENT_REVIEW_V1"

REVIEW_CONTRACT_VERSION = "wealth.advisory-intent-review.v1"
PROJECTION_VERSION = "wealth.held-quantity-projection.v1"
ENABLED_SCOPE = "ANALYZE_OPTIMIZER_HELD_POSITIONS"

DISCLOSURE_DISABLED = (
    "Investor Intent V1 is saved for your records only. It is not yet read or "
    "enforced by the portfolio optimizer, and it does not change current recommendations."
)
DISCLOSURE_ENABLED = (
    "The portfolio optimizer reads your Investor Intent for positions you currently hold, "
    "as advisory context, and checks each recommendation against it. It does not block "
    "trades or change your records: a recommendation that disagrees with your intent is "
    "flagged for your decision. Other advisory tools (position sizing, risk budget, idea "
    "review, Decision Workspace) do not read your intent yet."
)


def advisory_intent_review_enabled() -> bool:
    """Default OFF; only the exact value "true" (any case) enables it.

    Read per call, matching FEATURE_ASSET_SEARCH's env-var-boolean convention.
    """
    return os.environ.get(FLAG_ENV, "false").strip().lower() == "true"


def intent_disclosure() -> str:
    return DISCLOSURE_ENABLED if advisory_intent_review_enabled() else DISCLOSURE_DISABLED
