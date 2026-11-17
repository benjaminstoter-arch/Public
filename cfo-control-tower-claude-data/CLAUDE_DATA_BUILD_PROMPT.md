# Claude Data build instruction

Open Claude > Artifacts > Data. Import `demo_finance_monthly.csv` as a data source (or connect your own authorised BigQuery source), then add the prompt below.

---

Recreate Jimmy Chim's 16 November 2026 CFO Control Tower demonstration as faithfully as the public description permits. Use the attached demo CSV, never invent unseen original data. Use an understated blue/white design system, professional finance typography, 15%-width vertical left sidebar, clean compact tables, strong chart labels and a responsive layout. Label all numbers DEMO DATA, USD, and data cut-off October 2026. Build separate sidebar views: Overview, Growth, Financial, Operational, Trended Metrics.

Overview: headline KPIs and charts. Growth: geo revenue $ and geo growth % as separate charts, product, channel, ARR, customer trends. Financial: actual vs forecast revenue and EBITDA, gross profit and margin, opex, cash and cash flows. Operational: active customers, new customers, churn, CAC and pipeline. Include at least 12 meaningful charts with concise one-line insight under each and relevant sources and definitions.

Trended Metrics: a compact table with collapsible metric sections, text search, monthly/quarterly/annual time grain, date-range controls and selectable period count. Support separate toggles for YoY %, period-over-period %, absolute period-over-period USD changes and % of revenue rows. Format figures in $M/$K with one decimal while always exposing exact unrounded value on hover. Include small sparklines in the final column. Clicking any metric opens a larger modal chart with monthly, quarterly, annual grain and data-label toggle. Hover must identify source CSV/table, column and aggregation. Highlight key revenue, gross profit, EBITDA and cash metrics.

Include a source-audit panel revealing the SQL (only if connected to a real database) or the CSV aggregation formula if operating from CSV. Provide definition checks and integrity controls. Build dashboard version history where supported and set refresh to on each visit for live sources. Never claim CSV data are live.

Use the `metric_definitions.md` attached, and follow its aggregation rules. Validate components before display. Avoid extra tabs, invented KPIs or decorative content. Return a working dashboard and show its actual data lineage.

Reference articles: https://jimmysai.substack.com/p/claude-data and https://jimmysai.substack.com/p/i-built-this-cfo-control-tower-with-claude-dashboards

---

To move to real data, connect an authorised data source and agree a metric dictionary, chart query review and access controls before sharing. The standalone HTML preview in this package is a separate offline implementation, **not** a Claude-native artefact.