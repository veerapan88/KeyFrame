from flask import Blueprint, redirect, render_template, url_for

import data

bp = Blueprint("tickets", __name__, url_prefix="/tickets")


@bp.route("/")
def index():
    ticket_id = data.first_ticket_id()
    if not ticket_id:
        return render_template("dashboard/tickets_empty.html")
    return redirect(url_for("tickets.detail", ticket_id=ticket_id))


@bp.route("/<ticket_id>")
def detail(ticket_id):
    view = data.ticket_with_vendor(ticket_id)
    if not view:
        return render_template("dashboard/tickets_empty.html"), 404
    return render_template("dashboard/ticket_detail.html", **view)
