# CFO Control Tower: working offline replica

**Reference:** Jimmy Chim, *I rebuilt my CFO Dashboard with Claude Data* (16 November 2026), plus his 19 October 2026 CFO Control Tower article. This is an independent implementation of the **published features**, not a copy of his private code, native Claude artefact or private design-system ZIP. All financial figures are simulated.

## What to open

Double-click `CFO_Control_Tower_Replica.html`. It requires no installation and no internet connection.

The blue left navigation contains Overview, Growth, Financial, Operational and Trended Metrics. It includes 18 chart views (4 Overview, 6 Growth, 6 Financial and 6 Operational, with some repeats), KPI cards, hover values, 2024–2026 demo data, source validation, dynamic CSV import/export and browser-local version snapshots.

In Trended Metrics select a time grain, column count, comparisons, search for metrics, collapse sections or click a row for a modal chart. Hover table cells for exact amounts and source. In modal charts change time grain and data labels.

## Data

`demo_finance_monthly.csv` contains 34 synthetic monthly records for January 2024–October 2026. To use another dataset, prepare exactly the same columns, with at least 13 months of data, and choose **Import CSV**. All imports occur locally in the browser (no upload).

## What the replica cannot do

- It is **not** a native Claude Data artefact.
- It cannot connect directly to BigQuery, refresh live data or display executed SQL; the source panel makes this explicit.
- The exact typography, logo, branding files, layout screenshots and original dashboard source code were not published with the article. Visual appearance is an approximation based on the author's description and public examples.
- The offline saved history uses localStorage in the current browser, where available. It is not cloud version control.

## Claude-native build

Use `CLAUDE_DATA_BUILD_PROMPT.md`, `metric_definitions.md`, `design_tokens.json` and `demo_finance_monthly.csv`. Open Claude > Artifacts > Data, add your source, install your preferred brand files as a design system, paste the prompt and validate each metric/query.

## Confidentiality

No live data or client information is included. Do not connect confidential RBS/third-party systems until access and data handling are approved.