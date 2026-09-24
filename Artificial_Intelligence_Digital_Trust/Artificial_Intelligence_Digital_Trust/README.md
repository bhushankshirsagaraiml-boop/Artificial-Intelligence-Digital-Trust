# Artificial Intelligence & Digital Trust

A full-stack **Flask + SQLite** mini project built for a Second Year B.Tech (AI & ML) subject,
exploring how Artificial Intelligence and Digital Trust intersect — covering AI fundamentals,
digital trust principles, real-world challenges, and practical solutions, wrapped in a modern,
animated, glassmorphism UI.

---

## Features

- **10 pages**: Home, About AI, Digital Trust, AI Challenges, AI Solutions, AI Quiz,
  AI Trust Calculator, AI News, Contact, About Us, plus an Admin Login & Dashboard.
- **Interactive AI Quiz** — 10 MCQs scored on the backend, with a results page and
  animated score ring.
- **AI Trust Calculator** — a 5-question personal digital-trust assessment with a
  score out of 100, progress bar, and tailored recommendations.
- **Contact form** with server-side validation, stored in SQLite.
- **Password-protected Admin Dashboard** with Chart.js visualizations of quiz results,
  trust scores, and contact submissions.
- **Modern UI**: dark blue + cyan theme, glassmorphism cards, animated hero, scroll-reveal
  animations, animated counters, accordion FAQs, dark/light mode toggle, live search,
  scroll-to-top button, and a fully responsive layout.

---

## Tech Stack

| Layer      | Technology                          |
|------------|--------------------------------------|
| Backend    | Python 3, Flask                      |
| Database   | SQLite (auto-created on first run)   |
| Frontend   | HTML5, CSS3, Vanilla JavaScript      |
| Charts     | Chart.js                             |
| Icons      | Font Awesome 6                       |
| Fonts      | Space Grotesk + Inter (Google Fonts) |

---

## Project Structure

```
Artificial_Intelligence_Digital_Trust/
│
├── app.py                 # Main Flask application (routes, logic)
├── database.py             # SQLite connection, schema, CRUD helpers
├── database.db              # Auto-created on first run
├── requirements.txt
├── README.md
│
├── static/
│   ├── css/style.css        # Full design system & animations
│   ├── js/script.js         # Interactivity: theme, reveal, counters, search...
│   ├── images/
│   └── icons/
│
└── templates/
    ├── base.html             # Shared navbar / footer / layout
    ├── index.html            # Home
    ├── about.html            # About AI
    ├── digital_trust.html    # Digital Trust
    ├── challenges.html       # AI Challenges
    ├── solutions.html        # AI Solutions
    ├── quiz.html             # AI Quiz
    ├── result.html           # Quiz result page
    ├── calculator.html       # AI Trust Calculator
    ├── news.html              # AI News
    ├── contact.html            # Contact form
    ├── about_us.html            # About the project/team
    ├── login.html               # Admin login
    ├── dashboard.html           # Admin dashboard
    ├── 404.html
    └── 500.html
```

---

## Installation & Setup

**1. Clone / extract the project, then move into the folder:**
```bash
cd Artificial_Intelligence_Digital_Trust
```

**2. (Recommended) Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the app:**
```bash
python app.py
```

**5. Open your browser at:**
```
http://127.0.0.1:5000
```

The SQLite database (`database.db`) and all required tables are created automatically
the first time you run the app — no manual setup needed.

---

## Admin Dashboard

Navigate to `/admin/login` (also linked in the footer).

**Default credentials:**
```
Username: admin
Password: admin123
```

> For a real deployment, change the default admin password and the Flask
> `secret_key` in `app.py` before going live.

The dashboard shows:
- All contact form submissions
- All AI Quiz attempts (with score & percentage)
- All AI Trust Calculator results
- Two live Chart.js graphs (quiz score distribution & trust score trend)

---

## Database Tables

| Table          | Purpose                                              |
|----------------|-------------------------------------------------------|
| `contacts`     | Stores name, email, subject, message, timestamp       |
| `quiz_results` | Stores name, score, total, percentage, timestamp      |
| `trust_scores` | Stores name, score, and the 5 yes/no factor answers   |
| `admin_users`  | Stores admin username + hashed password               |

---

## Notes

- All forms are validated both on the client (HTML5 `required`) and the server
  (Flask route logic) with flash messages for feedback.
- Passwords are stored using Werkzeug's `generate_password_hash` / `check_password_hash`
  — never in plain text.
- The UI theme (dark/light) is remembered via a browser cookie.
