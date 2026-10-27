# CLAUDE.md | Ben Stoter | Meridian Commercial Performance

## Mission

Implement and validate a **native, editable Power BI report** using the synthetic Meridian Electronics 2023–2026 dataset. The intended UX is the offline six-page dashboard `Ben_Stoter_Meridian_Interactive_Dashboard.html`. Use the actual files in this repository, not assumed data structures. Do not replace the retail example with an M&A deal pipeline. Do not copy the LinkedIn author's Contoso branding. Maintain the six-page structure and the Ben Stoter visual theme.

## Read in order

1. This file.
2. `README.md` for technical and factual scope.
3. `data/qa_results.json` and `scripts/validate_data.py`.
4. `PowerBI/...SemanticModel/definition/model.tmdl`, `relationships.tmdl` and all referenced measures.
5. `Ben_Stoter_Meridian_PowerBI_Theme.json`.
6. Only then modify `PowerBI/...Report/definition/` and examine the HTML as a visual specification.

## Tooling

- Use the **official Microsoft skills-for-fabric Power BI authoring** guidance for PBIP, PBIR, TMDL and, when supported, calculation groups: https://github.com/microsoft/skills-for-fabric
- Prefer source-controlled text definitions over manual click sequences where safe. Do not assert that a PBIP file opens or renders until actually tested in Desktop.
- This project provides synthetic CSV data and a no-cloud local-test path. Do not request or use private workspaces, email or client files for this reproduction.

## Visual standard

Use the **Ben Stoter** design guide as the authority: `#BB974B` gold, `#ACA18B` taupe, `#414141` charcoal, `#000000` black, backgrounds off-white. Serif section titles resembling Playfair Display and Arial body labels. Preserve hierarchy, alignment, consistent units and restrained annotations. Use meaningful variance red/green, never colour alone. Show AC as solid gold, PY neutral grey, BU outlined/unfilled, FC hatched where supported. Use USD. Labels should say **AC**, **PY**, **BU** and **FC**. Distinguish forecast **versions** from selected comparison. Avoid excessive gridlines. Do not imply synthetic results represent real company performance.

## Semantic model

- Two facts: `FactSalesMonthly` (monthly actuals), `FactPlan` (budget + forecast versions).
- Shared conformed dimension tables: Date, Channel, Market, Category. PlanVersion connects only to FactPlan. Comparison remains disconnected.
- Preserve a single-direction star schema and one-to-many relationships from dimension to fact.
- Never concatenate fact-to-fact relationships. Use explicit DAX `DIVIDE`, avoid implicit aggregation on financial dimensions.
- Verify that time-intelligence calculations give the expected result under a full month/date range and year selection.
- Budget only exists for 2026. Handle non-2026 comparisons with honest blanks, not invented plans or false zeroes.
- `Forecast Sep 2026` is the most recent forecast; retain Apr and Jul snapshots for comparison history.
- Never introduce arbitrary margin assumptions into source values. `Gross Profit` derives from Revenue minus COGS in actuals.
- Consider native calculation groups once the main report has passed acceptance, but do not silently substitute them for the tested comparison logic.

## Six required pages

1. Executive overview: AC revenue, GP, GM, variance cards; monthly comparison; channel breakdown and management read-out.
2. Channel performance: Online vs Stores vs B2B; actual versus selected benchmark and variance.
3. Product contribution: Computing, Mobile, Audio, Gaming and Accessories, with variance.
4. Geographic analysis: UK, Germany, France and Netherlands.
5. Monthly development: monthly revenue, GP and variance trend.
6. Planning & versions: budget, latest forecast and April/July vintage analysis.

Shared slicers: calendar period or year, comparison PY/BU/FC, channel, market, category. **2026 Jan–Sep / BU** default reference view. Browser demo implements five selections already; native PBIR scaffold may need further slicers and theme alignment in Desktop.

## Verification gate: read-only by default

1. Run `python scripts/validate_data.py`. Do not change inputs to force a pass.
2. Run `python scripts/configure_project.py` on the target Windows machine to assign pDataRoot.
3. Parse JSON and TMDL; confirm every field/measure reference resolves.
4. Open `PowerBI/Meridian_Commercial_Performance.pbip` in Power BI Desktop; refresh and inspect every native visual. Fix the project in a copy if it fails. Do not conceal errors or label the scaffold production-ready before an actual native open-and-save validation.
5. Independently reconcile card totals and one country/channel/category matrix to input CSV.
6. Compare six pages visually with the HTML specimen; correct only necessary implementation differences.
7. Summarise remaining issues in `QA_REPORT.md`, mark whether native Desktop testing occurred, and wait for an explicit publishing authorisation. No access tokens, bulk organisation permissions or production data required.

## Change control

- Preserve source data and semantics unless an evidenced issue requires correction. Track any change to data grain, schema, measure logic or colour rules.
- Never replace or overwrite client files or unrelated Power BI models. This is a synthetic sandbox project.
- No cloud deployment, refresh credentials, publishing or sharing without specific human approval.
- Use UK English in documentation. Separate supported facts, assumptions and untested items.
