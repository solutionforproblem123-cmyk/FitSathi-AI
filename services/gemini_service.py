import google.generativeai as genai

from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_ai_recommendation(prompt):

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        print(e)

        return None


def generate_progress_analysis(summary):
    try:
        prompt = (
            "Analyze the following progress summary and provide a concise progress analysis:\n\n"
            f"{summary}"
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(e)
        return None
    
# ==========================================================
# AI Progress Analysis
# ==========================================================

def generate_progress_analysis(summary):
    """
    Generates AI-based fitness progress analysis
    using Gemini.
    """

    prompt = f"""
You are a professional fitness coach.

Analyze the following user's progress.

Current Weight: {summary['current_weight']} kg

Starting Weight: {summary['starting_weight']} kg

Weight Change: {summary['weight_change']} kg

Current BMI: {summary['current_bmi']}

Average Calories: {summary['average_calories']} kcal

Average Water Intake: {summary['average_water']} liters

Workout Completion: {summary['workout_completion']}%

Progress Entries: {summary['total_entries']}

Instructions:

1. Give a short progress summary.
2. Mention positive improvements.
3. Mention areas to improve.
4. Give 3 practical recommendations.
5. End with a motivational message.

Keep the response under 180 words.
Use simple English.
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception:

        return (
            "AI analysis is temporarily unavailable. "
            "Please try again later."
        )