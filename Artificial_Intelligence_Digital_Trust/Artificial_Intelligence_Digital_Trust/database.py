"""
database.py
------------
Handles all SQLite database operations for the
"Artificial Intelligence and Digital Trust" mini project.

Responsibilities:
    - Create a connection to database.db
    - Auto-create all required tables on first run
    - Provide small helper functions used by app.py for
      inserting and fetching records (CRUD operations)

Author: AI & ML Second Year Mini Project
"""

import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

DB_NAME = "database.db"


def get_connection():
    """Return a new SQLite connection with row access by column name."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Create all required tables if they do not already exist,
    and seed a default admin account so the dashboard is usable
    immediately after `python app.py` is run for the first time.
    """
    conn = get_connection()
    cur = conn.cursor()

    # 1. Contact form submissions
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # 2. Quiz attempt results
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # 3. AI Trust Calculator results
    cur.execute("""
        CREATE TABLE IF NOT EXISTS trust_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL,
            strong_password TEXT,
            mfa_enabled TEXT,
            data_backup TEXT,
            privacy_awareness TEXT,
            secure_browsing TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # 4. Admin users (for the protected dashboard)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    conn.commit()

    # Seed a default admin user: username = admin, password = admin123
    cur.execute("SELECT COUNT(*) as c FROM admin_users")
    if cur.fetchone()["c"] == 0:
        cur.execute(
            "INSERT INTO admin_users (username, password_hash) VALUES (?, ?)",
            ("admin", generate_password_hash("admin123")),
        )
        conn.commit()

    conn.close()


# ---------------------------------------------------------------------
# CRUD helper functions
# ---------------------------------------------------------------------

def insert_contact(name, email, subject, message):
    conn = get_connection()
    conn.execute(
        "INSERT INTO contacts (name, email, subject, message, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (name, email, subject, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()


def insert_quiz_result(name, score, total, percentage):
    conn = get_connection()
    conn.execute(
        "INSERT INTO quiz_results (name, score, total, percentage, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (name, score, total, percentage, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()


def insert_trust_score(name, score, answers):
    conn = get_connection()
    conn.execute(
        """INSERT INTO trust_scores
           (name, score, strong_password, mfa_enabled, data_backup,
            privacy_awareness, secure_browsing, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            name,
            score,
            answers.get("strong_password"),
            answers.get("mfa_enabled"),
            answers.get("data_backup"),
            answers.get("privacy_awareness"),
            answers.get("secure_browsing"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )
    conn.commit()
    conn.close()


def get_all_contacts():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM contacts ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def get_all_quiz_results():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM quiz_results ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def get_all_trust_scores():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM trust_scores ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def get_admin_by_username(username):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM admin_users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    return row


def get_dashboard_stats():
    """Aggregate counts + averages used for the dashboard chart cards."""
    conn = get_connection()
    total_contacts = conn.execute("SELECT COUNT(*) c FROM contacts").fetchone()["c"]
    total_quiz = conn.execute("SELECT COUNT(*) c FROM quiz_results").fetchone()["c"]
    total_trust = conn.execute("SELECT COUNT(*) c FROM trust_scores").fetchone()["c"]
    avg_quiz = conn.execute(
        "SELECT AVG(percentage) a FROM quiz_results"
    ).fetchone()["a"] or 0
    avg_trust = conn.execute(
        "SELECT AVG(score) a FROM trust_scores"
    ).fetchone()["a"] or 0
    conn.close()
    return {
        "total_contacts": total_contacts,
        "total_quiz": total_quiz,
        "total_trust": total_trust,
        "avg_quiz": round(avg_quiz, 1),
        "avg_trust": round(avg_trust, 1),
    }
