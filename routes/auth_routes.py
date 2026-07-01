# ==========================================================
# FitFusion AI - routes/auth_routes.py
# ----------------------------------------------------------
# Handles:
#   - User Registration
#   - User Login
#   - User Logout
# ==========================================================

import re
import traceback

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


EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


def init_auth_routes(app):

    # ======================================================
    # REGISTER
    # ======================================================

    @app.route("/register", methods=["GET", "POST"])
    def register():

        if request.method == "GET":
            return render_template("register.html")

        # -----------------------------
        # Read Form Data
        # -----------------------------

        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        height = request.form.get("height_cm", "").strip()
        weight = request.form.get("weight_kg", "").strip()

        # -----------------------------
        # Required Fields
        # -----------------------------

        if not all([
            full_name,
            email,
            password,
            confirm_password,
            age,
            gender,
            height,
            weight
        ]):
            flash("Please fill all required fields.", "error")
            return redirect(url_for("register"))

        # -----------------------------
        # Email Validation
        # -----------------------------

        if not re.match(EMAIL_REGEX, email):
            flash("Invalid email address.", "error")
            return redirect(url_for("register"))

        # -----------------------------
        # Password Validation
        # -----------------------------

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("register"))

        # -----------------------------
        # Duplicate Email
        # -----------------------------

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered.", "error")
            return redirect(url_for("register"))

        # -----------------------------
        # Numeric Conversion
        # -----------------------------

        try:
            age = int(age)
            height = float(height)
            weight = float(weight)
        except ValueError:
            flash("Invalid numeric values.", "error")
            return redirect(url_for("register"))

        # -----------------------------
        # Range Validation
        # -----------------------------

        if age < 5 or age > 120:
            flash("Invalid age.", "error")
            return redirect(url_for("register"))

        if height <= 0:
            flash("Invalid height.", "error")
            return redirect(url_for("register"))

        if weight <= 0:
            flash("Invalid weight.", "error")
            return redirect(url_for("register"))

        # -----------------------------
        # Save User
        # -----------------------------

        try:
            user = User(
                full_name=full_name,
                email=email,
                age=age,
                gender=gender,
                height=height,
                weight=weight
            )

            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            flash("Registration successful. Please login.", "success")
            return redirect(url_for("login"))

        except Exception as e:
            db.session.rollback()

            print("\n========== REGISTER ERROR ==========")
            print(e)
            traceback.print_exc()
            print("====================================")

            flash("Something went wrong. Please try again.", "error")
            return redirect(url_for("register"))

    # ======================================================
    # LOGIN
    # ======================================================

    @app.route("/login", methods=["GET", "POST"])
    def login():

        if request.method == "GET":
            return render_template("login.html")

        # -----------------------------
        # Read Form Data
        # -----------------------------

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter both email and password.", "error")
            return redirect(url_for("login"))

        # -----------------------------
        # Find User
        # -----------------------------

        user = User.query.filter_by(email=email).first()

        if user is None:
            flash("Invalid email or password.", "error")
            return redirect(url_for("login"))

        # -----------------------------
        # Verify Password
        # -----------------------------

        if not user.check_password(password):
            flash("Invalid email or password.", "error")
            return redirect(url_for("login"))

        # -----------------------------
        # Create Session
        # -----------------------------

        session.clear()

        session["user_id"] = user.id
        session["user_name"] = user.full_name
        session["user_email"] = user.email

        flash(f"Welcome back, {user.full_name}!", "success")

        return redirect(url_for("dashboard"))

    # ======================================================
    # LOGOUT
    # ======================================================

    @app.route("/logout")
    def logout():
        """
        Clears the current user session and redirects
        back to the login page.
        """

        session.clear()

        flash("You have been logged out successfully.", "success")

        return redirect(url_for("login"))


# ==========================================================
# Helper Functions
# ==========================================================

def _is_float(value):
    """
    Returns True if the given value can be converted
    to float, otherwise False.
    """

    try:
        float(value)
        return True

    except (TypeError, ValueError):
        return False