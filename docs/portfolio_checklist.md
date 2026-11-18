# Assignment 3 Part 2 · 30-mark portfolio preflight

**Assessment date:** Friday 20 November 2026, 23:59 (Sydney subject timezone to be confirmed on Canvas). **Submission:** ONE PDF per group with the live deployed app URL, repository URL and assessed commit SHA or release tag. All other materials must be in that commit.

Status below refers to the supplied project as reviewed and patched locally on **18 November 2026**. "In code" does not confirm deployed rendering. Do not claim a final mark from this checklist.

| # | Binary check | Current evidence / remaining task |
| ---: | --- | --- |
| 1 | Question one sentence in README | Present |
| 2 | Question on opening screen | Present in `app.py` |
| 3 | Question is arguable | Present, with two interpretations in README |
| 4 | Persona and decision | Maya, small-business policy adviser, in README |
| 5 | Three as-a/I-want/so-that stories | Present |
| 6 | Each story navigable in app | Pages 2–4 implement controls; verify deployed walkthrough |
| 7 | Every displayed number traces to source | All 44 Industries values tested; group should sample-check size/country pages |
| 8 | App answers question in text | Present in home page `Our answer` section |
| 9 | App states limitations | Home footer and Industries page |
| 10 | Units, baselines, time coverage | Labelled in chart captions; group to inspect every page |
| 11 | Claims supported by available data | Industries validated; check full app live |
| 12 | Chart captions/titles | Present on five charts |
| 13 | At least four charts | Five in this copy: EU trend, size, industry ranking, industry change, countries |
| 14 | Three Visual Vocabulary families | Change, ranking, deviation; verify reviewer classification |
| 15 | Chart forms fit tasks | Charts follow trend, size comparison, ranking, change and EU difference tasks |
| 16 | Axes/legends show units | Present in source; inspect rendered labels |
| 17 | Values readable without hovering | Added both industry-year labels and ranking labels; other pages have labels |
| 18 | Colour vision deficiency check | Okabe–Ito colours and redundant shapes/lines; **visual simulation still required** |
| 19 | Live URL loads under five seconds | **Unknown: no deployed app URL in supplied files** |
| 20 | Opens with whole-dataset truth | Home headline EU adoption and derived metrics |
| 21 | Two interactions change visible data | Industries year radio + multiselect in source; **latency untested** |
| 22 | Empty filter state avoids errors | Industries and countries give explicit info messages |
| 23 | Fits 1366×768 vertically | **Browser/device test outstanding** |
| 24 | Sources and refresh on screen | Shared footer on every page |
| 25 | Source & processed data in repo | Both folders bundled; confirm committed to group repo |
| 26 | Dictionary fully covers data | Source/processed schema present and expanded; **actual download dates need confirmation** |
| 27 | Submitted hash/tag resolves, app runs | **Unknown: group repository and commit not supplied** |
| 28 | Every member's provenance row | **Only Member 3 completed in this copy; Members 1/2/4 must complete their rows** |
| 29 | Data and AI disclosure present | Present, revised to include Member 3 ChatGPT use; **group to review accuracy** |
| 30 | Processed values regenerate | **Locally verified:** all four CSVs exactly regenerated from raw snapshots |

## Group handoff

Keep the group's existing app and repo. Merge the revised `pages/3_Industries.py`, add the tests, and merge documentation changes intentionally (especially the provenance row, which must be reviewed by the member named). A teammate must finish Members 1, 2 and 4's provenance rows with their real tools/prompts/verification and record the assessed commit. Only then create the one-page submission PDF.
