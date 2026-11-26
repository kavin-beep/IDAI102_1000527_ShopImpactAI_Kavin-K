# Assessment requirements status

Status refreshed 26 November 2026. The rubric totals 60 marks: planning 10, Python logic 15, interface 15, testing/creativity 10, GitHub/documentation 10. Distinguished is the highest named tier; no grade is guaranteed.

| Requirement | Evidence and current status |
| --- | --- |
| User needs, sketches, palette and feature planning | docs/design.md contains initial planning and wireframes |
| Product type, price, brand and date | Implemented and exercised in interface/browser checks |
| Price times multiplier calculation | Implemented; published EPA source rows and historical currency conversion recorded |
| Monthly spending and estimated CO2 dashboard | Implemented; month/year logic tested; desktop dashboard inspected |
| Badges and rules | Implemented and boundary-tested |
| Alternatives for each product type | Three shopping approaches per category plus named options with official source links; no unsupported ethical certification |
| Turtle footprint, leaf or badge | Turtle-generated SVG displayed conditionally; source included; desktop preview and assessor interpretation remain to be confirmed |
| Lists, dictionaries, control structures, datetime and modular code | Implemented in logic, storage and interface modules |
| Interactive UI and live updates | Working local app; add/edit/delete and saved preferences tested |
| 10–15 varied purchases for testing | 15 labelled synthetic records in tests; none preloaded for real users |
| Creative additions | Session-only workspace, goals, search, comparison, backups, tips and contrast |
| Sign-in and email features | Removed from the active app; users open the dashboard directly and no email workflow is required |
| Thorough testing | 86 automated tests pass; focused tests confirm direct home access and session isolation |
| Genuine usability feedback and refinement | Feedback record is prepared; no real participant feedback has been collected. An AI heuristic screen inspection is documented in docs/testing.md and does not replace participant feedback |
| app.py and requirements.txt | Present; dependencies installed and checked |
| Detailed README | Overview, features, integration, run/deployment steps, screenshots, repository and public app links are present |
| GitHub repository, naming and assessor access | Repository exists at kavin-beep/IDAI102_1000527_ShopImpactAI_Kavin-K and student details are present; assessor access is not independently verified |
| Streamlit Cloud deployment | Public app URL is in README. The app now uses temporary session-only storage and does not require database or email secrets; session persistence after refresh/restart is not promised |
| Submission PDF | Pending real student name, registration number, school, repository and live links |

The app has no demo workspace. Synthetic data belongs only in tests. Purchases, wishlist entries and preferences live only in the active Streamlit session and may be lost after refresh, reconnect or restart. Account and email backend modules remain in the repository as legacy code, but the running app does not import or expose them.
