-- ==========================================================
-- FitFusion AI - Smart Fitness Recommendation System
-- schema.sql
--
-- Purpose:
--   Final database structure (tables only, no sample data).
--   This is the single source of truth for the database
--   structure and can be used to regenerate database.db at
--   any time by running this file against SQLite.
--
-- Notes:
--   - Designed for SQLite (using TEXT/REAL/INTEGER storage
--     classes, which is SQLite's native type system).
--   - Authentication data is fully separated from fitness
--     profile data for scalability and security isolation.
--   - All "history" tables (bmi_records, calorie_records,
--     progress_tracker) keep every past entry instead of
--     overwriting, so charts/trends can be built later.
-- ==========================================================

-- Enforces foreign key constraints (OFF by default in SQLite).
-- This single line must be run on every new connection by the
-- backend (this will be handled in the database connection
-- layer, not here).
PRAGMA foreign_keys = ON;


-- ==========================================================
-- TABLE: users
-- ----------------------------------------------------------
-- Stores ONLY authentication-related data (login credentials).
-- Kept separate from fitness/profile data so:
--   - Login/auth logic stays simple and secure.
--   - Profile data can grow (more fields) without touching
--     the sensitive authentication table.
--   - Matches real-world practice of isolating credentials.
-- ==========================================================
CREATE TABLE IF NOT EXISTS users (
    user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);


-- ==========================================================
-- TABLE: user_profiles
-- ----------------------------------------------------------
-- Stores fitness-related personal data, separate from login
-- credentials. One-to-one relationship with "users" table.
-- This data is required by the BMI Calculator, Calorie
-- Calculator, Workout Recommendation, and Diet Recommendation
-- modules.
-- ==========================================================
CREATE TABLE IF NOT EXISTS user_profiles (
    profile_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL UNIQUE,
    full_name     TEXT NOT NULL,
    age           INTEGER,
    gender        TEXT CHECK (gender IN ('male', 'female', 'other')),
    height_cm     REAL,
    weight_kg     REAL,
    updated_at    TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (user_id) REFERENCES users (user_id)
        ON DELETE CASCADE
);


-- ==========================================================
-- TABLE: bmi_records
-- ----------------------------------------------------------
-- Stores every BMI calculation performed by a user over time.
-- Kept as a history table (not a single overwritten value) so
-- the Progress Tracking Dashboard can later plot BMI trends
-- on a chart.
-- ==========================================================
CREATE TABLE IF NOT EXISTS bmi_records (
    bmi_record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL,
    height_cm     REAL NOT NULL,
    weight_kg     REAL NOT NULL,
    bmi_value     REAL NOT NULL,
    bmi_category  TEXT NOT NULL CHECK (
        bmi_category IN ('Underweight', 'Normal', 'Overweight', 'Obese')
    ),
    recorded_at   TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (user_id) REFERENCES users (user_id)
        ON DELETE CASCADE
);


-- ==========================================================
-- TABLE: calorie_records
-- ----------------------------------------------------------
-- Stores every daily calorie requirement calculation for a
-- user. activity_level is restricted to a fixed set of values
-- using CHECK instead of a separate lookup table, to keep the
-- schema beginner-friendly while still avoiding free-text typos.
-- ==========================================================
CREATE TABLE IF NOT EXISTS calorie_records (
    calorie_record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id           INTEGER NOT NULL,
    activity_level    TEXT NOT NULL CHECK (
        activity_level IN (
            'sedentary', 'light', 'moderate', 'active', 'very_active'
        )
    ),
    daily_calories    REAL NOT NULL,
    recorded_at       TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (user_id) REFERENCES users (user_id)
        ON DELETE CASCADE
);


-- ==========================================================
-- TABLE: workout_plans
-- ----------------------------------------------------------
-- Stores workout recommendations generated for a user, based
-- on their fitness goal. plan_details is stored as TEXT
-- (JSON-formatted string) so the structure can evolve (e.g.
-- list of exercises, sets, reps) without requiring a schema
-- change -- the backend will handle parsing/serialization.
-- ==========================================================
CREATE TABLE IF NOT EXISTS workout_plans (
    workout_plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    goal            TEXT NOT NULL CHECK (
        goal IN ('weight_loss', 'weight_gain', 'maintenance', 'muscle_gain')
    ),
    plan_details    TEXT NOT NULL,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (user_id) REFERENCES users (user_id)
        ON DELETE CASCADE
);


-- ==========================================================
-- TABLE: diet_plans
-- ----------------------------------------------------------
-- Stores diet recommendations generated for a user, based on
-- their fitness goal. Mirrors workout_plans in structure for
-- consistency. plan_details stored as JSON-formatted TEXT for
-- the same flexibility reasons as workout_plans.
-- ==========================================================
CREATE TABLE IF NOT EXISTS diet_plans (
    diet_plan_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL,
    goal          TEXT NOT NULL CHECK (
        goal IN ('weight_loss', 'weight_gain', 'maintenance', 'muscle_gain')
    ),
    plan_details  TEXT NOT NULL,
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (user_id) REFERENCES users (user_id)
        ON DELETE CASCADE
);


-- ==========================================================
-- TABLE: progress_tracker
-- ----------------------------------------------------------
-- Stores periodic check-in entries (weight + optional notes)
-- so the dashboard can render progress charts over time.
-- Deliberately kept separate from bmi_records: a progress
-- check-in does not always involve a fresh BMI calculation,
-- and combining them would force unrelated data together.
-- ==========================================================
CREATE TABLE IF NOT EXISTS progress_tracker (
    progress_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    weight_kg    REAL NOT NULL,
    notes        TEXT,
    recorded_at  TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (user_id) REFERENCES users (user_id)
        ON DELETE CASCADE
);


-- ==========================================================
-- INDEXES
-- ----------------------------------------------------------
-- Speeds up the most common queries: "fetch all records for
-- this user" across every history table. Without these,
-- SQLite would scan the full table for every dashboard load.
-- ==========================================================
CREATE INDEX IF NOT EXISTS idx_bmi_records_user      ON bmi_records (user_id);
CREATE INDEX IF NOT EXISTS idx_calorie_records_user   ON calorie_records (user_id);
CREATE INDEX IF NOT EXISTS idx_workout_plans_user     ON workout_plans (user_id);
CREATE INDEX IF NOT EXISTS idx_diet_plans_user        ON diet_plans (user_id);
CREATE INDEX IF NOT EXISTS idx_progress_tracker_user  ON progress_tracker (user_id);