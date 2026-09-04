from flask import Blueprint, flash, redirect, render_template, request, url_for

import airtable_client as at
import data
from config import config
from services import stripe_refunds

bp = Blueprint("applications", __name__, url_prefix="/applications")


@bp.route("/invite")
def batch_invite():
    view = data.batch_invite_candidates()
    return render_template("dashboard/batch_invite.html", **view)


@bp.route("/invite/confirm", methods=["POST"])
def batch_invite_confirm():
    selected_ids = request.form.getlist("lead_id")
    view = data.batch_invite_candidates()
    prop = view["property"]
    fee = prop["fields"].get("Fee Amount", 0) if prop else 0
    return render_template(
        "dashboard/invite_interstitial.html",
        property=prop,
        inviting=len(selected_ids),
        fee=fee,
        selected_ids=selected_ids,
    )


@bp.route("/invite/send", methods=["POST"])
def batch_invite_send():
    # Phase 0 concierge: the actual invite SMS is sent by the landlord
    # themselves (PRD B2.2 pattern). This just records the invite in
    # Airtable when it's connected; the demo just moves on.
    if config.airtable_configured:
        for lead_id in request.form.getlist("lead_id"):
            at.create_record(at.TABLE_APPLICATION, {
                "Lead": [lead_id],
                "Status": "invited",
            })
    flash("Invites sent.")
    return redirect(url_for("applications.matrix"))


@bp.route("/")
def matrix():
    view = data.applications_matrix()
    if view["selected_id"]:
        return render_template(
            "dashboard/applications_selected.html",
            **view,
            refund_rows=data.refund_rows(),
        )
    return render_template("dashboard/applications_matrix.html", **view)


@bp.route("/<application_id>/select", methods=["POST"])
def select(application_id):
    if config.airtable_configured:
        at.update_record(at.TABLE_APPLICATION, application_id, {"Selected": True})
    flash("Applicant selected. Refunds for everyone else are now processing.")
    return redirect(url_for("applications.matrix"))


@bp.route("/refund-failure")
def refund_failure():
    failure = data.refund_failure()
    if not failure:
        return redirect(url_for("applications.matrix"))
    return render_template("dashboard/refund_failure.html", failure=failure,
                            stripe_ready=stripe_refunds.refund_is_available())


@bp.route("/refund-failure/retry", methods=["POST"])
def refund_failure_retry():
    charge_id = request.form.get("stripe_charge_id")
    amount_cents = int(float(request.form.get("amount", 0)) * 100)
    try:
        stripe_refunds.execute_refund(charge_id, amount_cents)
        flash("Refund retried successfully.")
    except stripe_refunds.RefundNotConfigured:
        flash("Stripe isn't configured yet — add STRIPE_SECRET_KEY to .env to enable this.")
    except stripe_refunds.LiveModeRejected as e:
        flash(str(e))
    except Exception as e:  # noqa: BLE001 — surface to the landlord, don't swallow
        flash(f"Refund failed again: {e}")
    return redirect(url_for("applications.refund_failure"))
