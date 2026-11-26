"""Exercise username sign-in and the persistent Streamlit account workspace."""
import os
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch
from accounts import Accounts
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"
PASSWORD = "Alice123"


def by_label(elements, label):
    return next(item for item in elements if item.label == label)


class AppTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.url = "sqlite:///" + (Path(self.tmp.name) / "ui.db").as_posix()
        self.env = patch.dict(os.environ, {"SHOPIMPACT_DATABASE_URL": self.url, "SHOPIMPACT_PUBLIC": "false"})
        self.env.start()
        from account_ui import account_service
        account_service.clear()
        self.db = Accounts(self.url)
        self.db.register_username_password("alice", PASSWORD)

    def tearDown(self):
        from account_ui import account_service
        account_service(self.url, False).engine.dispose()
        account_service.clear()
        self.db.engine.dispose()
        self.env.stop()
        self.tmp.cleanup()

    def start(self):
        app = AppTest.from_file(str(APP), default_timeout=30).run()
        self.assertFalse(app.exception)
        return app

    def sign_in(self, app, username="alice", password=PASSWORD):
        app.text_input(key="login_name").set_value(username)
        app.text_input(key="login_password").set_value(password)
        by_label(app.button, "Sign in").click().run()
        self.assertFalse(app.exception)
        return app

    def app(self):
        return self.sign_in(self.start())

    def test_login_page_has_only_sign_in_and_create_account(self):
        app = self.start()
        self.assertEqual([tab.label for tab in app.tabs], ["Sign in", "Create account"])
        labels = {item.label for item in app.text_input}
        self.assertIn("Username", labels)
        self.assertIn("Password", labels)
        self.assertNotIn("Email or username", labels)
        self.assertNotIn("Email address", labels)
        self.assertFalse(any("Recover" in item.label for item in app.button))

    def test_plant_mood_tracks_monthly_spending_and_carbon_goals(self):
        from ui import plant_mood

        self.assertEqual(plant_mood(1200, 5, 1000, 10, 2), "wilted")
        self.assertEqual(plant_mood(900, 8, 1000, 10, 2), "happy")
        self.assertEqual(plant_mood(900, 12, 1000, 10, 2), "growing")
        self.assertEqual(plant_mood(0, 0, 1000, 10, 0), "growing")

    def test_registration_password_limit_and_saved_login_after_sign_out(self):
        app = self.start()
        by_label(app.text_input, "Choose a username").set_value("newuser")
        by_label(app.text_input, "Choose a password").set_value("N3wPass8")
        by_label(app.text_input, "Confirm password").set_value("N3wPass8")
        by_label(app.button, "Create account").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["account_data"]["username"], "newuser")

        app.text_input(key="new_brand").set_value("Saved shop")
        app.button(key="add").click().run()
        self.assertFalse(app.exception)
        by_label(app.button, "Sign out").click().run()
        self.assertFalse(app.exception)
        self.sign_in(app, "newuser", "N3wPass8")
        self.assertEqual(by_label(app.metric, "Monthly spend").value, "INR 500.00")

        with self.assertRaises(ValueError):
            self.db.register_username_password("longpass", "password9")

    def test_themes_work_before_sign_in_and_preserve_account_data(self):
        app = self.start()
        app.selectbox(key="visual_theme").select("Night").run()
        self.assertFalse(app.exception)
        self.assertTrue(any("si-night" in item.value for item in app.markdown))
        app.checkbox(key="scenery_motion").uncheck().run()
        self.assertTrue(any("si-night si-paused" in item.value for item in app.markdown))
        self.sign_in(app)
        original = app.session_state["account_data"].copy()
        for theme in ["Day", "Normal", "Night"]:
            app.selectbox(key="visual_theme").select(theme).run()
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state["account_data"], original)
        app.checkbox(key="contrast").check().run()
        self.assertTrue(any(".si-scenery {display:none;}" in item.value for item in app.markdown))

    def test_deployment_refreshes_cached_rules_and_backup_version(self):
        import logic
        import storage
        with patch.object(logic, "VERSION", "epa-2022-inr-reference-v2"), patch.object(
            storage, "VERSION", "epa-2022-inr-reference-v2"
        ):
            app = self.app()
            self.assertFalse(app.exception)
            self.assertEqual(logic.VERSION, "useeio-2024-inr-reference-v3")
            self.assertEqual(storage.VERSION, logic.VERSION)

    def test_saved_estimates_change_only_after_confirmed_recalculation(self):
        from logic import make_purchase, VERSION
        row = make_purchase("New clothing", 1000, "Saved shop", date.today())
        row.update(methodology="epa-2022-inr-reference-v2", estimated_co2="1.53")
        token = self.db.login("alice", PASSWORD)
        saved = self.db.load(token)
        self.db.save(token, [row], saved["settings"], saved["revision"])
        app = self.app()
        self.assertEqual(app.metric[1].value, "1.53 kg")
        self.assertTrue(by_label(app.button, "Recalculate saved estimates").disabled)
        app.checkbox(key="approve_recalculation").check().run()
        by_label(app.button, "Recalculate saved estimates").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[1].value, "1.24 kg")
        latest = self.db.load(token)
        self.assertEqual(latest["purchases"][0]["methodology"], VERSION)
        self.assertEqual(latest["settings"], saved["settings"])

    def test_history_filters_limit_edit_choices_and_keep_saved_data(self):
        app = self.app()
        for brand in ["First shop", "Second shop"]:
            app.text_input(key="new_brand").set_value(brand)
            app.button(key="add").click().run()
        by_label(app.text_input, "Search purchases").set_value("Second shop").run()
        choices = by_label(app.selectbox, "Choose a purchase to edit").options
        self.assertEqual(len(choices), 1)
        self.assertIn("Second shop", choices[0])
        by_label(app.text_input, "Search purchases").set_value("No matches").run()
        self.assertFalse(app.exception)
        self.assertFalse(any(item.label == "Choose a purchase to edit" for item in app.selectbox))
        self.assertEqual(len(app.session_state["account_data"]["purchases"]), 2)

    def test_insights_follow_logged_month_and_saved_goal(self):
        app = self.app()
        app.text_input(key="new_brand").set_value("Insight shop")
        app.button(key="add").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(by_label(app.metric, "Average purchase").value, "INR 500.00")
        self.assertEqual(by_label(app.metric, "Spending goal remaining").value, "INR 9,500.00")
        self.assertEqual(by_label(app.metric, "Change from previous month").value, "No prior entries")
        app.number_input(key="budget").set_value(100.0)
        by_label(app.button, "Save goals & appearance").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(by_label(app.metric, "Above spending goal").value, "INR 400.00")

    def test_wishlist_skip_and_buy_keep_goals_and_history_separate(self):
        app = self.app()
        for name in ["Headphones", "Jacket"]:
            by_label(app.text_input, "What is it?").set_value(name)
            by_label(app.button, "Add to wishlist").click().run()
        wishlist = app.session_state["account_data"]["settings"]["wishlist"]
        self.assertEqual([w["name"] for w in wishlist], ["Headphones", "Jacket"])
        app.button(key=f"skip_{wishlist[0]['id']}").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["account_data"]["purchases"], [])
        self.assertEqual(by_label(app.metric, "Kept in your pocket").value, "INR 1,000.00")
        app.button(key=f"buy_{wishlist[1]['id']}").click().run()
        self.assertFalse(app.exception)
        saved = self.db.load(self.db.login("alice", PASSWORD))
        self.assertEqual([p["brand"] for p in saved["purchases"]], ["Jacket"])
        self.assertEqual({w["status"] for w in saved["settings"]["wishlist"]}, {"skipped", "bought"})

    def test_blank_brand_rejected(self):
        app = self.app()
        app.button(key="add").click().run()
        self.assertEqual(len(app.error), 1)
        self.assertEqual(app.session_state["account_data"]["purchases"], [])

    def test_add_edit_delete(self):
        app = self.app()
        app.text_input(key="new_brand").set_value("Local repair shop")
        app.selectbox(key="new_category").select("Repair services")
        app.button(key="add").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(by_label(app.metric, "Monthly spend").value, "INR 500.00")
        self.assertTrue(any("Repair Champion" in item.value for item in app.success))
        by_label(app.number_input, "Edit price (INR)").set_value(800.0)
        by_label(app.button, "Save changes").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(by_label(app.metric, "Monthly spend").value, "INR 800.00")
        by_label(app.checkbox, "Confirm deletion of this purchase").check().run()
        by_label(app.button, "Delete selected purchase").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["account_data"]["purchases"], [])


if __name__ == "__main__":
    unittest.main()
