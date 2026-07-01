from flask import (
    render_template,
    request,
    flash
)


def init_bmi_routes(app):

    @app.route("/bmi", methods=["GET", "POST"])
    def bmi():

        bmi_value = None
        category = None

        if request.method == "POST":

            try:

                height = float(
                    request.form.get("height")
                )

                weight = float(
                    request.form.get("weight")
                )

                if height <= 0 or weight <= 0:

                    raise ValueError

                height = height / 100

                bmi_value = round(
                    weight / (height * height),
                    2
                )

                if bmi_value < 18.5:
                    category = "Underweight"

                elif bmi_value < 25:
                    category = "Normal"

                elif bmi_value < 30:
                    category = "Overweight"

                else:
                    category = "Obese"

            except ValueError:

                flash(
                    "Please enter valid height and weight.",
                    "error"
                )

        return render_template(
            "bmi.html",
            bmi=bmi_value,
            category=category
        )