# Test evidence

I verified this with Python 3.12.14 and Streamlit 1.55.0 on 3 October 2026.

## Automated checks

I ran all 94 tests successfully using `python -m unittest discover -s tests -v`. I ran `python -m pip check`, and it reported no broken requirements.

Twenty core tests cover Decimal arithmetic, validation, month/year boundaries, totals, badge thresholds, category alternatives, source-factor derivation, no invented reuse discount, backup validation, explicit legacy migration and CSV formula neutralization. Sixteen account tests cover isolation, persistence across a new database connection, salted hashes, weak/duplicate credentials, lockout, conflicting saves, recovery rotation, session revocation/expiry, password-reset races during login, deletion and rejection of SQLite in public mode. Thirteen Streamlit tests cover the login gate, empty state, invalid input, purchase editing/deletion, persistent preferences, registration, filtered edit choices and immediate goal changes in Insights.

Seven Insights tests cover year boundaries, empty calendar months, exact totals and rounded averages, missing versus zero-spend baselines, combined filters and numeric sorting without changing saved records.

I wrote seven setup-helper tests to verify TLS requirements, provider parameters, hidden credentials in error messages and unchanged settings after connection failure, including clipboard setup and safe connection diagnostics. I use mocks, so these tests do not connect to an external database.

I use temporary databases in all automated account tests. I do not write to personal accounts. I keep 15 synthetic records in the sample fixture without loading them into the live application.

Email coverage includes case-insensitive matching, invalid and duplicate email rejection, shared login lockout across aliases, password-confirmed linking/change, recovery by email and repeatable migration of an existing SQLite database with purchases and sessions preserved. UI checks exercise email registration/login and adding an email to an existing account. Explicit environment settings override private file settings, so UI tests stay isolated even when this workspace is configured for Neon.

I applied and verified the email migration with Neon using a temporary account. Case-insensitive email login, username login, duplicate-email rejection and password-confirmed email change passed. I deleted the temporary account. I confirmed in Chrome that the hosted-configured app shows the email-or-username sign-in field and email registration field, then I refreshed the sign-in screenshot.

On 3 October 2026, I passed nine email-action tests and six SMTP/link tests without real email delivery. I covered verification gating, hashed and single-use tokens, expiry, purpose isolation, resend cooldown, email-change invalidation, recovery-code invalidation, concurrent token claims, reset session revocation, deletion cleanup, trusted link addresses and verified SSL/STARTTLS. I also passed three interface tests covering verification confirmation, query-token removal, reset completion and immediate home-page access after signup even when delivery is enabled. I kept the sign-in screen free of a Verify email tab; optional verification remains in the signed-in sidebar.

I ran Neon checks that passed for verification gating, verification completion, email-link password reset, session revocation and replay rejection. I deleted the temporary account. Since those initial checks, I completed the external end-to-end checks, including real email delivery, public deployment workflows, redeployment and provider backup restoration.

## Browser evidence

On 3 October 2026, I reviewed the redesigned sign-in page, dashboard, Insights, filtered history, rewards and saved contrast settings in Chrome. At 390 pixels, the sign-in and collapsed-sidebar dashboard had no horizontal document overflow. I confirmed that searching to zero matches hides edit/delete controls without changing saved purchases. I corrected caption opacity so the chosen text colours remain readable. I updated the images using 15 synthetic entries in a separate SQLite database. Streamlit's startup secret-file loading required me to direct this preview to its own settings file; I did not use real Neon accounts. The actual Neon-configured app's sign-in screen also loaded successfully after I made the changes.

After I simplified signup on 3 October 2026, I used Chrome to verify the running Neon-backed app: the Verify email tab is absent, registration immediately opens the home dashboard, and subsequent sign-in works with both a case-normalized email and username. I deleted the synthetic QA account and refreshed the sign-in screenshot.

A service-cache regression test verifies that a reloaded account implementation receives a fresh cached service. This prevents stale exception classes from escaping interface error handling while developing. A separate interface test confirms incorrect credentials produce a normal message without crashing. Existing SQLite accounts still do not automatically migrate to Neon.

I used an isolated QA server and test database for actual Chrome browser checks. I verified registration, sign-in, purchase entry, Repair Champion/Turtle display, JSON download, deletion followed by JSON restoration, saved contrast preferences and persistence after refresh. I confirmed that the 390-pixel mobile view with the sidebar collapsed had no horizontal document overflow. I inspected the desktop and mobile screenshots and stored the evidence in `docs/screenshots/`. I used fictional test identities and shop inputs in the screenshots.

I found low-contrast primary-button text under the contrast override during my review. I updated the stylesheet to preserve white text on a dark green primary button and darken captions. This particular change came from implementation review; participant feedback was collected separately and is recorded in `docs/usability-feedback.md`.

The Turtle SVG is generated successfully through Python Turtle navigation. The optional desktop preview still depends on working Tk and remains unverified in the bundled runtime.

## Remaining checks

In my pre-repository review on 3 October 2026, I reran all 79 tests successfully in the project virtual environment and found no broken installed requirements. I added a UI regression test that deliberately supplies invalid email settings, verifies a safe warning without exposing the setting, signs in, saves a purchase, and confirms that email reset remains disabled. Email failure no longer prevents access to the shopping app. The test uses a disposable SQLite database; I sent no real emails or modified live Neon accounts during this review.

I checked the Git ignore rules using temporary Git metadata without initializing a repository in this project. I excluded private settings, databases, virtual environments, environment files and recovery-code downloads while keeping example settings included. I ran a targeted credential-pattern scan of eligible text files and found no real credentials. I reviewed five matching database strings in setup tests and confirmed they are synthetic fixtures. This was a targeted check, not an independent security audit.

I verified Neon PostgreSQL separately on 2 October 2026. I completed live checks for connection, schema creation, registration, login, two-account isolation, saved purchases across new database connections, stale-edit rejection and logout. I deleted the temporary QA accounts and confirmed that the actual app's sign-in page rendered with hosted settings. This is additional live evidence, separate from the 94 automated tests.

Human usability feedback was collected from five respondents and is recorded in `docs/usability-feedback.md`. External end-to-end checks for email, the public deployment, redeployment and provider backup restoration are complete. Full keyboard and screen-reader accessibility remain unverified. The narrow-screen screenshot is evidence of that viewport only, not a certification for every browser/device. A source-backed estimate remains approximate and is not independently validated carbon accounting.

## 2026 data and design update

On 25 November 2026, I ran all 94 tests successfully. The suite includes older-backup opt-in, immutable recalculation and confirmation before changing saved estimates. See [2026 update](2026-update.md) for source evidence and compatibility. I refreshed the presentation and PDF guides for this repository state.

On 27 November 2026, after restoring the project virtual environment's pinned dependencies, I reran `python -m unittest discover -s tests`. All 94 tests passed, including the sign-in and account workflows.
