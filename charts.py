"""Earthy Altair charts. Every colour is paired with a text label or tooltip."""
import altair as alt
import pandas as pd
from ui import CATEGORY_COLORS

FONT = "Inter"
SCALE = alt.Scale(domain=list(CATEGORY_COLORS), range=list(CATEGORY_COLORS.values()))


def _style(chart, ink):
    """Apply shared transparent styling and readable axis and legend colors."""
    grid = "rgba(148,163,209,.18)" if ink != "#0F2E25" else "rgba(15,94,72,.10)"
    return (chart.configure(background="transparent", font=FONT)
            .configure_axis(labelColor=ink, titleColor=ink, gridColor=grid, domain=False, ticks=False,
                            labelFontSize=12, titleFontSize=12, titleFontWeight=600, labelPadding=8)
            .configure_legend(labelColor=ink, titleColor=ink, labelFontSize=12, symbolType="circle", symbolSize=140)
            .configure_view(strokeWidth=0))


def _frame(grouped):
    """Convert category totals into the labelled tabular data Altair expects."""
    return pd.DataFrame({"Category": list(grouped), "Value": [round(float(v), 2) for v in grouped.values()]})


def category_bars(grouped, unit, ink):
    """Build a sorted category bar chart with value labels and accessible tooltips."""
    data = _frame(grouped)
    base = alt.Chart(data).encode(
        y=alt.Y("Category:N", sort="-x", title=None),
        x=alt.X("Value:Q", title=unit),
        tooltip=[alt.Tooltip("Category:N"), alt.Tooltip("Value:Q", title=unit, format=",.2f")])
    bars = base.mark_bar(cornerRadiusEnd=10, size=26).encode(color=alt.Color("Category:N", scale=SCALE, legend=None))
    fmt = ",.0f" if unit == "INR" or data["Value"].max() >= 100 else ",.2f"
    labels = base.mark_text(align="left", dx=6, fontWeight=700, color=ink).encode(text=alt.Text("Value:Q", format=fmt))
    return _style((bars + labels).properties(height=max(150, 52 * len(data))), ink)


def category_donut(grouped, unit, ink):
    """Build a category-share donut with a total, unit caption, and hover details."""
    data = _frame(grouped)
    total = data["Value"].sum()
    data["Share"] = data["Value"] / total if total else 0
    arc = alt.Chart(data).mark_arc(innerRadius=62, outerRadius=104, cornerRadius=8, padAngle=0.025).encode(
        theta=alt.Theta("Value:Q", stack=True),
        color=alt.Color("Category:N", scale=SCALE, legend=alt.Legend(orient="bottom", title=None, columns=1, values=list(data["Category"]))),
        tooltip=[alt.Tooltip("Category:N"), alt.Tooltip("Value:Q", title=unit, format=",.2f"), alt.Tooltip("Share:Q", format=".0%")])
    centre = alt.Chart(pd.DataFrame({"t": [f"{total:,.0f}" if total >= 100 else f"{total:,.1f}"]})).mark_text(fontSize=24, fontWeight=800, color=ink, dy=-6).encode(text="t:N")
    caption = alt.Chart(pd.DataFrame({"t": [unit.split(" (")[0]]})).mark_text(fontSize=11, color=ink, opacity=.7, dy=16).encode(text="t:N")
    return _style((arc + centre + caption).properties(height=320), ink)


def trend_area(months, values, measure, ink):
    """Build a six-month trend chart with a gradient area and point tooltips."""
    data = pd.DataFrame({"Month": months, "Value": values})
    gradient = alt.Gradient(gradient="linear", x1=1, x2=1, y1=1, y2=0, stops=[
        alt.GradientStop(color="rgba(163,197,133,0.02)", offset=0),
        alt.GradientStop(color="rgba(163,197,133,0.30)", offset=0.5),
        alt.GradientStop(color="rgba(232,176,74,0.60)", offset=1)])
    base = alt.Chart(data).encode(x=alt.X("Month:N", sort=None, title=None, axis=alt.Axis(labelAngle=0)))
    area = base.mark_area(interpolate="monotone", color=gradient,
                          line={"color": "#E8B04A", "strokeWidth": 3}).encode(y=alt.Y("Value:Q", title=measure))
    dots = base.mark_point(filled=True, size=110, color="#A3C585", stroke="#17140F", strokeWidth=2, opacity=1).encode(
        y="Value:Q", tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Value:Q", title=measure, format=",.2f")])
    return _style((area + dots).properties(height=320), ink)
