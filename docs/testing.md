# Test evidence

On 26 November 2026, all 88 tests passed with Python 3.12 using:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The Streamlit tests verify the two-tab username login page, absence of email and recovery controls, account creation
with passwords up to eight characters, and saved purchases after signing out and signing in again. They also cover
shopping, wishlist, insights, themes and backups. Logic tests cover calculations, validation, estimate provenance, CSV
safety, backups and wishlist rules.

The suite also includes tests for account services and legacy email/database setup modules. Email delivery and
password recovery are not available in the current account UI.

## Manual review and evidence limits

The app saves user purchases and preferences to the configured account database. Local development uses SQLite;
public hosting requires persistent PostgreSQL configuration. JSON export/import is also provided for user backups.

The [usability feedback template](usability-feedback.md) is not evidence of participant testing. No genuine
participant feedback has been collected. Earlier AI heuristic inspections are not participant feedback or evidence
about the current interface.

The Turtle artwork is generated as SVG through Python Turtle navigation; the browser displays that image rather than
running a live Turtle animation.
