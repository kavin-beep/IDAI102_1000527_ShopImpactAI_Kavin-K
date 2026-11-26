# Test evidence

On 26 November 2026, all 90 tests passed with Python 3.12 using:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The local Streamlit app also started successfully and returned HTTP 200 from its root page on
`127.0.0.1:8504`. This is a local startup smoke test, not evidence that the public deployment or its
hosted PostgreSQL persistence works. The current shared public page showed Streamlit's **Not found** screen.

The Streamlit tests verify the two-tab username login page, absence of email and recovery controls, account creation
with passwords up to eight characters, and saved purchases after signing out and signing in again. They also cover
the Eco Journey plant's wilted, happy, growing and empty-month moods and its five evolving level forms, plus
shopping, wishlist, insights, themes and backups. Logic tests cover calculations, validation, estimate provenance,
CSV safety, backups and wishlist rules.

The suite also includes tests for account services and legacy email/database setup modules. Email delivery and
password recovery are not available in the current account UI.

## Manual review and evidence limits

The app saves user purchases and preferences to the configured account database. Local development uses SQLite;
public hosting requires persistent PostgreSQL configuration. JSON export/import is also provided for user backups.

Five genuine, dated informal feedback responses from friends, family and a classmate are recorded in the README.
They are self-reported impressions, not a structured task-based usability study. The
[usability feedback template](usability-feedback.md) supports more detailed follow-up; earlier AI heuristic
inspections are not participant observations.

The Turtle artwork is generated as SVG through Python Turtle navigation; the browser displays that image rather than
running a live Turtle animation.
