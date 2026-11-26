# Public deployment

Live app: [ShopImpact on Streamlit Community Cloud](https://shopimpact-duy7hphexgoshhqfexfmkt.streamlit.app/).

The current app opens directly to the dashboard. It does not require sign-in, email, database configuration or private
secrets. Deploy `app.py` from this repository on Streamlit Community Cloud and install the pinned dependencies from
`requirements.txt`.

## Data behavior

Purchases, wishlist entries and preferences are held in Streamlit session state only. The app does not save them to a
database. Sessions are separate, but anyone using the same active browser session can see its workspace. Data may be
lost after a refresh, reconnect, deployment or server restart. Download a JSON backup before ending the session if
you need to keep entries.

## Publish and verify

1. Push the repository to GitHub and create a Streamlit Community Cloud app with `app.py` as the entry point.
2. Deploy without database or email secrets.
3. Confirm the dashboard opens without a sign-in screen and that no email or account forms are shown.
4. Add a test purchase, confirm the totals update, then download and restore a JSON backup.
5. Confirm a fresh browser session starts with an empty workspace. Do not expect records to survive session loss or
   an app restart.
6. Check narrow screens, keyboard use, contrast, uploads and downloads.

## Legacy setup files

The repository retains account, email and database setup modules and their unit tests for historical compatibility.
They are not imported or used by the current app. The [Neon guide](neon-setup.md) and
[Gmail guide](email-setup.md) are not required for this release. Do not configure a database or email provider for
the current deployment.
