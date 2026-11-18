# Group final portfolio handoff

## Important project status

This is the **existing four-page Part 1 group app**, including the enhanced Member 3 Industries page for the Part 2 portfolio. It is not a newly invented research project.

- **Project question:** Since 2021, has AI adoption by European businesses been broad-based, or has it stayed concentrated in large firms, the tech sector and a few countries?
- **App entry point:** `app.py` at the repository root.
- **Data:** Two supplied Eurostat CSV source snapshots in `data/raw/`, processed by `python -m src.data` into four `data/processed/` CSVs.
- **Member 3:** Two labelled industry charts, a year selector and a sector selector. `tests/test_industries.py` traces all 44 values to Eurostat originals.
- **Member 1/2/4:** Existing EU trend, firm size and countries views retained from original group package.

## Verification

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m src.data
streamlit run app.py
```

The test suite checks data values and reproducibility, not Streamlit page rendering or the speed of the live deployed app. Verify deployment manually at 1366 x 768 and measure startup/interaction responsiveness.

## Before submitting (required)

1. Confirm each group member has reviewed the code and has committed their actual work and AI provenance row in `docs/ai_provenance.md`; placeholders are not valid submissions.
2. Check that the AI disclosures in `docs/disclosure.md` accurately reflect actual use of AI tools; correct unsupported statements rather than guessing.
3. Confirm the original source download dates in `docs/data_dictionary.md` if available; don't invent dates.
4. Confirm the app has at least four legible charts from three visual vocabulary families; visually inspect all pages and check color-vision accessibility.
5. Deploy the GitHub repository using Streamlit Community Cloud (`app.py` as entrypoint); open the public URL from a logged-out browser, test page loading and both interactive controls.
6. Copy the live app URL, the exact GitHub repository URL and the assessed commit SHA into the **one group PDF**. All work must be committed at that SHA, and deployment must refer to that version.

Reference checklist: `docs/portfolio_checklist.md`. Draft submission fields: `docs/submission_pdf_fields.md`.

## Git first-time setup (Windows PowerShell)

Create an **empty** repository on GitHub, then in the extracted project root run:

```powershell
git init -b main
git add .
git commit -m "Initial final portfolio: EU AI adoption narrative"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

Replace the repository URL with the real URL; log in when prompted. Do not commit passwords, keys, `secrets.toml`, or personal credentials. If Git is not installed, install Git for Windows or use GitHub Desktop, which supports large regular Git files.

The large Eurostat source CSV may exceed GitHub's *browser-upload* size limit, even though it is below the normal Git object limit. Use the Git/desktop workflow to include it.
