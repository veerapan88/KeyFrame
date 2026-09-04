"""Demo fixture data, shaped like Airtable records ({"id": ..., "fields": {...}}),
matching the example data in design/KeyFrame Wireframes.dc.html.

Used by data.py whenever Airtable isn't configured yet, so the app is fully
clickable from the start. Once AIRTABLE_TOKEN/AIRTABLE_BASE_ID are set and
backend/create_airtable_schema.py has been run, data.py reads real records
instead and this file stops being consulted.

Screening Fee dates are computed relative to "now" (not hardcoded) so the
refund countdown always looks like a live demo, whenever this is run.
"""

from datetime import datetime, timedelta

_NOW = datetime.now()

PROPERTY = {
    "id": "prop_a_unit2",
    "fields": {
        "Name": "Property A · Unit 2",
        "Address": "1400 W Example Ave, Unit 2",
        "Jurisdiction": "CA",
        "Fee Amount": 52.00,
        "Income Ratio Min": 3.0,
        "Credit Score Min": 650,
        "Eviction Lookback Years": 5,
        "Occupancy Max": 3,
        "Pet Policy": "Cats permitted, no dogs",
        "Smoking Policy": "No smoking",
        "Criteria Published": True,
    },
}

TRUSTED_INDIVIDUAL = {
    "id": "ti_1",
    "fields": {"Name": "Trusted Individual 1", "Phone": "+15551234567"},
}

LEADS = [
    {"id": "lead_01", "fields": {"Name": "Lead 01", "Status": "showed", "No Show Count": 0}},
    {"id": "lead_02", "fields": {"Name": "Lead 02", "Status": "showed", "No Show Count": 0}},
    {"id": "lead_03", "fields": {"Name": "Lead 03", "Status": "showing_scheduled", "No Show Count": 2}},
    {"id": "lead_04", "fields": {"Name": "Lead 04", "Status": "showed", "No Show Count": 0}},
    {"id": "lead_05", "fields": {"Name": "Lead 05", "Status": "qualified", "No Show Count": 0}},
    {"id": "lead_06", "fields": {"Name": "Lead 06", "Status": "qualified", "No Show Count": 0}},
    {"id": "lead_08", "fields": {"Name": "Lead 08", "Status": "qualified", "No Show Count": 0}},
]

SHOWINGS = [
    {"id": "show_1", "fields": {"Label": "Lead 01 · Mar 4, 10:00", "Lead": ["lead_01"],
                                 "Host": ["ti_1"], "Datetime": "2026-03-04T10:00:00",
                                 "Status": "confirmed", "No Show": False}},
    {"id": "show_2", "fields": {"Label": "Lead 02 · Mar 4, 11:30", "Lead": ["lead_02"],
                                 "Host": ["ti_1"], "Datetime": "2026-03-04T11:30:00",
                                 "Status": "confirmed", "No Show": False}},
    {"id": "show_3", "fields": {"Label": "Lead 03 · Mar 5, 09:00", "Lead": ["lead_03"],
                                 "Host": [], "Datetime": "2026-03-05T09:00:00",
                                 "Status": "scheduled", "No Show": False}},
    {"id": "show_4", "fields": {"Label": "Lead 04 · Mar 5, 14:00", "Lead": ["lead_04"],
                                 "Host": [], "Datetime": "2026-03-05T14:00:00",
                                 "Status": "completed", "No Show": True}},
    {"id": "show_5", "fields": {"Label": "Lead 05 · Mar 3, 15:00", "Lead": ["lead_05"],
                                 "Host": ["ti_1"], "Datetime": "2026-03-03T15:00:00",
                                 "Status": "completed", "No Show": False}},
]

HOST_READS = [
    {"id": "hr_lead01", "fields": {"Label": "Lead 01 read", "Showing": ["show_1"],
                                    "Showed Up": "Yes", "Would Rent": "Yes",
                                    "Notes": "Liked the layout, asked about parking.",
                                    "Guard Status": "cleared"}},
    {"id": "hr_lead02", "fields": {"Label": "Lead 02 read", "Showing": ["show_2"],
                                    "Showed Up": "Yes", "Would Rent": "Maybe",
                                    "Notes": "", "Guard Status": "pending"}},
    {"id": "hr_lead04", "fields": {"Label": "Lead 04 read", "Showing": ["show_4"],
                                    "Showed Up": "No", "Would Rent": None,
                                    "Notes": "", "Guard Status": "cleared"}},
    {"id": "hr_lead05", "fields": {"Label": "Lead 05 read", "Showing": ["show_5"],
                                    "Showed Up": "Yes", "Would Rent": "Yes",
                                    "Notes": "", "Guard Status": "pending"}},
]

APPLICATIONS = [
    {"id": "app_a", "fields": {"Name": "Applicant A", "Lead": ["lead_01"],
                                "Property": ["prop_a_unit2"], "Status": "submitted",
                                "Portable Report Used": False, "Selected": False,
                                "Applicant Token": "demo-token-a"}},
    {"id": "app_b", "fields": {"Name": "Applicant B", "Lead": ["lead_02"],
                                "Property": ["prop_a_unit2"], "Status": "submitted",
                                "Portable Report Used": False, "Selected": False,
                                "Applicant Token": "demo-token-b"}},
    {"id": "app_c", "fields": {"Name": "Applicant C", "Lead": ["lead_05"],
                                "Property": ["prop_a_unit2"], "Status": "submitted",
                                "Portable Report Used": True, "Selected": False,
                                "Applicant Token": "demo-token-c"}},
]

SCREENINGS = [
    {"id": "scr_a", "fields": {"Label": "Applicant A screening", "Application": ["app_a"],
                                "Status": "complete", "Income Pass": True, "Credit Pass": True,
                                "Credit Score": 710, "Eviction Pass": True, "Move In Pass": True,
                                "Occupancy Pass": True, "Pet Pass": True}},
    {"id": "scr_b", "fields": {"Label": "Applicant B screening", "Application": ["app_b"],
                                "Status": "complete", "Income Pass": True, "Credit Pass": False,
                                "Credit Score": 612, "Eviction Pass": True, "Move In Pass": True,
                                "Occupancy Pass": True, "Pet Pass": True}},
    {"id": "scr_c", "fields": {"Label": "Applicant C screening", "Application": ["app_c"],
                                "Status": "pending", "Income Pass": None, "Credit Pass": None,
                                "Credit Score": None, "Eviction Pass": None, "Move In Pass": None,
                                "Occupancy Pass": None, "Pet Pass": None}},
]

# Two demo moments: before a decision (screening in progress, 1d) and after
# Applicant A is selected (1e/1f). `SELECTED_APPLICATION_ID = None` renders
# the "in progress" state; set it to "app_a" to render the post-selection state.
SELECTED_APPLICATION_ID = "app_a"

SCREENING_FEES = [
    {"id": "fee_a", "fields": {"Name": "Fee — Applicant A", "Application": ["app_a"],
                                "Amount": 52.00,
                                "Submitted At": (_NOW - timedelta(days=6)).isoformat(),
                                "Status": "charged", "Portable Report Used": False}},
    {"id": "fee_b", "fields": {"Name": "Fee — Applicant B", "Application": ["app_b"],
                                "Amount": 52.00,
                                "Submitted At": (_NOW - timedelta(days=6)).isoformat(),
                                "Status": "refund_failed", "Refund Trigger": "selected_other",
                                "Portable Report Used": False,
                                "Stripe Charge Id": "ch_demo_applicant_b",
                                "Competitor Selected At": (_NOW - timedelta(days=2)).isoformat()}},
    {"id": "fee_c", "fields": {"Name": "Fee — Applicant C", "Application": ["app_c"],
                                "Amount": None, "Status": None,
                                "Portable Report Used": True}},
]

VENDORS = [
    {"id": "vendor_2", "fields": {"Name": "Vendor 2", "Trade": "electrical", "Times Used": 3}},
]

TICKETS = [
    {"id": "ticket_014", "fields": {
        "Name": "Ticket 014", "Property": ["prop_a_unit2"],
        "Description": "Kitchen outlets dead", "Since": "This morning",
        "Tried": "GFCI reset, breaker — no change",
        "Suspected Cause": "Failed GFCI or upstream wiring",
        "Urgency": "Same week · not a hazard",
        "Status": "triaging", "Vendor": ["vendor_2"],
    }},
]
