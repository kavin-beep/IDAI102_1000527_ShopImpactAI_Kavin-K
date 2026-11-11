"""Eco Journey rules: points, levels, streaks, milestones, everyday equivalents
and the mindful wishlist. Pure Python with no interface code, so it is easy to test.

Journey points reward logging and reflective habits. They are encouragement only:
they never change the fixed monthly badge rules in logic.py and are not a
measurement of real-world emissions savings.
"""
import json
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from uuid import uuid4

from insights import shift_month
from logic import CATALOG, ROOT, impact, make_purchase, money, month_records, summary

EQUIVALENTS = json.loads((ROOT / "data/equivalents.json").read_text(encoding="utf-8"))

POINTS = {"logged": 5, "lower": 20, "repair": 15, "skipped": 25}
LEVELS = [
    (0, "Seedling", "🌱"),
    (60, "Sprout", "🌿"),
    (180, "Sapling", "🪴"),
    (400, "Young tree", "🌳"),
    (800, "Forest keeper", "🌲"),
]
WISHLIST_LIMIT = 200
WISH_STATUSES = {"waiting", "bought", "skipped"}


def _is_lower(purchase):
    return bool(CATALOG.get(purchase["product_type"], {}).get("lower_impact"))


def eco_points(records, wishlist=()):
    """Return total points and a labelled breakdown."""
    breakdown = {
        "Purchases logged": len(records) * POINTS["logged"],
        "Reuse, repair & reusable choices": sum(map(_is_lower, records)) * POINTS["lower"],
        "Repair bonus": sum(p["product_type"] == "Repair services" for p in records) * POINTS["repair"],
        "Mindful skips": sum(item.get("status") == "skipped" for item in wishlist) * POINTS["skipped"],
    }
    return sum(breakdown.values()), breakdown


def level_for(points):
    index = max(i for i, (threshold, _, _) in enumerate(LEVELS) if points >= threshold)
    threshold, name, icon = LEVELS[index]
    if index + 1 < len(LEVELS):
        upcoming, next_name, next_icon = LEVELS[index + 1]
        progress = (points - threshold) / (upcoming - threshold)
        to_next = upcoming - points
    else:
        next_name = next_icon = None
        progress, to_next = 1.0, 0
    return {"number": index + 1, "name": name, "icon": icon, "progress": round(progress, 4),
            "to_next": to_next, "next_name": next_name, "next_icon": next_icon, "points": points}


def reuse_streak(records, month):
    """Consecutive months with at least one reuse, repair or reusable choice.

    The selected month may still be in progress, so a streak that ended last
    month stays alive until the selected month is over.
    """
    def has_choice(period):
        return any(_is_lower(p) for p in month_records(records, period))

    period = month if has_choice(month) else shift_month(month, -1)
    streak = 0
    while has_choice(period) and streak < 240:
        streak += 1
        period = shift_month(period, -1)
    return streak


def goal_months(records, budget, carbon_goal):
    """Months with at least 3 entries that stayed within both saved goals."""
    months = sorted({p["purchase_date"][:7] for p in records})
    kept = []
    for period in months:
        totals = summary(month_records(records, period))
        if totals["count"] >= 3 and totals["spend"] <= Decimal(str(budget)) and totals["co2"] <= Decimal(str(carbon_goal)):
            kept.append(period)
    return kept


def milestones(records, wishlist, month, budget, carbon_goal):
    lower = sum(map(_is_lower, records))
    repairs = sum(p["product_type"] == "Repair services" for p in records)
    skipped = sum(item.get("status") == "skipped" for item in wishlist)
    streak = reuse_streak(records, month)
    rules = [
        ("First step", "👣", "Log your first purchase.", len(records) >= 1),
        ("Thoughtful ten", "📒", "Log 10 purchases in your journal.", len(records) >= 10),
        ("Second life", "♻️", "Choose second-hand, refurbished, reusable or repair.", lower >= 1),
        ("Fixer", "🛠️", "Log 3 repair-service purchases.", repairs >= 3),
        ("Mindful pause", "⏸️", "Skip an item from your wishlist.", skipped >= 1),
        ("Steady habit", "🔥", "Reach a 3-month reuse & repair streak.", streak >= 3),
        ("Goal keeper", "🎯", "Finish a month of 3+ entries within both goals.",
         bool(goal_months(records, budget, carbon_goal))),
    ]
    return [{"name": n, "icon": i, "rule": r, "earned": e} for n, i, r, e in rules]


def equivalents(kg):
    """Translate an estimated kg CO2e into everyday US-average illustrations."""
    kg = Decimal(str(kg))
    factors = EQUIVALENTS["factors"]
    rows = [
        ("car_km", "🚗", "km in an average petrol car"),
        ("phone_charge", "📱", "smartphone charges"),
        ("tree_month", "🌳", "months of carbon uptake by a young urban tree"),
    ]
    result = []
    for key, icon, label in rows:
        value = (kg / Decimal(factors[key]["kg_per_unit"])).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        result.append({"key": key, "icon": icon, "value": value, "label": label})
    return result


def make_wish(name, product_type, price, added_on=None, record_id=None):
    if not isinstance(name, str) or not name.strip() or len(name.strip()) > 80:
        raise ValueError("Give the item a name between 1 and 80 characters.")
    added = date.fromisoformat(str(added_on or date.today()))
    return {"id": record_id or str(uuid4()), "name": name.strip(), "product_type": product_type,
            "price": str(money(price)), "estimated_co2": str(impact(price, product_type)),
            "added_on": added.isoformat(), "status": "waiting", "resolved_on": None}


def add_wish(wishlist, wish):
    if len(wishlist) >= WISHLIST_LIMIT:
        raise ValueError(f"Your wishlist holds up to {WISHLIST_LIMIT} items. Remove a few decided ones first.")
    return list(wishlist) + [wish]


def days_waiting(wish, today=None):
    end = date.fromisoformat(wish["resolved_on"]) if wish.get("resolved_on") else (today or date.today())
    return max((end - date.fromisoformat(wish["added_on"])).days, 0)


def resolve_wish(wishlist, wish_id, status, today=None):
    if status not in WISH_STATUSES - {"waiting"}:
        raise ValueError("Choose bought or skipped.")
    if not any(w["id"] == wish_id for w in wishlist):
        raise ValueError("That wishlist item no longer exists.")
    stamp = (today or date.today()).isoformat()
    return [{**w, "status": status, "resolved_on": stamp} if w["id"] == wish_id else w for w in wishlist]


def remove_wish(wishlist, wish_id):
    return [w for w in wishlist if w["id"] != wish_id]


def wish_to_purchase(wish, purchased_on=None):
    """The bought item becomes an ordinary purchase with a freshly calculated estimate."""
    return make_purchase(wish["product_type"], wish["price"], wish["name"], purchased_on or date.today())


def wishlist_summary(wishlist):
    skipped = [w for w in wishlist if w.get("status") == "skipped"]
    return {
        "waiting": sum(w.get("status") == "waiting" for w in wishlist),
        "bought": sum(w.get("status") == "bought" for w in wishlist),
        "skipped": len(skipped),
        "kept": sum((Decimal(w["price"]) for w in skipped), Decimal("0")),
        "co2_not_added": sum((Decimal(w["estimated_co2"]) for w in skipped), Decimal("0")),
    }


def month_story(records, month, budget, carbon_goal):
    """One friendly sentence that sums up the month, without judgement."""
    totals = summary(month_records(records, month))
    if not totals["count"]:
        return "A blank page — log a purchase and your month's story will start here."
    spend_share = float(totals["spend"]) / float(budget) if budget else 0
    co2_share = float(totals["co2"]) / float(carbon_goal) if carbon_goal else 0
    lower_share = totals["lower"] / totals["count"]
    entries = "entry" if totals["count"] == 1 else "entries"
    parts = [f"{totals['count']} {entries} so far"]
    if lower_share >= 0.5:
        parts.append(f"{lower_share:.0%} of them reuse, repair or reusable choices — lovely")
    elif totals["lower"]:
        parts.append(f"{totals['lower']} gave something a second life")
    if spend_share <= 1 and co2_share <= 1:
        parts.append("and you're inside both goals")
    elif spend_share > 1 and co2_share > 1:
        parts.append("and both goals have been passed — a good moment to pause")
    else:
        parts.append("with one goal passed and one still in reach")
    return ", ".join(parts) + "."
