# Legacy email setup

Email verification and password-reset helpers remain in the repository for legacy service tests, but are not used by
the current account UI. The app only displays **Sign in** and **Create account** tabs and identifies accounts by
username; it does not send account emails or provide password recovery.

Do not configure Gmail for the current app. Account passwords are stored as salted Argon2id hashes in the configured
SQLite or PostgreSQL account database.
