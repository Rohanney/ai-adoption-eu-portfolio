# Data and AI disclosure statement

## Data

All data come from two public Eurostat datasets, `isoc_eb_ai` and `isoc_eb_ain2` (see `docs/data_dictionary.md`). They are reused under Eurostat's free reuse policy with the source acknowledged. The raw files in `data/raw/` are exactly as downloaded. Every processed file is regenerated from them by `python -m src.data`. No values were entered or edited by hand.

The figures are survey estimates of the share of enterprises using at least one AI technology. They cover firms with 10 or more employees and exclude the financial sector. They measure whether a firm uses AI, not how much it uses it or what effect it had.

## AI use

The original group draft documents use of Claude (Anthropic), a large language model, during this project. For the Member 3 final-portfolio changes on 18 November 2026, ChatGPT (OpenAI) was also used; that use is described in row 3 of `docs/ai_provenance.md`. The original draft reports these uses:
- It helped sharpen the research question and propose how to divide the work.
- It wrote the first versions of `app.py`, `src/data.py` and the documentation templates.
- It drafted outline talking points for the Part 1 recordings.

Every number shown in the app is computed from the Eurostat files, not produced by the AI. Member 3 verification tested all 44 industry observations against the raw Eurostat file. Other members must add their own actual AI use and fallible verification checks before the group submits.

Member 3: Prepared an updated Industries page with a latest-year ranking and a two-year comparison, and checked the values using locally run tests. These tests check both the source records and the processed CSVs, but the final deployed rendering still requires human review.

**Group completion required:** Members 1, 2 and 4 must contribute factual first-person statements about their roles and checks; the group must review whether the Claude summary above precisely matches what happened.
