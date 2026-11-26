# Design and user needs

Students, young adults and families may want to understand purchases without specialist knowledge. Their main needs are quick entry, understandable totals, suggestions they can act on and encouragement without guilt. The first design uses an earthy green and cream palette, visible labels, whitespace, and a separate explanation of the model's limitations.

## Current layout

The 2026 "Conscious Market Journal" design places the app over slow, crossfading second-hand market, clothes-rack and forest footage (Mixkit, free licence) with a warm grain and bokeh layer. Panels are dark glass with Fraunces serif headlines, mono kickers and numbered section headings. The sign-in page reuses the established brand panel with username and password forms in two tabs; it does not ask for email or offer password recovery. Day warms the footage with a sun glow, Night tints it blue with stars, and turning off animated scenery (or the device's reduced-motion setting) removes the video. High contrast switches to black, white and yellow with no footage. Captions keep their intended text colour without Streamlit's default opacity reduction. A shared stylesheet supports the shopping pages.

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
| Session backup note  | Category chart             | Achievements      |
|                      | Goal progress              | Plant pal mascot  |
|                      |                            | Plant tip         |
|                      | Alternatives and comparison                      |
+----------------------+--------------------------------------------------+
```

Insights shows six calendar months ending at a chosen month, average purchase, remaining or exceeded spending goal, previous-month change and largest spending category. Missing entries are described explicitly and are not treated as proof of zero spending or emissions.

History combines search, month and category filters with date/price/impact sorting. Filtered results have their own totals and CSV download. The edit selector follows the displayed results; a zero-result view hides edit/delete controls while full backups remain available. Editing, explicit delete confirmation and confirmed JSON restoration remain supported. The explanation tab describes assumptions and privacy. Browser review confirmed stacked inputs at a 390-pixel viewport with the sidebar collapsed; no horizontal document overflow was detected in that view.

## Design choices

Use text labels with badge symbols so meaning is not conveyed by colour alone. Keep the most important totals above the chart. Present alternatives as options, without guilt or unsupported brand endorsements. Keep each active browser session separate and explain that its entries are temporary. Encourage JSON backup before ending the session. Synthetic test entries never populate real user sessions.

High contrast was reviewed in Chrome and primary-button text was corrected. Full keyboard navigation, zoom and screen-reader assessment remain pending; a contrast toggle alone is not an accessibility certification.

The dashboard plant pal uses a small inline SVG face and CSS motion. Its leaves wiggle on hover when motion is allowed. It appears wilted when monthly spending exceeds the user's goal, happy when purchases exist and estimated CO₂e is within its goal, and gently growing otherwise. The tip rotates through the sourced eco-tip list and is framed as advice from the plant.

## Feedback to collect

Five informal feedback responses from friends, family and a classmate are recorded in the README. These comments are genuine but are not a structured task-based usability study. For follow-up, ask participants to add a purchase, find a monthly total, edit a mistake, compare two choices, and save/restore a backup; record observations and permission-appropriate notes.
