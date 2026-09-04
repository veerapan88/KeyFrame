from flask import Blueprint, redirect, render_template, url_for

import data

bp = Blueprint("stub", __name__)


@bp.route("/properties")
def properties():
    return render_template("dashboard/properties.html", property=data.current_property())


@bp.route("/chat")
def chat():
    return redirect(url_for("sms.index"))


@bp.route("/settings")
def settings():
    return render_template("dashboard/settings.html", vendors=data.vendors())
