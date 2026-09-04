"""Thin wrapper around pyairtable. One function per table used by this app.

If AIRTABLE_TOKEN / AIRTABLE_BASE_ID aren't set, `config.airtable_configured`
is False and callers should fall back to backend/seed_data.py instead of
calling anything here — that's what lets the app run and be clicked through
before real Airtable credentials exist.
"""

from pyairtable import Api

from config import config

TABLE_PROPERTY = "Property"
TABLE_LEAD = "Lead"
TABLE_TRUSTED_INDIVIDUAL = "Trusted Individual"
TABLE_SHOWING = "Showing"
TABLE_HOST_READ = "Host Read"
TABLE_APPLICATION = "Application"
TABLE_SCREENING = "Screening"
TABLE_SCREENING_FEE = "Screening Fee"
TABLE_TICKET = "Ticket"
TABLE_VENDOR = "Vendor"
TABLE_MESSAGE_LOG = "Message Log"

_api = None


def _get_api() -> Api:
    global _api
    if _api is None:
        _api = Api(config.AIRTABLE_TOKEN)
    return _api


def table(name: str):
    if not config.airtable_configured:
        raise RuntimeError(
            "Airtable isn't configured yet — set AIRTABLE_TOKEN and "
            "AIRTABLE_BASE_ID in .env before calling airtable_client.table()."
        )
    return _get_api().table(config.AIRTABLE_BASE_ID, name)


def list_records(table_name: str, **kwargs):
    return table(table_name).all(**kwargs)


def get_record(table_name: str, record_id: str):
    return table(table_name).get(record_id)


def create_record(table_name: str, fields: dict):
    return table(table_name).create(fields)


def update_record(table_name: str, record_id: str, fields: dict):
    return table(table_name).update(record_id, fields)


def find_by_field(table_name: str, field_name: str, value: str):
    """Returns the first record where field_name == value, or None."""
    formula = f"{{{field_name}}} = '{value}'"
    records = table(table_name).all(formula=formula, max_records=1)
    return records[0] if records else None
