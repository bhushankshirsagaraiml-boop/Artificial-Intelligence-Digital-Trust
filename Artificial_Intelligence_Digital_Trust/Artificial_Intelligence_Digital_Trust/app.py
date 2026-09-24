"""
app.py
------
Main Flask application for the Second Year B.Tech (AI & ML) mini project:
"Artificial Intelligence and Digital Trust"

Run with:
    python app.py

Author  : Second Year AI & ML Mini Project
Stack   : Flask + SQLite + HTML5/CSS3/JS + Chart.js
"""

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash
)
from werkzeug.security import check_password_hash
from functools import wraps
import database as db

# ---------------------------------------------------------------------
# App configuration
# ---------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "ai_digital_trust_secret_key_2026"  # used to sign session cookies

# Create all tables (and default admin user) the first time the app runs
db.init_db()


# ---------------------------------------------------------------------
# Static content: Quiz questions, News, Team
# ---------------------------------------------------------------------

QUIZ_QUESTIONS = [
    {
        "q": "What does AI stand for?",
        "options": ["Automated Interface", "Artificial Intelligence", "Applied Informatics", "Advanced Integration"],
        "answer": 1,
    },
    {
        "q": "Which of these is a subset of Artificial Intelligence?",
        "options": ["Machine Learning", "Cloud Storage", "HTML", "Networking"],
        "answer": 0,
    },
    {
        "q": "Deep Learning is primarily based on which structure?",
        "options": ["Spreadsheets", "Neural Networks", "Flowcharts", "Databases"],
        "answer": 1,
    },
    {
        "q": "Which of the following best describes 'Digital Trust'?",
        "options": [
            "Trust in social media influencers",
            "Confidence in the security, privacy and reliability of digital systems",
            "A type of antivirus software",
            "A blockchain currency",
        ],
        "answer": 1,
    },
    {
        "q": "Which technique helps make AI decisions understandable to humans?",
        "options": ["Explainable AI (XAI)", "Data Mining", "Load Balancing", "Firewalling"],
        "answer": 0,
    },
    {
        "q": "A 'Deepfake' is an example of which AI-related challenge?",
        "options": ["Job Automation", "Misinformation / Media Manipulation", "Data Backup", "Network Latency"],
        "answer": 1,
    },
    {
        "q": "Which of these strengthens account security the most?",
        "options": ["Reusing the same password", "Multi-Factor Authentication (MFA)", "Sharing passwords", "Disabling updates"],
        "answer": 1,
    },
    {
        "q": "Generative AI is best known for producing:",
        "options": ["Only numeric data", "New text, images, audio or video content", "Only spreadsheets", "Physical hardware"],
        "answer": 1,
    },
    {
        "q": "'Bias in AI' usually results from:",
        "options": ["Too much encryption", "Unrepresentative or skewed training data", "Too many servers", "Fast internet speed"],
        "answer": 1,
    },
    {
        "q": "Which regulation-focused principle supports Responsible AI?",
        "options": ["Human Oversight", "Ignoring user consent", "Unlimited data collection", "Hiding algorithms permanently"],
        "answer": 0,
    },
]

AI_NEWS = [
    {
        "title": "Explainable AI Becomes a Core Requirement in Enterprise Systems",
        "summary": "Organizations are increasingly adopting Explainable AI (XAI) frameworks so that automated decisions in finance, healthcare and hiring can be audited and understood by humans.",
        "date": "2026-07-12",
        "category": "Responsible AI",
        "icon": "fa-solid fa-brain",
    },
    {
        "title": "Global Push for AI Regulation Gains Momentum",
        "summary": "Governments across the world are drafting new digital trust frameworks that require transparency reports and risk assessments before deploying large-scale AI systems.",
        "date": "2026-06-28",
        "category": "Policy",
        "icon": "fa-solid fa-scale-balanced",
    },
    {
        "title": "Deepfake Detection Tools See Major Accuracy Improvements",
        "summary": "New detection models combining audio, video and metadata analysis are helping platforms flag synthetic media faster, protecting users from misinformation.",
        "date": "2026-06-15",
        "category": "Security",
        "icon": "fa-solid fa-shield-halved",
    },
    {
        "title": "Privacy-Preserving Machine Learning Gains Industry Adoption",
        "summary": "Techniques like federated learning and differential privacy let companies train AI models without exposing individual user data, strengthening digital trust.",
        "date": "2026-05-30",
        "category": "Privacy",
        "icon": "fa-solid fa-user-shield",
    },
    {
        "title": "Universities Introduce Dedicated 'AI Ethics & Trust' Courses",
        "summary": "Reflecting industry demand, engineering colleges are adding coursework on responsible AI design, bias mitigation, and digital trust engineering.",
        "date": "2026-05-10",
        "category": "Education",
        "icon": "fa-solid fa-graduation-cap",
    },
    {
        "title": "Encryption Standards Updated to Counter AI-Assisted Attacks",
        "summary": "Cybersecurity bodies have released updated encryption guidelines to defend against increasingly sophisticated AI-powered cyberattacks.",
        "date": "2026-04-22",
        "category": "Cybersecurity",
        "icon": "fa-solid fa-lock",
    },
]

TEAM = [
    {
        "name": "Project Developer",
        "role": "Full Stack Python Developer & UI/UX Designer",
        "bio": "Designed and built this project end-to-end — Flask backend, SQLite database, and the complete responsive front-end — as part of the Second Year AI & ML curriculum.",
        "icon": "fa-solid fa-code",
    },
    {
        "name": "Faculty Guide",
        "role": "Project Mentor, Dept. of AI & ML",
        "bio": "Guided the research direction on AI ethics, digital trust principles and evaluation of the final deliverable.",
        "icon": "fa-solid fa-chalkboard-user",
    },
]


# ---------------------------------------------------------------------
# Admin auth decorator
# ---------------------------------------------------------------------

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Please log in to access the admin dashboard.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ---------------------------------------------------------------------
# Public Routes
# ---------------------------------------------------------------------

@app.route("/")
def index():
    stats = {
        "topics_covered": 10,
        "quiz_questions": len(QUIZ_QUESTIONS),
        "news_articles": len(AI_NEWS),
        "trust_factors": 5,
    }
    return render_template("index.html", stats=stats)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/digital-trust")
def digital_trust():
    return render_template("digital_trust.html")


@app.route("/challenges")
def challenges():
    return render_template("challenges.html")


@app.route("/solutions")
def solutions():
    return render_template("solutions.html")


@app.route("/news")
def news():
    return render_template("news.html", news_items=AI_NEWS)


@app.route("/about-us")
def about_us():
    return render_template("about_us.html", team=TEAM)


# ---------------------------------------------------------------------
# Quiz
# ---------------------------------------------------------------------

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        name = request.form.get("name", "Anonymous").strip() or "Anonymous"
        score = 0

        for i, question in enumerate(QUIZ_QUESTIONS):
            selected = request.form.get(f"q{i}")
            if selected is not None and int(selected) == question["answer"]:
                score += 1

        total = len(QUIZ_QUESTIONS)
        percentage = round((score / total) * 100, 1)
        db.insert_quiz_result(name, score, total, percentage)

        if percentage >= 80:
            message = "Excellent! You have a strong understanding of AI & Digital Trust."
            level = "excellent"
        elif percentage >= 50:
            message = "Good job! You know the basics — a bit more reading will help."
            level = "good"
        else:
            message = "Keep learning! Revisit the About AI and Digital Trust sections."
            level = "needs-improvement"

        return render_template(
            "result.html",
            name=name, score=score, total=total,
            percentage=percentage, message=message, level=level,
        )

    return render_template("quiz.html", questions=QUIZ_QUESTIONS)


# ---------------------------------------------------------------------
# AI Trust Calculator
# ---------------------------------------------------------------------

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    result = None
    if request.method == "POST":
        name = request.form.get("name", "Anonymous").strip() or "Anonymous"

        answers = {
            "strong_password": request.form.get("strong_password", "no"),
            "mfa_enabled": request.form.get("mfa_enabled", "no"),
            "data_backup": request.form.get("data_backup", "no"),
            "privacy_awareness": request.form.get("privacy_awareness", "no"),
            "secure_browsing": request.form.get("secure_browsing", "no"),
        }

        # Each "yes" answer contributes 20 points -> total out of 100
        score = sum(20 for v in answers.values() if v == "yes")
        db.insert_trust_score(name, score, answers)

        recommendations = []
        if answers["strong_password"] != "yes":
            recommendations.append("Use a strong, unique password with a mix of letters, numbers and symbols.")
        if answers["mfa_enabled"] != "yes":
            recommendations.append("Enable Multi-Factor Authentication (MFA) on all important accounts.")
        if answers["data_backup"] != "yes":
            recommendations.append("Maintain regular backups of important data (cloud or offline).")
        if answers["privacy_awareness"] != "yes":
            recommendations.append("Review privacy settings and permissions on apps and websites regularly.")
        if answers["secure_browsing"] != "yes":
            recommendations.append("Always browse using HTTPS and avoid untrusted public Wi-Fi for sensitive tasks.")

        if not recommendations:
            recommendations.append("Great job! Keep following these digital trust best practices.")

        if score >= 80:
            level = "High Trust"
        elif score >= 50:
            level = "Moderate Trust"
        else:
            level = "Low Trust"

        result = {
            "name": name, "score": score, "level": level,
            "recommendations": recommendations,
        }

    return render_template("calculator.html", result=result)


# ---------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("contact"))

        if "@" not in email or "." not in email:
            flash("Please enter a valid email address.", "error")
            return redirect(url_for("contact"))

        db.insert_contact(name, email, subject, message)
        flash("Thank you! Your message has been submitted successfully.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")


# ---------------------------------------------------------------------
# Admin Auth + Dashboard
# ---------------------------------------------------------------------

@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        admin = db.get_admin_by_username(username)
        if admin and check_password_hash(admin["password_hash"], password):
            session["admin_logged_in"] = True
            session["admin_username"] = username
            flash("Welcome back, admin!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/admin/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/admin/dashboard")
@admin_required
def dashboard():
    stats = db.get_dashboard_stats()
    contacts = db.get_all_contacts()
    quiz_results = db.get_all_quiz_results()
    trust_scores = db.get_all_trust_scores()

    return render_template(
        "dashboard.html",
        stats=stats, contacts=contacts,
        quiz_results=quiz_results, trust_scores=trust_scores,
    )


# ---------------------------------------------------------------------
# Error Handling
# ---------------------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


# ---------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
