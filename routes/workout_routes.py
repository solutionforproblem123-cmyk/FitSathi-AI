# ==========================================================
# FitFusion AI - routes/workout_routes.py
# ----------------------------------------------------------
# Purpose:
# Handles Workout Planner requests.
# Business logic is delegated to services/workout_service.py
# ==========================================================

from flask import (
    render_template,
    request,
    flash
)

from services.workout_service import generate_workout_plan


def init_workout_routes(app):

    @app.route("/workout", methods=["GET", "POST"])
    def workout():

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

                experience = request.form.get(
                    "experience",
                    ""
                ).strip().lower()

                workout_days = int(
                    request.form.get("workout_days", 0)
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

                if workout_days < 1 or workout_days > 7:
                    raise ValueError(
                        "Workout days must be between 1 and 7."
                    )

                result = generate_workout_plan(

                    age=age,

                    gender=gender,

                    height=height,

                    weight=weight,

                    goal=goal,

                    experience=experience,

                    workout_days=workout_days

                )

            except ValueError as error:

                flash(
                    str(error),
                    "error"
                )

            except Exception:

                flash(
                    "Unable to generate workout plan.",
                    "error"
                )
      #  print(result)
        
        return render_template(

            "workout.html",

            result=result

        )