# Finance × AI | Benjamin Stoter, CA(SA)

**Better financial decisions. Less manual work.**

A practical portfolio of corporate finance, M&A and finance automation projects.

## Live website

https://benjaminstoter-arch.github.io/Public/

## Featured case study: Would you buy this business?

Explore a fictional company's:
- Revenue growth and adjusted EBITDA
- Assumed EBITDA adjustments and earnings quality
- Valuation multiple and enterprise value sensitivities
- Enterprise value to equity value bridge
- Three key buyer questions: earnings quality, cash conversion and customer concentration

Change the assumptions in the browser and export the result as CSV.

## Why this matters

The aim is to move from collecting financial data to making commercial decisions faster, with clear assumptions and straightforward review controls.

## Data and limitations

All figures are synthetic. The project uses browser-based calculations, not an AI model. The illustration is not an investment recommendation. EBITDA adjustments are unverified assumptions and the formula checks do not validate source data.

## Roadmap

1. Financial upload and validation.
2. Working capital and cash conversion analysis.
3. Evidence-linked financial commentary.
4. Exportable board-ready Excel outputs.

## Project 2: Cash conversion and working capital

[Open the working capital case study](https://benjaminstoter-arch.github.io/Public/cash-conversion.html).

Illustrates cash after tax, capex and working capital movements, DSO/DIO/DPO, a working capital peg and the EV-to-equity completion bridge. Uses fictional figures and simplified assumptions. It is not a full cash flow statement or a due diligence conclusion.

## Project 3: Monthly FP&A Review

[Open the working monthly finance review](https://benjaminstoter-arch.github.io/Public/fpa-reporting.html).

Compares actual, budget and prior-year results, highlights material variances, checks gross profit and EBITDA arithmetic, suggests follow-up actions and exports results to CSV. The prototype uses fictional data and deterministic commentary rather than live AI. Root causes are not inferred from variance values alone.

## Project 4: Management Accounts CSV Review

[Open the CSV-to-management-report tool](https://benjaminstoter-arch.github.io/Public/fpa-upload.html) or [download the sample file](https://benjaminstoter-arch.github.io/Public/sample-management-accounts.csv).

Upload a CSV with **Month, Line item, Type, Actual, Budget, Prior year**. The tool validates files, calculates revenue, gross profit and EBITDA, reconciles budget variances and proposes review actions. It exports a report CSV and management summary.

- Data stays in the browser. No user financial file is sent to a server by the application.
- Supports Revenue, Direct costs and Operating costs, with costs entered as positive amounts in GBP units.
- Flag thresholds are editable. Commentary is deterministic and does not establish underlying causes.
- The example is fictional and the tool is a prototype, not an accounting or assurance product.
- Calculation and input checks: `node tests/fpa-core.test.js`.
