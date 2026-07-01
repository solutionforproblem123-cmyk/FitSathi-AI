# ==========================================================
# FitFusion AI - routes/calories_routes.py
# ----------------------------------------------------------
# Purpose:
# Handles Daily Calorie Recommendation requests.
# Business logic is delegated to services/calories_service.py
# ==========================================================

from flask import (
    render_template,
    request,
    flash
)

from services.calories_service import calculate_calories


def init_calories_routes(app):

    @app.route("/calories", methods=["GET", "POST"])
    def calories():

        result = None

        if request.method == "POST":

            try:

                age = int(request.form.get("age", 0))

                gender = request.form.get(
                    "gender",
                    ""
                ).strip().lower()

                height = float(
                    request.form.get("height", 0)
                )

                weight = float(
                    request.form.get("weight", 0)
                )

                activity = request.form.get(
                    "activity",
                    ""
                ).strip().lower()

                # -----------------------------------------
                # Basic Validation
                # -----------------------------------------

                if age <= 0:

                    raise ValueError(
                        "Invalid age."
                    )

                if height <= 0:

                    raise ValueError(
                        "Invalid height."
                    )

                if weight <= 0:

                    raise ValueError(
                        "Invalid weight."
                    )

                if gender not in [
                    "male",
                    "female"
                ]:

                    raise ValueError(
                        "Invalid gender."
                    )

                result = calculate_calories(

                    age=age,

                    gender=gender,

                    height=height,

                    weight=weight,

                    activity=activity

                )

            except ValueError as error:

                flash(
                    str(error),
                    "error"
                )

            except Exception:

                flash(
                    "Something went wrong while calculating calories.",
                    "error"
                )

        return render_template(

            "calories.html",

            result=result

        )