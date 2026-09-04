"""One-time script: creates the KeyFrame Airtable schema inside an existing
(empty) base via the Airtable Meta API.

Usage:
    1. In Airtable, create a new blank base. Copy its base ID from the URL
       (starts with "app..."). Put it in .env as AIRTABLE_BASE_ID.
    2. Put a Personal Access Token with data.records:read/write and
       schema.bases:write scopes, for that base, in .env as AIRTABLE_TOKEN.
    3. Run: python backend/create_airtable_schema.py
    4. Delete the base's default "Table 1" by hand afterward if it's empty —
       the API can't delete the table it's forced to create by default.

Safe to inspect before running: this only creates tables/fields, it never
deletes or overwrites existing ones. Re-running after partial completion
will fail on tables that already exist — check the base in Airtable first.
"""

from pyairtable import Api

from config import config

SELECT = lambda *names: {"choices": [{"name": n} for n in names]}  # noqa: E731

TABLES = [
    {
        "name": "Property",
        "fields": [
            {"name": "Name", "type": "singleLineText"},
            {"name": "Address", "type": "singleLineText"},
            {"name": "Jurisdiction", "type": "singleSelect",
             "options": SELECT("CA", "Chicago-Cook", "IL-other")},
            {"name": "Fee Amount", "type": "currency",
             "options": {"precision": 2, "symbol": "$"}},
            {"name": "Income Ratio Min", "type": "number",
             "options": {"precision": 1}},
            {"name": "Credit Score Min", "type": "number",
             "options": {"precision": 0}},
            {"name": "Eviction Lookback Years", "type": "number",
             "options": {"precision": 0}},
            {"name": "Move In By", "type": "date",
             "options": {"dateFormat": {"name": "us"}}},
            {"name": "Occupancy Max", "type": "number",
             "options": {"precision": 0}},
            {"name": "Pet Policy", "type": "singleLineText"},
            {"name": "Smoking Policy", "type": "singleLineText"},
            {"name": "Criteria Published", "type": "checkbox",
             "options": {"icon": "check", "color": "greenBright"}},
        ],
    },
    {
        "name": "Trusted Individual",
        "fields": [
            {"name": "Name", "type": "singleLineText"},
            {"name": "Phone", "type": "phoneNumber"},
            {"name": "Availability Notes", "type": "multilineText"},
        ],
    },
    {
        "name": "Lead",
        "fields": [
            {"name": "Name", "type": "singleLineText"},
            {"name": "Phone", "type": "phoneNumber"},
            {"name": "Status", "type": "singleSelect", "options": SELECT(
                "new", "pre-qualifying", "qualified", "declined",
                "showing_scheduled", "showed", "invited_to_apply",
            )},
            {"name": "No Show Count", "type": "number",
             "options": {"precision": 0}},
        ],
    },
    {
        "name": "Showing",
        "fields": [
            {"name": "Label", "type": "singleLineText"},
            {"name": "Datetime", "type": "dateTime", "options": {
                "dateFormat": {"name": "us"},
                "timeFormat": {"name": "12hour"},
                "timeZone": "client",
            }},
            {"name": "Status", "type": "singleSelect",
             "options": SELECT("scheduled", "confirmed", "completed")},
            {"name": "No Show", "type": "checkbox",
             "options": {"icon": "check", "color": "redBright"}},
        ],
    },
    {
        "name": "Host Read",
        "fields": [
            {"name": "Label", "type": "singleLineText"},
            {"name": "Showed Up", "type": "singleSelect",
             "options": SELECT("Yes", "No")},
            {"name": "Would Rent", "type": "singleSelect",
             "options": SELECT("Yes", "No", "Maybe")},
            {"name": "Notes", "type": "multilineText"},
            {"name": "Guard Status", "type": "singleSelect",
             "options": SELECT("pending", "cleared")},
        ],
    },
    {
        "name": "Application",
        "fields": [
            {"name": "Name", "type": "singleLineText"},
            {"name": "Status", "type": "singleSelect", "options": SELECT(
                "invited", "submitted", "fee_pending", "portable_report",
            )},
            {"name": "Portable Report Used", "type": "checkbox",
             "options": {"icon": "check", "color": "blueBright"}},
            {"name": "Selected", "type": "checkbox",
             "options": {"icon": "check", "color": "greenBright"}},
            {"name": "Applicant Token", "type": "singleLineText"},
        ],
    },
    {
        "name": "Screening",
        "fields": [
            {"name": "Label", "type": "singleLineText"},
            {"name": "Status", "type": "singleSelect",
             "options": SELECT("pending", "complete")},
            {"name": "Income Pass", "type": "checkbox",
             "options": {"icon": "check", "color": "greenBright"}},
            {"name": "Credit Pass", "type": "checkbox",
             "options": {"icon": "check", "color": "greenBright"}},
            {"name": "Credit Score", "type": "number",
             "options": {"precision": 0}},
            {"name": "Eviction Pass", "type": "checkbox",
             "options": {"icon": "check", "color": "greenBright"}},
            {"name": "Move In Pass", "type": "checkbox",
             "options": {"icon": "check", "color": "greenBright"}},
            {"name": "Occupancy Pass", "type": "checkbox",
             "options": {"icon": "check", "color": "greenBright"}},
            {"name": "Pet Pass", "type": "checkbox",
             "options": {"icon": "check", "color": "greenBright"}},
        ],
    },
    {
        # Field list per PRD §6, verbatim.
        "name": "Screening Fee",
        "fields": [
            {"name": "Name", "type": "singleLineText"},
            {"name": "Stripe Charge Id", "type": "singleLineText"},
            {"name": "Amount", "type": "currency",
             "options": {"precision": 2, "symbol": "$"}},
            {"name": "Submitted At", "type": "dateTime", "options": {
                "dateFormat": {"name": "us"},
                "timeFormat": {"name": "24hour"},
                "timeZone": "client",
            }},
            {"name": "Deadline By Submission", "type": "date",
             "options": {"dateFormat": {"name": "us"}}},
            {"name": "Competitor Selected At", "type": "dateTime", "options": {
                "dateFormat": {"name": "us"},
                "timeFormat": {"name": "24hour"},
                "timeZone": "client",
            }},
            {"name": "Deadline By Selection", "type": "date",
             "options": {"dateFormat": {"name": "us"}}},
            {"name": "Effective Deadline", "type": "date",
             "options": {"dateFormat": {"name": "us"}}},
            {"name": "Status", "type": "singleSelect", "options": SELECT(
                "charged", "report_delivered", "selected", "unselected",
                "refund_initiated", "refunded", "refund_failed",
            )},
            {"name": "Refund Trigger", "type": "singleSelect", "options": SELECT(
                "selected_other", "withdrew", "listing_removed",
            )},
            {"name": "Portable Report Used", "type": "checkbox",
             "options": {"icon": "check", "color": "blueBright"}},
        ],
    },
    {
        "name": "Vendor",
        "fields": [
            {"name": "Name", "type": "singleLineText"},
            {"name": "Trade", "type": "singleLineText"},
            {"name": "Phone", "type": "phoneNumber"},
            {"name": "Times Used", "type": "number",
             "options": {"precision": 0}},
        ],
    },
    {
        "name": "Ticket",
        "fields": [
            {"name": "Name", "type": "singleLineText"},
            {"name": "Description", "type": "multilineText"},
            {"name": "Since", "type": "singleLineText"},
            {"name": "Tried", "type": "multilineText"},
            {"name": "Suspected Cause", "type": "singleLineText"},
            {"name": "Urgency", "type": "singleLineText"},
            {"name": "Status", "type": "singleSelect", "options": SELECT(
                "reported", "triaging", "dispatched", "in_progress", "closed",
            )},
        ],
    },
    {
        "name": "Message Log",
        "fields": [
            {"name": "Label", "type": "singleLineText"},
            {"name": "Party", "type": "singleLineText"},
            {"name": "Channel", "type": "singleSelect",
             "options": SELECT("SMS", "chat", "email")},
            {"name": "Body", "type": "multilineText"},
            {"name": "Related Record", "type": "singleLineText"},
            {"name": "Timestamp", "type": "dateTime", "options": {
                "dateFormat": {"name": "us"},
                "timeFormat": {"name": "24hour"},
                "timeZone": "client",
            }},
        ],
    },
]

# (table_name, field_name, type, linked_table_name)
LINK_FIELDS = [
    ("Trusted Individual", "Property", "Property"),
    ("Lead", "Property", "Property"),
    ("Showing", "Lead", "Lead"),
    ("Showing", "Host", "Trusted Individual"),
    ("Host Read", "Showing", "Showing"),
    ("Application", "Lead", "Lead"),
    ("Application", "Property", "Property"),
    ("Screening", "Application", "Application"),
    ("Screening Fee", "Application", "Application"),
    ("Ticket", "Property", "Property"),
    ("Ticket", "Vendor", "Vendor"),
]


def main():
    if not config.AIRTABLE_TOKEN or not config.AIRTABLE_BASE_ID:
        raise SystemExit(
            "Set AIRTABLE_TOKEN and AIRTABLE_BASE_ID in .env first "
            "(see .env.example)."
        )

    api = Api(config.AIRTABLE_TOKEN)
    base = api.base(config.AIRTABLE_BASE_ID)

    existing = {t.name: t.id for t in base.schema().tables}
    table_ids = dict(existing)

    for spec in TABLES:
        if spec["name"] in existing:
            print(f"skip (exists): {spec['name']}")
            continue
        created = base.create_table(spec["name"], spec["fields"])
        table_ids[spec["name"]] = created.id
        print(f"created table: {spec['name']}")

    for table_name, field_name, _type, linked_table_name in LINK_FIELDS:
        t = base.table(table_name)
        existing_fields = {f.name for f in t.schema().fields}
        if field_name in existing_fields:
            print(f"skip (exists): {table_name}.{field_name}")
            continue
        t.create_field(
            field_name,
            "multipleRecordLinks",
            options={"linkedTableId": table_ids[linked_table_name]},
        )
        print(f"linked field: {table_name}.{field_name} -> {linked_table_name}")

    print("\nDone. If Airtable created a default 'Table 1' when the base was "
          "made, delete it by hand from the Airtable UI — the API can't.")


if __name__ == "__main__":
    main()
