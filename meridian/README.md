# Ben Stoter | Meridian Commercial Performance

**Personal portfolio demonstration | Ben Stoter | 27 October 2026**

A working, fully offline, six-page interactive retail sales dashboard, adapted from the approach described in Ilya Fedorkov’s LinkedIn article *Power BI with Claude Code: my method, prompts and CLAUDE.md* (26 October 2026). This is a **new implementation**, not the author’s original files or a copy of his commercial data. All underlying trading numbers and the Meridian Electronics company are synthetic. There is **no real company or client transactional data** in the package.

## Open the working demo now

Open [`index.html`](index.html) in Chrome or Edge (or the equivalent long-name dashboard file). No installation or internet connection is needed. The six navigable pages are:

1. Executive overview
2. Channel performance
3. Product contribution
4. Geographic analysis
5. Monthly development
6. Planning & versions

Use the period selector, comparison selector (`PY`, `BU`, `FC`), channel, market and product group filters. Select a channel or category row to focus the entire dashboard. Reset restores the default. The demo starts at **2026 YTD, January–September**, in USD and **AC versus BU**. All calculations respond to selections. Planned data is for 2026, so BU and FC will be unavailable or zero outside 2026; use PY when exploring 2023–2025.

## What is included

| Path | Description | Status |
| --- | --- | --- |
| `index.html` (also `Ben_Stoter_Meridian_Interactive_Dashboard.html`) | Full six-page, Ben Stoter-branded offline interactive dashboard | **Working and browser-tested** |
| `PowerBI/Meridian_Commercial_Performance.pbip` | Native Power BI project entry point | **Generated scaffold, needs Power BI Desktop validation** |
| `PowerBI/*.SemanticModel/definition/` | TMDL semantic model with shared dimensions, fact tables, relationships and DAX measures | **Generated and statically checked** |
| `PowerBI/*.Report/definition/` | PBIR report structure with six pages and built-in charts, cards and slicers | **Generated and statically checked** |
| `Ben_Stoter_Meridian_PowerBI_Theme.json` | Importable Power BI theme using gold and taupe | **Generated** |
| `data/FactSales_1400000.csv.gz` | **1,400,000** artificial individual customer orders, gzip compressed; supplied in the downloadable ZIP or regenerated using `scripts/make_data.py`, not checked into public GitHub | **Reconciled** |
| `data/FactSalesMonthly.csv` | Monthly facts, split by channel, country and category, optimised for quick Power BI testing | **Reconciled to detail** |
| `data/FactPlan.csv` | 2026 budget and three dated forecast versions | **Reconciled** |
| `data/Dim*.csv` | Date, channel, market, product group, plan version and comparison selectors | **Generated** |
| `data/qa_results.json` | Initial financial integrity tests | **PASS** |
| `scripts/validate_data.py` | Repeatable source-data reconciliation and duplicate checks | **Runnable** |
| `scripts/configure_project.py` | Points Power BI TMDL to your unzipped local data folder | **Runnable** |
| `CLAUDE.md` | Claude Code implementation brief and quality controls | **Ready to use** |
| `prompts/` | Reusable briefing and finishing prompts | **Ready to use** |

## How to open the native Power BI project

1. Extract the **entire** ZIP to a local directory on a Windows computer.
2. Run `python scripts/configure_project.py` **once** (Python 3 required). It writes the absolute data folder path into the TMDL `pDataRoot` parameter. If Python is unavailable, replace the placeholder in `PowerBI/Meridian_Commercial_Performance.SemanticModel/definition/expressions.tmdl` with the absolute path to the extracted `data` folder. Do not edit the 1.4m-order archive for this step.
3. Open `PowerBI/Meridian_Commercial_Performance.pbip` in a recent version of **Power BI Desktop**, ensuring the PBIP/PBIR/TMDL authoring features required by your Desktop build are supported.
4. Refresh all sources. Set the date slicer to 2026 and comparison to `BU` for the intended default. Review the visuals and re-import `Ben_Stoter_Meridian_PowerBI_Theme.json` if required.
5. Run the acceptance tests below, then save from Power BI Desktop. **Do not publish** until finance QA and organisational permissions are signed off.

**Important compatibility caveat:** this native PBIP/PBIR scaffold was generated without running Microsoft Power BI Desktop on this Linux environment. All JSON files can be parsed, all referenced pages and measures can be checked, and the CSV data can be reconciled, but **native visual rendering, theme import and source refresh have not been tested in Desktop or Fabric**. The offline HTML dashboard **has** been rendered and browser-tested. If Power BI Desktop rejects a schema fragment, Claude Code can use the included official Microsoft Power BI authoring skills and this project as the starting point to repair, open and save it. The included HTML is the visual reference and remains fully usable independently.

## Financial model and expected behaviour

- Dataset: synthetic 2023–September 2026 actuals, with budget/forecast for calendar 2026 only.
- Data grain: actuals at individual order and also month × channel × market × product; plan at month × channel × market × product × version.
- Dimensions: dates, channels, markets, product categories, forecast versions and disconnected comparison selector.
- Metrics: revenue, cost of goods sold, gross profit, gross margin, order count, actual versus previous year, budget and latest September 2026 forecast, value and percentage variance.
- Revenue and gross profit in **USD**. Gross margin and variances shown as percentages, negative figures in brackets in Power BI financial formats where practical.
- **Comparison conventions:** AC = actual; PY = previous year; BU = budget; FC = latest forecast, September 2026. April and July forecast vintages are preserved in the plan data and can be used for version analysis.
- The native PBIP starter uses **Import** mode for both fact tables so it works without a SQL server or Fabric capacity; use DirectQuery only after creating a sanctioned SQL endpoint and checking performance and licensing.
- The starter uses a disconnected DAX selector rather than a native **calculation group**. This replicates the comparison logic while avoiding compatibility risks. Implement calculation groups when the approved authoring environment is ready.
- The browser demo is more visually complete than the generated native PBIR scaffold. It is the approved **design reference**, not a claim that PBIR has already rendered identically.

## Acceptance tests before any real deployment

- Count exactly 1,400,000 unique order IDs in compressed detailed sales.
- Total sales in the order file equals the sum in the monthly aggregated actuals (USD, to the cent).
- For all aggregate actuals, gross profit = revenue less COGS, to the cent.
- Each actual monthly business key is unique; each plan monthly business key + version is unique.
- 2026 BU/FC appears only in 2026 periods and the latest forecast can be selected.
- Month, channel, country and product filters never increase totals beyond the unfiltered actuals.
- Revenue variance = AC minus selected comparison; variance percentage = variance divided by comparison (blank when denominator zero).
- Validate key cards and at least three breakdowns against the CSV group-by summaries independently.
- Ensure no client data, credentials, tokens or unattended cloud permissions enter this demonstration package.
- Validate Power BI Desktop native project open, source refresh, colour/theme rendering, slicers and all six pages before describing it as a production-ready `.pbip`.

## Personal brand styling applied

- Gold `#BB974B`, taupe `#ACA18B`, black `#000000`, charcoal `#414141`.
- Restrained cream backgrounds and high-contrast, dark table headers.
- Playfair Display-style serif hierarchy (using broadly available fallbacks in HTML), Arial body style, sentence-case headings.
- Actuals in solid gold, budget as outlined/unfilled columns, prior year grey, forecast as hatched columns where the interactive HTML supports it.
- Negative comparisons use red. Notes and figures are clearly designated synthetic and suitable for public demonstration.

## Suggested future upgrade

After native Desktop QA, consider a proper SQL source and a refreshable Import/DirectQuery decision, role-level access controls, calculation groups, documented semantic measures, CI checks and a single canonical versioned repository. None has been published or connected to live data in this pack.

**Method reference:** https://www.linkedin.com/pulse/power-bi-claude-code-my-method-prompts-claudemd-ilya-fedorkov-h5dte/  
**Microsoft Power BI authoring repository:** https://github.com/microsoft/skills-for-fabric


## Public repository and privacy

This is a personal portfolio demonstration by Ben Stoter. Meridian Electronics is fictional; all orders, budgets and forecasts were generated synthetically. No employer/client files, logos, contact details, user data or authentication credentials are needed or included. This public repository omits the compressed 1.4 million-order detail to keep source control small. Recreate it by running `python scripts/make_data.py` and then `python scripts/validate_data.py`; the monthly aggregates and sample dashboard JSON are supplied for immediate use. The native Power BI project is a generated starter and has **not** been opened or validated in Power BI Desktop. Do not treat it as production-ready.
