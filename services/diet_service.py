# ==========================================================
# FitFusion AI - services/diet_service.py
# ----------------------------------------------------------
# Purpose:
# Generates personalized diet plans.
# ==========================================================
import json
from services.gemini_service import generate_ai_recommendation
def calculate_bmi(height, weight):

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


def generate_diet_plan(

    age,
    gender,
    height,
    weight,
    goal,
    food_preference,
    meals

):

    bmi = calculate_bmi(height, weight)

    bmi_category = get_bmi_category(bmi)

    # ------------------------------------------------------
    # Diet Library
    # ------------------------------------------------------

    diet_library = {

        "vegetarian": {

            "Breakfast": [
                "Oats",
                "Milk",
                "Banana"
            ],

            "Lunch": [
                "Rice",
                "Dal",
                "Paneer",
                "Salad"
            ],

            "Snack": [
                "Apple",
                "Almonds"
            ],

            "Dinner": [
                "Chapati",
                "Mixed Vegetables",
                "Curd"
            ]

        },

        "non-vegetarian": {

            "Breakfast": [
                "Boiled Eggs",
                "Brown Bread",
                "Milk"
            ],

            "Lunch": [
                "Chicken Breast",
                "Rice",
                "Salad"
            ],

            "Snack": [
                "Greek Yogurt",
                "Banana"
            ],

            "Dinner": [
                "Fish",
                "Vegetables",
                "Chapati"
            ]

        },

        "vegan": {

            "Breakfast": [
                "Oats",
                "Soy Milk",
                "Banana"
            ],

            "Lunch": [
                "Brown Rice",
                "Rajma",
                "Salad"
            ],

            "Snack": [
                "Peanuts",
                "Apple"
            ],

            "Dinner": [
                "Tofu",
                "Vegetables",
                "Chapati"
            ]

        }

    }

    # ------------------------------------------------------
    # Default Preference
    # ------------------------------------------------------

    if food_preference not in diet_library:

        food_preference = "vegetarian"

    meal_plan = diet_library[food_preference]

    # ------------------------------------------------------
    # AI Recommendation
    # ------------------------------------------------------


    # ------------------------------------------------------
    # AI Recommendation
    # ------------------------------------------------------

    suggestions = []

    if bmi < 18.5:

        suggestions.append(
            "Increase your calorie intake using healthy foods."
        )

    elif bmi >= 25:

        suggestions.append(
            "Maintain a calorie deficit and avoid sugary drinks."
        )

    else:

        suggestions.append(
            "Maintain your current healthy eating habits."
        )

    # --------------------------------------------

    if goal == "weight loss":

        suggestions.append(
            "Eat more vegetables and lean protein."
        )

        suggestions.append(
            "Avoid fried and processed foods."
        )

    elif goal == "muscle gain":

        suggestions.append(
            "Consume protein after every workout."
        )

        suggestions.append(
            "Increase complex carbohydrate intake."
        )

    else:

        suggestions.append(
            "Follow a balanced diet with regular meal timings."
        )

    # --------------------------------------------

    if food_preference == "vegetarian":

        suggestions.append(
            "Include paneer, lentils and soy products."
        )

    elif food_preference == "vegan":

        suggestions.append(
            "Ensure adequate Vitamin B12 and Iron intake."
        )

    else:

        suggestions.append(
            "Choose grilled chicken, eggs and fish instead of fried foods."
        )

    recommendation = (
        f"Your BMI is {bmi} ({bmi_category}). "
        f"Your goal is {goal.title()}. "
        f"Follow the suggestions below for a healthier lifestyle."
    )

    # ------------------------------------------------------
    # Nutrition Summary
    # ------------------------------------------------------

    daily_calories = round(weight * 33)

    protein = round(weight * 1.8)

    carbs = round((daily_calories * 0.50) / 4)

    fats = round((daily_calories * 0.25) / 9)

    water = round((weight * 35) / 1000, 1)

# ------------------------------------------------------
# Gemini AI Recommendation
# ------------------------------------------------------

    prompt = f"""
You are an expert fitness and nutrition coach.

User Profile

Age: {age}

Gender: {gender}

Height: {height} cm

Weight: {weight} kg

BMI: {bmi}

Goal: {goal}

Food Preference: {food_preference}

Daily Calories: {daily_calories}

Protein: {protein} g

Carbs: {carbs} g

Fats: {fats} g

Water Intake: {water} liters

Give:

1. Personalized diet advice.

2. Foods to eat.

3. Foods to avoid.

4. Meal timing.

5. Hydration advice.

Limit response to around 150 words.

IMPORTANT:

Return ONLY valid JSON.

Do not write markdown.

Do not write explanations.

Use this exact JSON format:

{{
  "goal_analysis": "...",
  "foods_to_eat": [
    "...",
    "...",
    "..."
  ],
  "foods_to_avoid": [
    "...",
    "...",
    "..."
  ],
  "meal_timing": [
    "...",
    "...",
    "..."
  ],
  "hydration": "...",
  "coach_tip": "..."
}}
"""
    ai_response = generate_ai_recommendation(prompt)

    try:

        ai_response = ai_response.strip()

        if ai_response.startswith("```json"):
            ai_response = ai_response.replace("```json", "")

        if ai_response.startswith("```"):
            ai_response = ai_response.replace("```", "")

        ai_response = ai_response.replace("```", "").strip()

        print("RAW GEMINI RESPONSE:")
        print(ai_response)

        ai_response = json.loads(ai_response)

    except Exception as e:

        print("JSON ERROR:", e)

        ai_response = {

            "goal_analysis": recommendation,

            "foods_to_eat": [],

            "foods_to_avoid": [],

            "meal_timing": [],

            "hydration": "",

            "coach_tip": ""

        }

    return {

        "bmi": bmi,

        "bmi_category": bmi_category,

        "goal": goal.title(),

        "food_preference": food_preference.title(),

        "meals": meals,

        "meal_plan": meal_plan,

        "recommendation": ai_response,

        "daily_calories": daily_calories,

        "protein": protein,

        "carbs": carbs,

        "fats": fats,

        "water": water,

        "ai_suggestions": suggestions,

    }