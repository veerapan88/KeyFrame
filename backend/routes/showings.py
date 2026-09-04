from flask import Blueprint, render_template

import data

bp = Blueprint("showings", __name__, url_prefix="/showings")


@bp.route("/")
def index():
    return render_template("dashboard/showings.html", grouped=data.showings_by_day())


@bp.route("/reads")
def reads():
    return render_template("dashboard/host_reads.html", cards=data.host_read_cards())
