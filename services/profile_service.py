# ==========================================================
# FitFusion AI - services/profile_service.py
# ----------------------------------------------------------
# Business logic for User Profile
# ==========================================================

from database import db
from models import User


# ----------------------------------------------------------
# Get Profile
# ----------------------------------------------------------

def get_profile(user_id):
    """
    Returns the logged-in user's profile.
    """

    return db.session.get(User, user_id)


# ----------------------------------------------------------
# Update Profile
# ----------------------------------------------------------

def update_profile(
    user,
    full_name,
    age,
    gender,
    height,
    weight,
    goal,
    experience,
    workout_days,
    activity_level
):
    """
    Updates user profile information.
    """

    user.full_name = full_name

    user.age = age

    user.gender = gender

    user.height = height

    user.weight = weight

    user.goal = goal

    user.experience = experience

    user.workout_days = workout_days

    user.activity_level = activity_level

    db.session.commit()

    return user


# ----------------------------------------------------------
# BMI
# ----------------------------------------------------------

def calculate_bmi(user):

    if not user.height or not user.weight:
        return None

    height_m = user.height / 100

    return round(
        user.weight / (height_m ** 2),
        1
    )


# ----------------------------------------------------------
# Profile Summary
# ----------------------------------------------------------

def get_profile_summary(user):

    bmi = calculate_bmi(user)

    return {

        "name": user.full_name,

        "email": user.email,

        "age": user.age,

        "gender": user.gender,

        "height": user.height,

        "weight": user.weight,

        "goal": user.goal,

        "experience": user.experience,

        "workout_days": user.workout_days,

        "activity_level": user.activity_level,

        "bmi": bmi

    }