import functools
import os

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

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        # TODO This isn't really going to work when more than 1 user exists
        g.user = {
            "id": os.environ.get("USER_ID"),
            "username": os.environ.get("USER_NAME"),
        }


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        user = None

        # TODO Also this stuff won't really work when more than 1 user exists
        if username == os.environ.get("USER_NAME"):
            user = {
                "id": os.environ.get("USER_ID"),
                "username": os.environ.get("USER_NAME"),
            }

        if user is None:
            error = "Incorrect username."
        elif not password == user["USER_PW"]:
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
