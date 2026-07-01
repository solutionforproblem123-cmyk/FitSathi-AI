# FitFusion AI – Smart Fitness Recommendation System

Final Year B.Sc. Computer Science Project

## About

FitFusion AI is a web-based fitness recommendation system that will allow
users to register, log in, calculate BMI and daily calorie needs, receive
workout and diet recommendations, and track their fitness progress.

This project is built with future Android conversion (via WebView or PWA)
in mind, so the frontend and backend are kept cleanly separated.

## Tech Stack

- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Backend:** Python, Flask
- **Database:** SQLite (via Python's built-in `sqlite3` module)

## Current Project Status

> 🚧 Foundation Phase

At this stage, the project contains only:
- Folder structure
- Flask app skeleton with route placeholders
- Database schema (table definitions only)

No HTML pages, styling, JavaScript, or business logic have been added yet.
These will be built incrementally in later phases.

## Folder Structure

```
FitnessProject/
├── app.py
├── requirements.txt
├── database.db
├── README.md
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── database/
    └── schema.sql
```

## How to Run (Development)

1. Create a virtual environment (recommended):
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Flask app:
   ```
   python app.py
   ```

4. Open your browser at:
   ```
   http://127.0.0.1:5000/
   ```

## Next Steps

See project development roadmap (shared separately) for the order in which
modules will be implemented.