# QA report | 27 October 2026

## Completed

- Built and rendered an offline six-page interactive dashboard with working page navigation, year/period, comparison, channel, country and product group filters.
- Chromium headless test found **zero JavaScript page errors** when rendered from embedded HTML and exercised the controls. The 2026 Jan–Sep / BU overview was captured as `Ben_Stoter_Meridian_Overview.png`.
- Generated 1,400,000 synthetic detail orders for January 2023 to September 2026 and their monthly channel × country × category aggregate.
- Generated 2026 budget, April, July and September 2026 forecast version inputs and conformed dimensions.
- Reconciled monthly and detail revenue. See `data/qa_results.json` and run `python scripts/validate_data.py`.
- Created text-format Power BI Project starter with six pages, TMDL model, relationships, explicit DAX measures and import CSV connections.
- Applied gold and taupe colour palette to interactive demo and Power BI theme JSON.

## Not completed / needs a Windows Power BI test

- **Native .pbip Desktop open, refresh and save**: Not tested, because Power BI Desktop is unavailable on this Linux runtime.
- **Native PBIR visual render and theme fidelity**: Static file checks only; generated visuals may need revision to match the offline HTML and Power BI Desktop schema.
- **Native PBIR slicers on all five dimensions**: The starter includes Year and Comparison; channel, market and category filters are working in the HTML demo but should be built out in Desktop.
- **Model comparison calculation group**: Implemented as a disconnected comparison selector and SWITCH measures rather than a true Power BI calculation group.
- **Cloud publication / scheduled refresh / Fabric DirectQuery**: Intentionally not performed.

## Decision

The self-contained **HTML replica is ready for demonstration**. The native **Power BI Project remains a developer starter until tested and validated in Power BI Desktop**. No client data, client files or live systems were modified.
