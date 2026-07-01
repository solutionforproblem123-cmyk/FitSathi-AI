# ==========================================================
# FitFusion AI - routes/diet_routes.py
# ----------------------------------------------------------
# Purpose:
# Handles Diet Planner requests.
# Business logic is delegated to services/diet_service.py
# ==========================================================

from flask import (
    render_template,
    request,
    flash
)

from services.diet_service import generate_diet_plan


def init_diet_routes(app):

    @app.route("/diet", methods=["GET", "POST"])
    def diet():

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

                goal = request.form.get(
                    "goal",
                    ""
                ).strip().lower()

                food_preference = request.form.get(
                    "food_preference",
                    ""
                ).strip().lower()

                meals = int(
                    request.form.get("meals", 3)
                )

                # -----------------------------
                # Validation
                # -----------------------------

                if age <= 0:
                    raise ValueError("Invalid age.")

                if height <= 0:
                    raise ValueError("Invalid height.")

                if weight <= 0:
                    raise ValueError("Invalid weight.")

                if meals < 3 or meals > 6:
                    raise ValueError(
                        "Meals per day must be between 3 and 6."
                    )

                result = generate_diet_plan(

                    age=age,

                    gender=gender,

                    height=height,

                    weight=weight,

                    goal=goal,

                    food_preference=food_preference,

                    meals=meals

                )

            except ValueError as error:

                flash(
                    str(error),
                    "error"
                )

            except Exception:

                flash(
                    "Unable to generate diet plan.",
                    "error"
                )

        return render_template(

            "diet.html",

            result=result

        )