"""Refund-deadline computation (PRD §4 A5.4, §6 Screening Fee).

Deliberately pure functions with no Airtable/Stripe calls, so the one piece
of logic in this build with a real statutory deadline and per-instance
penalty attached can be unit-tested in isolation.

Per the PRD:
- deadline_by_submission = submitted_at + 30 days
- deadline_by_selection  = competitor_selected_at + 7 days (only once a
  competitor has actually been selected — nullable until then)
- effective_deadline = the earlier of the two that are set
- There is no code path that skips, denies, or delays a refund. That's not
  a missing feature here — it's intentionally absent (see PRD §5, §10.3).
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Optional

SUBMISSION_WINDOW_DAYS = 30
SELECTION_WINDOW_DAYS = 7


@dataclass
class RefundDeadline:
    deadline_by_submission: date
    deadline_by_selection: Optional[date]
    effective_deadline: date
    days_remaining: int


def compute_deadline(
    submitted_at: datetime,
    competitor_selected_at: Optional[datetime] = None,
    as_of: Optional[date] = None,
) -> RefundDeadline:
    """Computes the refund deadline for one Screening Fee record.

    `competitor_selected_at` is None until the landlord selects a different
    applicant (or the applicant withdraws / listing is pulled — those events
    are treated the same way by the caller, which passes the trigger time
    here). Until then only the 30-day submission deadline applies.
    """
    as_of = as_of or date.today()

    deadline_by_submission = (submitted_at + timedelta(days=SUBMISSION_WINDOW_DAYS)).date()

    deadline_by_selection = None
    if competitor_selected_at is not None:
        deadline_by_selection = (
            competitor_selected_at + timedelta(days=SELECTION_WINDOW_DAYS)
        ).date()

    candidates = [deadline_by_submission]
    if deadline_by_selection is not None:
        candidates.append(deadline_by_selection)
    effective_deadline = min(candidates)

    days_remaining = (effective_deadline - as_of).days

    return RefundDeadline(
        deadline_by_submission=deadline_by_submission,
        deadline_by_selection=deadline_by_selection,
        effective_deadline=effective_deadline,
        days_remaining=days_remaining,
    )


def format_countdown(days_remaining: int) -> str:
    """Always renders as days remaining, never a raw date — per iA §10.3."""
    if days_remaining < 0:
        return f"{abs(days_remaining)} days overdue"
    if days_remaining == 0:
        return "due today"
    if days_remaining == 1:
        return "1 day left"
    return f"{days_remaining} days left"


TERMINAL_STATUSES = {"refunded"}
NO_REFUND_OWED_STATUSES: set = set()  # intentionally empty — see module docstring
