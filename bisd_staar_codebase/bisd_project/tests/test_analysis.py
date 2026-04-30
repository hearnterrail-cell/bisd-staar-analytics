"""
test_analysis.py
Unit and validation tests for analysis.py pipeline.
Run with: python -m pytest tests/test_analysis.py -v
"""

import sys
from pathlib import Path
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from analysis import load_data, bisd_trend, district_comparison, gap_vs_state, recovery_index

BISD = "Beaumont ISD"


@pytest.fixture(scope="module")
def df():
    return load_data()


def test_load_returns_dataframe(df):
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_no_nulls(df):
    assert df.isnull().sum().sum() == 0, "Dataset contains unexpected nulls"


def test_percentages_in_range(df):
    for col in ["pct_met_grade_level", "pct_approaches", "pct_masters", "state_avg_met"]:
        assert df[col].between(0, 100).all(), f"{col} has out-of-range values"


def test_bisd_trend_has_expected_years(df):
    trend = bisd_trend(df)
    assert set(trend["year"]) == {2019, 2021, 2022, 2023, 2024}


def test_district_comparison_sorted_descending(df):
    comp = district_comparison(df, 2024)
    vals = comp["avg_pct_met"].tolist()
    assert vals == sorted(vals, reverse=True)


def test_gap_is_positive_for_bisd(df):
    """State average should exceed BISD in all years."""
    gap = gap_vs_state(df)
    assert (gap["gap"] > 0).all(), "BISD gap should be positive (below state)"


def test_gap_vs_state_columns(df):
    result = gap_vs_state(df)
    assert "gap" in result.columns
    assert "year" in result.columns


def test_recovery_index_structure(df):
    ri = recovery_index(df)
    assert "baseline_2019" in ri
    assert "current_2024" in ri
    assert "change_ppts" in ri
    assert ri["change_ppts"] == round(ri["current_2024"] - ri["baseline_2019"], 1)


def test_n_tested_positive(df):
    assert (df["n_tested"] > 0).all()
