"""Data-access layer for the dashboard/applicant routes.

Every function here reads from real Airtable when config.airtable_configured
is True, and from backend/seed_data.py otherwise — so the app is fully
clickable before Airtable credentials exist, and starts reading real data
the moment they're added to .env, with no route/template changes needed.
"""

from datetime import datetime
from typing import Optional

import airtable_client as at
import seed_data
from config import config
from services.refund_engine import compute_deadline, format_countdown


def _all(table_name: str, seed_list: list) -> list:
    if config.airtable_configured:
        return at.list_records(table_name)
    return seed_list


def _by_id(records: list, record_id: Optional[str]):
    if not record_id:
        return None
    return next((r for r in records if r["id"] == record_id), None)


def _linked(records: list, link_ids: Optional[list]):
    link_ids = link_ids or []
    return [_by_id(records, rid) for rid in link_ids if _by_id(records, rid)]


def _first_linked(records: list, link_ids: Optional[list]):
    linked = _linked(records, link_ids)
    return linked[0] if linked else None


# --- raw table accessors -------------------------------------------------

def properties():
    return _all(at.TABLE_PROPERTY, [seed_data.PROPERTY])


def trusted_individuals():
    return _all(at.TABLE_TRUSTED_INDIVIDUAL, [seed_data.TRUSTED_INDIVIDUAL])


def leads():
    return _all(at.TABLE_LEAD, seed_data.LEADS)


def showings():
    return _all(at.TABLE_SHOWING, seed_data.SHOWINGS)


def host_reads():
    return _all(at.TABLE_HOST_READ, seed_data.HOST_READS)


def applications():
    return _all(at.TABLE_APPLICATION, seed_data.APPLICATIONS)


def screenings():
    return _all(at.TABLE_SCREENING, seed_data.SCREENINGS)


def screening_fees():
    return _all(at.TABLE_SCREENING_FEE, seed_data.SCREENING_FEES)


def vendors():
    return _all(at.TABLE_VENDOR, seed_data.VENDORS)


def tickets():
    return _all(at.TABLE_TICKET, seed_data.TICKETS)


def current_property():
    props = properties()
    return props[0] if props else None


def selected_application_id() -> Optional[str]:
    """Which application (if any) has been selected — drives whether the
    applications screen renders the mid-screening (1d) or post-selection
    (1e/1f) state."""
    for app in applications():
        if app["fields"].get("Selected"):
            return app["id"]
    if not config.airtable_configured:
        return seed_data.SELECTED_APPLICATION_ID
    return None


# --- pipeline (1a/1i) ------------------------------------------------------

def pipeline_view():
    all_leads = leads()
    statuses = [l["fields"].get("Status") for l in all_leads]

    def count(*wanted):
        return sum(1 for s in statuses if s in wanted)

    showed_leads = []
    for lead in all_leads:
        if lead["fields"].get("Status") not in ("showed",):
            continue
        lead_showings = [
            s for s in showings()
            if lead["id"] in (s["fields"].get("Lead") or [])
        ]
        showing = lead_showings[0] if lead_showings else None
        lead_reads = [
            hr for hr in host_reads()
            if showing and showing["id"] in (hr["fields"].get("Showing") or [])
        ]
        read = lead_reads[0] if lead_reads else None
        showed_leads.append({
            "lead": lead,
            "showing": showing,
            "host_read": read,
            "no_show": lead["fields"].get("No Show Count", 0) >= 2,
        })

    return {
        "property": current_property(),
        "counts": {
            "inquiries": len(all_leads),
            "auto_declined": count("declined"),
            "qualified": count("qualified", "showing_scheduled", "showed", "invited_to_apply"),
            "showed": count("showed"),
            "interviewed": count("invited_to_apply"),
        },
        "showed_leads": showed_leads,
    }


# --- batch invite (1b/1c) --------------------------------------------------

def batch_invite_candidates():
    """Leads worth considering for an invite: showed up (or not yet shown,
    i.e. status=qualified with no showing yet) — a confirmed no-show is
    excluded, matching the pipeline's "Next" column logic."""
    prop = current_property()
    rows = []
    for lead in leads():
        if lead["fields"].get("Status") not in ("showed", "qualified"):
            continue
        lead_showings = [s for s in showings() if lead["id"] in (s["fields"].get("Lead") or [])]
        showing = lead_showings[0] if lead_showings else None
        lead_reads = [hr for hr in host_reads() if showing and showing["id"] in (hr["fields"].get("Showing") or [])]
        read = lead_reads[0] if lead_reads else None
        if read and read["fields"].get("Showed Up") == "No":
            continue
        rows.append({
            "lead": lead,
            "host_read_label": (read["fields"].get("Would Rent") if read else "—"),
            "interview_done": bool(read),
        })
    return {"property": prop, "candidates": rows}


# --- applications / comparison / refunds (1d/1e/1f/1j) ---------------------

def applications_matrix():
    prop = current_property()
    apps = applications()
    scr = screenings()
    fees = screening_fees()
    reads = host_reads()
    leads_ = leads()

    rows = []
    for app in apps:
        app_screening = next(
            (s for s in scr if app["id"] in (s["fields"].get("Application") or [])), None
        )
        app_fee = next(
            (f for f in fees if app["id"] in (f["fields"].get("Application") or [])), None
        )
        lead = _first_linked(leads_, app["fields"].get("Lead"))
        lead_showings = [s for s in showings() if lead and lead["id"] in (s["fields"].get("Lead") or [])]
        showing = lead_showings[0] if lead_showings else None
        read = next((r for r in reads if showing and showing["id"] in (r["fields"].get("Showing") or [])), None)

        rows.append({
            "application": app,
            "screening": app_screening,
            "fee": app_fee,
            "host_read": read,
        })

    invited = len(rows)
    results_in = sum(1 for r in rows if r["screening"] and r["screening"]["fields"].get("Status") == "complete")

    return {
        "property": prop,
        "rows": rows,
        "invited": invited,
        "results_in": results_in,
        "pending": invited - results_in,
        "selected_id": selected_application_id(),
    }


def refund_rows():
    """The 'not selected — refunds' table for 1e, plus the 1f failure state."""
    matrix = applications_matrix()
    selected_id = matrix["selected_id"]
    if not selected_id:
        return []

    rows = []
    for row in matrix["rows"]:
        app = row["application"]
        if app["id"] == selected_id:
            continue
        fee = row["fee"]
        if not fee:
            continue
        fee_fields = fee["fields"]
        if fee_fields.get("Portable Report Used"):
            rows.append({
                "application": app,
                "fee_display": "none (portable)",
                "status": "n/a",
                "countdown": "—",
                "notified": "Decline sent",
            })
            continue

        submitted_at = fee_fields.get("Submitted At")
        selected_at = fee_fields.get("Competitor Selected At")
        deadline = None
        if submitted_at:
            deadline = compute_deadline(
                submitted_at=datetime.fromisoformat(submitted_at),
                competitor_selected_at=datetime.fromisoformat(selected_at) if selected_at else None,
            )
        rows.append({
            "application": app,
            "fee_display": f"${fee_fields.get('Amount', 0):.0f}",
            "status": fee_fields.get("Status", "charged"),
            "countdown": format_countdown(deadline.days_remaining) if deadline else "—",
            "notified": "Sent on signing",
            "stripe_charge_id": fee_fields.get("Stripe Charge Id", ""),
        })
    return rows


def refund_failure():
    """Demo data for the A5-S11 interruptive alert (1f) — the applicant
    whose refund needs a backup payment method."""
    for row in refund_rows():
        if row["status"] == "refund_failed":
            return row
    return None


# --- showings (1g) ----------------------------------------------------------

def showings_by_day():
    leads_ = leads()
    tis = trusted_individuals()
    grouped: dict = {}
    for s in sorted(showings(), key=lambda r: r["fields"].get("Datetime", "")):
        dt = s["fields"].get("Datetime")
        if not dt:
            continue
        day = datetime.fromisoformat(dt).strftime("%a · %b %-d")
        lead = _first_linked(leads_, s["fields"].get("Lead"))
        host = _first_linked(tis, s["fields"].get("Host"))
        grouped.setdefault(day, []).append({
            "time": datetime.fromisoformat(dt).strftime("%H:%M"),
            "lead": lead,
            "host": host,
            "status": s["fields"].get("Status"),
            "no_show": s["fields"].get("No Show"),
        })
    return grouped


# --- host read (1h) ---------------------------------------------------------

def host_read_cards():
    return host_reads()


# --- tickets (1r) ------------------------------------------------------------

def ticket_with_vendor(ticket_id: str):
    t = _by_id(tickets(), ticket_id)
    if not t:
        return None
    vendor = _first_linked(vendors(), t["fields"].get("Vendor"))
    return {"ticket": t, "vendor": vendor}


def first_ticket_id() -> Optional[str]:
    all_tickets = tickets()
    return all_tickets[0]["id"] if all_tickets else None


# --- applicant hosted-link pages (1k/1l/1m/1n) -------------------------------

def application_by_token(token: str):
    for app in applications():
        if app["fields"].get("Applicant Token") == token:
            prop = _first_linked(properties(), app["fields"].get("Property"))
            return {"application": app, "property": prop}
    return None
