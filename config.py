# ==========================================================
# FitFusion AI - config.py
# --------------------------------------------------------
# Purpose:
#   Centralized application configuration. Keeping config in
#   its own file (instead of hardcoding values in app.py) is
#   a Flask best practice -- it allows different configs for
#   development/testing/production later without touching
#   the app factory itself.
# ==========================================================

import os

# --------------------------------------------------------
# Base directory of the project.
# Used to build an absolute path to the SQLite database file
# so the app works correctly regardless of where it's run
# from (important once this gets deployed or wrapped for
# Android WebView/PWA).
# --------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration shared by all environments.
    Environment-specific config classes (below) inherit from
    this and override only what differs.
    """

    # --------------------------------------------------------
    # Secret key, used by Flask for session signing (cookies),
    # CSRF protection, etc. Read from an environment variable
    # in production; falls back to a development-only default
    # so the app still runs out of the box for this phase.
    # --------------------------------------------------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "fitfusion-dev-secret-key")

    # --------------------------------------------------------
    # SQLAlchemy Database Configuration
    # --------------------------------------------------------
    # SQLite database file lives inside the Flask "instance"
    # folder -- the conventional location for files that
    # shouldn't be committed to version control (instance-
    # specific data). Flask automatically treats this folder
    # as outside the application package.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "fitfusion.db")
    )

    # Disables a SQLAlchemy feature that tracks every object
    # change for signaling purposes. Not needed for this
    # project and adds unnecessary overhead.
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Configuration used during local development."""
    DEBUG = True


class ProductionConfig(Config):
    """
    Configuration used in production.
    DEBUG is explicitly disabled -- debug mode must never be
    enabled in production as it exposes an interactive
    debugger and source code on errors.
    """
    DEBUG = False


# --------------------------------------------------------
# Maps a simple string name to its config class. Used by the
# app factory in app.py to select the right configuration
# (e.g. config_by_name["development"]).
# --------------------------------------------------------
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")