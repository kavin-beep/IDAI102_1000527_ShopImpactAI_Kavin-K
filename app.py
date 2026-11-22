"""ShopImpact: run with python -m streamlit run app.py."""
import json
import importlib
from pathlib import Path
from datetime import date
import streamlit as st
import logic as shopping_rules
import storage as backup_storage

# Community Cloud may rerun app.py while retaining imported modules from the
# previous deployment. Refresh the rules and backup bindings as one version.
source_version = json.loads((Path(__file__).resolve().parent / "data/emission_sources.json").read_text(encoding="utf-8"))["methodology"]
if shopping_rules.VERSION != source_version:
    importlib.reload(shopping_rules)
if backup_storage.VERSION != shopping_rules.VERSION:
    importlib.reload(backup_storage)

from logic import ROOT, CATALOG, SOURCE, VERSION, impact, make_purchase, month_records, summary, badges, update_purchase, recalculate_purchases
from storage import export_json, export_csv, import_json
from account_ui import require_account, save_account, sign_out, EMAIL_REQUEST_MESSAGE
from email_delivery import queue_email_action, queue_notice
from accounts import AccountError
from sqlalchemy.exc import SQLAlchemyError
import ui
import journey
# Refresh presentation code when Community Cloud retains an earlier module.
importlib.reload(ui)
importlib.reload(journey)
from ui import apply_styles, theme_controls
from insights import monthly_trend, month_insights, filter_purchases
import charts

COOL_OFF_DAYS = 7

st.set_page_config(page_title="ShopImpact | Conscious shopping", page_icon="🌿", layout="wide")
brand_slot = st.sidebar.container()
theme_controls()
apply_styles()
service, account, mailer = require_account()
if "tip_index" not in st.session_state:
    st.session_state.tip_index = 0
settings = account["settings"]
records = account["purchases"]
wishlist = settings.get("wishlist", [])
key = "personal"
this_month = date.today().strftime("%Y-%m")
points, breakdown = journey.eco_points(records, wishlist)
level = journey.level_for(points)
streak = journey.reuse_streak(records, this_month)
wish_totals = journey.wishlist_summary(wishlist)


def save_wishlist(updated, purchases=None):
    """Wishlist items live in the account's saved settings, beside goals."""
    return save_account(service, account, purchases=purchases, settings={**account["settings"], "wishlist": updated})


with brand_slot:
    ui.sidebar_brand(account["username"], level)

with st.sidebar:
    with st.expander("✉️ Account email"):
        if account.get("email"):
            st.caption(f"Sign-in email: {account['email']}")
            st.caption("Verified" if account.get("email_verified") else "Email not verified yet")
            if mailer and not account.get("email_verified") and st.button("Send verification email"):
                queue_email_action(service, mailer, account["email"], "verify")
                st.success(EMAIL_REQUEST_MESSAGE)
        else:
            st.write("Add an email to sign in with it next time.")
        with st.form("account_email", clear_on_submit=True):
            email = st.text_input("Sign-in email", max_chars=254, placeholder="name@example.com")
            email_password = st.text_input("Current password", type="password", max_chars=128)
            if st.form_submit_button("Save sign-in email"):
                try:
                    old_email = account.get("email")
                    account["email"] = service.set_email(st.session_state.auth_token, email, email_password)
                    account.update(service.load(st.session_state.auth_token))
                    if mailer and old_email != account["email"]:
                        queue_email_action(service, mailer, account["email"], "verify")
                        if old_email:
                            queue_notice(mailer, old_email, "ShopImpact email address changed",
                                         "Your ShopImpact sign-in email was changed after password confirmation. If you did not make this change, use your recovery code to secure your account.")
                    st.success("Email saved. You can sign in immediately; verify it from your inbox to enable email password resets." if mailer else "Email saved. You can sign in with your email or username.")
                except AccountError as error:
                    st.error(str(error))
                except SQLAlchemyError:
                    st.error("Your email could not be saved. Please try again.")
    left, right = st.columns(2)
    if left.button("Sign out", width="stretch"):
        sign_out(service)
    if right.button("Reload saved data", help="Load the latest saved data after changes in another tab.", width="stretch"):
        st.session_state.pop("account_data", None)
        for widget in ["contrast", "budget", "carbon_goal"]:
            st.session_state.pop(widget, None)
        st.rerun()
    with st.form("goals"):
        st.subheader("🎯 Your monthly goals")
        high_contrast = st.checkbox("High contrast", value=settings["contrast"], key="contrast")
        budget = st.number_input("Spending goal (INR)", min_value=100.0, value=float(settings["budget"]), step=100.0, key="budget")
        carbon_goal = st.slider("Estimated CO₂e goal (kg)", 10, 1000, int(settings["carbon_goal"]), step=10, key="carbon_goal")
        if st.form_submit_button("Save goals & appearance", type="primary", width="stretch"):
            if save_account(service, account, settings={**account["settings"], "budget": budget, "carbon_goal": carbon_goal, "contrast": high_contrast}):
                settings = account["settings"]
                st.success("Preferences saved.")
    st.caption("Goals help you reflect. They do not change the fixed badge rules.")
    st.info("Purchases save to your account. Sign in again after a refresh to continue. Download a backup whenever you want a separate copy.")

apply_styles(high_contrast)
night = st.session_state.get("visual_theme") == "Night" and not high_contrast
ink = ui.chart_ink(high_contrast)

if st.session_state.pop("celebrate", False):
    st.balloons()
for message in st.session_state.pop("toasts", []):
    st.toast(message[0], icon=message[1])

ui.hero(account["username"], level, streak, wish_totals["skipped"], date.today().strftime("%B %Y"))
if st.session_state.get("account_created"):
    st.success("Your account is ready. Welcome to ShopImpact!")
    with st.expander("Save your account recovery code"):
        st.write("Keep this code privately. It lets you recover your account if you forget your password.")
        st.code(st.session_state.recovery_code)
        st.download_button("Download recovery code", st.session_state.recovery_code,
                           "shopimpact-recovery-code.txt", "text/plain")
        if st.button("I saved my recovery code"):
            st.session_state.pop("account_created", None)
            st.session_state.pop("recovery_code", None)
            st.rerun()
st.caption("INR · USEEIO v1.4 reference factors · Sources reviewed 5 October 2026. Rough US-sector estimates, not product measurements.")
older_estimates = sum(p.get("methodology") != VERSION for p in records)
if older_estimates:
    st.info(f"{older_estimates} purchases retain their earlier reference estimates. New or edited entries use the updated data. Recalculate your history in How it works to compare all entries on the same basis.")

if st.session_state.get("personal"):
    with st.expander("Save entries from your previous session"):
        st.write("Your earlier session entries can be saved to this account. Estimates will be recalculated using the new sourced factors.")
        if st.button("Import my earlier session entries"):
            old = [make_purchase(p["product_type"], p["price"], p["brand"], p["purchase_date"], p["id"]) for p in st.session_state.personal]
            existing = {p["id"] for p in records}
            merged = records + [p for p in old if p["id"] not in existing]
            if save_account(service, account, purchases=merged):
                del st.session_state["personal"]
                st.rerun()

entry, wishes, insights, path, history, about = st.tabs(
    ["🌿 Dashboard", "⏸️ Mindful wishlist", "📈 Insights", "🏆 Eco journey", "🧾 History & backups", "📚 How it works"])
months = sorted({this_month} | {p["purchase_date"][:7] for p in records}, reverse=True)

with entry:
    if "next_dashboard_month" in st.session_state:
        st.session_state.month = st.session_state.pop("next_dashboard_month")
    if st.session_state.get("month") not in months:
        st.session_state.pop("month", None)
    heading, period = st.columns([3, 1], vertical_alignment="bottom")
    with heading:
        ui.section("📅", "Monthly overview", "Everything you logged for the month you choose.")
    month = period.selectbox("Dashboard month", months, key="month")
    monthly = month_records(records, month)
    totals = summary(monthly)
    ui.story_card(journey.month_story(records, month, budget, carbon_goal))
    with st.container(key="kpis"):
        a, b, c = st.columns(3)
        a.metric("Monthly spend", f"INR {totals['spend']:,.2f}")
        b.metric("Estimated CO₂e", f"{totals['co2']:,.2f} kg")
        c.metric("Reuse & repair choices", f"{totals['lower']} / {totals['count']}")

    if st.session_state.pop("purchase_saved", False):
        st.toast("Purchase saved. Your overview and history are up to date.", icon="✅")
    with st.container(key="card_add"):
        ui.section("🛒", "Add a purchase", "Four quick details — the estimate updates as you type.")
        c1, c2, c3, c4 = st.columns([1.7, 1.4, 1.9, 1.5])
        category = c1.selectbox("Product type", list(CATALOG), key="new_category",
                                format_func=lambda name: f"{ui.CATEGORY_ICONS.get(name, '🛒')}  {name}")
        price = c2.number_input("Price (INR)", min_value=0.0, max_value=10000000.0, value=500.0, step=50.0, key="new_price")
        brand = c3.text_input("Brand or shop", max_chars=80, placeholder="e.g. Local reuse shop", key="new_brand")
        purchased_on = c4.date_input("Purchase date", value=date.today(), min_value=date(2000, 1, 1), max_value=date(2100, 12, 31), key="new_date")
        preview = impact(price, category)
        ui.estimate_pill(preview, float(CATALOG[category]["multiplier"]), category, CATALOG[category]["lower_impact"],
                         journey.equivalents(preview)[2])
        if st.button("Add purchase", type="primary", key="add", icon="➕"):
            try:
                if len(records) >= 1000:
                    raise ValueError("This workspace supports 1,000 purchases. Export a backup before starting a new one.")
                updated = records + [make_purchase(category, price, brand, purchased_on)]
                if save_account(service, account, purchases=updated):
                    records = updated
                    st.session_state.tip_index += 1
                    st.session_state.purchase_saved = True
                    st.session_state.next_dashboard_month = purchased_on.strftime("%Y-%m")
                    if CATALOG[category]["lower_impact"]:
                        st.session_state.toasts = [("+20 eco points for a reuse, repair or reusable choice!", "🌱")]
                    st.rerun()
            except ValueError as error:
                st.error(str(error))

    main, rewards = st.columns([2, 1], gap="large")
    with main:
        ui.section("📊", "Your month at a glance", "Where your spending and estimated impact went.")
        chart_measure = st.radio("Chart measure", ["Estimated CO₂e", "Spending"], horizontal=True)
        if monthly:
            field = "estimated_co2" if chart_measure == "Estimated CO₂e" else "price"
            grouped = {}
            for purchase in monthly:
                product = purchase["product_type"]
                grouped[product] = grouped.get(product, 0) + float(purchase[field])
            unit = "Estimated kg CO₂e" if field == "estimated_co2" else "INR"
            bars, donut = st.columns([1.35, 1])
            bars.altair_chart(charts.category_bars(grouped, unit, ink), theme=None, width="stretch")
            donut.altair_chart(charts.category_donut(grouped, unit, ink), theme=None, width="stretch")
        else:
            ui.empty_state("🧺", "Add your first purchase to start your monthly dashboard.")
        ui.goal_rings([("💸", "Spending", float(totals["spend"]), budget, "INR"),
                       ("☁️", "Estimated CO₂e", float(totals["co2"]), carbon_goal, "kg")])
        for label, used, goal in [("Spending", float(totals["spend"]), budget), ("Estimated CO₂e", float(totals["co2"]), carbon_goal)]:
            if used > goal:
                st.caption(f"{label} is above your chosen goal. You can use the comparison tool to reflect on future choices.")
    with rewards:
        with st.container(key="badges"):
            ui.section("🏅", "Your achievements", "Fixed monthly badge rules.")
            earned = badges(monthly)
            for badge in earned:
                st.success(f"🏅 {badge}")
            if totals["lower"]:
                artwork = ROOT / "assets/turtle/leaf.svg"
                if artwork.exists():
                    st.image(str(artwork), caption="A Turtle leaf for a reuse, repair or reusable choice.", width=200)
                else:
                    st.info("Run tools/draw_rewards.py to generate the Turtle leaf.")
            if not earned:
                ui.empty_state("🌱", "Your next achievement starts with a thoughtful choice.")
            with st.expander("See badge rules"):
                st.write("Eco Saver: at least 3 purchases and a monthly estimated footprint of 50 kg CO₂e or less.")
                st.write("Low Impact Shopper: at least 3 reuse, repair or reusable choices, making up at least 60% of the month. This rewards habits, not verified emissions savings.")
                st.write("Repair Champion: at least one repair-service purchase this month.")
        tips = json.loads((ROOT / "data/eco_tips.json").read_text(encoding="utf-8"))
        ui.tip_card(tips[st.session_state.tip_index % len(tips)])
        if st.button("Another tip", icon="✨", width="stretch"):
            st.session_state.tip_index += 1
            st.rerun()

    ui.section("🌍", "What this month's estimate looks like", "The same estimated kg CO₂e, pictured with everyday US averages.")
    ui.equivalents_cards(journey.equivalents(totals["co2"]))
    st.caption(f"Illustrations from the [US EPA Greenhouse Gas Equivalencies Calculator]({journey.EQUIVALENTS['url']}) (page updated {journey.EQUIVALENTS['page_updated']}). They help picture a rough estimate; they are not measurements, offsets or savings.")

    ui.section("💡", f"Explore alternatives for {category.lower()}", "Ideas to try before buying new.")
    ui.alternatives_cards(CATALOG[category]["alternatives"])
    st.caption(CATALOG[category]["mapping_note"])
    with st.expander("Brand and service options to explore"):
        links = json.loads((ROOT / "data/alternative_links.json").read_text(encoding="utf-8"))
        for option in links[category]:
            st.markdown(f"[{option['name']}]({option['url']}) — {option['note']}")
        st.caption("Official pages checked 2 October 2026. These document reuse, repair or reusable-product options, not independent ethical certification or verified emissions savings. Check local availability and terms.")
    with st.expander("Compare a different choice", expanded=False):
        target = st.selectbox("Compare with", list(CATALOG), index=list(CATALOG).index(CATALOG[category]["compare_with"]))
        alternative_price = st.number_input("Alternative price (INR)", min_value=0.0, max_value=10000000.0, value=500.0)
        original, alternative = impact(price, category), impact(alternative_price, target)
        x, y = st.columns(2)
        x.metric("Current choice (estimated kg CO₂e)", f"{original:,.2f}")
        y.metric("Alternative (estimated kg CO₂e)", f"{alternative:,.2f}", delta=f"{alternative - original:+,.2f}", delta_color="inverse")
        st.caption("Reference-model comparison only. A lower price can lower this estimate without lowering physical emissions. Reuse benefits are not quantified by this model.")

with wishes:
    ui.section("⏸️", "Pause before you buy", f"Park things you want for {COOL_OFF_DAYS} days. Then decide calmly: buy it, or let it go.")
    w1, w2, w3 = st.columns(3)
    w1.metric("Waiting to decide", f"{wish_totals['waiting']}")
    w2.metric("Kept in your pocket", f"INR {wish_totals['kept']:,.2f}")
    w3.metric("Estimated CO₂e not added", f"{wish_totals['co2_not_added']:,.2f} kg")
    with st.form("wish_form", clear_on_submit=True):
        st.markdown("**Add something you're thinking about**")
        f1, f2, f3 = st.columns([2, 1.6, 1])
        wish_name = f1.text_input("What is it?", max_chars=80, placeholder="e.g. Wireless headphones")
        wish_type = f2.selectbox("Wish product type", list(CATALOG), format_func=lambda name: f"{ui.CATEGORY_ICONS.get(name, '🛒')}  {name}")
        wish_price = f3.number_input("Expected price (INR)", min_value=0.0, max_value=10000000.0, value=1000.0, step=100.0)
        if st.form_submit_button("Add to wishlist", type="primary", icon="⏸️"):
            try:
                if save_wishlist(journey.add_wish(wishlist, journey.make_wish(wish_name, wish_type, wish_price))):
                    st.session_state.toasts = [(f"Parked for {COOL_OFF_DAYS} days. Future you will thank you.", "⏸️")]
                    st.rerun()
            except ValueError as error:
                st.error(str(error))
    waiting = sorted((w for w in wishlist if w["status"] == "waiting"), key=lambda w: w["added_on"])
    if waiting:
        for wish in waiting:
            ui.wish_card(wish, journey.days_waiting(wish), COOL_OFF_DAYS)
            b1, b2, b3, _ = st.columns([1, 1, 1, 2])
            if b1.button("I skipped it", key=f"skip_{wish['id']}", icon="🎉", type="primary", width="stretch"):
                if save_wishlist(journey.resolve_wish(wishlist, wish["id"], "skipped")):
                    st.session_state.celebrate = True
                    st.session_state.toasts = [(f"+{journey.POINTS['skipped']} eco points — INR {float(wish['price']):,.0f} stays in your pocket!", "🎉")]
                    st.rerun()
            if b2.button("I bought it", key=f"buy_{wish['id']}", icon="🛍️", width="stretch"):
                try:
                    if len(records) >= 1000:
                        raise ValueError("This workspace supports 1,000 purchases. Export a backup before starting a new one.")
                    bought = journey.wish_to_purchase(wish)
                    if save_wishlist(journey.resolve_wish(wishlist, wish["id"], "bought"), purchases=records + [bought]):
                        st.session_state.toasts = [("Added to your purchases with a fresh estimate.", "🛍️")]
                        st.session_state.next_dashboard_month = bought["purchase_date"][:7]
                        st.rerun()
                except ValueError as error:
                    st.error(str(error))
            if b3.button("Remove", key=f"remove_{wish['id']}", icon="🗑️", width="stretch"):
                if save_wishlist(journey.remove_wish(wishlist, wish["id"])):
                    st.rerun()
    else:
        ui.empty_state("🛍️", "Nothing waiting. Next time you feel the urge to buy, park it here first.")
    decided = [w for w in wishlist if w["status"] != "waiting"]
    if decided:
        with st.expander(f"Decided items ({len(decided)})"):
            for wish in sorted(decided, key=lambda w: w.get("resolved_on") or "", reverse=True):
                ui.wish_card(wish, journey.days_waiting(wish), COOL_OFF_DAYS)
            if st.button("Clear decided items", icon="🧹"):
                if save_wishlist([w for w in wishlist if w["status"] == "waiting"]):
                    st.rerun()
    st.caption("Skipped items are not purchases, so they never enter your history or totals. 'Estimated CO₂e not added' uses the same rough price × category model and is not a verified saving.")

with insights:
    ui.section("📈", "See the bigger picture", "Six months of your recorded shopping, measured against your goals.")
    insight_month = st.selectbox("Insights month", months, key="insight_month")
    detail = month_insights(records, insight_month, settings["budget"])
    average, balance, change = st.columns(3)
    average.metric("Average purchase", f"INR {detail['average']:,.2f}" if detail["average"] is not None else "No entries")
    balance.metric("Above spending goal" if detail["remaining"] < 0 else "Spending goal remaining", f"INR {abs(detail['remaining']):,.2f}")
    change.metric("Change from previous month", f"INR {detail['spend_change']:+,.2f}" if detail["spend_change"] is not None else "No prior entries")
    st.caption("Compared with the previous calendar month, using logged entries only. Empty months mean no entries, not verified zero spending. Goals use your current saved preferences; these are not forecasts.")
    trend = monthly_trend(records, insight_month)
    measure = st.radio("Trend measure", ["Spending (INR)", "Estimated CO₂e (kg)"], horizontal=True)
    field = "spend" if measure == "Spending (INR)" else "co2"
    trend_col, mix_col = st.columns([1.6, 1], gap="large")
    trend_col.altair_chart(charts.trend_area([row["month"] for row in trend], [float(row[field]) for row in trend], measure, ink),
                           theme=None, width="stretch")
    with mix_col:
        mix = {}
        for purchase in month_records(records, insight_month):
            mix[purchase["product_type"]] = mix.get(purchase["product_type"], 0) + float(purchase["price"] if field == "spend" else purchase["estimated_co2"])
        if mix:
            st.altair_chart(charts.category_donut(mix, measure, ink), theme=None, width="stretch")
        else:
            ui.empty_state("🍩", "Your category mix appears once this month has entries.")
    if detail["top_category"]:
        st.info(f"Largest spending category: {detail['top_category']} · INR {detail['top_spend']:,.2f}")
    else:
        st.info("No purchases logged for this month. Add entries to reveal your patterns.")
    with st.expander("View the monthly numbers"):
        st.dataframe([{"Month": row["month"], "Entries": row["count"], "Spending (INR)": float(row["spend"]), "Estimated CO₂e (kg)": float(row["co2"])} for row in trend], hide_index=True, width="stretch")

with path:
    ui.level_card(level, journey.LEVELS)
    ui.section("✨", "How your points add up", "Points celebrate logging and thoughtful habits — they never change badge rules.")
    ui.points_grid(breakdown)
    ui.section("🗺️", "Milestones", "Lifetime moments on your journey.")
    ui.medal_grid(journey.milestones(records, wishlist, this_month, budget, carbon_goal))
    ui.section("🏅", f"Monthly badges · {month}", "The fixed rules, checked against the dashboard month.")
    current = badges(monthly)
    ui.medal_grid([
        {"name": "Eco Saver", "icon": "🌎", "rule": "3+ purchases and 50 kg CO₂e or less this month.", "earned": "Eco Saver" in current},
        {"name": "Low Impact Shopper", "icon": "♻️", "rule": "3+ reuse, repair or reusable choices, at least 60% of the month.", "earned": "Low Impact Shopper" in current},
        {"name": "Repair Champion", "icon": "🧵", "rule": "At least one repair-service purchase this month.", "earned": "Repair Champion" in current},
    ])
    st.caption(f"Points: {journey.POINTS['logged']} per purchase logged · {journey.POINTS['lower']} per reuse, repair or reusable choice · "
               f"{journey.POINTS['repair']} repair bonus · {journey.POINTS['skipped']} per skipped wishlist item. Streaks count consecutive months with at least one reuse, repair or reusable choice.")

with history:
    ui.section("🧾", "Your purchase history", "Search, filter, correct and export.")
    if records:
        query = st.text_input("Search purchases", placeholder="Brand, shop, category or date")
        f1, f2, f3 = st.columns(3)
        history_month = f1.selectbox("Filter month", ["All months"] + sorted({p["purchase_date"][:7] for p in records}, reverse=True))
        history_category = f2.selectbox("Filter category", ["All categories"] + list(CATALOG))
        order = f3.selectbox("Sort purchases", ["Newest first", "Oldest first", "Highest price", "Highest estimated impact"])
        filtered = filter_purchases(records, query, None if history_month == "All months" else history_month,
                                    None if history_category == "All categories" else history_category, order)
        if filtered:
            filtered_totals = summary(filtered)
            st.caption(f"Showing {len(filtered)} of {len(records)} purchases · INR {filtered_totals['spend']:,.2f} · {filtered_totals['co2']:,.2f} estimated kg CO₂e")
            st.dataframe([{"Date": p["purchase_date"], "Product type": f"{ui.CATEGORY_ICONS.get(p['product_type'], '')} {p['product_type']}", "Brand / shop": p["brand"],
                           "Price (INR)": float(p["price"]), "Estimated CO₂e (kg)": float(p["estimated_co2"])} for p in filtered], hide_index=True, width="stretch",
                         column_config={"Estimated CO₂e (kg)": st.column_config.ProgressColumn(
                             "Estimated CO₂e (kg)", format="%.2f", min_value=0.0, max_value=max(float(p["estimated_co2"]) for p in filtered) or 1.0)})
            st.download_button("Download filtered CSV", export_csv(filtered), "shopimpact-filtered.csv", "text/csv", icon="⬇️")
            lookup = {p["id"]: p for p in filtered}
            selected = st.selectbox("Choose a purchase to edit", list(lookup), format_func=lambda i: f"{lookup[i]['purchase_date']} · {lookup[i]['brand']} · INR {lookup[i]['price']} · {i[:8]}")
            record = lookup[selected]
            with st.form(f"edit_{key}_{selected}"):
                st.markdown("**✏️ Edit this purchase**")
                e1, e2 = st.columns(2)
                edit_type = e1.selectbox("Edit product type", list(CATALOG), index=list(CATALOG).index(record["product_type"]))
                edit_price = e2.number_input("Edit price (INR)", min_value=0.0, max_value=10000000.0, value=float(record["price"]))
                edit_brand = e1.text_input("Edit brand or shop", value=record["brand"], max_chars=80)
                edit_date = e2.date_input("Edit date", value=date.fromisoformat(record["purchase_date"]), min_value=date(2000, 1, 1), max_value=date(2100, 12, 31))
                if st.form_submit_button("Save changes", type="primary"):
                    try:
                        replacement = make_purchase(edit_type, edit_price, edit_brand, edit_date, selected)
                        if save_account(service, account, purchases=update_purchase(records, replacement)):
                            st.rerun()
                    except ValueError as error:
                        st.error(str(error))
            confirm_delete = st.checkbox("Confirm deletion of this purchase", key=f"confirm_{key}_{selected}")
            if st.button("Delete selected purchase", disabled=not confirm_delete, icon="🗑️"):
                if save_account(service, account, purchases=[p for p in records if p["id"] != selected]):
                    st.rerun()
        else:
            ui.empty_state("🔍", "No purchases match these filters. Try a different month, category or search.")
    else:
        ui.empty_state("🧾", "No purchases yet. Add one on the dashboard.")
    ui.section("💾", "Keep a copy", "JSON restores your entries. CSV is a spreadsheet-friendly report. Neither includes your goal settings.")
    d1, d2 = st.columns(2)
    d1.download_button("Download JSON backup", export_json(records), f"shopimpact-{key}.json", "application/json", icon="📦", width="stretch")
    d2.download_button("Download CSV report", export_csv(records), f"shopimpact-{key}.csv", "text/csv", icon="📄", width="stretch")
    uploaded = st.file_uploader("Restore a ShopImpact JSON backup", type=["json"], key=f"upload_{key}")
    confirm_restore = st.checkbox("Replace this workspace with the backup", key=f"restore_confirm_{key}")
    legacy = st.checkbox("Allow an older backup and recalculate its estimates", help="Earlier reference or illustrative estimates will be replaced with the current sourced factors.")
    if st.button("Restore backup", disabled=uploaded is None or not confirm_restore, icon="♻️"):
        try:
            restored = import_json(uploaded.getvalue(), allow_legacy=legacy)
            if save_account(service, account, purchases=restored):
                st.rerun()
        except ValueError as error:
            st.error(str(error))

with about:
    ui.section("📚", "An honest estimate, a helpful habit", "How ShopImpact turns a price into a rough CO₂e estimate.")
    st.write("Making, packaging and delivering products can release greenhouse gases. CO₂e means carbon dioxide equivalent: a common measure of their combined warming effect. ShopImpact uses the product category and price as clues to estimate that impact; spending itself does not directly create emissions.")
    st.write("ShopImpact uses price × category multiplier to estimate spending-related greenhouse gas emissions. The updated factors come from USEEIO Supply Chain GHG Emission Factors v1.4.0, published by the Cornerstone Sustainability Data Initiative in October 2025, including supply-chain margins and IPCC AR6 warming potentials.")
    st.write("The base currency is INR. A higher price can increase this estimate without changing physical emissions. Free items return zero in this model; that does not mean they have zero environmental impact.")
    st.write(f"The reference conversion is {SOURCE['fx_inr_per_usd']} INR per USD, the World Bank's annual average for {SOURCE['fx_year']}, matching the factors' 2024 dollar price basis. It is not a live exchange rate. Current prices are not inflation-adjusted; US sector averages may differ substantially from Indian products. Treat results as rough estimates, not certified carbon accounting.")
    st.write(f"Everyday equivalents (car kilometres, phone charges, tree months) divide the estimate by US EPA averages: {', '.join(f['derivation'] for f in journey.EQUIVALENTS['factors'].values())}. They are pictures of the estimate, not separate measurements.")
    st.write("The Mindful wishlist stores items you are considering in your account settings. Skipped items never become purchases; the 'not added' figure applies the same model to their expected prices and is not a verified saving.")
    with st.expander("Data freshness and reference years"):
        st.write("Reviewed 5 October 2026. A 2026 refresh means the latest verified source release available at review, not measured 2026 product emissions.")
        st.write(f"Factor release: v1.4.0 · Published {SOURCE['published']} · Dollar price basis: 2024 · Warming method: {SOURCE['gwp']}.")
        latest_fx = SOURCE["latest_available_annual_fx"]
        st.write(f"Latest available World Bank annual rate at review: {latest_fx['year']} · {latest_fx['inr_per_usd']} INR/USD. This is shown for context; calculations use the matching 2024 rate. No full-year 2026 rate is available yet.")
        st.caption("Data is a checked snapshot, not a live feed. Previous source files are archived for reproducibility.")
    st.write("Badges reflect your logged choices, not a certification of sustainability. Reused and new versions use the same category factor; no unsupported reuse discount is applied. Brand links document reuse, repair or reusable-product options, not independent certification or endorsements.")
    st.dataframe([{"Category": f"{ui.CATEGORY_ICONS.get(name, '')} {name}", "Reference kg CO₂e per INR": float(info["multiplier"]), "EPA NAICS": info["source_code"], "Mapping limitations": info["mapping_note"]} for name, info in CATALOG.items()], hide_index=True)
    st.markdown("[Published USEEIO dataset](https://zenodo.org/records/17202747) · [World Bank reference exchange rate](https://api.worldbank.org/v2/country/IND/indicator/PA.NUS.FCRF?date=2024&format=json) · "
                f"[EPA equivalencies]({journey.EQUIVALENTS['url']})")
    if older_estimates:
        with st.expander("Update my saved estimates"):
            st.write("Download a JSON backup first. Recalculation preserves purchase IDs, dates, brands and prices, and updates estimates and methodology. Badges and totals may change. Your goals stay the same.")
            approve_recalculation = st.checkbox("Use the updated reference data for all my purchases", key="approve_recalculation")
            if st.button("Recalculate saved estimates", disabled=not approve_recalculation):
                try:
                    if save_account(service, account, purchases=recalculate_purchases(records)):
                        st.rerun()
                except ValueError as error:
                    st.error(str(error))
    st.write("Purchases and preferences are saved separately for each account. Passwords are protected with Argon2id hashing. The database administrator can access purchase data; it is not end-to-end encrypted. Sign out on a shared computer. Sessions expire after 12 hours and a page refresh requires another sign-in.")
    st.write("Dates may include planned purchases. Your dashboard groups all entries by their selected purchase month and year.")
    st.caption("Built with Python, Streamlit, Altair, datetime, lists, dictionaries, and genuine Turtle-generated artwork.")
    with st.expander("Delete my account and purchases"):
        st.write("Download a backup first if you want to keep your purchase history. This permanently deletes your account and its data.")
        with st.form("delete_account"):
            password = st.text_input("Confirm your password", type="password", max_chars=128)
            confirmed = st.checkbox("I understand my account and purchases will be deleted")
            if st.form_submit_button("Permanently delete my account") and confirmed:
                try:
                    service.delete_account(st.session_state.auth_token, password)
                    st.session_state.clear()
                    st.rerun()
                except AccountError as error:
                    st.error(str(error))
                except SQLAlchemyError:
                    st.error("Account deletion failed. Please try again.")
