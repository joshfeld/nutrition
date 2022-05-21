from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

bp = Blueprint("calorie", __name__, url_prefix="/calorie")


@bp.route("/tracker", methods=("GET", "POST"))
def tracker():
    return render_template("calorie/tracker.html")
