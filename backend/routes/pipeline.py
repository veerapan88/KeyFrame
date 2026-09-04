from flask import Blueprint, render_template

import data

bp = Blueprint("pipeline", __name__)


@bp.route("/")
@bp.route("/pipeline")
def index():
    view = data.pipeline_view()
    return render_template("dashboard/pipeline.html", **view)
