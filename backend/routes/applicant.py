from flask import Blueprint, render_template

import data

bp = Blueprint("applicant", __name__, url_prefix="/apply")


@bp.route("/<token>")
def disclosure(token):
    view = data.application_by_token(token)
    if not view:
        return render_template("applicant/hardblock.html", token=token)
    prop = view["property"]
    if not prop or not prop["fields"].get("Criteria Published"):
        return render_template("applicant/hardblock.html", token=token)
    return render_template("applicant/disclosure.html", **view)


@bp.route("/<token>/pay")
def pay(token):
    view = data.application_by_token(token)
    return render_template("applicant/payment.html", **(view or {}), token=token)


@bp.route("/<token>/portable-report")
def portable_report(token):
    view = data.application_by_token(token)
    return render_template("applicant/portable_report.html", **(view or {}), token=token)


@bp.route("/<token>/receipt")
def receipt(token):
    view = data.application_by_token(token)
    return render_template("applicant/receipt.html", **(view or {}), token=token)


@bp.route("/<token>/deposit")
def deposit(token):
    view = data.application_by_token(token)
    prop = view["property"] if view else None
    jurisdiction = prop["fields"].get("Jurisdiction") if prop else "CA"
    return render_template("applicant/deposit.html", **(view or {}), token=token,
                            jurisdiction=jurisdiction)
