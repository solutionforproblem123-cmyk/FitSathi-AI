# ==========================================================
# FitFusion AI - routes/profile_routes.py
# ----------------------------------------------------------
# Handles:
#   - View Profile
#   - Update Profile
# ==========================================================

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from database import db
from models import User

from services.profile_service import (
    get_profile,
    update_profile,
    get_profile_summary
)


def init_profile_routes(app):

    @app.route("/profile", methods=["GET", "POST"])
    def profile():

        # ---------------------------------------
        # Login Required
        # ---------------------------------------

        if "user_id" not in session:

            flash(
                "Please login first.",
                "error"
            )

            return redirect(
                url_for("login")
            )

        user = get_profile(
            session["user_id"]
        )

        if user is None:

            session.clear()

            return redirect(
                url_for("login")
            )

        # ---------------------------------------
        # Update Profile
        # ---------------------------------------

        if request.method == "POST":

            try:

                update_profile(

                    user,

                    request.form["full_name"],

                    int(request.form["age"]),

                    request.form["gender"],

                    float(request.form["height"]),

                    float(request.form["weight"]),

                    request.form["goal"],

                    request.form["experience"],

                    int(request.form["workout_days"]),

                    request.form["activity_level"]

                )

                flash(

                    "Profile updated successfully.",

                    "success"

                )

                return redirect(
                    url_for("profile")
                )

            except Exception as e:

                db.session.rollback()

                print(e)

                flash(

                    "Unable to update profile.",

                    "error"

                )

        profile = get_profile_summary(user)

        return render_template(

            "profile.html",

            user=user

        )