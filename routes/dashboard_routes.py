# ==========================================================
# FitFusion AI - routes/dashboard_routes.py
# ----------------------------------------------------------
# Purpose:
# Protects the dashboard and loads the logged-in user.
# ==========================================================

import datetime

from flask import (
    render_template,
    redirect,
    url_for,
    session,
    flash
)

from models import db, User


def init_dashboard_routes(app):

    @app.route("/dashboard")
    def dashboard():

        # -------------------------------------------------
        # Check if user is logged in
        # -------------------------------------------------
        if "user_id" not in session:
            flash("Please login to continue.", "error")
            return redirect(url_for("login"))

        try:
            # -------------------------------------------------
            # Load logged-in user (SQLAlchemy 2.x)
            # -------------------------------------------------
            user = db.session.get(User, session["user_id"])

            # -------------------------------------------------
            # Invalid or expired session
            # -------------------------------------------------
            if user is None:
                session.clear()
                flash("Session expired. Please login again.", "error")
                return redirect(url_for("login"))

            # -------------------------------------------------
            # Render Dashboard
            # -------------------------------------------------
            from services.dashboard_service import get_dashboard_data
            from services.progress_service import get_progress_summary
            from services.gemini_service import generate_progress_analysis

            summary = get_progress_summary(user.id)
            analysis = generate_progress_analysis(summary)

            dashboard_data = get_dashboard_data(user)
            from datetime import datetime

            current_date = datetime.now().strftime("%A, %d %B")

            return render_template(
                "dashboard.html",
                dashboard=dashboard_data,
                current_date=current_date,
                analysis=analysis
            )

        except Exception as e:
            # -------------------------------------------------
            # Handle unexpected errors
            # -------------------------------------------------
            session.clear()

            print(f"[Dashboard Error] {e}")

            flash(
                "Something went wrong. Please login again.",
                "error"
            )

            return redirect(url_for("login"))