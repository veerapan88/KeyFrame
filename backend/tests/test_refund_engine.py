import os
import sys
import unittest
from datetime import date, datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.refund_engine import compute_deadline, format_countdown  # noqa: E402


class ComputeDeadlineTests(unittest.TestCase):
    def test_no_selection_yet_uses_30_day_submission_deadline(self):
        result = compute_deadline(
            submitted_at=datetime(2026, 1, 1),
            competitor_selected_at=None,
            as_of=date(2026, 1, 10),
        )
        self.assertEqual(result.deadline_by_submission, date(2026, 1, 31))
        self.assertIsNone(result.deadline_by_selection)
        self.assertEqual(result.effective_deadline, date(2026, 1, 31))
        self.assertEqual(result.days_remaining, 21)

    def test_selection_within_window_shortens_deadline_to_7_days_after_selection(self):
        # Selected on day 5 -> 7-day deadline (Jan 12) beats the 30-day one (Jan 31).
        result = compute_deadline(
            submitted_at=datetime(2026, 1, 1),
            competitor_selected_at=datetime(2026, 1, 5),
            as_of=date(2026, 1, 10),
        )
        self.assertEqual(result.deadline_by_selection, date(2026, 1, 12))
        self.assertEqual(result.effective_deadline, date(2026, 1, 12))
        self.assertEqual(result.days_remaining, 2)

    def test_late_selection_does_not_extend_past_30_day_deadline(self):
        # Selected on day 29 -> 7-day deadline (Jan 31) is later than the
        # 30-day one (Jan 31 too, in this case) — effective is the earlier
        # of the two, so it must never exceed the submission deadline.
        result = compute_deadline(
            submitted_at=datetime(2026, 1, 1),
            competitor_selected_at=datetime(2026, 1, 29),
            as_of=date(2026, 1, 30),
        )
        self.assertEqual(result.deadline_by_submission, date(2026, 1, 31))
        self.assertEqual(result.deadline_by_selection, date(2026, 2, 5))
        # earlier of Jan 31 and Feb 5 is Jan 31
        self.assertEqual(result.effective_deadline, date(2026, 1, 31))

    def test_overdue_is_negative_days_remaining(self):
        result = compute_deadline(
            submitted_at=datetime(2026, 1, 1),
            as_of=date(2026, 3, 1),
        )
        self.assertLess(result.days_remaining, 0)


class FormatCountdownTests(unittest.TestCase):
    def test_never_renders_a_raw_date(self):
        for days in (-3, -1, 0, 1, 2, 30):
            rendered = format_countdown(days)
            self.assertNotRegex(rendered, r"\d{4}-\d{2}-\d{2}")

    def test_wording(self):
        self.assertEqual(format_countdown(5), "5 days left")
        self.assertEqual(format_countdown(1), "1 day left")
        self.assertEqual(format_countdown(0), "due today")
        self.assertEqual(format_countdown(-2), "2 days overdue")


if __name__ == "__main__":
    unittest.main()
