from flask import Blueprint, render_template

bp = Blueprint("sms", __name__, url_prefix="/chat/sms")


@bp.route("/")
def index():
    return render_template("dashboard/sms_index.html")


@bp.route("/lead")
def lead_thread():
    return render_template("dashboard/sms_lead.html")


@bp.route("/trusted-individual")
def ti_thread():
    return render_template("dashboard/sms_trusted_individual.html")


@bp.route("/tenant")
def tenant_thread():
    return render_template("dashboard/sms_tenant.html")
