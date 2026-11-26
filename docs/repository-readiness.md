# Repository readiness review

Reviewed 26 November 2026. The core application is maintained at
`kavin-beep/IDAI102_1000527_ShopImpactAI_Kavin-K`.

## Current app behavior

- The app opens directly on the dashboard. Sign-in, account creation, recovery, email verification and reset UI are removed.
- Purchases, wishlist entries and preferences live only in the active Streamlit session. They are not written to a database and may be lost after a refresh, reconnect or restart.
- The app does not require database or email secrets. Legacy account, email and database setup modules remain in the repository but are not used by the running app.
- The README, deployment instructions, assessment status and testing evidence now describe the session-only behavior. Existing screenshots still show the previous account-enabled design and are labelled as such; a current direct-home screenshot is pending.

## Verification

All 86 automated tests pass in the project Python 3.12 environment. Tests verify direct home access, no login/email controls, session isolation, shopping interactions, calculations and backup handling. Separate legacy tests still exercise inactive account/email/database services; their presence does not indicate these features are available in the active UI.

The supplied assessment brief was rechecked against docs/requirements.md. The required purchase fields, live calculations, monthly dashboard, badges, alternatives, Python data structures and conditional Turtle artwork are implemented. Existing screenshots and the 15-record synthetic test fixture are present. Turtle desktop preview and assessor acceptance of the SVG integration remain to be confirmed.

Private-file exclusions were verified using Git's own ignore handling with temporary metadata outside the project. No real credentials were found by the targeted scan of eligible text files. The connection strings in setup tests are deliberately synthetic; real database settings remain private. No live user data was changed during this review.

## Before public launch and final submission

1. Confirm assessor access to `kavin-beep/IDAI102_1000527_ShopImpactAI_Kavin-K` as specified by the brief.
2. Deploy `app.py` to Streamlit Cloud without database or email secrets. Verify direct home access and JSON backup export/import.
3. Gather actual participant feedback using `docs/usability-feedback.md`; record changes and retest them. Do not present AI inspection as participant feedback.
4. Complete the assessment submission PDF with the actual student name, registration number, school, course and project links. The ten-page explanation PDF is a learning guide, not that completed submission.

Real participant feedback and final submission details remain pending. Passing automated tests alone does not establish those outcomes or guarantee an assessment grade.
