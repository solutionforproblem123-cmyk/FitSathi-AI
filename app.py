# ==========================================================
# FitFusion AI - app.py
# ----------------------------------------------------------
# Main Flask application entry point.
# Initializes configuration, database, blueprints and
# preserves all frontend routes until they are gradually
# moved into Blueprints.
# ==========================================================

import os

from flask import Flask, render_template

from config import DevelopmentConfig
from database import init_db
from routes import register_routes


# ==========================================================
# APP FACTORY
# ==========================================================

def create_app():

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        instance_relative_config=True
    )

    # ------------------------------------------------------
    # Load Configuration
    # ------------------------------------------------------

    app.config.from_object(DevelopmentConfig)

    # ------------------------------------------------------
    # Ensure instance folder exists
    # ------------------------------------------------------

    os.makedirs(app.instance_path, exist_ok=True)

    # ------------------------------------------------------
    # Initialize Database
    # ------------------------------------------------------

    init_db(app)

    # ------------------------------------------------------
    # Register Blueprints
    # ------------------------------------------------------

    register_routes(app)

    # ======================================================
    # FRONTEND ROUTES
    # (Temporary until moved into Blueprints)
    # ======================================================

    @app.route("/")
    def home():
        return render_template("index.html")


    @app.route("/contact")
    def contact():
        return render_template("contact.html")

    return app


# ==========================================================
# APP INSTANCE
# ==========================================================

app = create_app()


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)