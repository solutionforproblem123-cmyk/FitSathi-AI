# ==========================================================
# FitFusion AI - services/calories_service.py
# ----------------------------------------------------------
# Purpose:
# Contains all calorie calculation business logic.
# Routes should never contain calculation formulas.
# ==========================================================

# ----------------------------------------------------------
# Activity Multipliers
# ----------------------------------------------------------

ACTIVITY_FACTORS = {
    "sedentary": 1.20,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.90,
}


def calculate_bmr(age, gender, height, weight):
    """
    Calculates Basal Metabolic Rate (BMR)
    using the Mifflin-St Jeor Equation.

    Args:
        age (int)
        gender (str)
        height (float)  # cm
        weight (float)  # kg

    Returns:
        float
    """

    if gender == "male":

        return (
            (10 * weight)
            + (6.25 * height)
            - (5 * age)
            + 5
        )

    return (
        (10 * weight)
        + (6.25 * height)
        - (5 * age)
        - 161
    )


def calculate_tdee(bmr, activity):
    """
    Calculates Total Daily Energy Expenditure.
    """

    factor = ACTIVITY_FACTORS.get(activity)

    if factor is None:
        raise ValueError("Invalid activity level.")

    return bmr * factor


def calculate_calories(age, gender, height, weight, activity):
    """
    Complete calorie recommendation.

    Returns a dictionary which can be directly
    passed to the HTML template.
    """

    bmr = calculate_bmr(
        age,
        gender,
        height,
        weight
    )

    tdee = calculate_tdee(
        bmr,
        activity
    )

    maintenance = round(tdee)

    weight_loss = round(tdee - 500)

    weight_gain = round(tdee + 300)

    return {

        "bmr": round(bmr),

        "maintenance": maintenance,

        "weight_loss": weight_loss,

        "weight_gain": weight_gain,

        "activity": activity.title(),

        "gender": gender.title()

    }