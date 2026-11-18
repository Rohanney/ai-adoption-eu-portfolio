# AI provenance matrix

One row per substantive AI use. Every member must own at least one row, written by them about what they actually did. Each verification must name a check that **could have failed**.

| # | Artefact | Who | Tool | What was asked | What came back | How it was verified (a check that could fail) | Outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Question wording, member split, `app.py`, `src/data.py`, docs templates | Member 2 (TO FILL: name) | Claude (Anthropic), claude.ai, Oct 2026 | Sharpen an arguable question on AI adoption; propose a four-way split; build a Streamlit app and transform for Eurostat `isoc_eb_ai` / `isoc_eb_ain2` | A draft question, four section designs, working app and transform code, README / dictionary / matrix templates | Traced the large-firm EU27 latest-year value from the raw CSV (filter `indic_is=E_AI_TANY`, `unit=PC_ENT`, size `GE250`, `geo=EU27_2020`) to the app. This would have failed if the size-code mapping in `src/data.py` were wrong. Result: TO FILL | TO FILL (e.g. accepted; fixed X) |
| 2 | TO FILL (Member 1) | | | | | | |
| 3 | `pages/3_Industries.py`, `tests/test_industries.py`, industry validation and presentation guidance | Member 3 — Industries | ChatGPT (OpenAI), 18 Nov 2026 | Review the existing presented Industries page against the final portfolio rubric; add directly labelled ranking and comparison views, an empty-state message, and source-to-chart checks | Proposed page changes, testing code, evidence log and handoff | `python -m unittest discover -s tests -v` checks all 44 processed industry values against the exact raw Eurostat rows (EU27, 10+, AI technology indicator, percent unit, years); the checks would fail if the industry, indicator, geography, year or transform were wrong. Verified 25.37 (2021 ICT), 62.52 (2025 ICT), and 10.79 (2025 construction); regeneration produced four byte-identical processed CSVs | Automated local checks PASS. Member 3 to review final visual rendering and verify this row before group submission |
| 4 | TO FILL (Member 4) | | | | | | |

Examples of checks that could fail: a value traced to the raw CSV does not match; `python -m src.data` raises a validation error; a chart total disagrees with a hand calculation; a claim on screen is contradicted by a different year or country.
