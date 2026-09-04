"""Stripe Connect refund execution — isolated so the rest of the app never
calls the Stripe SDK directly.

Only runs against Stripe **test mode** (config.STRIPE_SECRET_KEY starting
with "sk_test_"). A live-mode key is rejected outright: this build hasn't
been reviewed for real money movement, and Phase 0's "real Stripe" posture
in the PRD refers to the actual pilot operation once the team is ready for
it, not to development/testing here.
"""

import stripe

from config import config


class RefundNotConfigured(Exception):
    pass


class LiveModeRejected(Exception):
    pass


def refund_is_available() -> bool:
    return config.stripe_configured and config.STRIPE_SECRET_KEY.startswith("sk_test_")


def execute_refund(stripe_charge_id: str, amount_cents: int) -> dict:
    """Issues a refund for a previously-charged application fee.

    Returns the Stripe Refund object (as a dict) on success. Raises on any
    failure — callers are expected to write the failure back to the
    Screening Fee record's status (refund_failed) rather than swallow it,
    per A5-S11's "must not silently fail" requirement.
    """
    if not config.stripe_configured:
        raise RefundNotConfigured("STRIPE_SECRET_KEY is not set in .env yet.")
    if not config.STRIPE_SECRET_KEY.startswith("sk_test_"):
        raise LiveModeRejected(
            "Refusing to run against a non-test-mode Stripe key. Use a "
            "sk_test_... key until this integration has been reviewed."
        )

    stripe.api_key = config.STRIPE_SECRET_KEY
    refund = stripe.Refund.create(charge=stripe_charge_id, amount=amount_cents)
    return refund.to_dict()
