# ==========================================================
# FitFusion AI - models.py
# --------------------------------------------------------
# Purpose:
#   Defines all SQLAlchemy ORM models for the application.
#   Phase 1 contains only the User model, matching the
#   project's auth/profile fields. Future phases (BMI,
#   Calorie, Workout, Diet, Progress) will add their own
#   model classes to this file, each as a separate class
#   with its own table -- keeping one file per concern
#   (models.py for data shape, routes/ for behavior).
#
# Note:
#   `db` is imported from database.py, not created here --
#   see database.py for why that separation exists.
# ==========================================================

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from database import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    height = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)

    # ----------------------------------------------------
    # Fitness Preferences
    # ----------------------------------------------------

    goal = db.Column(
        db.String(30),
        nullable=True,
        default="maintenance"
    )

    experience = db.Column(
        db.String(30),
        nullable=True,
        default="beginner"
    )

    workout_days = db.Column(
        db.Integer,
        nullable=True,
        default=3
    )

    activity_level = db.Column(
        db.String(30),
        nullable=True,
        default="moderate"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    progress_records = db.relationship(
        "Progress",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )

    def set_password(self, plain_password):
        self.password_hash = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        return check_password_hash(
            self.password_hash,
            plain_password
        )

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"


class Progress(db.Model):
    """
    Stores a user's daily fitness progress.
    """

    __tablename__ = "progress"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    weight = db.Column(db.Float, nullable=False)

    bmi = db.Column(db.Float, nullable=False)

    calories = db.Column(db.Integer, nullable=True)

    water = db.Column(db.Float, nullable=True)

    workout_completed = db.Column(
        db.Boolean,
        default=False
    )

    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="progress_records"
    )

    def __repr__(self):
        return (
            f"<Progress id={self.id} "
            f"user_id={self.user_id} "
            f"date={self.created_at}>"
        )