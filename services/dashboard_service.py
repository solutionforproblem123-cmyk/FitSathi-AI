from streamlit import user

from database import db
from models import User
from services.progress_service import (
    get_chart_data,
    get_progress_statistics
)


def get_dashboard_data(user):

    height_m = user.height / 100

    bmi = round(user.weight / (height_m ** 2), 1)

    calories = round(user.weight * 33)

    protein = round(user.weight * 1.8)

    water = round((user.weight * 35) / 1000, 1)

    chart = get_chart_data(user.id)

    stats = get_progress_statistics(user.id)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return {

    "bmi": bmi,

    "category": category,

    "calories": calories,

    "protein": protein,

    "water": water,

    "goal": user.goal,

    "workout_days": user.workout_days,

    "current_weight": user.weight,

    "height": user.height,

    "full_name": user.full_name,

    "chart": chart,

    "stats": stats

}