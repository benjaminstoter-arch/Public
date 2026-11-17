# CFO Control Tower: demo metric dictionary

All data in this package is **synthetic demonstration data**. Currency: USD. Monthly periods use `YYYY-MM`. No client data is included.

| Metric | Definition / aggregation |
|---|---|
| Revenue | `revenue_usd`; sum across periods |
| Gross profit | `gross_profit_usd`; sum |
| Gross margin | `gross_profit_usd / revenue_usd` weighted on periods |
| Operating expenditure | `operating_expenses_usd`; sum |
| EBITDA | `gross_profit_usd - operating_expenses_usd`; sum |
| EBITDA margin | `ebitda_usd / revenue_usd` weighted on periods |
| Cash balance | `cash_usd`; last month in period (not sum) |
| ARR | `arr_usd`; last month in period (not sum) |
| Pipeline | `pipeline_usd`; last month in period (not sum) |
| New customers | `new_customers`; sum |
| Active customers | `active_customers`; last month in period |
| Monthly churn | `churn_rate`; period average |
| CAC | `cac_usd`; period average |
| Revenue by geography | North America + EMEA + APAC = Revenue |
| Revenue by product | Product A + Product B + Product C = Revenue |
| Revenue by channel | Direct + Partner + Online = Revenue |
| Forecast revenue | `forecast_revenue_usd`; sum |
| Forecast EBITDA | `forecast_ebitda_usd`; sum |
| Operating cash flow | `cfo_usd`; sum |
| Investing cash flow | `cfi_usd`; sum |
| Financing cash flow | `cff_usd`; sum |

## Controls and checks

1. Ensure all months have unique `period` identifiers.
2. Validate Revenue equals the three geographic, product and channel splits (tolerance USD 0.02 from rounding).
3. Validate EBITDA approximately equals Gross profit less operating expenditure.
4. Quarterly and annual balances use their ending month, and 2026 annual data only contains Jan–Oct (partial year).
5. Difference comparisons use matched monthly, quarterly or annual periods; first-year values with no prior reference show `—`.
6. Real data imports should pass accounting reconciliation before use in a board or management pack.