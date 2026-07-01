# ==========================================================
# FitFusion AI - services/progress_service.py
# ----------------------------------------------------------
# Purpose:
# Business logic for Progress Tracker.
# ==========================================================

from datetime import datetime

from database import db
from models import Progress


# ----------------------------------------------------------
# BMI Calculation
# ----------------------------------------------------------

def calculate_bmi(height, weight):
    """
    Calculate BMI using height (cm) and weight (kg).
    """

    height_m = height / 100

    return round(weight / (height_m ** 2), 1)


# ----------------------------------------------------------
# Save Progress
# ----------------------------------------------------------

def save_progress(
    user,
    weight,
    calories,
    water,
    workout_completed,
    notes
):
    """
    Save a user's daily progress.
    """

    bmi = calculate_bmi(user.height, weight)

    progress = Progress(

        user_id=user.id,

        weight=weight,

        bmi=bmi,

        calories=calories,

        water=water,

        workout_completed=workout_completed,

        notes=notes,

        created_at=datetime.utcnow()

    )

    db.session.add(progress)

    db.session.commit()

    return progress


# ----------------------------------------------------------
# Latest Progress
# ----------------------------------------------------------

def get_latest_progress(user_id):

    return Progress.query.filter_by(
        user_id=user_id
    ).order_by(
        Progress.created_at.desc()
    ).first()


# ----------------------------------------------------------
# Progress History
# ----------------------------------------------------------

def get_progress_history(user_id):

    return Progress.query.filter_by(
        user_id=user_id
    ).order_by(
        Progress.created_at.desc()
    ).all()


# ----------------------------------------------------------
# Chart Data
# ----------------------------------------------------------

def get_chart_data(user_id):

    records = Progress.query.filter_by(
        user_id=user_id
    ).order_by(
        Progress.created_at.asc()
    ).all()

    labels = []

    weights = []

    bmi_values = []

    for record in records:

        labels.append(
            record.created_at.strftime("%d %b")
        )

        weights.append(record.weight)

        bmi_values.append(record.bmi)

    return {

        "labels": labels,

        "weights": weights,

        "bmi": bmi_values

    }

# ----------------------------------------------------------
# Progress Statistics
# ----------------------------------------------------------

def get_progress_statistics(user_id):

    records = Progress.query.filter_by(
        user_id=user_id
    ).order_by(
        Progress.created_at.asc()
    ).all()

    if not records:

        return {
            "total_entries": 0,
            "starting_weight": None,
            "current_weight": None,
            "weight_change": 0,
            "average_calories": 0,
            "average_water": 0,
            "workout_completion": 0
        }

    starting_weight = records[0].weight

    current_weight = records[-1].weight

    weight_change = round(
        current_weight - starting_weight,
        1
    )

    avg_calories = round(
        sum(r.calories for r in records if r.calories)
        / len(records)
    )

    avg_water = round(
        sum(r.water for r in records if r.water)
        / len(records),
        1
    )

    completed = sum(
        1
        for r in records
        if r.workout_completed
    )

    completion = round(
        completed * 100 / len(records)
    )

    return {

        "total_entries": len(records),

        "starting_weight": starting_weight,

        "current_weight": current_weight,

        "weight_change": weight_change,

        "average_calories": avg_calories,

        "average_water": avg_water,

        "workout_completion": completion

    }
def get_progress_summary(user_id):
    {
    "current_weight": 72,
    "starting_weight": 76,
    "weight_change": -4,
    "current_bmi": 23.4,
    "average_calories": 2150,
    "average_water": 2.8,
    "workout_completion": 87,
    "total_entries": 28
}

# ----------------------------------------------------------
# AI Progress Summary
# ----------------------------------------------------------

def get_progress_summary(user_id):

    stats = get_progress_statistics(user_id)

    latest = get_latest_progress(user_id)

    history = get_progress_history(user_id)

    return {

        "current_weight": stats["current_weight"],

        "starting_weight": stats["starting_weight"],

        "weight_change": stats["weight_change"],

        "average_calories": stats["average_calories"],

        "average_water": stats["average_water"],

        "workout_completion": stats["workout_completion"],

        "total_entries": stats["total_entries"],

        "current_bmi": latest.bmi if latest else None,

        "history_count": len(history)

    }