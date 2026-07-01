from routes.auth_routes import init_auth_routes
from routes.dashboard_routes import init_dashboard_routes
from routes.bmi_routes import init_bmi_routes
from routes.calories_routes import init_calories_routes
from routes.workout_routes import init_workout_routes
from routes.diet_routes import init_diet_routes
from routes.progress_routes import init_progress_routes
from routes.profile_routes import init_profile_routes


def register_routes(app):

    init_auth_routes(app)
    init_dashboard_routes(app)
    init_bmi_routes(app)
    init_calories_routes(app)
    init_workout_routes(app)
    init_diet_routes(app)
    init_progress_routes(app)
    init_profile_routes(app)