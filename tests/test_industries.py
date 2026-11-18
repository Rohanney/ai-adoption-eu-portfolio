"""Reproducibility and traceability tests for the Member 3 Industries page.

Run from the application root with: python -m unittest discover -s tests -v
"""

from __future__ import annotations

import unittest
from pathlib import Path

import pandas as pd

from src.data import (
    ALL_10,
    EU_LABEL,
    INDICATOR_PREFIX,
    RAW,
    SECTOR_LABELS,
    UNIT,
    build,
    validate,
)

ROOT = Path(__file__).resolve().parents[1]


class IndustryDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tables = build()
        validate(cls.tables)
        cls.sector = cls.tables["adoption_by_sector"]
        cls.raw = pd.read_csv(RAW / "isoc_eb_ain2.csv", keep_default_na=False)

    def raw_value(self, industry: str, year: int) -> float:
        matched = self.raw[
            (self.raw["nace_r2"] == industry)
            & (self.raw["size_emp"] == ALL_10)
            & (self.raw["geo"] == EU_LABEL)
            & (self.raw["indic_is"].str.startswith(INDICATOR_PREFIX))
            & (self.raw["unit"] == UNIT)
            & (self.raw["TIME_PERIOD"] == year)
        ]
        self.assertEqual(len(matched), 1, f"Raw observation not unique: {industry} {year}")
        return float(matched.iloc[0]["OBS_VALUE"])

    def processed_value(self, industry: str, year: int) -> float:
        label = SECTOR_LABELS[industry]
        rows = self.sector[(self.sector["sector"] == label) & (self.sector["year"] == year)]
        self.assertEqual(len(rows), 1, f"Processed observation not unique: {industry} {year}")
        return float(rows.iloc[0]["pct_enterprises"])

    def test_sector_coverage(self):
        self.assertEqual(set(self.sector["sector"]), set(SECTOR_LABELS.values()))
        self.assertEqual(set(self.sector["year"]), {2021, 2023, 2024, 2025})
        self.assertEqual(len(self.sector), 44)

    def test_all_sector_values_match_raw(self):
        for industry in SECTOR_LABELS:
            for year in [2021, 2023, 2024, 2025]:
                with self.subTest(industry=industry, year=year):
                    self.assertAlmostEqual(self.processed_value(industry, year), self.raw_value(industry, year), places=8)

    def test_presentation_statistics_trace_to_source(self):
        checks = [
            ("Information and communication", 2021, 25.37),
            ("Information and communication", 2025, 62.52),
            ("Construction", 2025, 10.79),
        ]
        for industry, year, expected in checks:
            with self.subTest(industry=industry, year=year):
                self.assertAlmostEqual(self.raw_value(industry, year), expected, places=2)
                self.assertAlmostEqual(self.processed_value(industry, year), expected, places=2)
        self.assertAlmostEqual(62.52 - 25.37, 37.15, places=2)
        self.assertAlmostEqual(62.52 - 10.79, 51.73, places=2)

    def test_regenerated_files_match_committed_processed_files(self):
        for name, generated in self.tables.items():
            committed = pd.read_csv(ROOT / "data" / "processed" / f"{name}.csv", keep_default_na=False)
            pd.testing.assert_frame_equal(
                committed.reset_index(drop=True),
                generated.reset_index(drop=True),
                check_dtype=False,
                check_exact=False,
                rtol=0,
                atol=1e-10,
            )


if __name__ == "__main__":
    unittest.main()
