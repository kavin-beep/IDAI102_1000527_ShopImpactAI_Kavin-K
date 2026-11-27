"""Tests for eco points, wishlist resolution and journey summaries."""

import unittest
from datetime import date
from decimal import Decimal
import journey
from logic import make_purchase


def buy(category, day, price=100):
    """Create a purchase fixture for eco-points and wishlist tests."""
    return make_purchase(category, price, "Test shop", day)


class JourneyTests(unittest.TestCase):
    """Verify points, levels, streaks, milestones, equivalents, and wishlist rules."""
    def test_points_and_breakdown(self):
        """Verifies points and breakdown."""
        records = [buy("Repair services", "2026-10-01"), buy("New clothing", "2026-10-02")]
        wish = journey.make_wish("Headphones", "New electronics", 2000, date(2026, 10, 1))
        wishlist = journey.resolve_wish([wish], wish["id"], "skipped", date(2026, 10, 9))
        total, breakdown = journey.eco_points(records, wishlist)
        self.assertEqual(breakdown["Purchases logged"], 10)
        self.assertEqual(breakdown["Reuse, repair & reusable choices"], 20)
        self.assertEqual(breakdown["Repair bonus"], 15)
        self.assertEqual(breakdown["Mindful skips"], 25)
        self.assertEqual(total, 70)

    def test_levels_and_boundaries(self):
        """Verifies levels and boundaries."""
        self.assertEqual(journey.level_for(0)["name"], "Seedling")
        self.assertEqual(journey.level_for(59)["to_next"], 1)
        self.assertEqual(journey.level_for(60)["name"], "Sprout")
        top = journey.level_for(5000)
        self.assertEqual((top["name"], top["progress"], top["next_name"]), ("Forest keeper", 1.0, None))
        self.assertAlmostEqual(journey.level_for(120)["progress"], 0.5)

    def test_streak_counts_consecutive_months_with_grace_for_current(self):
        """Verifies streak counts consecutive months with grace for current."""
        records = [buy("Second-hand clothing", d) for d in ("2026-07-03", "2026-08-03", "2026-09-03")]
        self.assertEqual(journey.reuse_streak(records, "2026-09"), 3)
        self.assertEqual(journey.reuse_streak(records, "2026-10"), 3)  # October still in progress
        self.assertEqual(journey.reuse_streak(records, "2026-11"), 0)
        records.append(buy("New clothing", "2026-06-01"))  # not a reuse choice
        self.assertEqual(journey.reuse_streak(records, "2026-09"), 3)

    def test_milestones(self):
        """Verifies milestones."""
        records = [buy("Repair services", "2026-10-0%d" % d, 50) for d in (1, 2, 3)]
        earned = {m["name"]: m["earned"] for m in journey.milestones(records, [], "2026-10", 10000, 100)}
        self.assertTrue(earned["First step"] and earned["Fixer"] and earned["Second life"] and earned["Goal keeper"])
        self.assertFalse(earned["Mindful pause"] or earned["Thoughtful ten"] or earned["Steady habit"])

    def test_goal_keeper_needs_both_goals(self):
        """Verifies goal keeper needs both goals."""
        records = [buy("New clothing", "2026-10-0%d" % d, 5000) for d in (1, 2, 3)]
        self.assertEqual(journey.goal_months(records, 10000, 100), [])
        self.assertEqual(journey.goal_months(records, 20000, 100), ["2026-10"])

    def test_equivalents_use_sourced_factors(self):
        """Verifies equivalents use sourced factors."""
        rows = {r["key"]: r["value"] for r in journey.equivalents(Decimal("24.42"))}
        self.assertEqual(rows["car_km"], Decimal("100.0"))
        self.assertEqual(rows["phone_charge"], Decimal("1969.4"))
        self.assertEqual(rows["tree_month"], Decimal("4.9"))
        self.assertTrue(all(v == 0 for v in (r["value"] for r in journey.equivalents(0))))

    def test_wishlist_lifecycle(self):
        """Verifies wishlist lifecycle."""
        wish = journey.make_wish("  Jacket ", "New clothing", 1000, date(2026, 10, 1))
        self.assertEqual((wish["name"], wish["estimated_co2"], wish["status"]), ("Jacket", "1.24", "waiting"))
        self.assertEqual(journey.days_waiting(wish, date(2026, 10, 8)), 7)
        wishlist = journey.add_wish([], wish)
        bought = journey.resolve_wish(wishlist, wish["id"], "bought", date(2026, 10, 5))
        self.assertEqual(wishlist[0]["status"], "waiting")  # original list untouched
        self.assertEqual(journey.days_waiting(bought[0], date(2030, 1, 1)), 4)
        purchase = journey.wish_to_purchase(bought[0], date(2026, 10, 5))
        self.assertEqual((purchase["brand"], purchase["price"], purchase["estimated_co2"]), ("Jacket", "1000.00", "1.24"))
        self.assertEqual(journey.remove_wish(bought, wish["id"]), [])

    def test_wishlist_summary_and_validation(self):
        """Verifies wishlist summary and validation."""
        a = journey.make_wish("A", "New clothing", 1000)
        b = journey.make_wish("B", "New electronics", 3000)
        items = journey.resolve_wish([a, b], a["id"], "skipped")
        totals = journey.wishlist_summary(items)
        self.assertEqual((totals["waiting"], totals["skipped"], totals["kept"], totals["co2_not_added"]), (1, 1, Decimal("1000.00"), Decimal("1.24")))
        for bad in ("", " ", "x" * 81):
            with self.subTest(name=bad), self.assertRaises(ValueError):
                journey.make_wish(bad, "New clothing", 10)
        with self.assertRaises(ValueError):
            journey.make_wish("Thing", "Unknown", 10)
        with self.assertRaises(ValueError):
            journey.resolve_wish(items, "missing", "skipped")
        with self.assertRaises(ValueError):
            journey.resolve_wish(items, a["id"], "waiting")
        with self.assertRaises(ValueError):
            journey.add_wish([a] * journey.WISHLIST_LIMIT, b)

    def test_month_story(self):
        """Verifies month story."""
        self.assertIn("blank page", journey.month_story([], "2026-10", 10000, 100))
        records = [buy("Second-hand clothing", "2026-10-01"), buy("Repair services", "2026-10-02")]
        story = journey.month_story(records, "2026-10", 10000, 100)
        self.assertIn("2 entries", story)
        self.assertIn("inside both goals", story)


if __name__ == "__main__":
    unittest.main()
