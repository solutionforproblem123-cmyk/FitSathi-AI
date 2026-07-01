# ==========================================================
# FitFusion AI - services/workout_service.py
# ----------------------------------------------------------
# Purpose:
# Generates personalized workout plans.
# ==========================================================
import json

from services.gemini_service import generate_ai_recommendation

def calculate_bmi(height, weight):
    """
    Calculate BMI.

    Args:
        height (cm)
        weight (kg)

    Returns:
        float
    """

    height_m = height / 100

    return round(weight / (height_m ** 2), 1)


def get_bmi_category(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    return "Obese"


def generate_workout_plan(
    age,
    gender,
    height,
    weight,
    goal,
    experience,
    workout_days
):

    bmi = calculate_bmi(height, weight)

    bmi_category = get_bmi_category(bmi)

    # ------------------------------------------------------
    # Workout Library
    # ------------------------------------------------------

    workout_library = {

    "weight loss": [

        {
            "exercise": "Brisk Walking",
            "sets": "30 min",
            "rest": "-",
            "calories": 180
        },
        {
            "exercise": "Jump Rope",
            "sets": "3 × 2 min",
            "rest": "60 sec",
            "calories": 120
        },
        {
            "exercise": "Bodyweight Squats",
            "sets": "3 × 15",
            "rest": "45 sec",
            "calories": 80
        },
        {
            "exercise": "Push Ups",
            "sets": "3 × 12",
            "rest": "60 sec",
            "calories": 70
        }

    ],

    "muscle gain": [

        {
            "exercise": "Bench Press",
            "sets": "4 × 10",
            "rest": "90 sec",
            "calories": 90
        },
        {
            "exercise": "Squats",
            "sets": "4 × 10",
            "rest": "90 sec",
            "calories": 100
        },
        {
            "exercise": "Deadlift",
            "sets": "4 × 8",
            "rest": "120 sec",
            "calories": 110
        },
        {
            "exercise": "Shoulder Press",
            "sets": "3 × 12",
            "rest": "60 sec",
            "calories": 75
        }

    ],

    "maintenance": [

        {
            "exercise": "Jogging",
            "sets": "20 min",
            "rest": "-",
            "calories": 160
        },
        {
            "exercise": "Push Ups",
            "sets": "3 × 15",
            "rest": "45 sec",
            "calories": 65
        },
        {
            "exercise": "Plank",
            "sets": "3 × 60 sec",
            "rest": "30 sec",
            "calories": 40
        }

    ]

}
    
    

    

    # ------------------------------------------------------
    # Goal Selection
    # ------------------------------------------------------

    if goal not in workout_library:

        goal = "maintenance"

    exercises = workout_library[goal]

    # ------------------------------------------------------
    # Weekly Plan
    # ------------------------------------------------------

    week = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    weekly_plan = {}

    index = 0

    for day in week:

        if index < workout_days:

            weekly_plan[day] = exercises.copy()

            index += 1

        else:

            weekly_plan[day] = ["Rest Day"]

    # ------------------------------------------------------
    # Recommendation Message
    # ------------------------------------------------------

    recommendation = (
        f"Your BMI is {bmi} ({bmi_category}). "
        f"Your goal is {goal.title()}. "
        f"We recommend training {workout_days} days per week. "
        f"Always perform a 5–10 minute warm-up before each workout "
        f"and finish with stretching to improve recovery."
    )
    prompt = f"""
You are an expert certified fitness coach.

User Profile:

Age: {age}
Gender: {gender}
Height: {height} cm
Weight: {weight} kg

BMI: {bmi}

Goal: {goal}

Experience: {experience}

Workout Days: {workout_days}

Return ONLY valid JSON.

Use this structure:

{{
  "goal_analysis":"...",
  "weekly_strategy":"...",
  "warmup":[
      "...",
      "...",
      "..."
  ],
  "workout_tips":[
      "...",
      "...",
      "..."
  ],
  "recovery":[
      "...",
      "...",
      "..."
  ],
  "coach_tip":"..."
}}

No markdown.

No explanation.

No code block.
"""
    ai_response = generate_ai_recommendation(prompt)

    try:
        ai_response = ai_response.strip()
        ai_response = ai_response.replace("```json", "")
        ai_response = ai_response.replace("```", "")
        ai_response = json.loads(ai_response)
    except Exception:
        ai_response = {
            "goal_analysis": recommendation,
            "weekly_strategy": "",
            "warmup": [],
            "workout_tips": [],
            "recovery": [],
            "coach_tip": ""
        }

    return {
        "bmi": bmi,
        "bmi_category": bmi_category,
        "goal": goal.title(),
        "experience": experience.title(),
        "workout_days": workout_days,
        "weekly_plan": weekly_plan,
        "recommendation": ai_response,
        "estimated_weekly_calories":
            sum(exercise["calories"] for exercise in exercises) * workout_days
    }