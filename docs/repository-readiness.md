# Repository readiness review

Reviewed 26 November 2026. The core application is maintained at
`kavin-beep/IDAI102_1000527_ShopImpactAI_Kavin-K`.

## Current app behavior

- The app opens on a username/password sign-in page with only **Sign in** and **Create account** tabs. No email or password recovery option is shown.
- New accounts accept passwords from 1–8 characters. Passwords are stored as salted Argon2id hashes and login attempts are rate-limited.
- Purchases, wishlist entries and preferences are saved per account in SQLite locally or PostgreSQL when hosted.
- A dashboard plant pal gives eco tips, wiggles leaves on hover (unless reduced motion is enabled), and changes expression against monthly spending and estimated CO₂e goals.
- Persistent data on Streamlit Cloud requires private PostgreSQL settings. Email setup files remain in the repository but are not used by the account UI.

## Verification

The Python 3.12 suite has 89 passing tests covering username sign-in, account creation, database persistence, password hashing/rate limiting, plant mood rules and shopping interactions. Tests use disposable databases and synthetic data. A local Streamlit startup smoke test returned HTTP 200 on 26 November 2026.

All 23 Python source, test and tool files were checked; each has a module-level docstring describing its purpose. Inline comments are used where they clarify non-obvious behavior rather than repeating the code.

The supplied assessment brief was rechecked against docs/requirements.md. The required purchase fields, live calculations, monthly dashboard, badges, alternatives, Python data structures and conditional Turtle artwork are implemented. Existing screenshots and the 15-record synthetic test fixture are present. Turtle desktop preview and assessor acceptance of the SVG integration remain to be confirmed.

Private-file exclusions were verified using Git's own ignore handling with temporary metadata outside the project. No real credentials were found by the targeted scan of eligible text files. The connection strings in setup tests are deliberately synthetic; real database settings remain private. No live user data was changed during this review.

## Before public launch and final submission

1. Confirm assessor access to `kavin-beep/IDAI102_1000527_ShopImpactAI_Kavin-K` as specified by the brief.
2. The shared public app page currently shows Streamlit's **Not found** screen. Restore or confirm the deployment, then verify its private persistent PostgreSQL configuration and check that account data survives sign-out, sign-in and redeployment.
3. Five informal feedback responses are recorded in the README. If a structured usability study is required, use `docs/usability-feedback.md` to observe tasks, record changes and retest them; do not describe the informal comments or AI inspection as a formal study.
4. Complete the assessment submission PDF with the actual student name, registration number, school, course and project links. The ten-page explanation PDF is a learning guide, not that completed submission.

Structured usability testing and final submission details remain pending. Passing automated tests alone does not establish those outcomes or guarantee an assessment grade.
