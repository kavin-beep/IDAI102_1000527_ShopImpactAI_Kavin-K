# Repository readiness review

I reviewed the repository on 25 November 2026. I maintain the core application at
`kavin-beep/IDAI102_1000527_ShopImpactAI_Kavin-K`.

## Small improvements completed

- Invalid optional email settings show a safe warning instead of preventing sign-in. Purchase saving and recovery codes continue to work; unavailable email reset remains disabled.
- Gmail setup accurately describes optional verification and verified-address password resets. Signup still opens the home page immediately.
- The chart uses the consistent CO₂e label. How it works explains manufacturing, packaging, transport, and the role of spending in simple language.
- TOML, imported directly by setup tools, is explicitly pinned in requirements.txt.
- Ignore rules cover private environment files, database files, recovery-code downloads, purchase exports and disposable caches. The example settings, source data, artwork, tests, documentation and explanation PDFs remain available for the repository.

## Verification

I passed all 94 automated tests in the project Python 3.12 environment. I ran the dependency check and found no broken requirements. I covered purchase calculations and validation, import/export, account isolation, signup/login, recovery, conflicting saves, email actions, Insights and Streamlit UI interactions. I wrote the email-configuration regression test to sign in and save a purchase despite invalid SMTP settings.

I rechecked the supplied assessment brief against docs/requirements.md. I implemented the required purchase fields, live calculations, monthly dashboard, badges, alternatives, Python data structures and conditional Turtle artwork. I included the existing screenshots and the 15-record synthetic test fixture. I still need to confirm the Turtle desktop preview and assessor acceptance of the SVG integration.

I verified private-file exclusions using Git's own ignore handling with temporary metadata outside the project. I found no real credentials in my targeted scan of eligible text files. I deliberately kept the connection strings in setup tests synthetic and my real database settings private. I changed no live user data during this review.

## Before public launch and final submission

1. Rotate the Neon database password previously shared in chat, then update private local and hosted settings. Do not put the replacement connection string in the repository or chat.
2. Confirm assessor access to `kavin-beep/IDAI102_1000527_ShopImpactAI_Kavin-K` as specified by the brief.
3. Deploy app.py to Streamlit Cloud with private PostgreSQL settings. Verify two-account isolation, recovery, downloads and persistence after redeployment. Add the actual public URL to the README.
4. If enabling email, complete private Gmail setup and check inbox delivery and reset links from the deployed app. Recovery codes remain available without email.
5. Gather actual participant feedback using docs/usability-feedback.md; record changes and retest them. Complete keyboard and screen-reader checks and database backup restoration checks.
6. Complete the assessment submission PDF with my actual name, registration number, school, course and project links. The ten-page explanation PDF is a learning guide, not that completed submission.

Public deployment, real feedback and final submission are pending. Passing automated tests alone does not establish those outcomes or guarantee an assessment grade.
