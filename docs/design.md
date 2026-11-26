# Design and intended needs

I designed ShopImpact for students, young adults and families who want to understand purchases without specialist knowledge. I prioritised quick entry, understandable totals, practical suggestions and encouragement without guilt. I used an earthy green and cream palette, visible labels, whitespace and a separate explanation of the model's limitations.

## Current layout

The 2026 "Conscious Market Journal" design places the app over slow, crossfading second-hand market, clothes-rack and forest footage (Mixkit, free licence) with a warm grain and bokeh layer. Panels are dark glass with Fraunces serif headlines, mono kickers and numbered section headings. The sign-in page pairs a video cover panel with labelled account forms; on narrow screens the panels stack. Day warms the footage with a sun glow, Night tints it blue with stars, and turning off animated scenery (or the device's reduced-motion setting) removes the video. High contrast switches to black, white and yellow with no footage. Captions keep their intended text colour without Streamlit's default opacity reduction. A shared stylesheet supports the same appearance across account and shopping pages.

```text
+----------------------+--------------------------------------------------+
| ShopImpact           | Title and reference estimate notice              |
| Account / sign out   | Dashboard | Insights | History | How it works     |
| High contrast        |                                                  |
|                      | Month selection                                  |
| Monthly goals        | Spending total | CO2 estimate | Lower choices    |
| Spending             |                                                  |
| Estimated CO2e       | Product type | Price | Brand | Date              |
|                      | Live impact preview                [Add purchase]|
| Backup reminder      | Category chart             | Achievements      |
|                      | Goal progress              | Turtle leaf       |
|                      |                            | Rotating tip      |
|                      | Alternatives and comparison                      |
+----------------------+--------------------------------------------------+
```

Insights shows six calendar months ending at a chosen month, average purchase, remaining or exceeded spending goal, previous-month change and largest spending category. Missing entries are described explicitly and are not treated as proof of zero spending or emissions.

History combines search, month and category filters with date/price/impact sorting. Filtered results have their own totals and CSV download. The edit selector follows the displayed results; a zero-result view hides edit/delete controls while full backups remain available. Editing, explicit delete confirmation and confirmed JSON restoration remain supported. The explanation tab describes assumptions and privacy. I reviewed the browser at a 390-pixel viewport with the sidebar collapsed and confirmed that the inputs stacked correctly; I detected no horizontal document overflow.

## Design choices

Use text labels with badge symbols so meaning is not conveyed by colour alone. Keep the most important totals above the chart. Present alternatives as options, without guilt or unsupported brand endorsements. Require sign-in before showing purchase data. Keep each account separate and show that entries save automatically. Recovery codes and explicit deletion support account ownership. Synthetic test entries never populate live accounts.

I reviewed high contrast in Chrome and corrected the primary-button text. I still need to complete full keyboard navigation, zoom and screen-reader assessments; a contrast toggle alone is not an accessibility certification.

## Feedback to collect

I will ask real people to add a purchase, find a monthly total, edit a mistake, compare two choices and save/restore a backup. I will record my observations and permission-appropriate notes. I have not conducted usability feedback yet.
