# ==========================================================
# FitFusion AI - routes/progress_routes.py
# ----------------------------------------------------------
# Handles:
#   - Progress Tracker
#   - Save Progress
#   - Progress History
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
from services.gemini_service import generate_progress_analysis
from services.progress_service import (
    get_progress_summary,
    save_progress,
    get_progress_history,
    get_latest_progress,
    get_chart_data,
    get_progress_statistics
)

from services.gemini_service import generate_progress_analysis

def init_progress_routes(app):

    @app.route("/progress", methods=["GET", "POST"])
    def progress():

        # -----------------------------------------
        # Login Required
        # -----------------------------------------

        if "user_id" not in session:

            flash("Please login first.", "error")

            return redirect(url_for("login"))

        user = db.session.get(User, session["user_id"])

        if user is None:

            session.clear()

            return redirect(url_for("login"))

        # -----------------------------------------
        # Save Progress
        # -----------------------------------------

        if request.method == "POST":

            weight = float(request.form["weight"])

            calories = int(request.form["calories"])

            water = float(request.form["water"])

            workout_completed = (
                request.form.get("workout_completed") == "yes"
            )

            notes = request.form.get("notes", "")

            save_progress(

                user,

                weight,

                calories,

                water,

                workout_completed,

                notes

            )

            flash(

                "Progress saved successfully!",

                "success"

            )

            return redirect(url_for("progress"))

        # -----------------------------------------
        # Load Progress
        # -----------------------------------------

        history = get_progress_history(user.id)

        latest = get_latest_progress(user.id)

        chart = get_chart_data(user.id)

        stats = get_progress_statistics(user.id) 
        
        summary = get_progress_summary(user.id)

        analysis = generate_progress_analysis(summary)

        return render_template(

            "progress.html",

            history=history,

            latest=latest,

            chart=chart,

            stats=stats,

            analysis=analysis

        )