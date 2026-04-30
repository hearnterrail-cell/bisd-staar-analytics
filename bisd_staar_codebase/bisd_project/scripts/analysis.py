"""
analysis.py
Core data cleaning, EDA, and statistical analysis for
Beaumont ISD STAAR Performance Study (Spring 2026).

Author : [Your Name]
Course : COSC5302 – Python Programming & Data Analytics
Date   : April 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
DATA_PATH = Path(__file__).parent.parent / "data" / "bisd_staar_data.csv"
BISD = "Beaumont ISD"

# ── Load & validate ───────────────────────────────────────────────────────────

def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load STAAR dataset and perform basic type coercions.

    Args:
        path: Path to the CSV file.

    Returns:
        Cleaned DataFrame ready for analysis.
    """
    df = pd.read_csv(path)
    df["year"] = df["year"].astype(int)
    df["n_tested"] = df["n_tested"].astype(int)
    for col in ["pct_met_grade_level", "pct_approaches", "pct_masters", "state_avg_met"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def validate_data(df: pd.DataFrame) -> None:
    """Run basic data quality checks and print a summary report."""
    print("=== Data Quality Report ===")
    print(f"Rows: {len(df):,}  |  Columns: {len(df.columns)}")
    print(f"Years covered: {sorted(df['year'].unique())}")
    print(f"Districts: {df['district'].nunique()}")
    print(f"Subjects: {df['subject'].nunique()}")
    nulls = df.isnull().sum()
    if nulls.any():
        print("Nulls detected:\n", nulls[nulls > 0])
    else:
        print("No null values found. ✓")
    out_of_range = (df["pct_met_grade_level"] < 0) | (df["pct_met_grade_level"] > 100)
    print(f"Out-of-range pct rows: {out_of_range.sum()}")
    print("===========================\n")


# ── Analysis functions ────────────────────────────────────────────────────────

def bisd_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Annual average 'met grade level' for BISD across all subjects/grades."""
    return (
        df[df["district"] == BISD]
        .groupby("year")["pct_met_grade_level"]
        .mean()
        .round(1)
        .reset_index()
        .rename(columns={"pct_met_grade_level": "avg_pct_met"})
    )


def district_comparison(df: pd.DataFrame, year: int = 2024) -> pd.DataFrame:
    """Compare all districts for a given year."""
    return (
        df[df["year"] == year]
        .groupby("district")["pct_met_grade_level"]
        .mean()
        .round(1)
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"pct_met_grade_level": "avg_pct_met"})
    )


def subject_breakdown(df: pd.DataFrame, district: str = BISD) -> pd.DataFrame:
    """Average performance by subject for a given district (all years)."""
    return (
        df[df["district"] == district]
        .groupby(["subject", "year"])["pct_met_grade_level"]
        .mean()
        .round(1)
        .reset_index()
    )


def gap_vs_state(df: pd.DataFrame, district: str = BISD) -> pd.DataFrame:
    """Calculate achievement gap between district and state average per year."""
    result = (
        df[df["district"] == district]
        .groupby("year")[["pct_met_grade_level", "state_avg_met"]]
        .mean()
        .round(1)
        .reset_index()
    )
    result["gap"] = (result["state_avg_met"] - result["pct_met_grade_level"]).round(1)
    return result


def recovery_index(df: pd.DataFrame, district: str = BISD) -> dict:
    """Compute pandemic recovery index (2024 vs 2019 baseline for BISD)."""
    pre  = df[(df["district"] == district) & (df["year"] == 2019)]["pct_met_grade_level"].mean()
    post = df[(df["district"] == district) & (df["year"] == 2024)]["pct_met_grade_level"].mean()
    return {
        "baseline_2019": round(pre, 1),
        "current_2024":  round(post, 1),
        "change_ppts":   round(post - pre, 1),
        "recovery_pct":  round((post / pre) * 100, 1),
    }


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    df = load_data()
    validate_data(df)

    print("── BISD Annual Trend ──")
    print(bisd_trend(df).to_string(index=False))

    print("\n── District Comparison (2024) ──")
    print(district_comparison(df, 2024).to_string(index=False))

    print("\n── BISD vs State Average Gap ──")
    print(gap_vs_state(df).to_string(index=False))

    print("\n── Pandemic Recovery Index ──")
    ri = recovery_index(df)
    for k, v in ri.items():
        print(f"  {k}: {v}")
