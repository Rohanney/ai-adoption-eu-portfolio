# Member 3 provenance row (copy into the group matrix after member review)

| Artefact | Who | Tool | What was asked | What came back | How verified (check that could fail) | Outcome |
| --- | --- | --- | --- | --- | --- | --- |
| `pages/3_Industries.py`, `tests/test_industries.py`, industry validation / portfolio handoff | Member 3 — Industries | ChatGPT (OpenAI), 18 Nov 2026 | Improve the already presented Industries section for the final portfolio and verify data source traceability | Suggested ranking and two-year comparison charts, direct labels, empty state and automated source-to-chart checks | Ran `python -m unittest discover -s tests -v` (4/4 passed); the tests match each of the 44 processed values to Eurostat raw CSV rows filtered by EU27, industry, firm size, indicator, unit and year, and check 62.52%, 25.37% and 10.79%. Wrong filters, missing rows or changed outputs would fail | Automated checks passed locally; visual verification and Member 3's confirmation required before submission |

Do not add fabricated AI uses. If earlier tools were used in Part 1, add separate, truthful rows describing the work and verification. The group matrix at `docs/ai_provenance.md` already includes this final-portfolio row.
