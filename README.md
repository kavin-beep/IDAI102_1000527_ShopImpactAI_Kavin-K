<div align="center">

<img src="docs/media/banner.svg" alt="ShopImpact — a conscious shopping journal. Small choices. A clearer picture." width="100%"/>

<a href="https://shopimpact-duy7hphexgoshhqfexfmkt.streamlit.app/">
  <img src="https://readme-typing-svg.demolab.com?font=Fraunces&size=30&duration=3200&pause=900&color=E8B04A&center=true&vCenter=true&width=860&height=56&lines=Understand+your+shopping;Picture+your+estimated+CO%E2%82%82e;Pause+before+you+buy;Celebrate+every+thoughtful+choice" alt="Typing tagline"/>
</a>

<p>
  <a href="https://shopimpact-duy7hphexgoshhqfexfmkt.streamlit.app/"><img src="https://img.shields.io/badge/▶%20Open%20the%20live%20app-shopimpact.streamlit.app-e8b04a?style=for-the-badge&labelColor=17140f" alt="Open the live app"/></a>
</p>

<p>
  <a href="https://github.com/kavin-beep/IDAI102_1000527_ShopImpactAI_Kavin-K/actions/workflows/tests.yml"><img src="https://github.com/kavin-beep/IDAI102_1000527_ShopImpactAI_Kavin-K/actions/workflows/tests.yml/badge.svg" alt="GitHub Actions test status"/></a>
  <img src="https://img.shields.io/badge/Python-3.12-f4ede1?style=flat-square&logo=python&logoColor=17140f&labelColor=e8b04a"/>
  <img src="https://img.shields.io/badge/Streamlit-1.55-f4ede1?style=flat-square&logo=streamlit&logoColor=FF4B4B&labelColor=211b14"/>
  <img src="https://img.shields.io/badge/Altair-charts-f4ede1?style=flat-square&labelColor=211b14"/>
  <img src="https://img.shields.io/badge/Data-Session%20only-f4ede1?style=flat-square&labelColor=211b14"/>
  <img src="https://img.shields.io/badge/Three.js-WebGL-f4ede1?style=flat-square&logo=three.js&logoColor=white&labelColor=211b14"/>
  <img src="https://img.shields.io/badge/Tests-86%20passing-f4ede1?style=flat-square&labelColor=5f7a45"/>
</p>

**🌐 Live app → [shopimpact-duy7hphexgoshhqfexfmkt.streamlit.app](https://shopimpact-duy7hphexgoshhqfexfmkt.streamlit.app/)**

<sub>
<a href="https://canva.link/v8iiqeb2k0bxb1g">Canva deck (21 slides)</a> ·
</sub>

</div>

---

## 🏠 Open the app

The app opens directly to the dashboard. No sign-in or email setup is required. The current workspace is temporary
and belongs only to the active Streamlit session; download a JSON backup to keep entries.

---

## 🛍️ What is ShopImpact?

**ShopImpact** turns a purchase list into a calm, cinematic habit journal. You record what you buy, see where your money
goes, picture a rough emissions estimate, pause before buying, and celebrate reuse and repair. It implements
**Scenario 1** of the Year 1 Python Programming assessment.

### Problem statement

People can find it difficult to understand the possible environmental impact of everyday purchases, the money they
spend over time, and which lower-impact alternatives are practical. ShopImpact presents these ideas in a simple,
private shopping journal without pretending that rough estimates are exact product measurements.

### Objectives

- Record purchases, edit or delete them, and review monthly spending and estimated impact.
- Explain broad category estimates and everyday equivalents clearly.
- Encourage reuse, repair and a mindful 7-day wishlist without guilt.
- Open directly into a private, session-only workspace with usable export, import and backup tools.
- Verify the implementation with automated tests and documented screenshots.

### Target users

ShopImpact is designed for students, young adults and families who want a plain-language overview of shopping habits.
It is intended for people with no specialist carbon-accounting knowledge and may be used on desktop or a narrow
mobile screen.

> **An estimate, with a clear purpose.** CO₂e means carbon dioxide equivalent. ShopImpact estimates impact as
> **price × category factor**. It does not measure a specific product's actual emissions.

| Built with | Workspace data | Checks | Release status |
| :---: | :---: | :---: | :---: |
| Python 3.12 · Streamlit · Altair | Current browser session only | 86 tests passed · 26 Nov 2026 | Live on Streamlit Cloud |

---

## ✨ Highlights

### 🎨 Cinematic "Conscious Market Journal" design
- **Living background:** slow crossfades between second-hand market, clothes-rack, produce-stall and forest footage, with film grain and warm WebGL bokeh. It is injected once into the page, so it keeps looping across every click; a watchdog restarts stalled clips and a still gradient sits underneath, so the screen never goes black.
- **Video hero:** a masked serif headline ("A little more *mindful*, every month."), a level orb that draws itself, counting stats and a scrolling ticker of habits.
- **Editorial details:** dark glass panels, Fraunces serif headlines, mono kickers, numbered section headings, a pill tab index, gentle 3D card tilt and an earthy chart palette.
- **Themes for every mood:** **Normal** (natural footage), **Day** (warm golden grade with sun and clouds) and **Night** (blue-graded footage, crescent moon and falling stars).
- **Respectful motion:** turning off *Animated scenery*, or the device's reduced-motion setting, removes the video and animations. **High contrast** switches to black, white and yellow with no footage.

### 🧾 A shopping journal you can trust
- Product type (with icons), brand or shop, price and date, plus a **live receipt-style estimate** that shows the kg CO₂e, a reuse/new tag and an everyday equivalent as you type.
- A month dashboard with a **month-in-a-sentence** summary, spending, estimated kg CO₂e, category bars and donut, and animated **goal rings**.
- Search, month and category filters, sorting by date, price or impact, editing, deletion, filtered CSV downloads and JSON backup and restore.

### ⏸️ Habits, not guilt
- **Mindful wishlist:** park something for a 7-day cool-off, then skip it (+25 eco points, money "kept in your pocket") or buy it (it becomes a purchase with a fresh estimate).
- **Eco journey:** eco points, five levels from *Seedling* to *Forest keeper*, a reuse and repair streak and seven lifetime milestones. Points never change the fixed badge rules.
- **Everyday equivalents:** each month's estimate pictured as car kilometres, smartphone charges and tree-months using US EPA factors.
- **Ideas before buying:** category alternatives, named reuse and repair options with official links, rotating tips and a Turtle-drawn leaf reward.

### 🏠 No sign-in required
- The app opens directly to the dashboard with a separate in-memory workspace for each active Streamlit session.
- Purchases, wishlist items and preferences are temporary; refreshes, reconnects or app restarts may clear them.
- Download a JSON backup to keep entries. Anyone using the same active browser session can see its workspace.

---

## 🖼️ Screens

<table>
  <tr>
    <td width="50%"><img src="docs/media/02-hero.jpg" alt="Video hero with serif headline, level orb and ticker"/><br/><sub><b>Home</b> — video hero, level orb, counting stats</sub></td>
    <td width="50%"><b>Direct home</b><br/><sub>The app opens directly without sign-in or email verification. Current direct-home screenshot pending.</sub></td>
  </tr>
  <tr>
    <td><img src="docs/media/03-add-purchase.jpg" alt="Monthly KPIs and the add a purchase form with a live estimate"/><br/><sub><b>Add a purchase</b> — KPIs and a live receipt-style estimate</sub></td>
    <td><img src="docs/media/04-month-glance.jpg" alt="Category bars, donut and achievements"/><br/><sub><b>Your month at a glance</b> — bars, donut and badges</sub></td>
  </tr>
  <tr>
    <td><img src="docs/media/05-equivalents.jpg" alt="Everyday equivalents and alternatives"/><br/><sub><b>Equivalents and alternatives</b> — car km, phone charges, tree-months</sub></td>
    <td><img src="docs/media/06-wishlist.jpg" alt="Mindful wishlist with cool-off cards"/><br/><sub><b>Mindful wishlist</b> — 7-day cool-off, skip or buy</sub></td>
  </tr>
  <tr>
    <td><img src="docs/media/07-insights.jpg" alt="Six-month trend and category mix"/><br/><sub><b>Insights</b> — six-month trend and category mix</sub></td>
    <td><img src="docs/media/08-journey.jpg" alt="Eco journey level card, points and milestones"/><br/><sub><b>Eco journey</b> — level, points, milestones</sub></td>
  </tr>
  <tr>
    <td><img src="docs/media/09-history.jpg" alt="Searchable purchase history with an impact column"/><br/><sub><b>History and backups</b> — search, filter, export</sub></td>
    <td><img src="docs/media/10-night.jpg" alt="Night theme with blue-graded footage, moon and stars"/><br/><sub><b>Night theme</b> — moon, stars, blue-graded footage</sub></td>
  </tr>
</table>

<sub>Existing images show the previous account-enabled design and fictional purchases; they do not represent the current session-only app. No real user data is shown.</sub>

---

## ⚙️ How it works

<div align="center"><img src="docs/media/architecture.svg" alt="Architecture: browser session, motion layer, Streamlit app, Python logic and reference data" width="100%"/></div>

```mermaid
flowchart LR
    A[Private browser session] --> B[Log a purchase]
    A --> W[Mindful wishlist]
    W -- buy --> B
    W -- skip --> J[Eco journey]
    B --> C[Python calculations]
    C --> D[Dashboard and Insights]
    C --> Q[Everyday equivalents]
    B --> J
    B --> S[Session-only workspace]
    W --> S
    S --> D
    D --> F[CSV reports and JSON backups]
```

### 📐 Data and calculations

- **Emission factors:** final **USEEIO Supply Chain GHG Emission Factors v1.4.0** (Cornerstone Sustainability Data Initiative, October 2025), IPCC AR6 warming potentials and 2024 USD prices. INR factors use the World Bank 2024 annual-average exchange rate. Values, source rows, mappings and URLs live in `data/emission_sources.json` and `data/product_catalog.json`.
- **Everyday equivalents:** US EPA Greenhouse Gas Equivalencies Calculator factors (page updated 4 August 2026): 3.93 × 10⁻⁴ t CO₂e per average petrol-car mile, 1.24 × 10⁻⁵ t CO₂ per smartphone charge and 0.060 t CO₂ per urban tree seedling per year (`data/equivalents.json`). They picture the estimate; they are not measurements, offsets or savings.
- **Honest limits:** these are **rough reference estimates**. US sector averages, broad category mappings, a fixed historical exchange rate and unadjusted prices are not a validated India-specific footprint. New and reused versions use the same factor; no unsupported reuse discount is invented. See the [methodology and migration policy](docs/2026-update.md). Existing purchases keep their stored estimates until recalculated in *How it works*.

---

## 🧭 Pages

| Tab | What you do there |
| --- | --- |
| 🌿 **Dashboard** | Pick a month, read the month in a sentence, add a purchase, see charts, goal rings, badges, equivalents and alternatives |
| ⏸️ **Mindful wishlist** | Park a want for 7 days, then skip it or buy it |
| 📈 **Insights** | Six-month trend, category mix, average purchase, goal balance and change from the previous month |
| 🏆 **Eco journey** | Level, eco points breakdown, lifetime milestones and monthly badges |
| 🧾 **History & backups** | Search, filter, sort, edit, delete, export CSV, and back up or restore JSON |
| 📚 **How it works** | Assumptions, factor table, privacy notes and estimate recalculation |

The sidebar holds **Theme & animation**, session-only monthly spending and CO₂e goals, and high contrast.

---

## 🚀 Run it locally

Clone the repository, open the folder in VS Code and run these in its PowerShell terminal:

```powershell
git clone https://github.com/kavin-beep/IDAI102_1000527_ShopImpactAI_Kavin-K.git
cd IDAI102_1000527_ShopImpactAI_Kavin-K
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt --no-cache-dir
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

Open the URL printed in the terminal (normally http://localhost:8501). The dashboard opens immediately with an empty
session workspace; no account or email setup is required. Purchases and preferences exist only for the active
Streamlit session and may be cleared by a refresh, reconnect or app restart. Download a JSON backup before ending the
session if you need to keep entries. VS Code tasks and a *Run ShopImpact* debug configuration are included (they need
Microsoft's Python and Python Debugger extensions).

**Turtle reward artwork**

```powershell
.\.venv\Scripts\python.exe tools/draw_rewards.py
.\.venv\Scripts\python.exe tools/draw_rewards.py --preview
```

The default command uses `turtle.TNavigator` with an SVG pen adapter. `--preview` uses `turtle.Turtle` and needs a
working Tk. The app shows the generated SVG when a qualifying choice exists; it is not a live browser Turtle animation.

---

## ☁️ Deploy on Streamlit Community Cloud

1. Push this repository to GitHub and create an app on [share.streamlit.io](https://share.streamlit.io) with `app.py` as the entry point.
2. No database or email secrets are required for the current session-only app. See [deployment instructions](docs/deployment.md).
3. Each active visitor session has separate in-memory data. It is not durable across refreshes, reconnects, or server restarts; users should download backups.

---

## 🔒 Storage and privacy

- No account, password, database or email address is used by the current app interface.
- Purchases, wishlist items and preferences are held in Streamlit session state, not written to a database. Sessions are separate, but anyone sharing the same active session can see its data.
- Session data may disappear after refresh, reconnect, deployment or server restart. JSON backups let users keep a copy; exports do not contain account credentials because there are no app accounts.
- Account and email backend modules remain in the repository for legacy tests/tools, but are not connected to the running app.

---

## 🧪 Testing

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

86 automated tests pass (26 November 2026), and every push and pull request runs the suite on GitHub Actions. Tests use disposable data and do not write to real users. See [test evidence](docs/testing.md).

| Test file | What it checks |
| --- | --- |
| [tests/test_logic.py](tests/test_logic.py) | Decimal rounding, price and date validation, factor provenance, summaries and badge rules |
| [tests/test_insights.py](tests/test_insights.py) | Six-month trends, month shifting, goal balance and history filters |
| [tests/test_journey.py](tests/test_journey.py) | Eco points, levels, streaks, milestones, EPA equivalents and the wishlist lifecycle |
| [tests/test_accounts.py](tests/test_accounts.py) | Legacy account service behavior; the running app no longer uses this service |
| [tests/test_app.py](tests/test_app.py) | Streamlit flows: direct home access, no login/email controls, isolated sessions, themes, purchases, insights and wishlist |
| [tests/test_email_actions.py](tests/test_email_actions.py), [tests/test_email_delivery.py](tests/test_email_delivery.py) | Legacy verification/reset services; these flows are not part of the running app |
| [tests/test_database_setup.py](tests/test_database_setup.py) | Hosted database configuration helpers |

---

## 🗂️ Project structure

```text
IDAI102_1000527_ShopImpactAI_Kavin-K/
├── app.py              # Dashboard, wishlist, insights, journey, history and backups
├── account_ui.py       # In-memory guest workspace for the active Streamlit session
├── accounts.py         # Legacy account service; not connected to the running app
├── logic.py            # Decimal calculations, purchases, monthly summaries, badge rules
├── insights.py         # Six-month trends, goal balance and filtered history views
├── journey.py          # Eco points, levels, streaks, milestones, equivalents, wishlist
├── ui.py               # Cinematic design system, background footage, themes, HTML components
├── charts.py           # Earthy Altair bars, donuts and trend areas
├── storage.py          # Validated JSON import/export and spreadsheet-safe CSV
├── email_delivery.py   # Legacy optional email helpers; not connected to the running app
├── data/               # Product catalog, source evidence, EPA equivalents, tips, links
├── tools/              # Turtle leaf, database and email setup helpers
├── tests/              # 86 app, logic and legacy service tests
├── docs/               # Design, methodology, testing, deployment; docs/media holds README art
└── output/             # 10-page guide (PDF) and PowerPoint presentation
```

---

## 🧰 Tech stack

| Layer | Tools |
| --- | --- |
| App | Python 3.12, Streamlit, Vega-Altair, pandas |
| Motion and design | CSS animation, Three.js (WebGL bokeh), Mixkit footage, Fraunces, Inter, JetBrains Mono |
| Data | USEEIO v1.4, World Bank 2024 INR rate, US EPA equivalencies |
| Accounts and storage | SQLAlchemy, Neon PostgreSQL or SQLite, argon2-cffi |
| Quality | unittest + Streamlit AppTest, GitHub Actions |

---

## 🎓 Assessment and presentations

- **Canva deck** (21 slides, with speaker notes): [canva.link/v8iiqeb2k0bxb1g](https://canva.link/v8iiqeb2k0bxb1g)
- **10-page code and data guide**: [`ShopImpact_10_Page_Explanation.pdf`](output/pdf/ShopImpact_10_Page_Explanation.pdf)

The PowerPoint deck and PDF guides are regenerated for the November 2026 current design and 94-test snapshot.
The [repository readiness review](docs/repository-readiness.md) records the implementation checks. No real participant
feedback has been collected yet, so [requirements](docs/requirements.md) and the
[feedback record/template](docs/usability-feedback.md) remain the accurate evidence for this assessment status.

---

## 📚 References

- [USEEIO v1.4 published dataset](https://zenodo.org/records/17202747)
- [World Bank 2024 INR exchange rate](https://api.worldbank.org/v2/country/IND/indicator/PA.NUS.FCRF?date=2024&format=json)
- [US EPA Greenhouse Gas Equivalencies Calculator — calculations and references](https://www.epa.gov/energy/greenhouse-gas-equivalencies-calculator-calculations-and-references)
- [Streamlit database guidance](https://docs.streamlit.io/develop/concepts/connections/connecting-to-data)
- [Vega-Altair charts](https://altair-viz.github.io/)
- [Python Turtle](https://docs.python.org/3/library/turtle.html)
- [OWASP password storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- Background and cover footage: [Mixkit](https://mixkit.co/) free stock video licence

---

## 🙏 Credits

- Name: Kavin K
- Grade: IBCP Y1
- Name of Mentor: Syed Ali Beema S
- Registration No: 1000527
- Name of School: Jain Vidyalaya
- AI assistance: OpenAI ChatGPT (Codex) assisted with coding, debugging and documentation; Anthropic Claude assisted with the ShopImpact 2.0 redesign, the cinematic UI, new features and presentations. Project direction and final decisions were made by the student.

<div align="center"><sub>Small choices. A clearer picture. 🌿</sub></div>
