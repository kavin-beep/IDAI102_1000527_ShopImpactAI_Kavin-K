# Repository readiness review

Reviewed 26 November 2026. The core application is maintained at
`kavin-beep/IDAI102_1000527_ShopImpactAI_Kavin-K`.

## Current app behavior

- The app opens on a username/password sign-in page with only **Sign in** and **Create account** tabs. No email or password recovery option is shown.
- New accounts accept passwords from 1–8 characters. Passwords are stored as salted Argon2id hashes and login attempts are rate-limited.
- Purchases, wishlist entries and preferences are saved per account in SQLite locally or PostgreSQL when hosted.
- Persistent data on Streamlit Cloud requires private PostgreSQL settings. Email setup files remain in the repository but are not used by the account UI.

## Verification

The Python 3.12 test suite covers username sign-in, account creation, database persistence, password hashing/rate limiting, and shopping interactions, calculations and backup handling. Tests use disposable databases and synthetic data.

The supplied assessment brief was rechecked against docs/requirements.md. The required purchase fields, live calculations, monthly dashboard, badges, alternatives, Python data structures and conditional Turtle artwork are implemented. Existing screenshots and the 15-record synthetic test fixture are present. Turtle desktop preview and assessor acceptance of the SVG integration remain to be confirmed.

Private-file exclusions were verified using Git's own ignore handling with temporary metadata outside the project. No real credentials were found by the targeted scan of eligible text files. The connection strings in setup tests are deliberately synthetic; real database settings remain private. No live user data was changed during this review.

## Before public launch and final submission

1. Confirm assessor access to `kavin-beep/IDAI102_1000527_ShopImpactAI_Kavin-K` as specified by the brief.
2. Verify Streamlit Cloud has a persistent PostgreSQL URL configured and confirm account data survives sign-out, sign-in and redeployment.
3. Gather actual participant feedback using `docs/usability-feedback.md`; record changes and retest them. Do not present AI inspection as participant feedback.
4. Complete the assessment submission PDF with the actual student name, registration number, school, course and project links. The ten-page explanation PDF is a learning guide, not that completed submission.

Real participant feedback and final submission details remain pending. Passing automated tests alone does not establish those outcomes or guarantee an assessment grade.
