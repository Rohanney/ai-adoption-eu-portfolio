# Member 3 · Industries — final portfolio verification

**Scope:** The completed presentation's Industries page of the existing four-page Eurostat Streamlit app. The group question and established data sources have not changed.

**Research question:** Since 2021, has AI adoption by European businesses been broad-based, or has it stayed concentrated in large firms, the tech sector and a few countries?

## Verified industry evidence

Source file: `data/raw/isoc_eb_ain2.csv`, filtered by the Eurostat text labels listed below. Processed file: `data/processed/adoption_by_sector.csv`. Indicator: enterprises using at least one AI technology; unit: percentage of enterprises; geography: EU27; enterprise size: 10 or more persons employed; economic activities: 11 sectors; survey years: 2021, 2023, 2024, 2025.

| Displayed statement | Value | Source filter / calculation |
| --- | ---: | --- |
| Information and communication, 2021 | 25.37% | Exact `OBS_VALUE` for 2021, EU27, industry `Information and communication`, 10+ firms, AI indicator and percent unit |
| Information and communication, 2025 | 62.52% | Same filters, 2025 |
| Change in information and communication, 2021–2025 | +37.15 percentage points | 62.52 − 25.37 |
| Construction, 2025 | 10.79% | Same filters, industry `Construction`, 2025 |
| Difference between the leading and trailing industry, 2025 | 51.73 percentage points | 62.52 − 10.79 |

These are **percentage points**, not percent growth, and they do **not** imply a 51.73 percentage point gap in employment or output.

## How to reproduce

From the project root (directory containing `app.py`), after installing `requirements.txt`:

```bash
python -m src.data
python -m unittest discover -s tests -v
streamlit run app.py
```

The first command reads the bundled original Eurostat CSVs and regenerates all four files in `data/processed/`. The test suite checks all 44 industry values against the original source rows with an exact filter on industry, geography, size, indicator, unit and year; checks three presentation numbers and two differences; checks coverage and duplicates through `validate()`; and checks that regenerated tables agree with the packaged processed data.

**Local verification on 18 November 2026:** All 4 tests passed. `python -m src.data` wrote 535 size observations, 112 country observations, 44 industry observations, and 2 refresh metadata records. All four regenerated CSVs were byte-for-byte identical to those supplied in the original `Member3_Industries.zip` before any user-interface edits. Python syntax compilation passed.

## Visual and interpretation decisions

1. The 2025 horizontal bar chart is a **ranking** chart and labels every value directly.
2. The paired-year dot chart shows **change** and labels both years directly; it uses circles and diamonds as redundant cues in addition to colours.
3. The combined group app also includes an EU time-series **change** chart and a country-versus-EU **deviation** chart, providing at least three chart families across the portfolio.
4. Selecting a comparison year or a subset of industries changes the charts. Clearing all industries displays an information message rather than a blank or an exception.
5. The page acknowledges that survey percentages describe adoption *within* each industry. They cannot establish productivity effects, causes or total numbers of users, nor can they be summed to a 100% whole.

## Before final submission — checks not established by local data tests

- Run the original **group deployment** and check both charts, labels and mobile/desktop layout visually, especially at 1366×768 with no horizontal page scrolling.
- Check colour-vision-deficiency rendering of the deployed charts; the design uses a colour-vision-conscious palette and multiple non-colour cues, but this is not a substitute for a visual simulation.
- Check page load under 5 seconds and UI interaction latency around 1 second from the deployed URL.
- Confirm the group's actual CSV download dates, verify the other members' provenance rows, and agree on the final commit or release tag.
- Do not treat this local copy as the assessed version until the changes are merged into the **existing group repository** and the deployed app is updated from that commit.

## Industry intelligence enhancement — 18 November 2026

The Member 3 page now includes four directly labelled chart views: a **2021/2023/2024/2025 heatmap** (44 cells for 11 industries), a **2025 ranking**, a **selected earlier year versus 2025 connected-dot comparison**, and an **individual industry trend** using actual year spacing. The KPI strip reports the top and bottom industry, their percentage-point difference and the largest observed 2021–2025 increase. Both the ranking and heatmap change when industries are filtered. The spotlight is deliberately independent of the comparison filter.

All computed statistics use the same version-controlled `data/processed/adoption_by_sector.csv` source that the four local tests already check against raw Eurostat records. The following derived 2025 KPI values were recomputed from that CSV: Information and communication **62.52%**, construction **10.79%**, their gap **51.73 percentage points**, and the largest 2021–2025 increase **+37.15 percentage points** (information and communication). The four heatmap colours (`#263547`, `#235873`, `#0B6A8B`, `#0072B2`) yield white-on-colour contrast ratios of approximately **12.48, 7.74, 6.09 and 5.19** respectively, providing redundant printed values in addition to colour.

The heatmap's discrete survey years do not imply a 2022 observation. The spotlight x-axis is quantitative in calendar years, so the 2021–2023 span is visibly twice a single-year interval. The policy text recommends *investigating* lower adoption, rather than claiming a measured causal effect. The deployed visual layout, interactions and page load times must still be checked separately, since static code/data tests cannot certify them.
