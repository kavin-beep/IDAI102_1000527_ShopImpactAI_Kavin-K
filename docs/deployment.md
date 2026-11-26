# Public deployment

Live app: [ShopImpact on Streamlit Community Cloud](https://idai1021000527shopimpactaikavin-k-dt4pcaipehuzgmnvp9gr4b.streamlit.app/).

On 26 November 2026, the shared app page showed Streamlit's **Not found** screen, and direct checks redirected
to Streamlit's app-auth route. The deployment and its hosted database are therefore not verified from this
workspace; the deployment owner must confirm the app exists and is publicly accessible.

ShopImpact uses username/password accounts and saves purchases and preferences in a database. For Streamlit Community
Cloud, configure a persistent PostgreSQL database before relying on account data surviving deployments or restarts.

## Configure

Add these values to the app's private Streamlit Secrets, using a real provider connection string:

```toml
SHOPIMPACT_PUBLIC = true
SHOPIMPACT_DATABASE_URL = "postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE?sslmode=require"
```

Never commit database credentials. The app creates its schema on startup. Public mode rejects a local SQLite
database. For local development, no secrets are required; the app stores data in the ignored
`personal_data/shopimpact.db` file.

## Publish and verify

1. Push the repository to GitHub and create a Streamlit Community Cloud app with `app.py` as the entry point.
2. Add the persistent PostgreSQL secrets above and deploy.
3. Create an account with a username and password of 1–8 characters. The UI has only **Sign in** and **Create account**; no email or recovery flow is shown.
4. Add a purchase, sign out, sign in again, and confirm purchases and preferences remain.
5. Confirm account isolation with a second account and test JSON backup export/import.
6. Check narrow screens, keyboard use, contrast, uploads and downloads.

The [Neon guide](neon-setup.md) contains hosted database setup details. The Gmail guide is not needed by this account UI.
