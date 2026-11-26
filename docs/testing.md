# Test evidence

On 26 November 2026, all 86 tests passed with Python 3.12 using:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The Streamlit tests verify that the app opens directly on the home dashboard, does not render login or email controls,
keeps guest data isolated between sessions, and preserves intended shopping, wishlist, insights, theme and backup
behavior. Logic tests cover calculations, validation, estimate provenance, CSV safety, backups and wishlist rules.

The suite also includes tests for legacy account, email and database setup modules. Those modules remain in the
repository but are not used by the running app. Their tests do not imply that sign-in, email delivery or persistent
database storage is available in the current UI.

## Manual review and evidence limits

The app's current behavior is directly home, with a session-only workspace. JSON export/import is provided so users
can keep a backup. Session state is temporary and may be cleared after refresh, reconnect, deployment or restart.

The [usability feedback template](usability-feedback.md) is not evidence of participant testing. No genuine
participant feedback has been collected. Earlier AI heuristic inspections of the sign-in flow describe the previous
design and are not participant feedback or evidence about the current interface.

The Turtle artwork is generated as SVG through Python Turtle navigation; the browser displays that image rather than
running a live Turtle animation.
